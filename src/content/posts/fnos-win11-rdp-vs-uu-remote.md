---
title: "飞牛虚拟机 Win11 用 UU 远程连接卡顿，改用 RDP 后流畅度堪比本机"
description: "fnOS 上的 Win11 虚拟机：显卡是 QEMU stdvga 导致分辨率锁死，改 VirtIO-GPU 解决；但远程用 UU 远程/串流软件依旧卡到没法用、鼠标还被钳在窗口里——因为软编码在虚拟机内抢 CPU。改用 RDP（指令级重定向，不做像素编码）后与操作本机无差别，附完整开启步骤与四个踩坑。"
pubDatetime: 2026-11-07T12:00:00+08:00
draft: false
tags:
  - fnOS
  - 虚拟机
  - Win11
  - RDP
  - 远程桌面
---

> 环境：fnOS 虚拟机应用 / Win11 24H2（build 26100）+ 精简版 Win11（Tiny11 23H2 基底）/ 先后用过 UU 远程、VNC、RDP
> 初诊 → 复诊，状态：已解决

## 一、结论先行

| 现象 | 根因 | 处置 | 结果 |
|---|---|---|---|
| 分辨率调不了 | 虚拟机 GPU 类型是 **QEMU 标准 VGA（stdvga）**，Windows **没有任何 WDDM 驱动** | GPU 类型改 **VirtIO-GPU** 后重启 | ✅ 解决 |
| 画面模糊、拖影、发虚 | 同上（无 D3D、无 DXGI 桌面复制） | 同上 | ✅ 明显改善 |
| UU 报「被控制端显卡驱动过低」 | 虚拟显卡**没有硬件编码器**（NVENC/QSV/AMF） | 无法消除 | ⚠️ 能力缺失告警 |
| **卡得没法用**（鼠标拖影、动画掉帧） | **UU 软编码在客户机内跑**，吃满 4 vCPU | 换 **RDP** | ✅ 与操作本机无差别 |
| **鼠标被钳制在窗口内**，只能 Ctrl+Alt+Del 脱出 | UU 退到**绝对定位鼠标模式** | 换 **RDP** | ✅ 可自由移出窗口 |

**一句话**：`stdvga` 在 Windows 上是「无驱动」状态，换成 `VirtIO-GPU` 才有真正的显示驱动；而**远程方式**上，凡走「截屏 + 视频编码」的串流软件（UU/GameViewer）在虚拟机上必然退化——没有硬件编码器就只能软编，软编就要和 Windows 抢 CPU。**正解是 RDP：它传绘图指令不传画面，不做像素编码，因此完全不需要 GPU 硬编。**

## 二、症状一：分辨率锁死——虚拟显卡根本没驱动

设备管理器 → 显示适配器，出问题时是这两项：

```text
显示适配器
├─ GameViewer Virtual Display Adapter   ← UU「超级屏」自装的软件虚拟屏（ROOT\DISPLAY\0000）
└─ Microsoft 基本显示适配器              ← 真正的虚拟显卡，但没驱动，微软兜底
```

用命令取真实硬件 ID：

```powershell
Get-CimInstance Win32_VideoController | Format-List Name, PNPDeviceID, DriverVersion
```

输出里的 `PNPDeviceID` 决定一切：

| PNPDeviceID 含 | 虚拟显卡类型 | 说明 |
|---|---|---|
| `VEN_1234&DEV_1111` | **QEMU 标准 VGA（stdvga）** | Windows 无 WDDM 驱动，只能用兜底驱动 ← **本次就是这个** |
| `VEN_1AF4&DEV_1050` | VirtIO-GPU | 有官方驱动（viogpudo） |
| `VEN_1B36&DEV_0100` | QXL | 驱动在 spice-guest-tools，**不在** virtio-win ISO 里 |
| `VEN_15AD` | VMware SVGA | 走 VMware Tools |

