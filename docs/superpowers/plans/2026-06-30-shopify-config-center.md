---
title: Shopify 网站配置中心实施计划
type: implementation_plan
status: implemented
created: 2026-06-30
scope: website-config-center
boundary: static-local-config-only
---

# Shopify 网站配置中心 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有 ABI 智能化独立站网站中新增一个统一配置中心,集中承接 DeepSeek API Key、Shopify 测试店域名、T7 preflight、CLI/Dev MCP 授权指引、人审文本和证据台账。

**Architecture:** 采用静态优先设计:配置页由 `kb/site/index.html` 渲染,结构化内容由 `kb/_build/build_site_data.py` 注入 `kb/site/kb_data.js`。V1 只做浏览器本地配置、命令生成、状态展示和审批文本生成,不保存 Shopify token、不代替 `shopify auth login`、不读取或写入店铺;V2 才考虑在本地 `server.py` 模式增加只读 preflight endpoint。

**Tech Stack:** Vanilla HTML/CSS/JS, `localStorage`, generated `kb_data.js`, Python build scripts, optional Flask backend, existing RAG/KG/site validation flow.

---

## Current Pending Plan Inventory

| Item | Current State | Next Plan |
|---|---|---|
| T5 provider 问答验收 | 网站已上线,页面手动录入 DeepSeek API Key;服务器默认不保存 Key | 用户在页面输入 Key 后做真实问答 smoke,记录为 provider-call evidence |
| T6 多源深挖 | 执行队列、离线草稿工具、中文社媒入库 SOP 已就绪;已有多批视频入库 | 等真实字幕、帖子正文、截图文字或 browser-harness 可读转写后继续入库 |
| T7 配置中心 | 当前只有执行准备度卡片、Runbook、前置包和 CLI 脚本 | 本计划新增网站内统一配置页面 |
| T7 测试店真实只读 | blocked_auth,待测试店域名和现场授权 | 用户创建/提供 development store 后,按配置中心生成命令和审批文本执行 |
| T7 受控写 | blocked_auth,需先只读、再 mutation preview、再人审 | 仅在测试店、低风险对象、逐次审批后执行 |
| UCP/Catalog 接入 | needs_external_verification | T7 测试店链路跑通后再推进 Agent profile、Catalog readiness |
| 线上重部署 | 上一版已推送;本计划尚未实现 | 配置中心开发验收后再选择是否部署到 Tencent Cloud |

## Product Decision

### V1 Must Do

新增 `#config` 配置中心,面向两个用户:
- 运营/审批人:知道当前是否仍处在未登录、未读取、未写入、未输出密钥值状态,并复制明确审批文本。
- 开发执行者:输入测试店域名,复制本地 preflight、CLI 登录、只读检查、mutation preview 的下一步命令。

V1 只允许:
- 在浏览器本地保存非敏感配置,例如 `store_domain`、`remember_deepseek_key` 偏好、审批人名称、最近证据摘要。
- 继续沿用现有 DeepSeek API Key 手动录入方式;若用户勾选记住,仍只进入当前浏览器 `localStorage`。
- 显示 Shopify 相关命令和审批文本,由用户在终端或 Shopify 浏览器会话中现场执行。
- 记录本地 evidence log,内容只含时间、动作、状态、边界、用户粘贴的非敏感摘要。

V1 禁止:
- 不实现 OAuth callback。
- 不保存 Shopify token、password、private key、Admin API access token。
- 不在前端静态文件写入任何 Key。
- 不从网站直接调用 Shopify Admin API。
- 不从线上服务器执行 `shopify auth login` 或 `t7_test_store_preflight.py`,因为线上服务器环境不代表用户本机。
- 不把用户勾选或本地配置说成真实授权完成。

### V2 Optional

仅在本地 `python server.py` 模式下增加 `/api/t7/preflight`:
- 只执行 `python3 ../tools/t7_test_store_preflight.py --store-domain ... --json`。
- 返回脚本 JSON 中的 set/unset 和 pass/action,不返回任何环境变量值。
- 当 `request.host` 不是 `localhost` 或 `127.0.0.1` 时拒绝。
- 默认不纳入 V1,避免线上误用。

## File Structure

### Create

- `docs/superpowers/plans/2026-06-30-shopify-config-center.md`
  本实施计划。

