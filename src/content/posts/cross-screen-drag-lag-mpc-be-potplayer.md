---
title: "两个显示器跨屏拖动卡顿：MPC-BE 卡 1 秒的根因是两屏缩放比例不一致"
description: "笔记本内屏与 1440p 外接屏拖窗口时 MPC-BE 滞后约 1 秒、PotPlayer 跟手。逐条推翻混合刷新率与 DPI 感知假设，读 MPC-BE 源码定位到 OnDpiChanged 里的深色菜单整体重建，最终用四次 A/B 实测证明：真正的触发条件是两屏缩放值不同，与刷新率、分辨率都无关。"
pubDatetime: 2026-11-05T14:00:00+08:00
draft: false
tags:
  - Windows
  - MPC-BE
  - 高DPI
  - 排错
---

> 场景：笔记本内屏 + 外接屏，分辨率、DPI、刷新率三者全不同。拖动播放器窗口从外接屏移到内屏时，MPC-BE 明显滞后约 1 秒，PotPlayer 时刻跟手。
> 全部数据为本机实测 + MPC-BE 源码核对。

## 一、结论（先给最终版）

分两层，缺一层都不完整：

1. **触发条件：两屏缩放比例不一致。** 把外接屏从 150% 改成 175%、与内屏对齐后，同样的拖动动作立刻不卡——**刷新率 240/144 依然不同、分辨率依然不同，照样顺滑**。
2. **放大因素：MPC-BE 每次跨屏的处理成本比同侪高一个量级。** 它要在 UI 线程上同步销毁并重建 7 个菜单、重建主菜单、遍历所有菜单项重设颜色。所以同样跨屏，别的程序只是轻微迟滞，它是肉眼可见的 1 秒。

两个机制互补：`WM_DPICHANGED` 只在窗口跨越**缩放不同**的显示器边界时发送；缩放一致就一条消息都不发，重建无从发生。等式是：

```text
可感知的卡顿 ≈ (跨屏触发的 DPI 变更次数) × (单次 OnDpiChanged 成本)
```

要让左边归零，把「次数」压到 0（两屏缩放一致）是根治且不牺牲观感；把「成本」压下去（关 `DarkMenu`）只减痛，还要拿深色菜单去换。

**最终建议：统一两屏缩放，`DarkMenu` 保持 `1`。** 深色菜单留着，卡顿也没了，什么都不用放弃。

## 二、实测环境

```text
\\.\DISPLAY1  内屏（主）  2560×1600 @240Hz  175%  物理 x 0–2560
\\.\DISPLAY2  外接屏       2560×1440 @144Hz  150%  物理 x 2560–5120
两屏物理紧贴、顶对齐；虚拟桌面 5120×1600
```

> 上表是**排查开始时**的状态（两屏缩放不同）。当日 13:23 已把外屏改为 175%，与内屏对齐，卡顿消失——见 §七。改后虚拟桌面不变，但外屏逻辑分辨率降为 1463×823。

**刷新率档位（实测枚举，不是猜）**

| 屏幕 | 支持档位 |
|---|---|
| 内屏 | **60、240** |
| 外接屏 | 59、60、120、144 |

内屏没有 144 也没有 120，两屏**除 60Hz 外没有任何共同档位**，所以「把两块屏刷成一样」这条路只剩双双降到 60，代价太大。

## 三、四条假设，三条被实测推翻

排查真正的难点不是找原因，而是**先把错的原因排掉**。这次四条假设里三条是错的。

### 假设 1：混合刷新率导致 MPO 失效 → **对视频播放成立，对本题不成立**

硬件叠加层（MPO）要求跨屏呈现时钟一致，240 与 144 凑不到一起时 DWM 会退回软件合成。这确实是**播放中**跨屏卡顿的原因之一。

但本次现象发生在**根本没播放、窗口里什么都没加载**的默认状态，此时压根没有 D3D 交换链，MPO 无从谈起。

**教训：先确认现象发生时程序到底在做什么，再套机制。**

### 假设 2：DPI 感知级别不同 → **推翻，两者完全相同**

用 `GetProcessDpiAwareness` 实测（注意：这个 API 的第一个参数是**进程句柄**，不是 PID，直接传 PID 会返回 `0x80070057 E_INVALIDARG`）：

| 程序 | DPI 感知 |
|---|---|
| `PotPlayerMini64.exe` | **PER_MONITOR_AWARE (2)** |
| `mpc-be64.exe` | **PER_MONITOR_AWARE (2)** |

两者 manifest 也都声明了 `PerMonitorV2`（PotPlayer 的 exe 里没有明文 manifest，但运行时值相同，说明它是在代码里调 API 设的）。

