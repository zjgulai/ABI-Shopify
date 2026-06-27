# -*- coding: utf-8 -*-
"""生产检索:可插拔嵌入 + 可选向量库 + 图谱 1 跳扩展。

默认路径仍是零外部服务的 LSA + numpy,生产可显式切到:
- KB_EMBEDDER=st / --embedder st: sentence-transformers,默认 BAAI/bge-m3
- KB_EMBEDDER=openai / --embedder openai: OpenAI embeddings
- KB_VECTOR_STORE=chroma / --store chroma: Chroma 文件级持久向量库
- KB_GRAPH_BACKEND=neo4j: Neo4j 图谱查询(默认 JSON)
"""
import json
import math
import os
import re
import importlib.util
from typing import Any

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAG = os.path.dirname(HERE)
KB = os.path.dirname(RAG)
CHUNKS = os.path.join(RAG, "chunks.jsonl")
GRAPH = os.path.join(KB, "_kg", "graph.json")
STORE = os.path.join(HERE, "index_store")
MANIFEST = os.path.join(STORE, "manifest.json")

DEFAULT_ST_MODEL = os.environ.get("KB_ST_MODEL", "BAAI/bge-m3")
DEFAULT_OPENAI_MODEL = os.environ.get("KB_OPENAI_EMBED_MODEL", "text-embedding-3-large")


def toks(s: str) -> list[str]:
    s = (s or "").lower()
    out = re.findall(r"[a-z0-9]+", s)
    han = re.findall(r"[一-鿿]", s)
    out += han + [han[i] + han[i + 1] for i in range(len(han) - 1)]
    return out


def norm_rows(x: Any) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float32)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    arr /= np.linalg.norm(arr, axis=1, keepdims=True) + 1e-9
    return arr