### Modify

- `kb/_build/build_site_data.py`
  新增 `configuration_center` 数据对象,包括配置状态、流程步骤、命令模板、人审模板、敏感变量名、禁止项和验收提示。

- `kb/site/index.html`
  新增导航入口、配置中心 section、CSS、浏览器本地状态管理、命令生成、审批文本生成和 evidence log 交互。

- `kb/site/README.md`
  记录配置中心使用方式、安全边界和 V1/V2 区别。

- `kb/10-自动化编排/T7测试店授权前置包.md`
  增加“网站配置中心入口”说明,但仍声明真实授权必须用户现场执行。

- `kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md`
  增加配置中心作为 Runbook 前置入口的引用。

- `kb/迭代方案与PRD_TODO.md`
  将 T7 配置中心加入 TODO,状态为 planned 或 implemented,视执行阶段而定。

- `.kiro/plan/task_plan.md`
  新增“T7 配置中心批次”计划。

- `.kiro/plan/progress.md`
  开发完成后记录构建、检索、浏览器和边界验收。

## UI Layout

### Navigation

在桌面导航和移动导航中新增:

```html
<a href="#config">配置</a>
```

首屏 CTA 新增一个次级按钮:

```html
<button class="btn ghost" onclick="document.getElementById('config').scrollIntoView()">配置授权中心</button>
```

### Section: `#config`

放在 `#readiness` 之前,标题:

```html
<section id="config" class="alt">
  <div class="wrap">
    <div class="section-head">
      <div>
        <div class="eyebrow">Configuration Center</div>
        <h2 class="t">配置与授权中心</h2>
        <p class="lead">统一管理 DeepSeek Key、Shopify 测试店域名、T7 前置检查、人审文本和证据台账。这里不登录 Shopify,不保存 Shopify token,不直接写店铺。</p>
      </div>
    </div>
    ...
  </div>
</section>
```

页面布局为三行:

1. 状态总览 `config-summary-grid`
   4 张状态卡:
   - DeepSeek RAG: `requires_user_input` 或 `local_browser_saved`
   - Shopify 测试店域名: `requires_user_input` 或 `local_ready`
   - T7 preflight: `blocked_auth_preflight_ready`
   - 店铺读写: `blocked_auth`

2. 双栏主工作区 `config-layout`
   左栏是表单:
   - DeepSeek Key: 复用现有 `dskey` 的安全说明,保留在问答模块;配置中心只展示“跳转到问答 Key 输入区”按钮,避免两个 Key 输入框不同步。
   - Shopify development store domain: 输入 `name.myshopify.com`。
   - Approval owner: 输入审批人名称,只保存在浏览器本地。
   - Checkbox:
     - 我确认目标是测试店 / development store。
     - 我确认不在此页面输入 Shopify token/password/private key。
     - 我确认真实 `shopify auth login` 只在我现场执行。
   - Buttons:
     - 保存到本浏览器
     - 清除本地配置
     - 生成命令与审批文本

   右栏是输出:
   - Preflight command
   - Shopify auth login instruction
   - Read-only approval text
   - Controlled-write approval text
   - Forbidden actions list

3. Evidence log `config-evidence-log`
   表格字段:
   - time
   - store_domain
   - action
   - status
   - boundary
   - note

   V1 evidence log 只写浏览器 localStorage,不提交到 Git,不传服务器。

## Data Contract

在 `kb/_build/build_site_data.py` 新增:

