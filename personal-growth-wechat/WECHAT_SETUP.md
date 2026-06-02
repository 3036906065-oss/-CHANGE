# 微信测试号配置教程

## 1. 进入测试号

打开微信公众平台测试号页面：

```text
https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
```

扫码登录后，你会看到：

- `appID`
- `appsecret`
- 测试号二维码
- 已关注用户列表
- 模板消息接口
- 接口配置信息

## 2. 配置服务器 URL 和 Token

先把项目部署到 Render Web Service。部署完成后，Render 会给你一个公网域名，例如：

```text
https://kovan-growth-wechat-web.onrender.com
```

在微信测试号页面的「接口配置信息」里填写：

```text
URL=https://kovan-growth-wechat-web.onrender.com/wechat
Token=kovan_growth_2026_change_me
```

注意：`Token` 必须和 Render 环境变量 `WECHAT_VERIFY_TOKEN` 完全一致。

如果你把 Token 改成了：

```text
Kovan_2026_private_token
```

那么微信后台也必须填同一个：

```text
Token=Kovan_2026_private_token
```

保存时，微信会向 `/wechat` 发起 GET 请求。系统验证通过后会返回 `echostr`，微信后台就会提示配置成功。

## 3. 关注测试号

用你的微信扫描测试号二维码。

关注后，页面会出现你的 `微信号 / openid`。把 openid 填入：

```text
WECHAT_OPENIDS=你的 openid
```

如果要给多人推送，用英文逗号分隔：

```text
WECHAT_OPENIDS=openid1,openid2
```

## 4. 新增模板

在「模板消息接口」里点击新增测试模板。

模板标题可以写：

```text
个人成长推送
```

模板内容填：

```text
{{title.DATA}}
日期：{{date.DATA}}

{{content.DATA}}

{{remark.DATA}}
```

保存后得到 `模板 ID`，填入：

```text
WECHAT_TEMPLATE_ID=你的模板 ID
```

如果你想早晚分别用两个模板，也可以填：

```text
WECHAT_TEMPLATE_ID_MORNING=早间模板 ID
WECHAT_TEMPLATE_ID_EVENING=晚间模板 ID
```

## 5. 填写 appID 和 appsecret

```text
WECHAT_APP_ID=测试号 appID
WECHAT_APP_SECRET=测试号 appsecret
WECHAT_VERIFY_TOKEN=和微信后台 Token 一致
```

## 6. 测试发送

先本地预览：

```bash
python -m personal_growth_push send-morning --dry-run
```

确认内容没问题后发送：

```bash
python -m personal_growth_push send-morning
```

晚上训练饮食测试：

```bash
python -m personal_growth_push send-evening
```

## 7. 内容过长怎么办

本项目会按照 `WECHAT_MAX_CONTENT_CHARS` 自动分段发送。

默认：

```text
WECHAT_MAX_CONTENT_CHARS=1400
```

如果你的模板消息被截断，可以改成：

```text
WECHAT_MAX_CONTENT_CHARS=900
```

这样会发送更多条，但每条更稳。