> **为什么 stdvga 必然出问题**：`Microsoft 基本显示适配器` 不支持 **DXGI 桌面复制**（Desktop Duplication 需要 WDDM 1.2+ / D3D11）。远程软件靠它抓屏，抓不到就退回 GDI 兼容路径，于是画面糊、CPU 占用高，同时弹「显卡驱动过低」。

## 三、修复：改 GPU 类型，5 分钟，不用下载任何东西

1. **建快照**（fnOS 虚拟机应用 → 选中该 VM → 快照）
2. VM 内**正常关机**（不是强制断电）
3. fnOS 虚拟机 → 编辑该 VM → **GPU 类型改成 `VirtIO-GPU`** → 保存
4. **开机**
5. Windows 会**自动装上驱动**，设备管理器变成：

```text
显示适配器
├─ GameViewer Virtual Display Adapter
└─ Red Hat VirtIO GPU DOD controller     ← Microsoft 基本显示适配器 已消失
```

6. 验证：

```powershell
Get-CimInstance Win32_VideoController | Format-List Name, PNPDeviceID, DriverVersion
```

期望 `Name` = `Red Hat VirtIO GPU DOD controller`，`PNPDeviceID` 含 `VEN_1AF4&DEV_1050`。桌面右键 → 显示设置，**分辨率下拉框应该可选了**。

### ★ 关键经验：不用先下 837 MB 的 virtio-win ISO

`pnputil /enum-drivers | Select-String "viogpudo"` **查不到**该驱动，但改完 GPU 类型重启后 Win11 24H2 **自己就装上了**（推测走 Windows Update 驱动库）。

**正确顺序永远是**：改 GPU 类型 → 重启 → 看设备管理器 → **装不上再考虑下 ISO**。

## 四、为什么 UU 的「显卡驱动过低」提示消不掉

`DOD` = **Display Only Driver（纯显示驱动）**。它有 WDDM 显示能力、能调分辨率、能走 DXGI 桌面复制，但**没有 3D 加速引擎，也没有硬件编码器**。

UU 远程的被控端编码链路绑死在真实 GPU 的硬编上（NVIDIA NVENC / Intel QSV / AMD AMF）。旁证：

- 官方说明写「**暂不支持虚拟机、WinServer 等平台设备**」
- 「真彩模式」要求被控端是 NVIDIA/AMD/Intel，且主被控端编码格式要匹配

所以这句提示**不是「驱动版本旧」，而是「这台机器没有能用的硬件编码器」**。升级/重装驱动都无效。

**实际影响**：会退回 CPU 软编码，画面能用、清晰度正常，代价是 CPU 占用高一些——但在 4 vCPU 的虚拟机上，这个代价足以把整个系统拖死（见 §六）。

## 五、症状二：卡得没法用 + 鼠标被钳制

新装的一台 Win11（4 vCPU / 8 G），症状：鼠标拖影、窗口拖动卡、动画掉帧。当时的猜测是「装在机械盘上」，结果换用 fnOS 自带 VNC 立刻可接受 ⇒ **与存储无关**。

### 5.1 先排除的两个误判方向

| 曾被怀疑 | 实测 | 结论 |
|---|---|---|
| qcow2 在机械盘（7200rpm） | 盘确实是机械盘，4K 随机写 ~100 IOPS | 只影响**开机和加载**，不影响「拖窗口」这种已加载后的交互 |
| virtio-vga 缺驱动导致软件合成 | QEMU 参数已是 `-device virtio-vga`，等于 VirtIO-GPU，驱动自动装上（同 §三） | 不是主因 |

**判据**：卡在「**已进入桌面后的连续交互**」⇒ 查画面链路；卡在「**开机/开程序/磁盘 100%**」⇒ 查存储。这两类症状必须分开定位，否则容易一头扎进磁盘里。

### 5.2 为什么 VNC 反而比 UU 流畅

这是本次最反直觉、也最值得记的一点：