```python
configuration_center = {
    "storageKey": "abi.shopify.config.v1",
    "statuses": [
        {
            "id": "deepseek-key",
            "label": "DeepSeek RAG Key",
            "status": "requires_user_input",
            "detail": "页面手动录入;服务器不保存。",
        },
        {
            "id": "shopify-store-domain",
            "label": "Shopify 测试店域名",
            "status": "requires_user_input",
            "detail": "仅保存 name.myshopify.com 格式域名,不保存 token。",
        },
        {
            "id": "t7-preflight",
            "label": "T7 本地前置检查",
            "status": "blocked_auth_preflight_ready",
            "detail": "复制命令到本机终端执行;线上站点不代跑。",
        },
        {
            "id": "shopify-read-write",
            "label": "Shopify 读写",
            "status": "blocked_auth",
            "detail": "未登录、未读取、未写入;需用户现场授权。",
        },
    ],
    "commandTemplates": {
        "preflight": "python3 kb/tools/t7_test_store_preflight.py --store-domain {store_domain}",
        "authLogin": "shopify auth login",
        "readOnlyCheck": "shopify auth whoami",
    },
    "approvalTemplates": {
        "readOnly": "同意在 {store_domain} 测试店执行 T7 只读连接检查。",
        "controlledWrite": "同意仅在 {store_domain} 测试店,对 {target} 执行本次 mutation: {planned_change};禁止生产店写入和资金动作。",
    },
    "forbidden": [
        "不要在页面输入 Shopify password/token/private key。",
        "不要把 Shopify token 写入 Git、kb_data.js 或前端静态文件。",
        "不要从线上服务器执行本机 preflight 或 Shopify auth login。",
        "不要在未生成 mutation preview 和未逐次人审前写店铺。",
    ],
    "officialLinks": [
        {"label": "Shopify CLI", "url": "https://shopify.dev/docs/api/shopify-cli"},
        {"label": "Development stores", "url": "https://shopify.dev/docs/apps/build/dev-dashboard/stores/development-stores"},
        {"label": "Generated test data", "url": "https://shopify.dev/docs/api/development-stores/generated-test-data"},
        {"label": "Shopify AI Toolkit", "url": "https://shopify.dev/docs/apps/build/ai-toolkit"},
    ],
}
```

然后将 `configurationCenter` 放进 `data`:

```python
data = {
    ...
    "configurationCenter": configuration_center,
}
```

## Implementation Tasks

### Task 1: Add Configuration Data Contract

**Files:**
- Modify: `kb/_build/build_site_data.py`

- [ ] **Step 1: Back up file**

Run:

```bash
mkdir -p /Users/pray/.Codex/file-history/shopify-config-center-20260630
cp kb/_build/build_site_data.py /Users/pray/.Codex/file-history/shopify-config-center-20260630/build_site_data.py
```

Expected: backup file exists.

- [ ] **Step 2: Add `configuration_center` object**

Insert the data contract shown above after `execution_readiness`.

- [ ] **Step 3: Add object to generated data**

Modify the final `data={...}` to include:

```python
"configurationCenter": configuration_center,
```

- [ ] **Step 4: Build site data**

Run:

```bash
cd /Users/pray/project/shopify/kb/_build
python3 build_site_data.py
```

Expected output includes:

```text
kb_data.js: ... KB | nodes 14 chunks 640
```

- [ ] **Step 5: Inspect generated object**

Run:

```bash
cd /Users/pray/project/shopify
node -e "const fs=require('fs'),vm=require('vm');const code=fs.readFileSync('kb/site/kb_data.js','utf8');const ctx={window:{}};vm.createContext(ctx);vm.runInContext(code,ctx);console.log(ctx.window.KB.configurationCenter.storageKey);console.log(ctx.window.KB.configurationCenter.statuses.length)"
```

Expected:

```text
abi.shopify.config.v1
4
```

### Task 2: Add Configuration Center UI Shell

**Files:**
- Modify: `kb/site/index.html`

- [ ] **Step 1: Back up file**

Run:

```bash
cp kb/site/index.html /Users/pray/.Codex/file-history/shopify-config-center-20260630/site-index.html
```

Expected: backup file exists.

- [ ] **Step 2: Add nav links**

In desktop nav, insert `配置` before `准备度`:

```html
<a href="#config">配置</a>
```

In mobile nav, insert:

```html
<a href="#config" onclick="toggleMenu(false)">配置</a>
```

- [ ] **Step 3: Add hero CTA**

Add:

```html
<button class="btn ghost" onclick="document.getElementById('config').scrollIntoView()">配置授权中心</button>
```

- [ ] **Step 4: Add CSS**

Append near workbench CSS:

