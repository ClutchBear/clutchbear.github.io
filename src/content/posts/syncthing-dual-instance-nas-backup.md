---
title: "Syncthing 双实例与 NAS 备份 · 运维手册"
description: "Windows 同一台机器跑两个 Syncthing 实例做 vault 双向镜像，再把多个工作目录单向备份到飞牛 NAS。含拓扑、.stignore 规则、计划任务自启、重装恢复与 23 条踩坑记录。"
pubDatetime: 2026-10-22T15:00:00+08:00
draft: false
tags:
  - Syncthing
  - NAS
  - 备份
  - Windows
  - 运维
---


> 覆盖从零搭建到踩坑收敛的全过程。
> **说明**：本文所有设备 ID、内网 IP、卷号、用户名等标识均已替换为占位符，路径与端口按实际环境填写即可。

## 一、这套东西在干什么

一句话：**把几个工作目录和 Obsidian vault，自动镜像到飞牛 NAS 上**，同时在 Windows 本机内让 vault 的 D 盘主站与 OneDrive 副份互相同步。

拆开就是三条链路：

| 链路 | 方向 | 作用 |
|---|---|---|
| 本机 `sthome` ⇄ `sthome2` | 双向 | D 盘 vault 主站 ⇄ OneDrive vault 副份，12 秒内互通 |
| 本机 `sthome` → NAS | 单向（sendonly → receiveonly） | 各工作目录 + vault 备份到 NAS |
| 本机 `sthome2` | 不连 NAS | 只负责 OneDrive 那一份 |

## 二、为什么必须跑两个实例

Syncthing 官方明确**不支持同一台设备上的两个 folder 互相直连**。而这里有两个物理目录需要互相同步：

- `D:\workbuddy\obsidian仓库`（主站，Obsidian 实际打开的）
- `C:\Users\<用户名>\OneDrive\obsidian仓库`（OneDrive 镜像，只做云端留底）

所以必须起**两个独立的 home**，各自是一个"设备"，互加为远程设备后用 TCP 直连。代价是本机常驻 4 个 `syncthing.exe` 进程 —— 这是正常的，不是重复启动。

> **进程拓扑：2 实例 × (监控进程 + 工作进程) = 4 个进程**。看到 4 个别去杀。

## 三、拓扑图

```text
┌──────────────────── Windows 本机（127.0.0.1）────────────────────┐
│                                                                  │
│  [sthome 主实例]              [sthome2 镜像实例]                  │
│   GUI :56899 / 数据 :56902     GUI :53689 / 数据 :53692           │
│   设备ID <主实例ID>            设备ID <镜像实例ID>                 │
│      │                              │                             │
│      │ tcp://127.0.0.1:53692         │                             │
│      └──────── sendreceive ─────────┘                             │
│      │                              │                             │
│  D:\workbuddy (vault 主站)     OneDrive\obsidian仓库 (副份)        │
│  D:\workbuddy  D:\work                                            │
│  D:\tools      D:\blog                                            │
└──────────────────┬───────────────────────────────────────────────┘
                   │ tcp :22000  sendonly → receiveonly
                   ▼
┌───────────────── 飞牛 NAS（<NAS-IP>）─────────────────┐
│  Syncthing 容器    GUI :8384 / 同步 :22000             │
│  设备ID <NAS设备ID>                                    │
│  /vol<卷号>/1000/<数据盘>/bak/                          │
│    workbuddy · work · tools · blog                     │
└────────────────────────────────────────────────────────┘
```

## 四、关键路径与端口（最容易记错的地方）

