# 部署教程

## 方案一：Render

Render 需要两个服务：

- Web Service：提供 `/wechat`，给微信服务器做 URL 和 Token 验证。
- Background Worker：继续跑每天 7:00、7:30、18:00 的定时任务。

1. 把项目推送到 GitHub。
2. 在 Render 新建 Blueprint，选择本仓库，Render 会读取 `render.yaml`。
3. 创建后会出现：

```text
kovan-growth-wechat-web
kovan-growth-wechat-worker
```

4. Web Service 的 Build Command：

```bash
pip install -r requirements.txt
```

5. Web Service 的 Start Command：

```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

6. Worker 的 Start Command：

```bash
python -m personal_growth_push run
```

7. 两个服务都至少配置：

```text
TIMEZONE=Asia/Shanghai
PLAN_START_DATE=2026-06-01
OPENAI_MODEL=gpt-5.4-mini
WECHAT_VERIFY_TOKEN=你自己设置的微信验证 Token
```

8. Worker 还需要配置：

```text
OPENAI_API_KEY=你的 OpenAI Key
WECHAT_APP_ID=微信测试号 appID
WECHAT_APP_SECRET=微信测试号 appsecret
WECHAT_OPENIDS=你的微信 openid
WECHAT_TEMPLATE_ID=模板 ID
```

9. 部署后打开 Web Service 的 `/health`：

```text
https://你的服务名.onrender.com/health
```

应返回：

```json
{"status":"ok","wechat_token_configured":true}
```

10. Worker 日志应该能看到：

```text
Scheduler started. News 07:00, morning 07:30, evening 18:00 (Asia/Shanghai).
```

## 部署后填入微信后台的 URL 和 Token

如果 Render Web Service 域名是：

```text
https://kovan-growth-wechat-web.onrender.com
```

那么微信测试号「接口配置信息」填写：

```text
URL=https://kovan-growth-wechat-web.onrender.com/wechat
Token=你在 Render 里设置的 WECHAT_VERIFY_TOKEN
```

如果 Render 给你的域名不同，以 Render 页面显示的服务域名为准，末尾加 `/wechat`。

## 方案二：Railway

1. 新建 Railway 项目并连接 GitHub 仓库。
2. Railway 会读取 `railway.json` 中的 Web 启动命令。
3. 在 Variables 中填入 `.env.example` 里的变量。
4. 部署后查看 Logs，确认定时器启动。

## 方案三：Docker

```bash
docker build -t kovan-growth-wechat .
docker run --env-file .env kovan-growth-wechat
```

## 本地守护运行

如果你先不部署，可以在本机运行：

```bash
python -m personal_growth_push run
```

但电脑关机或休眠后定时推送会停止。长期使用建议放到 Render、Railway、VPS 或 NAS。

## 常见问题

### 1. 微信没有收到

先运行：

```bash
python -m personal_growth_push health
```

确认 `wechat_enabled` 是 `true`。再检查：

- `WECHAT_OPENIDS` 是否是测试号页面里的用户 openid
- `WECHAT_TEMPLATE_ID` 是否正确
- 用户是否已关注测试号
- 模板字段是否包含 `title/date/content/remark`

### 2. 新闻抓不到

运行：

```bash
python -m personal_growth_push fetch-news
```

如果部署平台无法访问 RSS，可以在 `.env` 里替换 `NEWS_FEEDS`。

### 3. OpenAI 失败

系统会自动回退到内置内容。检查：

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- 平台网络是否能访问 OpenAI API

### 4. 免费平台休眠

如果平台会休眠，定时任务可能不稳定。请选择后台 Worker、付费常驻服务，或使用外部定时器定时调用命令。