def load_chunks() -> list[dict[str, Any]]:
    with open(CHUNKS, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def index_text(chunk: dict[str, Any]) -> str:
    return " ".join(
        [
            chunk.get("text", ""),
            chunk.get("doc_title", ""),
            chunk.get("section", ""),
            chunk.get("summary", ""),
            " ".join(chunk.get("tags") or []),
            " ".join(chunk.get("sources") or []),
        ]
    )


def canonical_embedder(name: str | None) -> str:
    name = (name or os.environ.get("KB_EMBEDDER") or "lsa").strip().lower()
    aliases = {
        "lsa": "lsa",
        "local": "lsa",
        "st": "st",
        "sentence-transformers": "st",
        "sentence_transformers": "st",
        "bge": "st",
        "bge-m3": "st",
        "openai": "openai",
    }
    if name not in aliases:
        raise ValueError(f"unknown embedder: {name}")
    return aliases[name]


def canonical_store(name: str | None) -> str:
    name = (name or os.environ.get("KB_VECTOR_STORE") or "numpy").strip().lower()
    aliases = {"numpy": "numpy", "np": "numpy", "chroma": "chroma", "chromadb": "chroma"}
    if name not in aliases:
        raise ValueError(f"unknown vector store: {name}")
    return aliases[name]


def write_json(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_manifest() -> dict[str, Any]:
    if not os.path.exists(MANIFEST):
        return {"embedder": "lsa", "store": "numpy", "model": "lsa-svd", "chunks": 0}
    with open(MANIFEST, encoding="utf-8") as f:
        return json.load(f)


def dependency_doctor() -> dict[str, Any]:
    deps = {
        "numpy": importlib.util.find_spec("numpy") is not None,
        "sentence_transformers": importlib.util.find_spec("sentence_transformers") is not None,
        "chromadb": importlib.util.find_spec("chromadb") is not None,
        "openai": importlib.util.find_spec("openai") is not None,
        "neo4j": importlib.util.find_spec("neo4j") is not None,
        "mcp": importlib.util.find_spec("mcp") is not None,
    }
    env = {
        "KB_EMBEDDER": os.environ.get("KB_EMBEDDER", ""),
        "KB_VECTOR_STORE": os.environ.get("KB_VECTOR_STORE", ""),
        "KB_GRAPH_BACKEND": os.environ.get("KB_GRAPH_BACKEND", ""),
        "OPENAI_API_KEY_set": bool(os.environ.get("OPENAI_API_KEY")),
        "NEO4J_URI_set": bool(os.environ.get("NEO4J_URI")),
        "NEO4J_PASSWORD_set": bool(os.environ.get("NEO4J_PASSWORD")),
    }
    return {"dependencies": deps, "env": env, "manifest": read_manifest()}


class LSAEmbedder:
    """离线潜在语义嵌入(TF-IDF + 截断 SVD),零外部依赖。"""

    name = "lsa"
    model_name = "lsa-svd"

    def __init__(self, dim: int = 160):
        self.dim = dim

    def fit(self, texts: list[str]) -> "LSAEmbedder":
        df: dict[str, int] = {}
        docs: list[dict[str, int]] = []
        for t in texts:
            c: dict[str, int] = {}
            for w in toks(t):
                c[w] = c.get(w, 0) + 1
            docs.append(c)
            for w in c:
                df[w] = df.get(w, 0) + 1

        vocab_terms = [w for w, d in df.items() if d >= 2]
        self.vocab = {w: i for i, w in enumerate(vocab_terms)}
        vsize = len(self.vocab)
        n_docs = len(docs)
        self.idf = np.zeros(vsize, dtype=np.float32)
        for w, i in self.vocab.items():
            self.idf[i] = math.log(1 + n_docs / df[w])

        X = np.zeros((n_docs, vsize), dtype=np.float32)
        for row, counts in enumerate(docs):
            for w, freq in counts.items():
                col = self.vocab.get(w)
                if col is not None:
                    X[row, col] = (1 + math.log(freq)) * self.idf[col]
        X /= np.linalg.norm(X, axis=1, keepdims=True) + 1e-9

        k = min(self.dim, max(1, n_docs - 1), vsize)
        if k == 0:
            self.Vk = np.zeros((1, 0), dtype=np.float32)
            self.Sk = np.ones(1, dtype=np.float32)
            self.doc_emb = np.zeros((n_docs, 1), dtype=np.float32)
            return self

        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        self.Vk = Vt[:k]
        self.Sk = S[:k]
        self.doc_emb = U[:, :k] * S[:k]
        self.doc_emb = norm_rows(self.doc_emb)
        return self

    def embed_query(self, q: str) -> np.ndarray:
        vsize = len(self.vocab)
        if vsize == 0:
            return np.zeros(self.doc_emb.shape[1], dtype=np.float32)
        x = np.zeros(vsize, dtype=np.float32)
        counts: dict[str, int] = {}
        for w in toks(q):
            counts[w] = counts.get(w, 0) + 1
        for w, freq in counts.items():
            col = self.vocab.get(w)
            if col is not None:
                x[col] = (1 + math.log(freq)) * self.idf[col]
        x /= np.linalg.norm(x) + 1e-9
        qk = (x @ self.Vk.T) / (self.Sk + 1e-9)
        qk /= np.linalg.norm(qk) + 1e-9
        return qk.astype(np.float32)

    def save(self, path: str) -> None:
        np.savez(
            path,
            Vk=self.Vk,
            Sk=self.Sk,
            doc_emb=self.doc_emb,
            idf=self.idf,
            vocab=np.array(list(self.vocab.keys()), dtype=object),
        )

    def load(self, path: str) -> "LSAEmbedder":
        z = np.load(path, allow_pickle=True)
        self.Vk = z["Vk"]
        self.Sk = z["Sk"]
        self.doc_emb = z["doc_emb"]
        self.idf = z["idf"]
        self.vocab = {w: i for i, w in enumerate(z["vocab"].tolist())}
        return self


class STEmbedder:
    """sentence-transformers 嵌入,默认 bge-m3。"""

    name = "st"

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or DEFAULT_ST_MODEL
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as exc:
            raise RuntimeError("sentence-transformers 未安装,请按需安装或改用 --embedder lsa") from exc
        self.model = SentenceTransformer(self.model_name)

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        return norm_rows(
            self.model.encode(
                texts,
                batch_size=16,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
        )

    def embed_query(self, q: str) -> np.ndarray:
        return self.embed_texts([q])[0]


class OpenAIEmbedder:
    """OpenAI embedding API。需要 OPENAI_API_KEY。"""

    name = "openai"

    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or DEFAULT_OPENAI_MODEL
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY 未设置,无法使用 OpenAIEmbedder")
        try:
            from openai import OpenAI
        except Exception as exc:
            raise RuntimeError("openai 包未安装,请按需安装或改用 --embedder lsa") from exc
        self.client = OpenAI(api_key=api_key)

    def embed_texts(self, texts: list[str]) -> np.ndarray:
        resp = self.client.embeddings.create(model=self.model_name, input=texts)
        vectors = [item.embedding for item in resp.data]
        return norm_rows(vectors)

    def embed_query(self, q: str) -> np.ndarray:
        return self.embed_texts([q])[0]


def make_embedder(kind: str, model: str | None = None):
    if kind == "lsa":
        return LSAEmbedder()
    if kind == "st":
        return STEmbedder(model)
    if kind == "openai":
        return OpenAIEmbedder(model)
    raise ValueError(f"unknown embedder: {kind}")


class ChromaVectorStore:
    """Chroma 持久向量库适配层。依赖缺失时只在显式使用时抛出。"""

    def __init__(self, path: str, collection_name: str = "shopify_kb"):
        self.path = path
        self.collection_name = collection_name
        try:
            import chromadb
        except Exception as exc:
            raise RuntimeError("chromadb 未安装,请安装后使用 --store chroma") from exc
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def rebuild(self, chunks: list[dict[str, Any]], vectors: np.ndarray) -> None:
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )
        batch_size = 128
        for start in range(0, len(chunks), batch_size):
            end = start + batch_size
            batch = chunks[start:end]
            self.collection.add(
                ids=[c["id"] for c in batch],
                embeddings=[v.tolist() for v in vectors[start:end]],
                documents=[c.get("text", "") for c in batch],
                metadatas=[
                    {
                        "stage": c.get("stage") or "",
                        "source_file": c.get("source_file") or "",
                        "doc_title": c.get("doc_title") or "",
                        "section": c.get("section") or "",
                        "sources": "|".join(c.get("sources") or []),
                        "tags": "|".join(c.get("tags") or []),
                    }
                    for c in batch
                ],
            )

    def query(self, qvec: np.ndarray, n_results: int) -> list[tuple[str, float]]:
        res = self.collection.query(
            query_embeddings=[qvec.tolist()],
            n_results=max(1, n_results),
            include=["distances"],
        )
        ids = (res.get("ids") or [[]])[0]
        distances = (res.get("distances") or [[]])[0]
        return [(cid, 1.0 - float(dist)) for cid, dist in zip(ids, distances)]


class JsonGraphStore:
    def __init__(self, path: str = GRAPH):
        self.G = json.load(open(path, encoding="utf-8"))
        self.lab = {e["id"]: e["label"] for e in self.G["entities"]}

    def _labels(self, rel_type: str, sid: str, direction: str) -> list[str]:
        out = []
        for rel in self.G["relations"]:
            if rel["type"] != rel_type:
                continue
            if direction == "in" and rel["target"] == sid:
                out.append(self.lab[rel["source"]])
            if direction == "out" and rel["source"] == sid:
                out.append(self.lab[rel["target"]])
        return out

    def expand(self, sid: str) -> tuple[list[str], list[str], list[str]]:
        return (
            self._labels("SUPPORTS", sid, "in"),
            self._labels("BELONGS_TO", sid, "in"),
            self._labels("NEXT", sid, "out"),
        )


class Neo4jGraphStore:
    def __init__(self):
        uri = os.environ.get("NEO4J_URI")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD")
        if not uri or not password:
            raise RuntimeError("NEO4J_URI 与 NEO4J_PASSWORD 必须设置才能使用 Neo4j 图谱后端")
        try:
            from neo4j import GraphDatabase
        except Exception as exc:
            raise RuntimeError("neo4j 包未安装,请按需安装或改用 KB_GRAPH_BACKEND=json") from exc
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def _vals(self, cypher: str, sid: str) -> list[str]:
        with self.driver.session() as session:
            return [row["label"] for row in session.run(cypher, sid=sid)]

    def expand(self, sid: str) -> tuple[list[str], list[str], list[str]]:
        return (
            self._vals("MATCH (n)-[:SUPPORTS]->(s {id:$sid}) RETURN n.label AS label", sid),
            self._vals("MATCH (n)-[:BELONGS_TO]->(s {id:$sid}) RETURN n.label AS label", sid),
            self._vals("MATCH (s {id:$sid})-[:NEXT]->(n) RETURN n.label AS label", sid),
        )


def make_graph_store(kind: str | None = None):
    kind = (kind or os.environ.get("KB_GRAPH_BACKEND") or "json").strip().lower()
    if kind == "json":
        return JsonGraphStore()
    if kind == "neo4j":
        return Neo4jGraphStore()
    raise ValueError(f"unknown graph backend: {kind}")


def matches_filter(chunk: dict[str, Any], stage: str | None, source: str | None, tag: str | None) -> bool:
    if stage and stage not in (chunk.get("stage") or ""):
        return False
    if source and source not in (chunk.get("sources") or []):
        return False
    if tag and tag not in (chunk.get("tags") or []):
        return False
    return True


def build_index(
    embedder: str | None = None,
    store: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    os.makedirs(STORE, exist_ok=True)
    chunks = load_chunks()
    texts = [index_text(c) for c in chunks]
    embedder_kind = canonical_embedder(embedder)
    store_kind = canonical_store(store)

    if embedder_kind == "lsa":
        emb = LSAEmbedder().fit(texts)
        vectors = emb.doc_emb
        emb.save(os.path.join(STORE, "lsa.npz"))
        model_name = emb.model_name
    else:
        emb = make_embedder(embedder_kind, model)
        vectors = emb.embed_texts(texts)
        np.save(os.path.join(STORE, "vectors.npy"), vectors)
        model_name = emb.model_name

    write_json(os.path.join(STORE, "meta.json"), chunks)
    if store_kind == "chroma":
        ChromaVectorStore(os.path.join(STORE, "chroma")).rebuild(chunks, vectors)

    manifest = {
        "index_version": 2,
        "embedder": embedder_kind,
        "store": store_kind,
        "model": model_name,
        "chunks": len(chunks),
        "graph_backend_default": "json",
    }
    write_json(MANIFEST, manifest)
    return manifest


class Retriever:
    def __init__(self, graph_backend: str | None = None):
        self.manifest = read_manifest()
        self.embedder_kind = canonical_embedder(self.manifest.get("embedder") or "lsa")
        self.store_kind = canonical_store(self.manifest.get("store") or "numpy")
        self.meta = json.load(open(os.path.join(STORE, "meta.json"), encoding="utf-8"))
        self.by_id = {d["id"]: d for d in self.meta}
        self.graph = make_graph_store(graph_backend)

        if self.embedder_kind == "lsa":
            self.emb = LSAEmbedder().load(os.path.join(STORE, "lsa.npz"))
            self.vectors = self.emb.doc_emb
        else:
            self.emb = make_embedder(self.embedder_kind, self.manifest.get("model"))
            self.vectors = np.load(os.path.join(STORE, "vectors.npy"))

        self.chroma = None
        if self.store_kind == "chroma":
            self.chroma = ChromaVectorStore(os.path.join(STORE, "chroma"))

    def status(self) -> dict[str, Any]:
        return {
            "manifest": self.manifest,
            "chunks_loaded": len(self.meta),
            "vector_dim": int(self.vectors.shape[1]) if self.vectors.ndim == 2 else 0,
            "graph_backend": type(self.graph).__name__,
        }

    def _search_numpy(
        self,
        qvec: np.ndarray,
        k: int,
        stage: str | None,
        source: str | None,
        tag: str | None,
    ) -> list[tuple[float, dict[str, Any]]]:
        sims = self.vectors @ qvec
        out = []
        for idx in np.argsort(-sims):
            chunk = self.meta[int(idx)]
            if not matches_filter(chunk, stage, source, tag):
                continue
            out.append((float(sims[idx]), chunk))
            if len(out) >= k:
                break
        return out

    def _search_chroma(
        self,
        qvec: np.ndarray,
        k: int,
        stage: str | None,
        source: str | None,
        tag: str | None,
    ) -> list[tuple[float, dict[str, Any]]]:
        assert self.chroma is not None
        raw = self.chroma.query(qvec, max(k * 8, k + 20))
        out = []
        for cid, score in raw:
            chunk = self.by_id.get(cid)
            if not chunk or not matches_filter(chunk, stage, source, tag):
                continue
            out.append((score, chunk))
            if len(out) >= k:
                break
        return out

    def search(self, q: str, k: int = 5, stage: str | None = None, source: str | None = None, tag: str | None = None):
        qvec = self.emb.embed_query(q)
        if self.store_kind == "chroma":
            return self._search_chroma(qvec, k, stage, source, tag)
        return self._search_numpy(qvec, k, stage, source, tag)

    def graph_expand(self, sid: str) -> tuple[list[str], list[str], list[str]]:
        return self.graph.expand(sid)

    def ask(self, q: str, k: int = 5):
        hits = self.search(q, k)
        from collections import Counter

        stages = Counter(d["stage"] for _, d in hits if d.get("stage")).most_common(1)
        ge = None
        if stages:
            sid = "stage_" + stages[0][0][:2]
            ge = (sid,) + self.graph_expand(sid)
        return hits, ge
