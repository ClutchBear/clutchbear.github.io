---
title: "GitHub Copilot 无法开通（重定向循环）— 自查、申诉与解封全记录"
description: "GitHub Copilot 开通页 ERR_TOO_MANY_REDIRECTS 不是浏览器或代理问题，是账号被打了资格限制标记。本文复盘识别判据、免费账号申诉路径、坦白信写法与本机清理核查清单，全程隐去个人信息。"
pubDatetime: 2026-10-09T22:30:00+08:00
draft: false
tags:
  - GitHub
  - Copilot
  - 账号风控
  - 申诉
  - 解封
---


> **一句话结论**：`ERR_TOO_MANY_REDIRECTS` 不是浏览器或代理问题，是 GitHub 后台给账号打了「Copilot 资格限制」标记（administrative block）。本单根因是早年使用过共享凭据服务，走「坦白 + 彻底清理 + 主动更正此前不实陈述」路径，从开票到解封约 22 小时。
> **最终状态：已完全解封，VS Code 与网页端均实测可用。**
> 本文为复盘记录，**人物、邮箱、账号 ID、工单号均已隐去**，仅保留可复用的流程与判据。

**事件档案**

| 项 | 值 |
|---|---|
| 账号 | （用户名 / 邮箱 / 账号 ID 已隐去，注册逾十年） |
| 工单号 | （已隐去） |
| 现象 | `/github-copilot/signup` 无限重定向；Dashboard 顶部持久红色横幅 "Your account is unable to sign up for Copilot. Please contact Support." |
| 根因 | 早年使用过共享 Copilot 凭据的"开车平台" |
| 指控原文 | 检测到账号使用 credential-sharing service，违反 ToS 与 Acceptable Use Policies |
| 往返 | 4 封（开票 → Support 索要素 → GitHub 指控 → 坦白回复 → 解封） |
| 红线 | **再检测到 = Copilot 永久吊销 + GitHub 账号永久封禁** |

---

## 一、事件时间线

| 时间（北京） | 事件 |
|---|---|
| 约事发前一个月初 | 首次撞上 signup 重定向循环，当时未深究 |
| 凌晨 01:42 | 提交工单（附两张截图：循环报错页 + Dashboard 红条） |
| 凌晨 02:00 前后 | Support 回复：**确认账号被限制**，不披露原因，索要三要素（用户名 / 首次发现时间 / 计划 workflow） |
| 当天 17:11 UTC | **GitHub 正式指控**：检测到凭据共享服务；给出解封三步（卸载工具、撤销授权、确认遵守 ToS）；警告再犯永久封号 |
| 当天白天 | 自查三处 + 本机扫描；一度误判为某个社区所致（后排除） |
| 当天 21:05 | 确认根因 = 早年共享凭据平台；**本机六处扫描零残留** |
| 当天 21:5x | 发出坦白版回信（认早年使用 + 更正此前不实陈述 + 清理证明） |
| 当天 21:51 UTC | **Support 回复：限制已解除（lifted the restriction）** |
| 当天 22:05 | 网页端显示 Copilot Free 契约；VS Code 实测可用 |
| 当天 22:36 | 网页端 Copilot Chat 实测可用（延迟约 25 分钟，属许可开通排队） |

---

## 二、根因：早年的共享凭据平台

- **共享凭据平台 / "开车平台"**：把付费 Copilot 席位放进池子多人均摊，用户用别人的凭据白嫖 → GitHub 明确认定为**凭据共享**，违反 ToS
- 封禁不是即时生效的：账号被标记后，用户往往到很久之后想开官方免费档时才发现（本单就是这样，**约事发前一个月初首次撞墙**）
- 这类平台的账号在你不登录时依然保留：只要没退出，风险敞口一直在

### 一次被排除的误判（记录以免重犯）

事件中曾把 **某中文 AI 交流社区** 当成嫌疑：它是普通论坛（帖子如"免费克5.5o""送住宅IP给 chatgpt/codex 用""有没有token 发一下"），OAuth 授权记录存在且当时刚撤销，时间点看着很像。

**排除依据**：① 该站只是普通论坛，自身**不提供**共享的 Copilot 凭据；② 真正的凭据共享行为发生在早年的共享平台；③ 事后证明撤销该授权只是一次顺手的卫生操作（这类不认识的第三方授权原本就该清），**不是解封原因**。

> 教训：**相关性 ≠ 因果**。时间吻合只是线索，判据应该是"这个服务是否真的共享了凭据"。

---

## 三、现象识别（可复用的判据）

### ERR_TOO_MANY_REDIRECTS 三种成因

