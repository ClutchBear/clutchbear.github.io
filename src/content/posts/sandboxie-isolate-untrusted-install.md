---
title: "Sandboxie 隔离安装不受信任程序-通用流程"
description: "用 Sandboxie-Classic 在沙盒里试运行来路不放心的 Windows 程序：建盒、在盒里装、桌面快捷方式包一层 Start.exe /box，卸载不干净或全家桶也污染不了真机。"
pubDatetime: 2026-10-09T14:00:00+08:00
draft: false
tags:
  - Windows
  - Sandboxie
  - 沙盒
  - 安全
  - 配置清单
---


> 适用场景：想试用一个「来路不太放心 / 卸载不干净 / 爱装全家桶」的 Windows 程序（网盘客户端、破解工具、国产软件等），又不想污染真机。
> 本流程在本机用夸克网盘实测跑通：装在沙盒里、桌面双击直达、下载文件能取回、删盒即归零。

## 结论

- **用 Sandboxie-Classic（免费无证书机制），不用 Plus**：Plus 无证书只有 10 天全功能试用，到期后高级沙盒类型（隐私模式等）被锁；Classic 核心隔离引擎与 Plus 同一套代码，全功能永久免费，只是界面老式。
- **通用动作只有三个**：建盒 → 在盒里装程序 → 桌面快捷方式包一层 `Start.exe /box:盒子名`。
- 彻底清理 = 右键盒子 → 删除内容，真机无痕。
- Windows Sandbox 走不通：家庭版不支持（需 Pro 的 Hyper-V），不用折腾。

## 一、为什么 Sandboxie 能隔离