```css
.config-summary-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px}
.config-layout{display:grid;grid-template-columns:.95fr 1.05fr;gap:16px;align-items:start}
.config-card,.config-panel{background:#fff;border:1px solid var(--line);border-radius:12px;padding:15px;box-shadow:var(--sh2)}
.config-card h3,.config-panel h3{font-size:15px;margin:8px 0 6px}
.config-card p,.config-panel p{font-size:12.5px;color:#3a4a60}
.config-form{display:grid;gap:10px}
.config-form label{font-size:12px;font-weight:800;color:var(--ink)}
.config-form input,.config-form textarea{width:100%;border:1px solid var(--line);border-radius:8px;padding:10px 12px;font-size:13px}
.config-form textarea{min-height:74px;resize:vertical}
.config-check{display:flex;gap:8px;align-items:flex-start;font-size:12.5px;color:#3a4a60}
.command-box{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#0b1f3a;color:#e9f4ff;border-radius:8px;padding:10px;font-size:12px;white-space:pre-wrap;overflow:auto}
.config-actions{display:flex;gap:8px;flex-wrap:wrap;margin-top:10px}
.evidence-log{width:100%;border-collapse:collapse;font-size:12px;margin-top:12px;background:#fff}
.evidence-log th,.evidence-log td{border:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}
.evidence-log th{background:#f7faff}
@media(max-width:1060px){.config-summary-grid,.config-layout{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.config-summary-grid,.config-layout{grid-template-columns:1fr}}
```

- [ ] **Step 5: Add HTML section**

Insert before `<section id="readiness">`:

```html
<section id="config" class="alt"><div class="wrap">
  <div class="section-head"><div><div class="eyebrow">Configuration Center</div><h2 class="t">配置与授权中心</h2>
  <p class="lead">统一管理 DeepSeek Key、Shopify 测试店域名、T7 前置检查、人审文本和证据台账。这里不登录 Shopify,不保存 Shopify token,不直接写店铺。</p></div>
  <span class="mini-link" onclick="document.getElementById('chat').scrollIntoView()">管理 DeepSeek Key →</span></div>
  <div class="config-summary-grid" id="configSummary"></div>
  <div class="config-layout">
    <div class="config-panel">
      <h3>本地配置</h3>
      <div class="config-form">
        <label for="shopifyStoreDomain">Shopify 测试店域名</label>
        <input id="shopifyStoreDomain" autocomplete="off" placeholder="abi-t7-smoke-20260630.myshopify.com"/>
        <label for="approvalOwner">审批人</label>
        <input id="approvalOwner" autocomplete="off" placeholder="例如: Pray"/>
        <label for="mutationTarget">低风险写入目标</label>
        <input id="mutationTarget" autocomplete="off" placeholder="例如: 测试商品 gid 或 handle"/>
        <label for="plannedChange">计划变更</label>
        <textarea id="plannedChange" placeholder="例如: 给测试商品追加 tag ai-toolkit-controlled-write-smoke"></textarea>
        <label class="config-check"><input id="confirmDevStore" type="checkbox"/> 我确认目标是测试店 / development store。</label>
        <label class="config-check"><input id="confirmNoSecrets" type="checkbox"/> 我不会在此页面输入 Shopify token/password/private key。</label>
        <label class="config-check"><input id="confirmManualLogin" type="checkbox"/> 我确认真实 shopify auth login 只由我现场执行。</label>
      </div>
      <div class="config-actions">
        <button class="btn" onclick="saveShopifyConfig()">保存到本浏览器</button>
        <button class="btn ghost" onclick="clearShopifyConfig()">清除</button>
        <button class="btn ghost" onclick="renderConfigOutputs()">生成文本</button>
      </div>
    </div>
    <div class="config-panel">
      <h3>命令与审批文本</h3>
      <p>复制到本机终端或审批记录中使用。线上网站不代跑这些命令。</p>
      <div id="configOutputs"></div>
    </div>
  </div>
  <div class="config-panel" style="margin-top:16px">
    <h3>本地证据台账</h3>
    <p>只写入当前浏览器 localStorage,不上传服务器,不提交 Git。</p>
    <div class="config-form">
      <label for="evidenceNote">新增证据摘要</label>
      <textarea id="evidenceNote" placeholder="例如: preflight 输出 status=local_pass_auth_required,未登录 Shopify,未读写店铺。"></textarea>
    </div>
    <div class="config-actions">
      <button class="btn" onclick="addConfigEvidence()">追加证据</button>
      <button class="btn ghost" onclick="clearConfigEvidence()">清空本地台账</button>
    </div>
    <div style="overflow:auto"><table class="evidence-log" id="configEvidenceLog"></table></div>
  </div>
</div></section>
```

- [ ] **Step 6: Syntax check**

