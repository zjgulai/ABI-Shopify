# 部署 SOP · Shopify AI 知识库网站 → 腾讯云轻量服务器

> 目标:把本网站(含 DeepSeek RAG 问答)部署到 `101.34.52.232`,域名 `platform.shopify.lute-tlz-dddd.top`,**全程独立 Docker 环境,绝不污染其他应用**。
> 说明:出于安全,本助手不登录你的服务器、不经手你的密钥;以下命令由**你**在服务器执行。

---

## 0. 隔离保证(为什么不会污染其他应用)
- 独立 compose **project**:`shopify-kb`;容器名 `shopifykb-app` / `shopifykb-caddy`。
- 独立**网络** `shopify-kb-net`、独立**卷** `shopify-kb-caddy-data/-config`。
- app 容器**不映射主机端口**(仅在专属网络内 `expose:8000`)。
- 仅当主机 80/443 空闲时,用**独立 Caddy 容器**接管(方案 A);若已被占用,走方案 B(只绑回环 `127.0.0.1:8088`,由你现有 nginx 反代)。
- 主机层面**只在缺失时安装 Docker**,不触碰其他容器、端口、系统包。

---

## 1. 前置(各 5 分钟)
**1.1 DNS**:在域名服务商给 `platform.shopify.lute-tlz-dddd.top` 加一条 **A 记录 → `101.34.52.232`**。验证:
```bash
dig +short platform.shopify.lute-tlz-dddd.top   # 应返回 101.34.52.232
```
**1.2 腾讯云防火墙**:轻量服务器控制台 → 防火墙 → 放行 **TCP 80、443**(方案 B 若复用现有 nginx 则按其端口)。
**1.3 DeepSeek Key**:准备好 `sk-...`(在 platform.deepseek.com 申请);上线后在网站页面手动录入,不写入服务器 `.env`。

---

## 2. 打包并上传(在你的 Mac 上)
### 2.0 推荐:一键发布脚本
当前项目已固化 release 目录发布流程,推荐从仓库根目录执行:
```bash
cd /Users/pray/project/shopify
scripts/deploy_shopify_kb.sh --dry-run   # 本地重建 + 预演
scripts/deploy_shopify_kb.sh             # 发布到 /opt/shopify-kb/releases/<timestamp>-<commit>
```

脚本会自动执行:
- 重建 `_rag/chunks.jsonl` 与 `site/kb_data.js`。
- 构建本地检索索引并执行 `eval_retrieval.py --min-pass-rate 1.0`。
- 检查 tracked 工作区是否干净;若生成产物变更,先提交再发布。
- rsync `kb/` 到新的 release 目录,不复制 `.env`。
- 软链 `/opt/shopify-kb/shared/.env`,写 `DEPLOY_MANIFEST.txt`。
- 用 `docker-compose.behind-proxy.yml + docker-compose.vector.yml` 重建 `shopify-kb` 独立 project。
- 等待 `shopifykb-app` healthy,再做公网 `/api/health`、静态哈希和 Playwright 配置中心 smoke。

手动命令保留如下,用于首次建站、排障或脚本不可用时。

## 2.1 手动打包并上传(在你的 Mac 上)
```bash
cd /Users/pray/project/shopify
tar czf kb.tgz kb                       # 打包整个知识库(含 site / _rag / _kg)
scp kb.tgz ubuntu@101.34.52.232:~/      # 上传
```

## 3. 登录服务器并解包
```bash
ssh ubuntu@101.34.52.232
tar xzf kb.tgz                          # 解出 ~/kb
```

## 4. 安装 Docker(若未安装)
```bash
docker --version || {
  curl -fsSL https://get.docker.com | sudo sh
  sudo usermod -aG docker $USER && newgrp docker
}
docker compose version                  # 确认 compose v2 可用
```

## 5. 配置运行参数(Key 在页面手动录入)
```bash
cd ~/kb/site/deploy
cp .env.example .env                    # 默认只配置模型名;不要在服务器写入 API Key
chmod 600 .env
```

## 6. 端口决策 → 选 A 或 B
```bash
sudo ss -tlnp | grep -E ':80 |:443 ' && echo "80/443 已被占用 → 用方案B" || echo "80/443 空闲 → 用方案A"
```

### 方案 A · 独立 Caddy 自动 HTTPS(推荐,80/443 空闲时)
```bash
cd ~/kb/site/deploy
docker compose up -d --build            # 构建并启动(project: shopify-kb)
```
Caddy 会自动为该域名申请 Let's Encrypt 证书(需 DNS 已生效 + 80/443 放行)。

### 方案 B · 复用你现有 nginx(80/443 已被占用)
```bash
cd ~/kb/site/deploy
docker compose -f docker-compose.yml -f docker-compose.behind-proxy.yml up -d --build
# app 现仅监听 127.0.0.1:8088;把 vhost 加入你现有 nginx:
sudo cp nginx-vhost.example.conf /etc/nginx/conf.d/shopify-kb.conf
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d platform.shopify.lute-tlz-dddd.top   # 签 HTTPS
```

