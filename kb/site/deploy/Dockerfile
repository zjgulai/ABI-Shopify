# Shopify AI 经营知识库 — 生产镜像(Flask + 服务端 RAG + DeepSeek 代理)
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
ARG INSTALL_VECTOR_EXTRAS=0
ARG KB_EMBEDDER=lsa
ARG KB_VECTOR_STORE=numpy
ARG KB_ST_MODEL=BAAI/bge-m3
ARG HF_ENDPOINT=
ENV KB_EMBEDDER=${KB_EMBEDDER} \
    KB_VECTOR_STORE=${KB_VECTOR_STORE} \
    KB_ST_MODEL=${KB_ST_MODEL} \
    HF_ENDPOINT=${HF_ENDPOINT}
WORKDIR /app
COPY site/deploy/requirements.deploy.txt /tmp/req.txt
COPY site/deploy/requirements.vector.txt /tmp/req-vector.txt
RUN pip install --timeout 120 --retries 5 \
    -i https://mirrors.cloud.tencent.com/pypi/simple \
    --trusted-host mirrors.cloud.tencent.com \
    -r /tmp/req.txt
RUN if [ "$INSTALL_VECTOR_EXTRAS" = "1" ]; then \
      pip install --timeout 600 --retries 5 \
        --index-url https://download.pytorch.org/whl/cpu \
        --trusted-host download.pytorch.org \
        torch; \
      pip install --timeout 600 --retries 5 \
        -i https://mirrors.cloud.tencent.com/pypi/simple \
        --trusted-host mirrors.cloud.tencent.com \
        -r /tmp/req-vector.txt; \
    fi
# 只拷运行所需(保持 retriever 期望的相对结构:/app/_rag, /app/_kg, /app/site)
COPY _rag/chunks.jsonl      /app/_rag/chunks.jsonl
COPY _rag/kb_index          /app/_rag/kb_index
COPY _kg/graph.json         /app/_kg/graph.json
COPY site                   /app/site
# 构建期只生成零外网依赖的 LSA 索引;生产向量索引由 entrypoint 按运行网络预热。
RUN cd /app/_rag/kb_index && python cli.py build --embedder lsa --store numpy
COPY site/deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /app/site
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1
# 2 worker,gunicorn 生产服务
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn","-b","0.0.0.0:8000","-w","2","--timeout","120","server:app"]