Run:

```bash
awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' kb/site/index.html | node --check -
```

Expected: no output.

### Task 3: Add Browser State and Text Generation

**Files:**
- Modify: `kb/site/index.html`

- [ ] **Step 1: Add helper functions before chat section JS**

Insert before `// ---- retrieval (client-side) ----`:

```javascript
const CONFIG=K.configurationCenter||{};
const CFG_KEY=CONFIG.storageKey||'abi.shopify.config.v1';
const EVIDENCE_KEY=CFG_KEY+'.evidence';
function loadShopifyConfig(){
  try{return JSON.parse(localStorage.getItem(CFG_KEY)||'{}')}catch(e){return {}}
}
function saveShopifyConfig(){
  const cfg={
    storeDomain:document.getElementById('shopifyStoreDomain').value.trim().toLowerCase().replace(/^https?:\/\//,'').replace(/\/$/,''),
    approvalOwner:document.getElementById('approvalOwner').value.trim(),
    mutationTarget:document.getElementById('mutationTarget').value.trim(),
    plannedChange:document.getElementById('plannedChange').value.trim(),
    confirmDevStore:document.getElementById('confirmDevStore').checked,
    confirmNoSecrets:document.getElementById('confirmNoSecrets').checked,
    confirmManualLogin:document.getElementById('confirmManualLogin').checked,
    savedAt:new Date().toISOString()
  };
  localStorage.setItem(CFG_KEY,JSON.stringify(cfg));
  renderConfigCenter();
  bubble('a','Shopify 配置已保存到本浏览器;未保存 Shopify token/password/private key。');
}
function clearShopifyConfig(){
  localStorage.removeItem(CFG_KEY);
  ['shopifyStoreDomain','approvalOwner','mutationTarget','plannedChange'].forEach(id=>document.getElementById(id).value='');
  ['confirmDevStore','confirmNoSecrets','confirmManualLogin'].forEach(id=>document.getElementById(id).checked=false);
  renderConfigCenter();
}
function validShopifyDomain(s){
  return /^[a-z0-9][a-z0-9-]*\.myshopify\.com$/.test((s||'').trim().toLowerCase());
}
function fillTemplate(t,cfg){
  return (t||'').replaceAll('{store_domain}',cfg.storeDomain||'your-dev-store.myshopify.com')
    .replaceAll('{target}',cfg.mutationTarget||'{target}')
    .replaceAll('{planned_change}',cfg.plannedChange||'{planned_change}');
}
function commandBlock(label,text){
  return `<p style="margin-top:10px"><b>${esc(label)}</b></p><div class="command-box">${esc(text)}</div><div class="config-actions"><button class="btn ghost small" onclick="navigator.clipboard&&navigator.clipboard.writeText(${JSON.stringify(text)})">复制</button></div>`;
}
function renderConfigOutputs(){
  const cfg=loadShopifyConfig();
  const tpl=CONFIG.commandTemplates||{};
  const approvals=CONFIG.approvalTemplates||{};
  const preflight=fillTemplate(tpl.preflight,cfg);
  const authLogin=tpl.authLogin||'shopify auth login';
  const readOnly=fillTemplate(approvals.readOnly,cfg);
  const controlledWrite=fillTemplate(approvals.controlledWrite,cfg);
  document.getElementById('configOutputs').innerHTML=[
    commandBlock('本地 preflight',preflight),
    commandBlock('Shopify CLI 登录指引',authLogin),
    commandBlock('只读连接审批文本',readOnly),
    commandBlock('低风险写入审批文本',controlledWrite),
    `<p style="margin-top:10px"><b>禁止项</b></p><ul>${listItems(CONFIG.forbidden||[])}</ul>`
  ].join('');
}
function renderConfigSummary(){
  const cfg=loadShopifyConfig();
  const statuses=(CONFIG.statuses||[]).map(x=>({...x}));
  const domainItem=statuses.find(x=>x.id==='shopify-store-domain');
  if(domainItem&&validShopifyDomain(cfg.storeDomain)){
    domainItem.status='local_ready';
    domainItem.detail='测试店域名格式已保存到本浏览器;仍未登录 Shopify。';
  }
  document.getElementById('configSummary').innerHTML=statuses.map(s=>`<div class="config-card">${statusPill(s.status)}<h3>${esc(s.label)}</h3><p>${esc(s.detail)}</p></div>`).join('');
}
function renderConfigEvidence(){
  let rows=[];try{rows=JSON.parse(localStorage.getItem(EVIDENCE_KEY)||'[]')}catch(e){}
  document.getElementById('configEvidenceLog').innerHTML='<tr><th>时间</th><th>店铺</th><th>动作</th><th>状态</th><th>边界</th><th>摘要</th></tr>'+
    rows.map(r=>`<tr><td>${esc(r.time)}</td><td>${esc(r.storeDomain)}</td><td>${esc(r.action)}</td><td>${esc(r.status)}</td><td>${esc(r.boundary)}</td><td>${esc(r.note)}</td></tr>`).join('');
}
function addConfigEvidence(){
  const cfg=loadShopifyConfig();
  const note=document.getElementById('evidenceNote').value.trim();
  if(!note){bubble('a','请先填写证据摘要。');return}
  let rows=[];try{rows=JSON.parse(localStorage.getItem(EVIDENCE_KEY)||'[]')}catch(e){}
  rows.unshift({time:new Date().toISOString(),storeDomain:cfg.storeDomain||'',action:'manual_evidence_note',status:'local_note',boundary:'no Shopify login/read/write by this page',note});
  localStorage.setItem(EVIDENCE_KEY,JSON.stringify(rows.slice(0,20)));
  document.getElementById('evidenceNote').value='';
  renderConfigEvidence();
}
function clearConfigEvidence(){
  localStorage.removeItem(EVIDENCE_KEY);
  renderConfigEvidence();
}
function renderConfigCenter(){
  const cfg=loadShopifyConfig();
  if(document.getElementById('shopifyStoreDomain')){
    document.getElementById('shopifyStoreDomain').value=cfg.storeDomain||'';
    document.getElementById('approvalOwner').value=cfg.approvalOwner||'';
    document.getElementById('mutationTarget').value=cfg.mutationTarget||'';
    document.getElementById('plannedChange').value=cfg.plannedChange||'';
    document.getElementById('confirmDevStore').checked=!!cfg.confirmDevStore;
    document.getElementById('confirmNoSecrets').checked=!!cfg.confirmNoSecrets;
    document.getElementById('confirmManualLogin').checked=!!cfg.confirmManualLogin;
  }
  renderConfigSummary();
  renderConfigOutputs();
  renderConfigEvidence();
}
renderConfigCenter();
```