| | UU 远程 / GameViewer | fnOS 自带 VNC |
|---|---|---|
| 编码在哪跑 | **客户机内**（Windows 里的服务进程） | **宿主机 QEMU 里**（内建 VNC server） |
| 抓屏方式 | DXGI 桌面复制 → 拿不到就退 GDI | 直接读 QEMU 的**帧缓冲内存** |
| 编码 | 无硬编码 ⇒ libx264 **软编码** | RFB 轻量压缩（hextile/zlib），几乎不耗 CPU |
| 对客户机 CPU 的占用 | **高**（4 vCPU 直接吃满） | **≈0** |
| 额外组件 | 还装 `GameViewer Virtual Display Adapter`（超级屏，多一层桌面合成） | 无 |

**一句话**：VNC 的服务端在虚拟机**外面**，画面靠宿主机读帧缓冲；UU 的服务端在虚拟机**里面**，要和 Windows 抢那 4 个 vCPU。画面质量 VNC 更差，但**不占用被控端资源**，所以实际体感更流畅。

### 5.3 鼠标被钳在窗口里：同一个根因的第二个症状

同一个 UU 客户端，连这台虚拟机时鼠标锁在窗口里；连办公室的物理机完全正常。

**这不是两件事，是同一个根因。**

远程软件的鼠标有两种模式，用哪种由**被控端能力探测**决定：

| 模式 | 实现前提 | 表现 |
|---|---|---|
| **相对模式**（游戏/真彩模式） | 能隐藏本地光标 + 能拿到 Raw Input 相对位移 + 有 DXGI/硬编走高级通道 | 光标「无限移动」，随时可还给本地 ⇒ **能自由移出窗口** |
| **绝对定位模式**（兼容回退） | 以上任一不满足就退到这里 | 本地坐标 → 远端坐标**一一映射**，光标一旦跑出窗口映射就失效 ⇒ **必须钳制在窗口内** |

虚拟机上能力探测全线失败（无硬编、只有 DOD 纯显示驱动、DXGI 桌面复制可靠性存疑），于是退到绝对定位 ⇒ 鼠标锁死。物理机显卡/硬编/桌面复制齐全 ⇒ 走相对模式。**所以「连办公室电脑没事」恰好印证了根因在虚拟机的图形能力，不在网络、不在 UU 的版本。**

**Ctrl+Alt+Del 为什么能脱身**：它把 Windows 切到安全桌面（`Winlogon`），远程软件在这个桌面上拿不到常规窗口捕获，于是释放了钳制。反过来也说明——钳制是在普通桌面下生效的。

## 六、为什么 RDP 堪比本机

VNC 已经够用，但 RDP 还能再好一档，因为它是**指令级重定向**（传「画一个矩形、贴一段文字」），不是像素级截屏，1080p 桌面通常只要 **1~5 Mbps**，且自带剪贴板、声音、多显示器、文件重定向。

| | RDP | VNC | UU / 串流软件 |
|---|---|---|---|
| 传输内容 | **绘图指令 + 表面重定向**（D3D/GDI 命令流） | 帧缓冲**像素差分** | 截屏 → **视频编码**（x264/HEVC）|
| 谁负责渲染 | **客户端本地渲染**，文字用本机字体清晰输出 | 远端渲染好，客户端只是贴图 | 远端编码、客户端解码 |
| 静止桌面带宽 | **≈0**（只有心跳） | 低 | 持续码流 |
| 滚动 / 打字 | 几十 ~ 几百 kbps | 整片区域重传，明显滞后 | 有 GOP 缓冲，延迟 2~3 帧起 |
| 分辨率 | 自动匹配客户端窗口，**点对点无缩放** | 固定为客户机设置 | 可能要缩放 |
| 启用条件 | 无 GPU 要求，**软件渲染即可** | 无 | 要求硬编，虚拟机里必退化 |

**一句话**：RDP 是「把怎么画告诉客户端」，VNC 是「画好了给你看」，串流是「拍成视频给你播」。所以 RDP 在局域网里的体感上限就是本机——它压根没有编码/解码这两段延迟。

> 这也解释了为什么 RDP **不需要**虚拟显卡有 3D 加速或硬编码器：它不做像素编码。之前一路纠缠的「virtio-vga 无硬编」问题，对 RDP 完全免疫。