### 假设 3：MPC-BE 开了「窗口吸附到桌面边缘」 → **推翻**

`SnapToDesktopEdges=0`，本来就是关的。

### 假设 4：MPC-BE 空闲时仍在渲染 → **推翻**

| 程序 | 空闲时加载的图形模块 | 模块数 | 工作集 |
|---|---|---|---|
| MPC-BE | 仅 `dwmapi.dll` | 72 | 35.1 MB |
| PotPlayer | 仅 `dwmapi.dll` | 115 | 119.8 MB |

两者都没加载 `d3d9` / `d3d11` / `dxgi`，说明窗口里是纯 GDI 绘制，没有渲染循环。

## 四、放大因素：`OnDpiChanged` 里的深色菜单重建

`src/apps/mplayerc/MainFrm.cpp` 第 2195 行起：

```cpp
LRESULT CMainFrame::OnDpiChanged(WPARAM wParam, LPARAM lParam)
{
    const int dpix = LOWORD(wParam);
    const int dpiy = HIWORD(wParam);
    OverrideDPI(dpix, dpiy);
    ...
    m_wndToolBar.ScaleToolbar();      // 重建工具栏按钮图像
    m_wndInfoBar.ScaleFont();         // 下面 6 个都是重建字体
    m_wndStatsBar.ScaleFont();
    m_wndSeekBar.ScaleFont();
    m_wndPlaylistBar.ScaleFont();
    m_wndStatusBar.ScaleFont();
    m_wndPreView.ScaleFont();
    m_wndFlyBar.Scale();

    CMenuEx::ScaleFont();
    const auto& s = AfxGetAppSettings();
    if (s.bUseDarkTheme && s.bDarkMenu) {          // ← 关键分支
        m_popupMenu.DestroyMenu();                  // 销毁 7 个菜单
        m_popupMainMenu.DestroyMenu();
        m_VideoFrameMenu.DestroyMenu();
        m_PanScanMenu.DestroyMenu();
        m_ShadersMenu.DestroyMenu();
        m_AfterPlaybackMenu.DestroyMenu();
        m_NavigateMenu.DestroyMenu();

        m_popupMenu.LoadMenuW(IDR_POPUP);           // 从资源重新加载 7 个菜单
        m_popupMainMenu.LoadMenuW(IDR_POPUPMAIN);
        ...
        CMenu defaultMenu;
        defaultMenu.LoadMenuW(IDR_MAINFRAME);       // 连主菜单也重建一遍
        CMenu* oldMenu = GetMenu();
        if (oldMenu) {
            SetMenu(&defaultMenu);
            oldMenu->DestroyMenu();
        }
        m_hMenuDefault = defaultMenu.Detach();
        SetColorMenu();                             // 遍历每个菜单项重设颜色
    }

    if (!m_bFullScreenChangingMode) {
        MoveWindow(reinterpret_cast<RECT*>(lParam));
    }
    RecalcLayout();
    return 0;
}
```

开启深色主题时，配置正好命中这段：

```ini
[Theme]
UseDarkTheme=1
DarkMenu=1
DarkTitle=1
```

`SetColorMenu()` 会把主菜单和所有弹出菜单的**每一个菜单项**逐个设成自绘（owner-draw）并算颜色。菜单越多、子项越深，耗时越久。

所以一次跨屏 = 7 次 `DestroyMenu` + 8 次 `LoadMenuW` + 全菜单项重着色 + 工具栏图像重建 + 7 处字体重建，全部在 UI 线程同步跑完。**拖动时窗口在 DPI 边界附近来回，一次拖动还可能触发好几次**，累加成肉眼可见的 1 秒滞后。

PotPlayer 的窗口框架是自绘的，没有「资源菜单」这一层，DPI 变化时只需重排位图，成本低一个量级，所以看起来时刻跟手。

> 注意这只是**放大因素**，不是触发条件。它只在 `WM_DPICHANGED` 真的发出来时才付出成本——两屏缩放一致时这条消息一条都不发，`OnDpiChanged` 压根执行不到。

## 五、想继续用 MPC-BE 的话

按代价从小到大：

**方案 A：只关深色菜单（仅在无法统一缩放时才需要）**

```ini
[Theme]
DarkMenu=0
```

跳过整个菜单重建分支，跨屏立刻变轻。代价是菜单变浅色，与深色标题栏/深色对话框不一致——而 `DarkDialogs=0` 本来就是关的，视觉上其实还能接受。

> 本方案只降低单次跨屏的**成本**，不减少**次数**。两屏 DPI 不同时，消息照样反复发，只是每次便宜一些。要彻底消除，得走 §七 的「两屏缩放一致」。经实测，后者才是决定性的一步。

**方案 B：整体关深色主题**

```ini
UseDarkTheme=0
```