| 成因 | 判据 | 处理 |
|---|---|---|
| Cookie / 扩展损坏 | 无痕窗口下正常 | 清 Cookie，不申诉 |
| 代理出口地区问题 | 关代理直连后正常 | 换网络，不申诉 |
| **账号资格限制（administrative block）** | 无痕、换网络、清 Cookie 全无效；循环中途常闪现 *"Your account is unable to sign up for Copilot. Please contact Support."*；Dashboard 顶部出现持久红条 | **只能开票**（GitHub Community #180874 确认） |

### 5 步自查（按顺序，别跳）

| # | 检查项 | 操作 |
|---|---|---|
| 1 | 清 GitHub Cookie | 地址栏锁图标 → Cookie → 删 `github.com` 相关（**不用清全部浏览器数据**） |
| 2 | 无痕窗口 | 无痕正常 = 本地问题，不必申诉 |
| 3 | 关代理 / 换节点 | 出口 IP 在不支持地区会触发循环 |
| 4 | 手机流量 | 排除本机网络 |
| 5 | `github.com/settings/copilot` | 看后台到底报什么（本单：只给 "Start using Copilot Free" 入口，无任何 active plan → 排除组织席位冲突） |

### GitHub 自己也给的一层验证

support 流程中有一页 **AI 预检**，它会先判断"这是不是账号级限制"。本单 AI 预检直接说需要人工复查 → 等于**系统先承认了账号限制的存在**，这个页面截图可以留作佐证。

---

## 四、申诉流程（GitHub 免费账号完整路径）

流程共经过 5 屏，全程选错会绕到账单团队：

1. `https://support.github.com/contact`
2. 选类别：**Copilot**（比选 Account 更对口；页面若提示"免费账号不含技术支持"不必理会——**资格/封禁类问题对免费账号照样受理**）
3. 问题类型：**帐单、注册或激活 → 注册或激活**
4. 计划：**Copilot Free**（不要选 Pro/Business，否则路由到账单团队）
5. 子类别：**一般问题或功能请求**（另一项"错误、问题/API 限流/Actions"是技术故障入口，账号资格不归它管）

> AI 预检页会给几个选项，若看到"开始讨论"那是发社区论坛，**走左下「继续创建工单」**。

**纪律**

- ⚠️ **只开一张票**；重复开票会被判为重票、降优先级
- Subject 有 80 字符上限，被截断不影响
- **From 显示的邮箱就是回复去向**，别看错
- 等待期间：**别反复刷新 signup 页**（自动化特征会加重标记）、**别注册新号**（会被判规避封禁、按设备/IP 指纹连坐）

---

## 五、工单模板（四封，个人信息已替换为占位符）

### 5.1 首封工单（英文，直接用）

**Subject**
```
Unable to sign up for GitHub Copilot - infinite redirect loop on /github-copilot/signup
```

**Body**
```
Hi GitHub Support,

I'm writing about my account (username: [你的用户名], email: [你的邮箱]).

When I visit https://github.com/github-copilot/signup while logged in, the page
enters an infinite redirect loop, and the browser finally reports
ERR_TOO_MANY_REDIRECTS ("github.com redirected you too many times").
At one point the page briefly showed:
"Your account is unable to sign up for Copilot. Please contact Support."

What I have already tried, without success:
- Cleared all cookies and site data for github.com, then signed in again
- Tested in a private/incognito window and in a different browser
- Disabled all browser extensions
- Tried different network routes (direct connection and via VPN)

About my account:
- I have used this account for many years for personal
  development: reporting issues to open-source projects, hosting my personal
  pages, and regular code hosting.
- This is my only GitHub account. It has no organization seats or paid plans.
- I access GitHub from China, where connectivity to github.com is unreliable
  without a VPN/proxy. I understand this may sometimes trigger automated
  region checks, but all my usage is normal, personal development work.

Could you please review my account and tell me why Copilot signup is blocked,
or restore my eligibility? I'm happy to provide any additional verification
if needed.

Thank you very much for your time.

Best regards,
[你的用户名]
Date: 2026-10-09

Attachment: screenshot of the error page
```

> **写法要点**：GitHub 风控的典型触发点是「脚本化访问 / 非官方客户端 / 多账号 / 异常地区」。前三条要干净，第四条（VPN）**主动坦白并解释网络现实**——服务端本来就记着你的 IP，主动说明远好过被比对出来。
> ⚠️ **反面教材**：本单初稿里写了 "I have never used Copilot through unsupported clients"——这句话后来成了需要更正的**虚假陈述**。见 §5.4。