- [ ] **Step 2: Run JS check**

Run:

```bash
awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' kb/site/index.html | node --check -
```

Expected: no output.

### Task 4: Update Documentation and TODO State

**Files:**
- Modify: `kb/site/README.md`
- Modify: `kb/10-自动化编排/T7测试店授权前置包.md`
- Modify: `kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md`
- Modify: `kb/迭代方案与PRD_TODO.md`
- Modify: `.kiro/plan/task_plan.md`
- Modify: `.kiro/plan/progress.md`

- [ ] **Step 1: Back up files**

Run:

```bash
cp kb/site/README.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/site-README.md
cp kb/10-自动化编排/T7测试店授权前置包.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/T7测试店授权前置包.md
cp kb/10-自动化编排/AI-Toolkit_UCP测试店受控写验收Runbook.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/T7-Runbook.md
cp kb/迭代方案与PRD_TODO.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/迭代方案与PRD_TODO.md
cp .kiro/plan/task_plan.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/task_plan.md
cp .kiro/plan/progress.md /Users/pray/.Codex/file-history/shopify-config-center-20260630/progress.md
```

- [ ] **Step 2: Update `kb/site/README.md`**

Add:

```markdown
## 配置与授权中心
- `#config` 用于统一录入测试店域名、生成 T7 preflight 命令、复制只读/受控写审批文本和记录本地证据摘要。
- 配置中心只保存非敏感配置到当前浏览器 localStorage;不保存 Shopify token、password、private key。
- 真实 `shopify auth login`、测试店读取和 mutation 执行仍必须由用户现场确认。
```

- [ ] **Step 3: Update T7 preflight package**

Add after “本地 preflight”:

```markdown
也可以在网站 `#config` 配置与授权中心录入测试店域名,由页面生成本地 preflight 命令和审批文本。该页面不执行 Shopify 登录、不读取或写入店铺、不保存 Shopify token。
```

- [ ] **Step 4: Update Runbook**

Add before read-only connection:

```markdown
建议先打开网站 `#config` 配置与授权中心,确认测试店域名、人审文本和本地 preflight 输出。配置中心生成的文本只是执行前准备,不代表 Shopify 已授权。
```

- [ ] **Step 5: Update TODO**

Add:

```markdown
- [ ] T7 网站配置与授权中心(测试店域名、preflight 命令、人审文本、本地证据台账)
```

After implementation change to checked.

- [ ] **Step 6: Update `.kiro/plan/task_plan.md`**

Add a section:

```markdown
## T7 配置中心批次