界面回归浅色，一致性好但观感变了。

**方案 C：保持现状，接受这 1 秒**

如果只是偶尔拖一下，不影响使用。视频全屏播放时根本不跨屏。

> 改 ini 前提：**MPC-BE 必须已退出**。它在关闭时会把内存配置覆写回 ini，运行中改的会被覆盖。
> 该 ini 是 **UTF-8 with BOM + CRLF**，改值必须按字节替换，别用会重写编码的编辑器。

## 六、方法论备忘（本次踩到的三个坑）

**坑 1：查屏幕拓扑必须先设 DPI 感知**

未设 DPI 感知的进程枚举显示器，拿到的是 DPI 虚拟化后的坐标，会**凭空出现空洞**。本次第一轮就报了「两屏之间隔 244 像素」，实际物理上完全紧贴。

```python
user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))  # PER_MONITOR_AWARE_V2
```

**坑 2：`GetProcessDpiAwareness` 要的是句柄**

```python
h = kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
shcore.GetProcessDpiAwareness(h, byref(v))      # 传 PID 会返回 E_INVALIDARG
```

**坑 3：别靠猜，去看源码**

「MPC-BE 优化差」「DPI 感知不同」这类说法都只是想当然。开源项目直接读 `OnDpiChanged` 的二十行代码，比任何推测都准。

**判据法：先确认「现象发生时程序在做什么」**

本次最容易走偏的地方，是把「播放中的渲染问题」当成「拖窗口的问题」。两者现象相似、机制完全不同，用错了会一直调渲染器而毫无效果。

## 七、验证：同日 A/B 实测定论

13:23 复测：**把外接屏从 150% 改成 175%，与内屏对齐后，同样的拖动动作立刻不卡了。**

运行时实测（`GetDpiForMonitor`，进程先设 `PER_MONITOR_AWARE_V2`）：

| 屏幕 | 物理 | 刷新率 | DPI | 缩放 | 逻辑分辨率 |
|---|---|---|---|---|---|
| `\\.\DISPLAY1` 内屏 | 2560×1600 | 240Hz | 168 | 175% | 1463×914 |
| `\\.\DISPLAY2` 外接 | 2560×1440 | 144Hz | 168 | 175% | 1463×823 |

这一组数据一次性证伪了两件事：

| 假设 | 数据 | 判定 |
|---|---|---|
| 混合刷新率（240 vs 144）导致 | 依然 240/144 不一致，却顺滑 | **否** |
| 分辨率不同（1600 vs 1440）导致 | 依然不同，却顺滑 | **否** |
| 两屏 DPI 不一致导致 | 150/175 卡 → 175/175 不卡 | **是** |

13:26 再把 `DarkMenu` 改回 `1`（其余一律不动，两屏保持 175%/175%），再拖一次：

> **完全不卡，菜单也是深色。**

四次组合摆在一起，结论没有歧义：

| 两屏缩放 | `DarkMenu` | 结果 |
|---|---|---|
| 175% / 150% | 1（原厂默认） | **卡约 1 秒** |
| 175% / 175% | 0 | 顺滑 |
| **175% / 175%** | **1** | **顺滑** |
| 175% / 150% | 0 | 未单独测（已无必要） |

**`DarkMenu` 对卡顿没有独立贡献。** 它只在 `WM_DPICHANGED` 真的发出来时才付出成本。

### 代价与替代方案

外接屏 2560×1440 在 175% 下只剩 **1463×823** 逻辑像素，能并排放的窗口明显变少（150% 时是 1707×960）。想给外屏更多空间又不重新触发卡顿：

**两边同时降到 150%**——内屏 1707×1067、外屏 1707×960。

关键是两边**相等**，而不是必须等于某个特定值。任何两边一致的百分比都成立。

⚠️ 这条设置会被**显卡驱动更新、换线、拔插显示器**重置。哪天感觉「又卡了」，第一件事就是回来看两屏缩放是不是又被拆成了不同值——别再去翻播放器设置和渲染器。

## 八、最终选择

实测对比后日常用 **PotPlayer**（`PotPlayerMini64.exe`）：

- 跨屏拖动跟手
- 画质差异肉眼分辨不出（都是硬件解码 + 基本色彩管理）
- 既然看不出差别，就选天天能感觉到的那个维度

> 两屏缩放统一为 175% 后，MPC-BE 跨屏**同样不卡**，`DarkMenu` 也保持深色。所以这个选择不再是「卡与不卡」的取舍，纯粹是顺手程度——两个现在都能用，选那个习惯的就行。

MPC-BE 的 `VideoRenderer` 已恢复出厂默认 `VideoRenderer=3`（EVR CP），原 ini 另存备份保留。
