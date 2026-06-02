# Kovan 个人成长微信自动推送系统

这是一个可长期运行的 Python 项目，用于每天自动生成并推送：

- 早上 7:30：英语学习 + 国际重点新闻
- 晚上 18:00：健身计划 + 饮食计划
- 早上 7:00：提前抓取并缓存 Reuters/BBC/AI 科技新闻
- `/wechat`：微信服务器配置验证入口

系统根据 Kovan 的个人信息、力量水平和 90 天目标设计：

- 男，2006-09-14，178cm，80kg
- 90 天减脂增肌重组，目标体重约 75kg
- 5 练 2 休：Push / Pull / Legs / 有氧恢复 / Upper / Lower / Rest
- 饮食目标：2300-2400 kcal
- 建立英语学习习惯，并每天掌握国际重点新闻

## 项目目录

```text
personal-growth-wechat/
  personal_growth_push/
    config.py              # 环境变量与配置
    main.py                # 命令行入口
    webhook.py             # Flask /wechat 验签服务
    scheduler.py           # APScheduler 定时任务
    jobs.py                # 早晚推送编排
    openai_client.py       # OpenAI Responses API 封装
    wechat.py              # 微信测试号模板推送
    profile.py             # Kovan 训练与饮食基础数据
    services/
      fitness.py           # 健身计划
      nutrition.py         # 饮食计划
      english.py           # 英语学习内容
      news.py              # RSS 新闻抓取与摘要
  data/                    # 运行缓存，部署时自动生成
  tests/
  requirements.txt
  app.py                   # gunicorn app:app 入口
  .env.example
  DEPLOYMENT.md
  WECHAT_SETUP.md
  Dockerfile
  Procfile
  render.yaml
  railway.json
```

## 本地运行

1. 安装 Python 3.11+
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 创建配置：

```bash
cp .env.example .env
```

4. 填入 `.env`：

- `OPENAI_API_KEY`
- `WECHAT_APP_ID`
- `WECHAT_APP_SECRET`
- `WECHAT_VERIFY_TOKEN`
- `WECHAT_OPENIDS`
- `WECHAT_TEMPLATE_ID`

5. 本地预览：

```bash
python -m personal_growth_push preview-morning
python -m personal_growth_push preview-evening
```

6. 不发送微信，只看将要发送的内容：

```bash
python -m personal_growth_push send-morning --dry-run
python -m personal_growth_push send-evening --dry-run
```

7. 启动自动任务：

```bash
python -m personal_growth_push run
```

8. 本地启动 webhook 服务：

```bash
gunicorn app:app --bind 0.0.0.0:10000
```

Windows 本地也可以先用 Flask 内置服务调试：

```bash
flask --app app run --port 10000
```

## 命令说明

```bash
python -m personal_growth_push health
python -m personal_growth_push fetch-news
python -m personal_growth_push preview-morning
python -m personal_growth_push preview-evening
python -m personal_growth_push send-morning --dry-run
python -m personal_growth_push send-evening --dry-run
python -m personal_growth_push run
```

可以用 `--date YYYY-MM-DD` 预览某一天：

```bash
python -m personal_growth_push --date 2026-06-01 preview-evening
```

## 内容生成逻辑

健身和饮食模块使用本地结构化计划，稳定、可控、不会因为 API 失败中断。

英语和新闻模块优先使用 OpenAI Responses API 生成个性化内容；如果没有配置 API Key 或接口失败，会使用内置兜底内容，保证每天仍有推送。

新闻模块默认 RSS：

- Reuters via Google News
- BBC World
- AI Technology

你可以在 `.env` 中通过 `NEWS_FEEDS` 替换或增加 RSS。

## 微信模板字段

测试号模板建议配置为：

```text
{{title.DATA}}
日期：{{date.DATA}}

{{content.DATA}}

{{remark.DATA}}
```

代码会自动把较长内容分段发送，避免一条模板消息过长。

## 微信服务器配置

部署到 Render Web Service 后，在微信测试号「接口配置信息」填写：

```text
URL：https://你的 Render Web Service 域名/wechat
Token：WECHAT_VERIFY_TOKEN 的值
```

如果你使用项目里的 `render.yaml` 且服务名没有被 Render 改名，URL 通常是：

```text
https://kovan-growth-wechat-web.onrender.com/wechat
```

Token 示例：

```text
kovan_growth_2026_change_me
```

更推荐你把 Token 改成一串只有自己知道的随机字符串，并保证微信后台和 Render 环境变量完全一致。

## 长期维护建议

- 每周固定检查一次体重、腰围、卧推/深蹲/硬拉表现。
- 连续 2 周体重不下降时，把每日热量减少 100-150 kcal 或增加 10-15 分钟 Zone 2。
- 如果睡眠差、训练动作变形，优先降训练量，不要硬加重量。
- 新闻 RSS 源偶尔会变化，抓取失败时看 `data/news_YYYY-MM-DD.json` 和运行日志。

更多部署细节见 `DEPLOYMENT.md`，微信测试号配置见 `WECHAT_SETUP.md`。