目标:把 DeepSeek Key、Shopify 测试店域名、T7 preflight、授权文本和本地证据台账统一进网站配置页。

非目标:
- 不实现 Shopify OAuth callback。
- 不保存 Shopify token/password/private key。
- 不从网站直接读写店铺。
- 不把本地配置视为真实授权完成。
```

### Task 5: Rebuild and Static Validation

**Files:**
- Generated: `kb/site/kb_data.js`
- Generated: `kb/_rag/chunks.jsonl`

- [ ] **Step 1: Build RAG chunks**

Run:

```bash
cd /Users/pray/project/shopify/kb/_build
python3 build_rag.py
```

Expected: `chunks:` count remains parseable.

- [ ] **Step 2: Build retriever index**

Run:

```bash
cd /Users/pray/project/shopify/kb/_rag/kb_index
python3 cli.py build
```

Expected:

```text
indexed chunks: ... | embedder=lsa
```

- [ ] **Step 3: Build site data**

Run:

```bash
cd /Users/pray/project/shopify/kb/_build
python3 build_site_data.py
```

Expected: `kb_data.js` generated.

- [ ] **Step 4: Python and JS checks**

Run:

```bash
cd /Users/pray/project/shopify
python3 -m py_compile kb/_build/build_site_data.py kb/site/server.py kb/tools/t7_test_store_preflight.py
node --check kb/site/kb_data.js
awk '/<script>/{flag=1; next} /<\/script>/{flag=0} flag' kb/site/index.html | node --check -
```

Expected: no output for `node --check`; py_compile returns 0.

- [ ] **Step 5: RAG eval**

Run:

```bash
cd /Users/pray/project/shopify/kb/_rag/kb_index
python3 eval_retrieval.py --min-pass-rate 1.0
```

Expected:

```text
pass_rate=1.00 (5/5)
```

- [ ] **Step 6: Config search smoke**

Run:

```bash
cd /Users/pray/project/shopify/kb/_rag/kb_index
python3 cli.py search 'T7 网站配置中心 测试店域名 preflight 人审文本 不保存 Shopify token' -k 5
```

Expected: top results include `site/README.md`, `T7测试店授权前置包.md`, or Runbook.

### Task 6: Browser E2E Validation

**Files:**
- Validate: `kb/site/index.html`
- Validate: `kb/site/kb_data.js`

- [ ] **Step 1: Start static preview**

Run:

```bash
cd /Users/pray/project/shopify/kb/site
python3 -m http.server 8765
```

Expected: `http://127.0.0.1:8765` serves the site.

- [ ] **Step 2: Desktop smoke with Playwright or browser harness**

Check:
- `#config` appears in nav.
- Configuration Center section renders.
- Enter `abi-t7-smoke-20260630.myshopify.com`.
- Save.
- Reload.
- Domain persists in browser localStorage.
- Generated command contains:

```text
python3 kb/tools/t7_test_store_preflight.py --store-domain abi-t7-smoke-20260630.myshopify.com
```

- Generated read-only approval text contains:

```text
同意在 abi-t7-smoke-20260630.myshopify.com 测试店执行 T7 只读连接检查。
```

- [ ] **Step 3: Mobile smoke**

Viewport: 390x844.

Check:
- Mobile menu has `配置`.
- Form fields do not overflow.
- Command boxes scroll instead of breaking layout.
- Buttons are tap-friendly.

- [ ] **Step 4: LocalStorage safety inspection**

In browser console:

```javascript
localStorage.getItem('abi.shopify.config.v1')
localStorage.getItem('abi.shopify.config.v1.evidence')
```

