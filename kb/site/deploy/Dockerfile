# Shopify AI 经营知识库 — 生产镜像(Flask + 服务端 RAG + DeepSeek 代理)
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY site/deploy/requirements.deploy.txt /tmp/req.txt
RUN pip install --timeout 120 --retries 5 \
    -i https://mirrors.cloud.tencent.com/pypi/simple \
    --trusted-host mirrors.cloud.tencent.com \
    -r /tmp/req.txt
# 只拷运行所需(保持 retriever 期望的相对结构:/app/_rag, /app/_kg, /app/site)
COPY _rag/chunks.jsonl      /app/_rag/chunks.jsonl
COPY _rag/kb_index          /app/_rag/kb_index
COPY _kg/graph.json         /app/_kg/graph.json
COPY site                   /app/site
# 构建期生成离线索引(容器自包含,启动即用)
RUN cd /app/_rag/kb_index && python cli.py build
WORKDIR /app/site
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1
# 2 worker,gunicorn 生产服务
CMD ["gunicorn","-b","0.0.0.0:8000","-w","2","--timeout","120","server:app"]