### 5.2 中文对照（自己看，不提交）

> 你好：我的账号在登录状态下访问 Copilot 开通页陷入无限重定向，浏览器报 ERR_TOO_MANY_REDIRECTS，页面曾短暂显示"Your account is unable to sign up for Copilot"。我已尝试清 Cookie、无痕、换浏览器、禁用扩展、切换网络，均无效。账号注册多年，只有这一个，无组织席位、无付费计划。因中国大陆直连 github.com 不稳定，我通过 VPN 访问，理解这可能触发自动地区检查，但均为正常个人开发使用。请核查为何 Copilot 开通被阻断，或恢复我的资格。

### 5.3 Support 第一轮追问：三要素回复

Support 会先要三样东西：**受影响用户名 / 首次发现时间 / 计划怎么使用 Copilot**。按次序逐条给即可。

```
- Affected username: [你的用户名]

- When I first noticed the restriction: approximately 30 days ago, around
  early September (I do not recall the exact date). It recurred today,
  October 9, 2026 (UTC+8), when opening
  https://github.com/github-copilot/signup resulted in an infinite redirect
  loop (ERR_TOO_MANY_REDIRECTS) and my dashboard showed "Your account is
  unable to sign up for Copilot. Please contact Support."

- Intended Copilot workflow: purely personal use. I would use Copilot Free
  inside VS Code for code completion and chat while working on small personal
  projects (Python/Rust/Go tools and my personal pages).
```

> **时间点不确定就写区间**（"约 30 天前/9 月初，记不清确切日期"）——后台有首次拦截记录，给区间比编精确日期可信。

### 5.4 ★ 收到指控后的坦白回信（本单实际促成解封的那封）

```
Hi,

Thank you for the explanation, and I owe you a fully honest answer, including
a correction to my earlier messages.

After carefully checking my records, I now recall that in 2024 I briefly used
a service called "CoCopilot" (cocopilot.org), which shared pooled GitHub
Copilot credentials among its users. At the time I did not fully understand
that this violated the GitHub Terms of Service and the Acceptable Use
Policies. I stopped using it long ago, and my earlier statement that I had
"never used Copilot through unsupported clients" was written from memory and
was inaccurate - I apologize for that. It was an oversight, not an attempt to
mislead.

To be clear: I have never shared my own credentials with others for profit,
and I have not used any credential-sharing service for a long time.

Upon receiving your message, I have taken the following actions:

1. Logged out of cocopilot.org and will never visit or use it again.
2. Removed all related extensions, tokens and configuration from my editors
   (VS Code / JetBrains). I verified that no Copilot-related or
   credential-sharing extension or configuration remains on my machines.
3. Reviewed github.com/settings/installations and
   github.com/settings/applications: only "Cloudflare Workers and Pages"
   (official) remains among GitHub Apps, and as a precaution I revoked all
   OAuth applications, so there are currently no authorized OAuth apps on my
   account at all.
4. I confirm that I agree to abide by the GitHub Terms of Service and the
   Acceptable Use Policies, including the prohibition on sharing
   credentials, and I will never use any credential-sharing tool or service
   again.

This account has been used for many years, is my only GitHub account, and is
very important to me. This usage was brief, ended long before this
restriction, and I have now fully remediated my account.

Could you please restore my Copilot eligibility? Thank you for your time.

Best regards,
[你的用户名]
Ticket [编号已隐去]
```

**这四个设计点是本单能成的关键**：

1. **主动更正此前的虚假陈述**并说明是"记忆疏忽"——GitHub 手里有你所有的信，装作没说过最危险
2. **只认那一段**（早年一次），不扩散到其他站点，避免引出新怀疑
3. **清理要给出可验证的清单**（退出账号、编辑器零残留、OAuth 全撤销），而不是空口承诺
4. **给复核者一个台阶**：短暂使用 + 早已停止 + 单账号 + 多年老号，构成典型的"初犯悔过"画像

> **别走的那条路**：初稿曾打算写"我不认识某社区也没用过"——这条不仅与事实不符，而且**后台有 OAuth 授权时间戳**。对已经检测到的指控，否认 = 零胜率；坦白 + 清理 = 唯一正解（也要承认存在"坦白后仍不解封"的可能）。

---

## 六、本机/账号清理核查清单（通用，给出证据链）

### 账号侧三处

| 检查点 | 入口 | 期望结果 |
|---|---|---|
| 已安装 GitHub Apps | `github.com/settings/installations` | 只剩认识/官方的 |
| 已授权 GitHub Apps | `github.com/settings/applications`（Authorized GitHub Apps） | 同上 |
| 已授权 OAuth Apps | 同页 **Authorized OAuth Apps** 段 | 不认识的第三方一律 Revoke |
| 组织席位冲突 | `github.com/settings/copilot` | 若有 active plan 说明已分配，不能再开个人 Free |