| 项 | 值 | 备注 |
|---|---|---|
| 程序与配置根 | `D:\Program Files\syncthing\` | 迁到此处的目的是**重装系统不丢配置** |
| 主实例 home | `D:\Program Files\syncthing\sthome` | GUI **127.0.0.1:56899** |
| 镜像实例 home | `D:\Program Files\syncthing\sthome2` | GUI **127.0.0.1:53689** |
| API key | `sthome\config.xml` 里的 `<apikey>` | **会变，必须动态读，别硬编码** |
| NAS Syncthing GUI | `http://<NAS-IP>:8384` | 有 basic auth |
| NAS 同步端口 | `22000/tcp + udp` | 未映射时表现为设备一直 offline |
| NAS 备份落点 | `\\<NAS-IP>\<数据盘>\bak\`（映射为 `Y:\bak`） | 容器内映射为 `/data/{name}-backup` |
| NAS 容器卷根 | `/vol<卷号>/1000/<数据盘>/bak` | ⚠️ 卷号不一定是 `vol1`，先 `ls /vol*` 确认，这里踩过坑 |

> 🔴 **最常见的错**：把 `8384` 当成本机 GUI。8384 是 NAS 的，本机是 **56899**。
> 另外 `56902` 是同步协议口，**不是 SSH** —— 拿它去连 VS Code Remote-SSH 必然失败。

## 五、五个 folder 明细

| label | folder id | 类型 | 本机路径 | 文件数 | 体积 | 备份到 NAS |
|---|---|---|---|---|---|---|
| workbuddy | `workbuddy` | sendonly | `D:\workbuddy` | 8,598 | 0.85 GiB | ✅ |
| obsidian仓库 | `obsidianvault` | sendreceive | `D:\workbuddy\obsidian仓库` | 1,103 | 0.10 GiB | ⚠️ 见待办 |
| blog | `ojxzz-vhqis` | sendonly | `D:\blog` | 443 | 0.01 GiB | ✅ |
| work | `4ensc-samjr` | sendonly | `D:\work` | 25,520 | 71.20 GiB | 🔄 传输中 |
| tools | `cdtek-swtnq` | sendonly | `D:\tools` | 24,604 | 59.00 GiB | 🔄 传输中 |

> `obsidianvault` 在**两个实例里各有一份**：主实例指向 D 盘主站，镜像实例指向 OneDrive 副份，靠两实例互连实现双向同步。
> 注意它是唯一一个 **sendreceive**（双向）的 folder —— 因为 vault 两边都要能改。

## 六、`.stignore` 规则体系 —— 为什么必须有 `(?d).git`

### 6.1 规则的作用

`.stignore` 放在 folder 根目录，每行一条 glob。本次优化的核心目的是**把"体积大、文件碎、可重建"的东西挡在同步之外**，否则几十万个小文件会把扫描和传输拖死。

### 6.2 五类规则

| 类别 | 典型条目 | 理由 |
|---|---|---|
| 归档与旧备份 | `/_archive`、`/bak/backup-*`、`/*log*.txt` | 十几 GB 的历史快照，没有备份价值 |
| 依赖与构建产物 | `node_modules`、`.venv`、`dist`、`target`、`__pycache__` | 可随时重建，且小文件极多 |
| 版本库元数据 | `(?d).git`、`.git-*`、`.hg`、`.svn` | **见 6.3，这条不能省** |
| 浏览器 profile | `cdp-profile-*` | Chromium 调试缓存，几千个碎文件且天天变 |
| 通用垃圾 | `*.log`、`*.tmp`、`*.pyc`、`Thumbs.db`、`.DS_Store` | 无价值 |

### 6.3 🔴 `(?d).git` 是**必须**的，两次踩同一个坑

**现象**：folder 里出现几十到几百条 `hashing: open \\?\D:\...\.git\objects\xx\...: Access is denied.`

**根因**：git 对象文件在被并发写入 / 删除挂起（delete-pending）时，任何读取都会返回 `ERROR_ACCESS_DENIED(5)`。Syncthing 扫描时撞上就记一条错误。

**两次实绩**：

| 场景 | folder | 错误数 | 缺失的规则 |
|---|---|---|---|
| 上午 | `workbuddy` | 34 | 重写 `.stignore` 时把旧配置里的 `(?d).git` 弄丢了 |
| 傍晚 | `work` | 397 | `.stignore` 从来没写过这条 |

**代价**：git 历史不进 NAS 备份（工作文件照备）。可接受 —— 这些仓库基本都有远端仓库，历史可重新拉取。

**教训**：`(?d).git` 属于"重写 `.stignore` 时绝对不能删"的条目。改动前先 `GET /rest/db/ignores?folder=<id>` 备份现有内容。

### 6.4 嵌套 folder 守卫

`D:\workbuddy\obsidian仓库` 同时落在 `workbuddy` 和 `obsidianvault` 两个 folder 下，而 Syncthing **不支持 folder 路径嵌套**。所以 `D:\workbuddy\.stignore` 里必须有一行 `/obsidian仓库`，让 vault 子树只走 `obsidianvault` 通道。

## 七、开机自启：最终方案是**计划任务**，不是 Run 键

### 7.1 演进过程（三代方案，前两代都失败）

| 代 | 方案 | 结果 |
|---|---|---|
| 1 | `HKCU\...\Run\SyncthingVault` = 某个 pythonw 脚本 | ❌ 依赖宿主软件的 Python 绝对路径，版本一变就静默失效 |
| 2 | Run 键直接调 `syncthing.exe serve --no-console` | ❌ 被 Windows 启动项节流**延迟约 95 秒**；等它触发时用户已手动启动 → 撞锁 → **自动弹出浏览器** |
| 3 | **两个独立计划任务** | ✅ 端到端实测通过 |

### 7.2 现在生效的配置

```text
任务名：Syncthing Autostart (Main)
  执行：D:\Program Files\syncthing\syncthing.exe
  参数：serve --no-console --no-browser -H "D:\Program Files\syncthing\sthome"

任务名：Syncthing Autostart (Mirror)
  执行：同上
  参数：serve --no-console --no-browser -H "D:\Program Files\syncthing\sthome2"
```

两个任务的共同属性：

| 属性 | 值 | 为什么 |
|---|---|---|
| 触发器 | `MSFT_TaskLogonTrigger`（登录时） | 用户级，不需要管理员 |
| 延迟 | 无 | Run 键的 95 秒延迟就是被这个坑的 |
| `ExecutionTimeLimit` | `PT0S`（不限） | 长驻进程，超时会被杀 |
| `MultipleInstances` | `IgnoreNew` | 防重复启动 |
| 运行身份 | `Interactive` / `Limited` | 不需要提权 |
| `--no-browser` | 必加 | 撞锁时不弹浏览器 |
| `--no-console` | 必加 | 不闪黑窗（Win11 24H2+ 默认已生效） |

### 7.3 🔴 为什么必须是**两个**任务

**计划任务的多个 Action 是串行执行的。** 如果建一个任务带两个 Action，第一个 `syncthing serve` 是长驻进程永不退出，第二个 Action **永远轮不到** —— 镜像实例永远起不来。

### 7.4 判断"谁启动的"的指纹

跑着的进程命令行如果是 `syncthing.exe -H ...`（**没有** `serve --no-console`），说明是手动 bat 启动的；如果有 `serve --no-console`，才是计划任务启动的。这个指纹是定位自启问题的关键。

## 八、重装系统后如何恢复（3 步）

程序和配置都在数据盘，**重装 C 盘不会丢**。但自启登记在注册表 / 计划任务里，**重装必丢**，需要重建。

### 8.1 三个文件都在程序目录

| 文件 | 编码 | 用途 |
|---|---|---|
| `install-autostart.ps1` | UTF-8 **带 BOM** | 真正干活的脚本：注册两个计划任务 |
| `enable-autostart.bat` | **GBK** + CRLF | 双击入口，有中文进度输出 |
| `syncthing-autostart.vbs` | **GBK** + CRLF | 静默版，无窗口 |

### 8.2 操作

1. 双击 `enable-autostart.bat`（想静默就双击 `.vbs`）；
2. 看到两个任务注册成功的提示；
3. 重登或重启，**不点任何东西**，直接开 `http://127.0.0.1:56899` —— 出界面就成功。

脚本是幂等的，重复跑无副作用（`Register-ScheduledTask -Force`）。

> ⚠️ **别再用 `.reg` 文件恢复 Run 键** —— 会恢复已废弃的启动方式，重新引入 95 秒延迟 + 弹浏览器。

### 8.3 如果还是起不来，查这个

```powershell
Get-ScheduledTaskInfo -TaskName "Syncthing Autostart (Main)" | Select LastTaskResult, LastRunTime
```

`LastTaskResult = 0` 是成功；`2147946720`（0x80070420）是"任务实例已在运行"，属正常。

## 九、踩坑全记录

按"现象 → 根因 → 修法"排列，都是实际踩到的。

### 9.1 拓扑与路径类

**① 移动程序目录后整个自启废掉**
把 Syncthing 目录搬到新位置后，三个启动脚本里的路径、注册表 Run 项**全都还指着旧位置** ⇒ 手动和开机都起不来。
> **通用教训**：移动任何常驻程序目录后，必须同步检查 ①程序内脚本 ②注册表 Run/自启 ③计划任务 ④快捷方式。

**② 同机双实例必须两个 home**
Syncthing 不支持同一设备上两个 folder 直连，硬配会死循环。

**③ 嵌套 folder 会被直接拒绝**
`D:\workbuddy` 已同步时再加 `D:\workbuddy\space\tools`，Syncthing 直接报错。修法是在父 folder 的 `.stignore` 里排除子目录。

**④ v2.x 设备地址必须带协议前缀**
裸写 `127.0.0.1:53692` 报 `first path segment in URL cannot contain colon`，必须写 `tcp://127.0.0.1:53692`。

**⑤ 真死循环的三个触发条件**（记住，别碰）
- 同一物理目录在本机配成两个 folder；
- 两台设备互相 `sendreceive` 同一目录；
- folder 路径互相包含。

### 9.2 NAS 容器类

**⑥ 设备一直 offline → 22000 没映射**
现象是设备 `connected=false`，但 NAS 的 8384 GUI 能打开。真因是 compose 里缺 `22000:22000/tcp` + `udp`，或加了没重建容器。

**⑦ `Failed to verify encryption consistency`**
NAS 端 folder 被建成了"加密接收"（receive-encrypted），而本机是明文共享。修法：NAS 删掉该 folder、清空加密残留，重新接受时选**「仅接收」**。

**⑧ `mkdir /data/blog-backup: permission denied` —— 不是权限问题，是没挂载**
Syncthing 想在容器根 FS 建目录，`/data` 归 root，PUID=1000 建不了。
**判据**：看宿主机 `Y:\bak` 下有没有对应目录 —— 没有就是 volume 没生效，别去折腾 chown。

**⑨ 最阴的一个：目录 `root:root 700` → 静默写入失败**
挂载正确、PUID=1000 正确，但 `/data/workbuddy-backup` 属主是 `root root 700`，1000 号用户进不去。
现象极隐蔽：**不报错**，只是 `needItems=1` 一直不掉，探针文件 180 秒仍不落地。
**修法**：NAS 上 `chown -R 1000:1000 <备份落点>`。
> 存量十几万文件是早期以 root 运行时写进去的，所以"看着有内容"具有欺骗性。

**⑩ `docker exec syncthing id` 返回 root 是正常现象**
linuxserver 镜像用 s6-overlay，PID 1 是 root，`docker exec` 默认也落 root。**这个结果不能用来判定 Syncthing 进程用户**。要查真用户得看 `Config.Env` 里的 PUID/PGID。

### 9.3 忽略规则类

**⑪ 漏 `(?d).git` → 34 条 / 397 条 `Access is denied`**
见第六章。两次都是同一个坑。

**⑫ 「连 `Get-Acl` 都拒绝」的文件不是占用**
某个目录里有 2 个文件能 `stat` 出大小但一读就拒绝访问，`Get-Acl` / `icacls` 也报"拒绝访问"。
根因是文件 DACL 对当前用户完全无授权（所在目录属主是**旧系统遗留的孤儿 SID**，与当前账户 SID 不同）。
**修法**：管理员 `takeown /F <file> /A` → `icacls <file> /reset` → `icacls <file> /grant "*S-1-5-32-545:(R)"`。
**判据**：三步都做了仍失败 ⇒ 不是 ACL 而是**删除挂起**，重启即解。

### 9.4 自启类

**⑬ Run 键被节流延迟 95 秒**
现象是"重启后 GUI 打不开，手动点 bat 才行"，看起来像没生效。
真相：日志里有 `Seems to already be running, launching GUI instead` ⇒ Run 键**确实执行了**，只是被 Windows 启动项节流拖到开机后 95 秒。等它触发时用户已手动启动，于是撞锁并自动开浏览器。
**结论**：Run 键不适合常驻服务，改用计划任务。

**⑭ 一个计划任务多个 Action 串行执行**
第一个长驻进程不退出，第二个永远轮不到。必须拆成两个任务。

### 9.5 脚本编码类（中文 Windows 专属）

**⑮ `.bat` 一片「'xxx' 不是内部或外部命令」+ 中文乱码**
三重根因叠加：① 文件存成 **UTF-8**，而中文版 cmd 按 **ACP=936(GBK)** 逐字节解析；② 用 **LF** 换行；③ 顶部写 `chcp 65001` 会破坏后续行的解析。
**修法**：**GBK 编码 + CRLF 换行 + 不写 `chcp`**。

**⑯ 批处理里的 `find` / `reg` 被 Git Bash 的同名程序顶掉**
现象 `find: 鈥�/i鈥�: No such file`。
**修法**：系统工具一律写全路径 `%SystemRoot%\System32\reg.exe`、`tasklist.exe`、`findstr.exe`。

**⑰ `.ps1` 在 PowerShell 5.1 里中文乱码**
PS 5.1 靠 **BOM** 识别 UTF-8 ⇒ 必须存成 `utf-8-sig`。

**⑱ `.reg` 文件注释别写中文**
reg 期望 ANSI/UTF-16，UTF-8 中文注释有解析风险 ⇒ 注释一律英文，文件用 CRLF。

### 9.6 工具链类

**⑲ 常驻代理会劫持 localhost API**
urllib 直连 `127.0.0.1:56899` 报 **502 Bad Gateway**（代理把 localhost 也拦了）。
**修法**：`urllib.request.build_opener(urllib.request.ProxyHandler({}))` 绕开。

**⑳ API key 会变**
从 `config.xml` 读 `<apikey>`，硬编码旧 key 会 403。

**㉑ SMB 目录列表有缓存**
删掉文件后 `os.listdir` 仍显示存在。**判据用 `os.stat`**，删掉会报 `WinError 59`。

**㉒ 🔴 绝不能让带文件访问限制的 shell 启动 Syncthing**
从受安全策略约束的进程树（如某些带沙箱/安全中心的终端）启动，会**继承文件访问规则**，扫描时读私人目录被拦 ⇒ 同步必然残废（本次实测 507+ 文件被拦）。
**常驻服务只能由用户自己双击启动，或走计划任务。**

**㉓ 受限环境里无法让进程常驻**
`Start-Process` / `WMI Win32_Process.Create` / `wscript` 都可能被安全策略拦（LOLBin 规则），沙箱内启动的进程随会话结束被回收。
连带后果：`reg.exe`、`wscript.exe`、`cscript.exe` 可能都在黑名单里 ⇒ **注册表导入和 VBS 执行无法在沙箱内实测**，只能静态解析验证后到真机自检。

## 十、REST API 速查

本机 GUI `http://127.0.0.1:56899`，头带 `X-API-Key`（从 `sthome\config.xml` 读）。

```python
# 读忽略规则（改动前先备份！）
GET  /rest/db/ignores?folder=<id>

# 下发忽略规则（body: {"ignore": ["line1", "line2", ...]}）
POST /rest/db/ignores?folder=<id>

# 触发扫描
POST /rest/db/scan?folder=<id>

# 状态 / 进度 / 错误
GET  /rest/db/status?folder=<id>
GET  /rest/db/completion?folder=<id>&device=<29位设备ID>
GET  /rest/folder/errors?folder=<id>

# 配置读写
GET  /rest/config/folders
PUT  /rest/config/folders/<id>
GET  /rest/config/devices
PUT  /rest/config/devices/<完整29位设备ID>    # 不能用索引！
```

**两个坑**：
- `/rest/config/devices/<idx>` 不存在，必须用**完整 29 位设备 ID**；
- `/rest/db/completion` 在只有一个设备时返回 **dict 不是 list**。

## 十一、待办 / 未完成

| 项 | 状态 | 说明 |
|---|---|---|
| 🔴 `obsidianvault` → NAS 通道 | **未打通** | completion 0%，1,217 项待传；备份落点下查不到 `vault` 目录 ⇒ **NAS 端大概率还没接受这个 folder 共享**。需在 NAS GUI 点接受，类型选**仅接收** |
| `work` 传输 | 进行中 | 43.6%，剩 40.83 GiB |
| `tools` 传输 | 进行中 | 81.1%，剩 11.16 GiB |
| `bak\数码` | 有意排除 | 与备份无关，不挂进容器 |
| 旧启动器清理 | 待定 | 只启动不写自启的 bat、依赖 pythonw 的旧脚本是否删除 |

## 十二、几条铁律

- 🔴 **绝不由带访问限制的 shell 启动 Syncthing**（见 9.6 ㉒）；
- 🔴 改 `.stignore` 前先 GET 备份，**`(?d).git` 不能删**；
- 🔴 接收端一律 **Receive Only（仅接收）**，防本地误动回流；
- 🔴 手机若要接这套，只加主实例设备、用静态地址，别开全球发现。