程序在沙盒里运行时，它对**文件系统、注册表、系统服务**的所有写入都被重定向到沙盒目录（`C:\Sandbox\<用户名>\<盒名>\`），真机看不到这些改动：

- 它想写的注册表（自启动、文件关联、HKCU 污染）→ 落在盒子里
- 它想装的系统服务（如夸克的 `QuarkDriveService`）→ 装不进真机
- 它想改的文件关联、右键菜单 → 只在盒子内生效

删盒 = 这些改动全部消失。

## 二、通用流程（5 步）

### 第 1 步：装 Sandboxie-Classic

- 下载：`https://github.com/sandboxie-plus/Sandboxie/releases/latest` → Assets 里选 **`Sandboxie-Classic-x64-v5.x.x.exe`**（不要选 Plus / ARM64）
- ⚠️ 本机 Classic 装在 `C:\Program Files\Sandboxie\`（**不是** `Sandboxie-Plus\`，后面快捷方式路径要用对）
- 装完重启一次（要装内核驱动）
- ⚠️ 改沙盒配置前确认托盘里 Sandboxie Control 在运行

### 第 2 步：新建盒子

Sandboxie Control → 沙盒(S) → 创建新盒子 → 命名（英文小写，如 `quark`、`testapp`）。

> Plus 版才有「隐私模式」选项；Classic 标准盒对隔离软件写入已足够。如果担心程序**读取**真机个人文件，这是 Classic 的短板，敏感场景换 Plus 付费或虚拟机。

### 第 3 步：在盒里安装程序

右键盒子 → **在此沙盒中运行 → 运行任意程序** → 选安装包。安装程序的写入被重定向，装完后程序只存在于 `C:\Sandbox\<用户名>\<盒名>\drive\C\` 里。

### 第 4 步：桌面快捷方式（★ 关键一步）

先找到沙盒内主程序的真实路径：右键盒子 → **浏览保存内容** → 进 `drive\C\` 找到安装目录，记下主程序 exe 完整路径。

桌面右键 → 新建 → 快捷方式，**目标**按这个模板填：

```text
"C:\Program Files\Sandboxie\Start.exe" /box:盒子名 "C:\Sandbox\用户名\盒名\drive\C\程序路径\主程序.exe"
```

**起始位置**填：

```text
"C:\Program Files\Sandboxie"
```

改图标：快捷方式属性 → 更改图标 → 浏览 → 选沙盒内的主程序 exe，外观和原生一致。

**本机实测实例（夸克）**：

```text
"C:\Program Files\Sandboxie\Start.exe" /box:quark "C:\Sandbox\xin\quark\drive\C\Program Files\Quark\quark.exe"
```

⚠️ **最大坑**：快捷方式**不能直接指向** `C:\Sandbox\...` 里的 exe——那是让 Windows 裸启动沙盒目录里的文件，Sandboxie 只会事后弹确认框、甚至直接在沙盒外跑起来（写入真机）。**必须包一层 `Start.exe /box:盒名`**，进程一出生就被接管，无弹窗。

### 第 5 步：日常使用 / 取文件 / 彻底清理

| 动作 | 操作 |
|---|---|
| 日常启动 | 双击桌面快捷方式，不用开 Sandboxie Control |
| 取回下载的文件 | 右键盒子 → **快速恢复**；或「浏览保存内容」里右键文件 → 恢复到任意文件夹 |
| 看程序改了什么 | 右键盒子 → 浏览保存内容，所有落盘改动都在这里 |
| 彻底清理 / 重装 | 右键盒子 → **删除内容** → 全部归零；重装时快捷方式不用动（装回同一路径即可） |

## 三、两个可选提速项

1. **右键菜单**：Sandboxie Control → 配置(C) → 系统设置 → 勾选「在上下文菜单中添加"在沙盒中运行"」→ 以后任何 exe 右键即可入盒。
2. **强制文件夹**：右键盒子 → 沙盒设置 → 程序 → 强制文件夹，把沙盒内程序安装目录加进去 → 任何从该目录启动的程序强制入盒，双击开始菜单快捷方式也自动进沙盒。双刃剑：之后想不经沙盒运行反而要绕开，日常单一用法无所谓。

## 四、验证是否真的在沙盒里

打开 Sandboxie Control，沙盒名下出现该程序的全部进程（带沙盒图标）即成功。个别进程名是 `SandboxieDCo.../SandboxieRpcSs...` 之类的服务存根，属正常现象——那是 Sandboxie 替沙盒进程补的服务，正说明程序想装的真机服务被截留了。

## 五、坑清单（实测汇总）

| 坑 | 说明 |
|---|---|
| 快捷方式直指沙盒内 exe | 会在沙盒外裸跑或弹拦截框，必须包 `Start.exe /box:盒名` |
| Start.exe 路径 | Classic 在 `C:\Program Files\Sandboxie\`，与 Plus 的 `Sandboxie-Plus\` 不同 |
| Plus 证书 10 天 | 不是全部功能到期，标准沙盒仍永久免费；但 Classic 更省心，全功能无限制 |
| 家庭版无 Windows Sandbox | 需 Pro/Hyper-V，社区强开脚本不稳定，不折腾 |
| 沙盒内登录态 | 删除内容后盒内程序账号要重新登 |
| 取文件忘了恢复 | 下载的文件落在盒子里，真机找不到——记得快速恢复 |
| 重装程序 | 先删内容再重装；快捷方式指向的路径不变就不用改 |

## 六、一分钟核对清单

1. 装的是 **Classic** 版（无证书焦虑）
2. 盒名是英文小写
3. 安装程序是**从盒子的右键菜单**启动的
4. 快捷方式目标 = `"C:\Program Files\Sandboxie\Start.exe" /box:盒名 "沙盒内exe路径"`，起始位置 = `"C:\Program Files\Sandboxie"`
5. Sandboxie Control 里能看到进程挂在盒名下
6. 下载的文件用「快速恢复」取回真机

---
*实测环境：Win11 家庭中文版 25H2 + Sandboxie-Classic v5.73.5，以夸克网盘客户端为样本（2026-10-09）。*