> 撤销 Git Credential Manager / VS Code 的 OAuth 授权**无害**——下次推送/登录会自动重新授权。

### 本机侧（PowerShell，本单实测命令）

```powershell
# 1. VS Code 扩展黑名单扫描
code --list-extensions | Select-String -Pattern "copilot|coco"

# 2. VS Code 用户设置里有无数共享/代理配置
Select-String -Path "$env:APPDATA\Code\User\settings.json" `
  -Pattern "copilot|cocopilot|github-enterprise" -ErrorAction SilentlyContinue

# 3. 编辑器本地历史（早年配过也可能留下痕迹）
Get-ChildItem "$env:APPDATA\Code\User\History","$env:APPDATA\Code\User\workspaceStorage" `
  -Recurse -Include "*.json","*.txt","*.md" -ErrorAction SilentlyContinue |
  Select-String -Pattern "cocopilot" -List

# 4. 扩展存储里有没有 copilot 相关目录
Get-ChildItem "$env:APPDATA\Code\User\globalStorage" -Directory |
  Where-Object Name -match "copilot|coco"

# 5. JetBrains 全家配置
Get-ChildItem "$env:APPDATA\JetBrains" -Recurse -Include "*.xml","*.json","*.options" `
  -ErrorAction SilentlyContinue | Select-String -Pattern "cocopilot" -List
```

**本单结果：六处全部零命中**（扩展 / settings.json / 本地历史 / workspaceStorage / globalStorage / 编辑器配置）。早年的痕迹在这台机器上已随环境变更消失，这也是回信里"我验证过机器上没有残留"能站得住的原因。

---

## 七、解封后验证与"网页端延时"

| 入口 | 现象 | 说明 |
|---|---|---|
| VS Code（`GitHub.copilot` + `GitHub.copilot-chat`） | 解封后立即可用 | 插件走自己的鉴权通道，**它通了 = 限制真的解除** |
| github.com/copilot 网页端 | 显示 Copilot Free 契约 + "license is on its way"；聊天一度 `Access denied / Single sign-on to view this chat` | **许可还在开通排队**，几分钟到几十分钟；不是二次封禁 |
| 收尾 | 网页聊天能正常检索仓库作答 | 全链路可用 |

网页端若长时间仍 Access denied：退出 GitHub 重新登录一次即可；它本来也是 Copilot 最次要的入口。

---

## 八、复盘：四条可复用的铁律

1. **陈述纪律**：工单里每一句否定都应能被后台记录验证。记不清就说"记不清"，**别写绝对化的 "never used / I do not recognize"**——这类句子一旦被记录戳穿，性质从"违规"升级为"违规 + 欺瞒"。
2. **发现假陈述立刻改**：与其等对方比对出来，不如自己更正并归因于记忆疏忽。本单从更正到位到解封，不到一小时。
3. **相关性不是因果**：时间吻合的"嫌疑对象"要按"它是否真的共享凭据"来判定，否则会把申诉写歪。
4. **清理要有证据链**：退出、卸载、扫描命令与结果——写给复核者看的是动作，不是形容词。

---

## 九、长期红线（给自己）

- 🔴 **绝不再用任何共享 AI 凭据的服务**（CoCopilot 一类的"开车/合租/号池"）。本单已收到明确警告：**再检测到一次 = Copilot 永久吊销 + GitHub 账号永久封禁，无第二次申诉**。
- 🔴 灰色 AI 社区/论坛：**用邮箱注册，禁用 GitHub OAuth 登录**（OAuth 授权会把你的账号和那个站绑在一起，站被风控归类你就跟着挨刀）。
- 🔴 VS Code 只装官方 `GitHub.copilot` / `GitHub.copilot-chat`，其余任何带 copilot 字样的第三方扩展一律不碰。
- ℹ️ Copilot Free 官方本来免费——**为了白嫖免费产品的共享池去赌一个多年老号，账算不过来**。

---

## 来源

- GitHub Community **#180874**：该重定向循环 = 账号侧资格限制的官方确认（循环背后实际是不能开通的提示）
- GitHub Community **#173478 / #192492 / #190119**：同类案例、工单话术与官方风控回复模板触发点
- devactivity.com：administrative block 机制与申诉要点
- 本单四封往返邮件（工单编号已隐去）原文
- 本机 PowerShell 扫描结果