### 方案 C · 生产检索后端(bge/Chroma/Neo4j,显式启用)
适用:需要 T4b 生产检索验收。该方案在方案 A 或 B 的基础上追加 `docker-compose.vector.yml`,会新增独立 `shopifykb-neo4j` 容器和 `shopify-kb-neo4j-*` 卷,不暴露主机端口。
```bash
cd /opt/shopify-kb/current/kb/site/deploy
# 首次启用前:在 /opt/shopify-kb/shared/.env 写入 NEO4J_PASSWORD 和模型配置,不要提交到 Git
docker compose -p shopify-kb \
  -f docker-compose.yml \
  -f docker-compose.behind-proxy.yml \
  -f docker-compose.vector.yml \
  up -d --build
```
回滚到轻量检索:
```bash
docker compose -p shopify-kb -f docker-compose.yml -f docker-compose.behind-proxy.yml up -d --build
docker compose -p shopify-kb -f docker-compose.vector.yml rm -sf neo4j
```

---

## 7. 验证
```bash
docker compose -p shopify-kb ps                 # 两个容器 Up / healthy
docker compose -p shopify-kb logs -f app        # 看 gunicorn 启动、retriever loaded
# 方案A:
curl -sI https://platform.shopify.lute-tlz-dddd.top | head -1
curl -s https://platform.shopify.lute-tlz-dddd.top/api/health      # {"ok":true,"client_key_supported":true,...}
# 方案B:
curl -sI http://127.0.0.1:8088 | head -1
```
浏览器打开 `https://platform.shopify.lute-tlz-dddd.top` → 在页面填入 DeepSeek API Key → 试问答(应返回答案 + 来源)。

---

## 8. 运维
```bash
# 更新(改了内容后):本机重新 scp kb.tgz → 服务器解包 →
cd ~/kb/site/deploy && docker compose -p shopify-kb up -d --build
# 日志 / 重启 / 停止
docker compose -p shopify-kb logs -f
docker compose -p shopify-kb restart
docker compose -p shopify-kb down                # 停并删本项目容器/网络(不动别人)
docker compose -p shopify-kb down -v             # 连同本项目卷一起删(含证书缓存)
```

### release 目录更新时的 `.env` 处理
如果使用 `/opt/shopify-kb/releases/<timestamp>/shopify-kb` + `/opt/shopify-kb/current` 软链方式发布,`.env` 不应进 Git 归档。推荐把运行参数放到共享目录,每次切 release 后链接进去:
```bash
sudo mkdir -p /opt/shopify-kb/shared
# 首次:从当前 release 的 .env.example 创建,不要写入 API Key
sudo cp /opt/shopify-kb/current/kb/site/deploy/.env.example /opt/shopify-kb/shared/.env
sudo chmod 600 /opt/shopify-kb/shared/.env

# 每次切换 current 后:
sudo ln -sfn /opt/shopify-kb/shared/.env /opt/shopify-kb/current/kb/site/deploy/.env
cd /opt/shopify-kb/current/kb/site/deploy
docker compose -p shopify-kb -f docker-compose.yml -f docker-compose.behind-proxy.yml up -d --build
```

## 9. 可选:给站点加访问口令(内部知识库建议)
本站内嵌了内部资料,若需限制访问,在 `Caddyfile` 的域名块内加:
```
basic_auth { admin <用 `caddy hash-password` 生成的哈希> }
```
然后 `docker compose -p shopify-kb up -d`。

## 10. 故障排查
| 现象 | 原因 / 处理 |
|---|---|
| HTTPS 证书签发失败 | DNS 未生效或 80 未放行;`dig` 确认解析、放行 80,再 `docker compose -p shopify-kb restart caddy` 看日志 |
| 端口冲突(80/443 占用) | 改用**方案 B** |
| `env file .../.env not found` | release 目录不带 `.env`;按 §8 将 `/opt/shopify-kb/shared/.env` 链接到当前 release |
| vector 构建耗时/模型下载慢 | 先确认磁盘/内存;可临时把 `SHOPIFY_KB_ST_MODEL` 改为 `BAAI/bge-small-zh-v1.5`,并在验收中记录该边界 |
| `/api/chat` 提示需填 API Key | 在网页问答区域手动录入 DeepSeek API Key;服务器默认不保存 Key |
| 构建拉包慢(国内) | 在 `Dockerfile` 的 pip 行加 `-i https://mirrors.tencent.com/pypi/simple`,docker 配 registry mirror |
| 问答慢/超时 | gunicorn timeout 已设 120s;DeepSeek 首响较慢属正常 |

## 11. 文件清单(`site/deploy/`)
`Dockerfile` · `docker-compose.yml`(方案A)· `docker-compose.behind-proxy.yml`(方案B)· `docker-compose.vector.yml`(方案C)· `entrypoint.sh` · `Caddyfile` · `nginx-vhost.example.conf` · `.env.example` · `.dockerignore` · `requirements.deploy.txt` · `requirements.vector.txt`
