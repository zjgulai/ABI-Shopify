# Shopify AI 经营知识库 · 网站

## 两种打开方式

### A. 直接看(静态,双击即可)
双击 `index.html` 即可浏览:全景图、AI 开店 10 步、全流程节点(点击展开 + 完整文档)、能力地图、知识库本地检索、下一步路线图。
> 此模式下「DeepSeek 问答」使用页面手动录入的 API Key 从浏览器直连 DeepSeek;若浏览器拦截跨域请求,请用 B 模式。

### B. 完整版(含 RAG 代理,推荐)
```bash
cd ../_rag/kb_index && python cli.py build      # 1) 建检索索引(一次)
cd ../../site
pip install -r requirements.txt                  # 2) 装 flask
python server.py                                 # 3) 打开 http://localhost:8000
```
问答流程:页面手动录入 API Key → 你的问题 → 服务端 RAG 检索知识库 top-6 → 拼上下文 → 用本次请求的 API Key 调用 DeepSeek(`deepseek-v4-flash`)→ 返回答案 + 来源。

## 安全
- **Key 不写进任何文件**,部署默认不需要在服务器 `.env` 中配置 `DEEPSEEK_API_KEY`。
- B 模式下 Key 由页面随单次请求发给本服务端,服务端只用于转发 DeepSeek 请求,不落盘、不写日志。
- 勾选“记住到本浏览器”时,Key 仅保存在当前浏览器 localStorage;不勾选则只保留在当前页面内存中。

## 文件
- `index.html` 单文件前端 · `kb_data.js` 站点数据(由 `../_build/build_site_data.py` 生成)
- `server.py` 安全后端 · `assets/` 商业图