实测原话：**「跟本机用起来几乎没有区别。我刚开始还以为是操作笔记本呢……」**

## 七、开启 RDP：步骤与四个坑

在客户机内管理员 PowerShell 执行：

```powershell
# 1) 允许 RDP 连接（注册表闸门）
Set-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name fDenyTSConnections -Value 0

# 2) 启动服务
Set-Service TermService -StartupType Automatic
Start-Service TermService

# 3) 放行防火墙 —— ★ 必须用 -Name（语言无关的稳定 ID），不要用 -DisplayGroup
Enable-NetFirewallRule -Name 'RemoteDesktop-UserMode-In-TCP','RemoteDesktop-UserMode-In-UDP'

# 4) 验证监听
Get-NetTCPConnection -LocalPort 3389 -State Listen
```

宿主机侧 `mstsc /v:<Win11-IP>` 连接即可。

### 坑 1：`-DisplayGroup "远程桌面"` 在中文系统上报 ObjectNotFound

```text
Enable-NetFirewallRule : 找不到任何"DisplayGroup"属性等于"远程桌面"的 MSFT_NetFirewallRule 对象
```

**原因**：`DisplayGroup` 是 **MUI 本地化显示字符串**，同一台机器上 `Get-NetFirewallRule` 返回的可能是英文 `Remote Desktop`、也可能是资源键，取决于系统的语言资源加载状态——拿它做筛选项天然不可靠，中文系统尤其容易踩。

> **实测佐证（中文版 Win11 Pro 25H2）**：规则 `RemoteDesktop-UserMode-In-TCP` 的 `DisplayName` 实际返回 **`Remote Desktop - User Mode (TCP-In)`**（纯英文）。也就是说中文系统上这个组的真实值就是英文 `Remote Desktop`，写 `-DisplayGroup "远程桌面"` 必然 `ObjectNotFound`。但 `-DisplayGroup "Remote Desktop"` 也不建议用——换个语言包它又可能变，`-Name` 才是唯一稳定锚点。

**正确做法**：用 `-Name`，规则 ID 是**语言无关**的固定字符串。

| 规则 Name | 作用 |
|---|---|
| `RemoteDesktop-UserMode-In-TCP` | RDP 3389/TCP 入站 |
| `RemoteDesktop-UserMode-In-UDP` | RDP UDP 传输（可选，提升弱网体验） |
| `RemoteDesktop-Shadow-In-TCP` | 远程协助/影子会话（不需要） |

先确认规则确实存在：

```powershell
Get-NetFirewallRule -Name 'RemoteDesktop-UserMode-In-TCP','RemoteDesktop-UserMode-In-UDP' -ErrorAction SilentlyContinue |
    Format-Table Name, DisplayName, Enabled, Profile, Direction
```

**若返回空**（精简版系统可能删了预置规则），直接新建一条，不用管组名：

```powershell
New-NetFirewallRule -DisplayName 'Remote Desktop (TCP-In) 3389' -Direction Inbound `
    -Protocol TCP -LocalPort 3389 -Action Allow -Profile Any
```

### 坑 2：`Restart-Service TermService` 之后 listener 要十几秒才 LISTENING

实测时间线：

```text
T+0s   Restart-Service TermService -Force     → 成功，无报错
T+3s   netstat -ano | findstr :3389
       TCP  [::]:3389  [::]:0  CLOSED  4528   ← 只有 IPv6 dual-stack 条目，状态 CLOSED
       UDP  0.0.0.0:3389 / [::]:3389           ← UDP 正常
T+180s 再次 netstat（期间没做任何配置改动）
       TCP  0.0.0.0:3389  0.0.0.0:0  LISTENING  12628   ← 自己好了