Expected:
- Contains store domain and user-entered notes.
- Does not contain Shopify token/password/private key.

### Task 7: Security and Boundary Review

**Files:**
- Review: `kb/site/index.html`
- Review: `kb/site/server.py`
- Review: `kb/site/kb_data.js`
- Review: `kb/_build/build_site_data.py`

- [x] **Step 1: Search for real secret patterns**

Run:

```bash
cd /Users/pray/project/shopify
rg -n "<real secret/token regex bundle>" .kiro docs kb \
  -g '!kb/site/kb_data.js' \
  -g '!kb/_rag/chunks.jsonl' \
  -g '!kb/_rag/kb_index/index_store/meta.json'
```

Expected: only documented environment-variable placeholders, no real values.

- [ ] **Step 2: Confirm no Shopify network call in config page**

Run:

```bash
rg -n "shopify\\.com|myshopify\\.com|admin/api|graphql|auth login|fetch\\(" kb/site/index.html
```

Expected:
- `fetch(` only belongs to `/api/health`, `/api/chat`, DeepSeek chat, not Shopify Admin API.
- Shopify URLs only appear as docs links or generated text, not executed network calls.

- [ ] **Step 3: Confirm server has no Shopify write endpoint**

Run:

```bash
rg -n "shopify|mutation|Admin|graphql|preflight" kb/site/server.py
```

Expected:
- V1: no Shopify endpoint.
- V2 if added later: endpoint is localhost-only and executes only local preflight script.

### Task 8: Commit

**Files:**
- Stage only formal files under `.kiro`, `docs`, and `kb`.
- Leave `inbox/` and `tmp/` untracked unless explicitly promoted.

- [ ] **Step 1: Check status**

Run:

```bash
git status --short
```

Expected:
- Modified formal files.
- `?? inbox/` and `?? tmp/` may remain untracked.

- [ ] **Step 2: Stage**

Run:

```bash
git add docs/superpowers/plans/2026-06-30-shopify-config-center.md .kiro kb
```

- [ ] **Step 3: Review staged diff**

Run:

```bash
git diff --cached --stat
git diff --cached --check
```

Expected: no whitespace warnings.

- [ ] **Step 4: Commit**

Run:

```bash
git commit -m "Add Shopify website configuration center"
```

- [ ] **Step 5: Push**

Run:

```bash
git push
```

## Acceptance Criteria

- 网站新增 `配置` 导航和 `#config` 配置与授权中心。
- 用户可在网站输入测试店域名并保存到当前浏览器。
- 页面可生成 T7 preflight 命令、Shopify CLI 登录指引、只读审批文本、受控写审批文本。
- 页面能显示当前事实边界:未登录 Shopify、未读取店铺、未写店铺、未输出密钥值。
- 页面不保存 Shopify token/password/private key。
- 页面不直接调用 Shopify Admin API。
- 线上站点不会执行用户本机 preflight。
- `DeepSeek API Key` 仍沿用页面手动录入方式;服务器不保存。
- RAG/KG/site rebuild 正常。
- 默认 retrieval eval 保持 `5/5`。
- Desktop 和 mobile 视口无明显重叠、溢出或不可点击控件。

## Open Decisions Before Implementation

1. V1 是否只做静态配置中心? 推荐:是。
2. 是否把 DeepSeek Key 输入框移动到配置中心? 推荐:暂不移动,只放跳转入口,避免两个 Key 框状态不一致。
3. 是否允许 localStorage 保存测试店域名? 推荐:允许,因为不是 secret。
4. 是否允许 localStorage 保存审批人名称和证据摘要? 推荐:允许,但页面提示不要写 token、password、private key。
5. 是否立即做 V2 local server preflight endpoint? 推荐:先不做;V1 验收后再决定。

## Self-Review

- Spec coverage: 覆盖了用户要求的未登录、未读取、未写入、未输出密钥值状态展示,以及 T7 `local_pass_auth_required` 后续配置和授权统一入口。
- Placeholder scan: 无 TBD、implement later 等占位写法;`TODO` 仅出现在既有文件名 `kb/迭代方案与PRD_TODO.md` 和清单章节语境中。
- Boundary consistency: V1 不做 Shopify OAuth、不保存 Shopify 凭据、不读写店铺;真实授权仍需用户现场执行。