```

**判据**：TCP 3389 显示 **`CLOSED` 而不是 `LISTENING`** = 「socket 已绑定但还没 `listen()`」，是 listener **正在初始化**，不是配置错误、也不是证书缺失。此时 `PortNumber` / `fEnableWinStation` / `SecurityLayer` 全是正常值就说明配置没问题，**等**即可（或再 `Restart-Service` 一次并等 15~30 秒）。

> 别被 CLOSED 带偏去查证书、查 IPsec、查端口占用——那是「等了很久仍 CLOSED」才需要做的排查。同理，`Get-NetTCPConnection -LocalPort 3389 -State Listen` 在初始化期间会直接抛 `ObjectNotFound`（CIM 查不到匹配对象），这个报错**等价于「还没监听」，不是命令写错**。

### 坑 3：`Restart-Service TermService -Force` 会不会踢掉当前会话

不会。重启 TermService 只断开 **RDP 会话**，当前是**控制台会话**（在虚拟机窗口/VNC 里操作），不受影响。反过来，如果你正通过 RDP 连着自己去重启 TermService，就会把自己踢下线——那种情况要在**另一个**会话里操作。

### 坑 4（更前置）：家庭版根本没有 RDP 服务端

`fDenyTSConnections` 改成功了也不代表能用——**Win11 家庭版没有 `TermService` 的完整实现**，系统属性里「远程桌面」那一栏是灰的。先确认：

```powershell
(Get-CimInstance Win32_OperatingSystem).Caption
(Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion').EditionID
```

| `EditionID` | RDP 服务端 |
|---|---|
| `Professional` / `Enterprise` / `EnterpriseS`(LTSC) / `Education` | ✅ 有 |
| `Core` / `CoreSingleLanguage`（家庭版） | ❌ **没有** |

精简版系统的基底版本不同批次会有差异，装完先查这个，别在防火墙上空转。

## 八、日常使用：双屏窗口模式 + 预配置文件 + IP 固定

### 8.1 双显示器的正确用法：窗口模式，把 RDP 丢到副屏

实测（本机内屏 2560×1600 + 外置 2560×1440，均 175%）：

> 原话：**「我现在两个显示器，外置的显示器，可以直接把 RDP 的拖过去。感觉就跟操作一台机子一样。」**

| 用法 | 操作 | 客户机分辨率 | 适合 |
|---|---|---|---|
| **窗口模式（推荐）** | 全屏时按 **`Ctrl+Alt+Break`** 切回窗口，或直接用 `mstsc` 窗口 | 跟窗口大小，可拖动缩放 | **主屏干活 + 副屏放虚拟机**，等于两台机器并排 |
| **多显示器全屏** | 连接前「显示」页勾 **在所有监视器上显示** | 两块屏拼接（如 5120×1600） | 虚拟机里也要双屏工作 |

窗口模式的关键好处是**两个系统各自占一屏、互不抢焦点**：主屏的浏览器/编辑器不受影响，副屏的 Windows 就是一台独立机器。

> 💡 **为什么拖过去不糊**：因为两台显示器**缩放比例都是 175%**。若两屏缩放不同（比如内屏 175%、外屏 100%），把 RDP 窗口拖过屏会触发 `WM_DPICHANGED`，客户端要按新 DPI 重新协商会话分辨率，会有一次明显的重绘/模糊。**这是本机已知的坑，跨屏软件都中招**。所以要么保持两屏缩放一致，要么连接时固定用全屏。

### 8.2 预配置连接文件（免每次手调）

`mstsc /v:<IP>` 每次都用默认设置：单显示器、不重定向驱动器、每次都弹证书警告、全屏后还得手改。存一份 `.rdp` 把设置固化下来（放本地任意目录，双击即连）：

```ini
screen mode id:i:2
use multimon:i:0
desktopwidth:i:2560
desktopheight:i:1440
desktopscalefactor:i:175
session bpp:i:32
full address:s:<Win11-IP>
username:s:<用户名>
prompt for credentials:i:0
promptcredentialonce:i:1
authentication level:i:0
negotiate security layer:i:1
enablecredsspsupport:i:1
audiomode:i:0
audioplaybackmode:i:1
redirectclipboard:i:1
redirectprinters:i:0
redirectcomports:i:1
redirectsmartcards:i:0
redirectposdevices:i:0
drivestoredirect:s:*
devicestoredirect:s:*
usbdevicestoredirect:s:
autoreconnection enabled:i:1
bandwidthautodetect:i:1
networkautodetect:i:1
connection type:i:7
disable wallpaper:i:0
allow font smoothing:i:1
allow desktop composition:i:1
disable full window drag:i:0
disable menu anims:i:0
disable themes:i:0
disable cursor setting:i:0
bitmapcachepersistenable:i:1
smart sizing:i:1
keyboardhook:i:2
```

关键字段含义：

| 字段 | 作用 |
|---|---|
| `full address` | 目标地址（**IP 变了要改这里**）|
| `username` | 预填账号，省一次输入 |
| `authentication level=0` | **不验证证书**，免掉「证书不受信任」弹窗；局域网自签名场景适用 |
| `prompt for credentials=0` | 密码在当前会话里提示一次，不再走 UAC 式弹窗 |
| `drivestoredirect=*` | 把本机所有盘挂进客户机当盘符 |
| `redirectclipboard=1` | 双向剪贴板 |
| `connection type=7` | 自动检测（局域网下等价于「局域网 10 Mbps 或更高」，全特效可开）|
| `desktopscalefactor=175` | 客户端 DPI，跟两块屏一致，避免文字过大/过小 |

🔴 **编码必须是 UTF-16LE 带 BOM**（`FF FE` 开头）——这是 `.rdp` 的标准格式。用记事本另存成 UTF-8 会让中文用户名/备注乱码。转码命令：

```powershell
$p = '.\fnOS-Win11.rdp'
$t = [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)
[IO.File]::WriteAllText($p, $t, [Text.Encoding]::Unicode)
```

### 8.3 🔴 IP 必须固定，否则 `.rdp` 会失效

客户机的 IP 是向 DHCP **动态申请**的。NAS/路由器重启后地址会漂，`.rdp` 里的 `full address` 一失效，双击就连不上（表现为「连不上或找不到计算机」）。

处理方式：**OpenWrt DHCP 静态租约**，按 MAC 绑定。

先在 NAS 上取客户机 MAC：

```sh
ip neigh show <Win11-IP>
```

然后在 OpenWrt 里建租约：`MAC → IP`。

⚠️ **改之前先看现有条目**，同一个 MAC 误加两条租约会导致分配行为异常：

```sh
uci show dhcp | grep -A5 '=host'
```

验证方式：重启虚拟机后再看一次 `ipconfig`，IP 应该还是原来的地址。

### 8.4 日常操作流

```powershell
# ① 常规：双击 .rdp 文件（推荐）

# ② 临时连（不想用配置文件）
mstsc /v:<Win11-IP>

# ③ 已知 IP 变了，先确认客户机当前地址（在 VNC 里看）
Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' } |
    Select-Object IPAddress, InterfaceAlias

# ④ 全屏 <-> 窗口 切换
#    连上后按 Ctrl+Alt+Break

# ⑤ 从宿主机确认 3389 通不通
Test-NetConnection <Win11-IP> -Port 3389
```

> `mstsc` 是 GUI 程序，命令敲完提示符**立刻**返回属于正常——窗口独立弹出，shell 不等它。

## 九、其他坑与备选方案

### 9.1 飞牛官方驱动链接已 403

官方《如何安装和使用虚拟机》仍挂着 `virtio-win-0.1.266.iso` 的下载链接，实测**三种 Referer 全部 403**（无 Referer / 帮助页正文 / 根域）⇒ **文件已下架，是文档没更新**，不是防盗链。

**可用源（Fedora 官方，实测 200）**：

| 版本 | 体积 |
|---|---|
| 最新稳定（`fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/`） | ~837 MB |
| 固定 0.1.266（`archive-virtio/virtio-win-0.1.266-1/`） | ~691 MB |

国内没有可靠镜像（清华/阿里均未同步 virtio-win）。体积大，建议宿主机下好再用远程软件的文件传输送进虚拟机，别在虚拟机里裸下。

### 9.2 只看「监视器」节点会误判

设备管理器里「监视器 → Generic Monitor」的驱动日期是 **2006/6/21**、版本跟着 Windows 版本走。这是微软给通用监视器定的**固定假日期**，每台 Windows 都一样，**与显卡无关**。判断显卡必须看「**显示适配器**」节点。

### 9.3 别把 `GameViewer Virtual Display Adapter` 当成显卡

它是 `ROOT\DISPLAY\0000` 枚举的**软件虚拟屏**（UU 超级屏功能装的），不随真实显卡变化。装了真显卡驱动后它仍然存在，属正常。若怀疑它干扰，可右键禁用试一次（不行再启用）——它也是鼠标绝对定位的嫌疑之一。

### 9.4 GPU 直通：官方自己劝退

飞牛支持硬件直通（显卡/声卡/USB/网卡）：虚拟机应用 → 侧边栏「硬件」→ **硬件直通选项** → 开启 → 编辑虚拟机 → 添加硬件 → **添加 PCI 设备**。

但官方文档原文警告：

> 「**显卡直通成功率并不高，且有可能造成宿主机崩溃，需谨慎操作**」
> 「**不建议非专业用户尝试硬件直通操作**」

前置工作还包括：BIOS 开 VT-x/AMD-V + IOMMU、GRUB 声明 IOMMU、vfio/blacklist 屏蔽宿主机驱动、按 IOMMU 分组整组直通。失败日志：`/var/apps/trim.vm/var/log/error.log`。

⇒ **为一个 NAS 上的 Win11 冒崩宿主机风险，不值得。**

### 9.5 远程方案对比与选型

| 场景 | 方案 | 理由 |
|---|---|---|
| **局域网（首选）** | **RDP**（`mstsc`） | 完全不依赖 GPU，软件渲染，延迟最低。⚠️ Win11 **家庭版**没有服务端 |
| 局域网 / 临时救急 | **fnOS 自带 VNC 控制台** | **实测比 UU 流畅得多**，只是画面质量朴素、无剪贴板 |
| 外网穿透 | **Tailscale / ZeroTier + RDP** | 走内网地址，最稳，不暴露端口 |
| 外网、不愿组网 | **RustDesk 自建中继** | 自带 VP8/H.264 软件编码，不挑显卡 |
| 外网、能接受多一跳 | **CF Tunnel + rdp2tcp** | 能穿 NAT，延迟增加 |
| ❌ 不推荐 | ~~UU 远程 / GameViewer~~ | 无硬编码 ⇒ 客户机内软编码，4 vCPU 上直接把系统压死 |

> ⚠️ **RDP 和 UU 互斥**：Win11 桌面版只允许一个交互式会话，RDP 连入会把控制台会话切走，此时 UU 那边看到的是锁屏/黑屏。两者选一个，别同时开。（所以「RDP 连着的时候 UU 显示黑屏」不是故障。）

## 十、命令速查

```powershell
# 看真实显卡型号与驱动
Get-CimInstance Win32_VideoController | Format-List Name, PNPDeviceID, DriverVersion

# 查 virtio 显卡驱动是否已在驱动库
pnputil /enum-drivers | Select-String "viogpudo" -Context 0,4

# 手动只装显卡驱动（挂载 ISO 后）
# 光驱:\viogpudo\w11\amd64\  → 右键 viogpudo.inf → 安装（无 w11 目录就用 w10\amd64）

# ── RDP 服务端状态（客户机侧，管理员）───────────────
Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server' | Select fDenyTSConnections   # 0=允许
Get-NetFirewallRule -Name 'RemoteDesktop-UserMode-In-TCP','RemoteDesktop-UserMode-In-UDP' | Select Name,Enabled
netstat -ano | Select-String ':3389'            # LISTENING 才算好；CLOSED=还在初始化
Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp' |
    Select PortNumber,fEnableWinStation,UserAuthentication,SecurityLayer
(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '127.*' }).IPAddress

# ── 宿主机侧 ────────────────────────────────────────
mstsc /v:<Win11-IP>                             # 临时连
Test-NetConnection <Win11-IP> -Port 3389        # 先验 3389 通不通
```
