---
title: "WSL2 + Podman + Dev Containers：不用 Docker Desktop 的容器化开发环境配置清单"
description: "在 Windows 11 + WSL2 里跑 rootless Podman，宿主侧用 VS Code + Dev Containers 连过去，全程不装 Docker Desktop。含 systemd 启用、rootless socket、UID 映射对齐、国内镜像加速，以及最坑的那个「Dev Containers require Docker to run」弹框的三层根因和实测修法。"
pubDatetime: 2026-10-07T15:00:00+08:00
draft: false
tags: ["WSL2", "Podman", "Dev Containers", "容器", "开发环境"]
---

> **摘要**：想在 Windows 上搞容器化开发，又不想装 Docker Desktop（授权、内存占用、都要收费/重启）？这套方案是：**WSL2 里跑 rootless Podman，Windows 侧 VS Code 用 Dev Containers 扩展连过去**。本文按实际配置顺序写成清单，每一步都给了可复制的命令和"期望输出"，最后附一张常见故障排查表和一份 13 项收官验证清单。

> **事实依据**：微软官方文档确认 **Podman 5+ 只需把 `dev.containers.dockerPath` 设为 `podman`**（Dev Containers 只跟命令行交互、不直接碰引擎）；Podman man page 确认 rootless socket 路径与 `podman.socket` 用法；WSL2 专属的「根分区非 shared mount」坑与 rootless 自检脚本来自 DDEV 文档；UID 映射修法经 Podman 官方 troubleshooting 与多方实测交叉验证。文中「实测」字样均为本机（Debian 13 + WSL 3.0.2）跑通的结果。

---

## 0. 前置确认（2 分钟）

| # | 命令 | 期望 |
|---|---|---|
| 0.1 | `wsl --version`（Windows 侧） | WSL ≥ 0.67.6（支持 systemd）；本机 3.0.2 ✓ |
| 0.2 | `lsb_release -a`（WSL 内） | Ubuntu 24.04+ / Debian 13 → 自带 Podman 5.x；**Ubuntu 22.04 只有 3.4，先升级系统或换源** |
| 0.3 | `id -u` | 非 0 的普通用户（理想 1000，后面 UID 对齐全靠它） |

**核心布局先说清**：项目代码放 **WSL 内部的 ext4**（如 `~/projects/demo`），**绝不放 `/mnt/c`、`/mnt/d`** —— 根因有二：跨系统文件读写慢 1–2 个数量级；rootless Podman 对 drvfs/9p 路径做 overlay/bind 挂载会直接报错。

---

## 1. WSL2 发行版初始化 + systemd

### 1.1 启用 systemd

编辑 `/etc/wsl.conf`（没有就创建，有就合并 —— 别出现两个同名段）：

```ini
[boot]
systemd=true
# WSL2 专属坑：根分区在 systemd 接管前挂载、未标记 shared，
# rootless 容器会警告 "/ is not a shared mount"，这行永久修复
command = mount --make-rshared /

[user]
default=xin
```

### 1.2 重启生效（Windows PowerShell）

```powershell
wsl --shutdown
Start-Sleep -Seconds 8
wsl
```

### 1.3 验证

```bash
ps -p 1 -o comm=        # 必须输出 systemd
systemctl --user is-active podman.socket 2>/dev/null || echo "socket 未启用（第 2 步处理）"
```

---

## 2. Podman 安装与 rootless socket

### 2.1 安装（WSL 内）

```bash
sudo apt update && sudo apt install -y podman podman-compose
podman --version        # 期望 5.x
```

> 装完若末尾报 `Job for systemd-binfmt.service failed ...` —— WSL2 已知现象，不影响 Podman 使用，处理见 §5.1。

### 2.2 确认 subuid/subgid 已分配

rootless 运行的前提，发行版建用户时一般自动配好：

```bash
grep $(whoami) /etc/subuid /etc/subgid
# 若为空：sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

### 2.3 启用 rootless API socket

systemd 用户级，按需拉起、常驻监听：

```bash
systemctl --user enable --now podman.socket
systemctl --user is-active podman.socket          # active
ls $XDG_RUNTIME_DIR/podman/podman.sock            # /run/user/1000/podman/podman.sock
```

### 2.4 防休眠掉线（可选但推荐）

```bash
sudo loginctl enable-linger $USER
```

不加的话，最后一个 WSL 终端关闭后用户级 systemd 服务可能停掉，VS Code 连一半报 socket 不存在。

**linger 生效验证**（`wsl --shutdown` 冷启动、重新打开发行版后跑，三项全过才算 linger 落地）：

```bash
ls -l /run/user/$(id -u)/bus                  # srw-rw-rw-，/run/user/1000/bus 存在
systemctl --user is-active podman.socket      # active
ls -l /run/user/$(id -u)/podman/podman.sock   # srw-rw----，podman.sock 存在
```

> 两个实测坑：
> ① 刚打完 `enable-linger` 就 `ls .../bus` 可能扑空 —— user instance（含 D-Bus）是**异步拉起**的，等几秒或重开终端再看；`systemctl --user` 能静默成功本身就是 user instance 已起来的证据。
> ② 判断 linger **真正持久化**的铁证 = `wsl --shutdown` 冷启动后 bus **直接就在**（没先手动跑任何 systemctl/loginctl）。此后不用再管：每次启动发行版，bus 与 podman.sock 自动就位。

### 2.5 `DOCKER_HOST` 写进 shell 配置

按默认 shell 二选一。**本机 Debian 默认 shell 是 zsh（装了 oh-my-zsh）→ 写 `.zshenv`**：zsh 的环境变量放 `.zshenv` 所有会话都读；`.bashrc` 对 zsh 不生效，写了也白写。

```bash
# zsh（本机现状）：
echo 'export DOCKER_HOST="unix:///run/user/$UID/podman/podman.sock"' >> ~/.zshenv
source ~/.zshenv && echo $DOCKER_HOST
# 期望输出：unix:///run/user/1000/podman/podman.sock

# bash（默认 shell 是 bash 才用这条）：
# echo 'export DOCKER_HOST="unix:///run/user/$UID/podman/podman.sock"' >> ~/.bashrc
# source ~/.bashrc
```

### 2.6 ★ 装 `podman-docker` 兼容层（必做）

**2026-10-07 实测升级为必做步骤** —— Dev Containers 扩展硬依赖 `docker` 命令，跳过它 Reopen 必弹框：

```bash
sudo apt install -y podman-docker
docker --version    # 应输出 podman version 5.x（垫片转发成功）
```

**为什么必做**（实测复盘）：`dockerPath=podman` 设置对 Dev Containers 扩展（0.469.0）的**内部 server 初始化不生效** —— 它硬调用字面意义的 `docker` 命令，日志报 `Error: spawn docker ENOENT`，随后弹 "Dev Containers require Docker to run"（完整排障过程见 §4.0 拦路虎三）。装上垫片后 `/usr/bin/docker` 存在并转发给 podman，这条链路即通。

路线取舍（结论已反转）：

| 路线 | 原理 | 实测结论 |
|---|---|---|
| `podman-docker` 垫片（**必装**） | `/usr/bin/docker` 转发给 podman CLI | **Reopen 成功的实锤修法**；"只会喊 docker"的工具零改动可用 |
| 只设 `dev.containers.dockerPath=podman` | Dev Containers 直接调 podman CLI | **不完整**：扩展内部链路仍硬找 `docker`，单靠它 Reopen 弹框；但 §3.2 的设置仍要写（构建等链路会读它），与垫片叠加双保险 |

垫片代价：**`docker compose`（v2 插件风格）不工作**、buildx 没有 —— 对纯 Dockerfile 工作流无影响（Compose 走 `podman-compose`，见 §3.2）；卸载干净：`sudo apt remove podman-docker`。

### 2.7 容器 CLI 与 socket 路径对应表

查阅用，无必做操作；末尾的 `docker context` 命令仅"WSL 里装了真 Docker CLI 且想让它连 Podman"时才需要。

| 模式 | CLI | socket 路径 | 启用命令 | DOCKER_HOST |
|---|---|---|---|---|
| rootless（本方案） | `podman`（登录用户） | `/run/user/<uid>/podman/podman.sock`（`$XDG_RUNTIME_DIR/podman/podman.sock`） | `systemctl --user enable --now podman.socket` | `unix:///run/user/$UID/podman/podman.sock` |
| rootful | `sudo podman` | `/run/podman/podman.sock` | `sudo systemctl enable --now podman.socket` | `unix:///run/podman/podman.sock` |
| docker 垫片 | `/usr/bin/docker`（→podman） | 跟随 `dockerPath`/`DOCKER_HOST` | 同上二选一 | 同上 |

让真 Docker CLI 连 Podman 的备选：`docker context create podman-rootless --docker host="unix://$XDG_RUNTIME_DIR/podman/podman.sock" && docker context use podman-rootless`。

### 2.8 验证引擎可跑

```bash
podman run --rm docker.io/library/alpine echo ok
podman info --format '{{.Store.GraphDriverName}} {{index .Store.GraphStatus "Native Overlay Diff"}}'
# 期望：overlay true（原生 rootless overlay，最快路径；false 则删掉 storage.conf 里的 mount_program）
```

### 2.9 国内加速

拉镜像 500 / 超时 / 挂起时做；**2026-10-07 实测 daocloud 拉取成功**。

写 `/etc/containers/registries.conf.d/000-mirrors.conf`（用 `sudo tee` 而非重定向，保证 root 属主）：

```bash
sudo tee /etc/containers/registries.conf.d/000-mirrors.conf > /dev/null <<'EOF'
unqualified-search-registries = ["docker.io"]

[[registry]]
prefix = "docker.io"
location = "docker.io"

[[registry.mirror]]
location = "docker.m.daocloud.io"
EOF
```

配置含义：

| 段 | 作用 |
|---|---|
| `unqualified-search-registries` | `podman run alpine` 这种短名去哪找（补全成 `docker.io/library/alpine`） |
| `[[registry]] prefix/location = "docker.io"` | 显式声明 docker.io 本体仍可用 —— 镜像站全挂时回源直连 |
| `[[registry.mirror]] daocloud` | 拉取先走 daocloud 镜像，失败自动回退 docker.io 本体；prefix 匹配所以显式写 `docker.io/library/...` 也命中 |

验证（2026-10-07 实测输出）：

```bash
podman run --rm docker.io/library/alpine echo ok
# Trying to pull docker.io/library/alpine:latest...
# Getting image source signatures
# Copying blob e2de96513ba9 done
# Copying config 320994c3b9 done
# Writing manifest to image destination
# ok
```

> 备选与避坑：`1ms.run` 也可用（测活返回 401 = 服务活着，registry `/v2/` 未带 token 回 401 是规范行为不是故障）；`dockerproxy.net` 已死（000 连不上）。`quay.io` 国内基本没有可用公共加速，演示镜像一律用 `docker.io/library/...`。

---

## 3. VS Code 与 Dev Containers 设置

### 3.1 Windows 侧装扩展

VS Code + 扩展 **WSL**（ms-vscode-remote.remote-wsl）+ **Dev Containers**（ms-vscode-remote.remote-containers）。

> **2026-10-07 勘误（重要）**：新版 Dev Containers（0.469.0 + VS Code 1.140 实测）是 **UI 侧扩展** —— 本体永远只显示在 `Local - Installed` 分组，**不会出现在 `WSL: Debian - Installed`**。它在 WSL 里只放 server 组件（`~/.vscode-remote-containers/dist/vscode-remote-containers-server-0.469.0.js`，Dev Containers 输出日志里 `test -f` 这行即证据）。**WSL 分组里没有它 = 正常现象，不是故障**（WSL 分组里出现的 Python/Pylance/Container Tools 等是语言/工具类扩展，两码事）。
> 判断扩展就位：① `Ctrl+Shift+P` 能搜到 `Dev Containers:` 命令；② 扩展面板 Local 分组里 Dev Containers 旁边有激活耗时标记（如 `118ms`）。
> Reopen 弹 "require Docker" 的真根因自始至终是 **WSL 里没有字面意义的 `docker` 命令**（server 组件硬调用 `docker`，`dockerPath` 拦不住），修法见 §4.0 拦路虎三。

### 3.2 ★ 设置要写在 WSL 远程那一侧

设置面板切到「远程 [WSL: Debian]」标签页，或直接编辑 `~/.vscode-server/data/Machine/settings.json`；`~/.vscode-server` 还不存在就先 `mkdir -p` 建好再写文件，VS Code 首连不会覆盖它：

```json
{
  "dev.containers.dockerPath": "podman",
  "dev.containers.dockerComposePath": "podman-compose"
}
```

> 只用 Dockerfile、不用 Compose 的话，第二行可省。两处都设（用户级 + WSL 远程级）最稳。
>
> **2026-10-07 实战例外**：即使 `dockerPath=podman` 设置全对，Dev Containers 扩展（0.469.0）初始化 host server 时仍会**硬调用 `docker` 命令**（日志 `Error: spawn docker ENOENT`，`dockerPath` 拦不住这条链路）→ 弹 "require Docker"。此时 `podman-docker` 垫片是**实际必需**（见 §4.0 拦路虎三）：只用 Dockerfile 不用 Compose 的场景无副作用，卸载干净（`sudo apt remove podman-docker`）。

### 3.3 需要裸 Docker API 的场景

少数工具走 socket 而非命令行：把 socket 路径填进 `dev.containers.dockerSocketPath`（或在项目 devcontainer.json 里用 `remoteEnv.DOCKER_HOST`），路径即 `/run/user/1000/podman/podman.sock` —— **别去造 `/var/run/docker.sock` 全局软链**。

---

## 4. 最小可用配置示例（项目根建 `.devcontainer/`）

### 4.0 从零创建步骤（全新发行版适用，一条条复制即可）

> 本机 Debian 13 是全新环境：没有 git、没有 `~/projects`、没有任何项目文件。按 ①→⑤ 走完，得到的就是 §4.1/§4.2 的最小示例（内容一致，此处带写入命令，直接整块复制）。

**① 前置安装**（全新 Debian 没有 git，VS Code 远程侧 git 状态与 §6 第 9 条验证都靠它）：

```bash
sudo apt update && sudo apt install -y git
```

**② 建项目骨架**：

```bash
mkdir -p ~/projects/demo && cd ~/projects/demo
git init                    # 项目纳入 git；报 git: command not found 就回到 ①
mkdir -p .devcontainer
```

**③ 写 `.devcontainer/Dockerfile`**（heredoc 必须用带引号的 `<<'EOF'`，否则 `$USER_GID`、`$USERNAME` 会被 shell 当变量展开成空串，写坏文件）：

```bash
cat > .devcontainer/Dockerfile <<'EOF'
FROM docker.io/library/python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates sudo \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid $USER_GID $USERNAME \
 && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
 && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
EOF
```

**④ 写 `.devcontainer/devcontainer.json`**（同样 `<<'EOF'` 防 `${localWorkspaceFolder}` 被 shell 展开）：

```bash
cat > .devcontainer/devcontainer.json <<'EOF'
{
  "name": "py-dev",
  "build": { "dockerfile": "Dockerfile", "context": ".." },

  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind",
  "workspaceFolder": "/workspace",

  "containerUser": "dev",
  "remoteUser": "dev",
  "updateRemoteUserUID": true,
  "runArgs": ["--userns=keep-id:uid=1000,gid=1000"],

  "forwardPorts": [8000],
  "portsAttributes": { "8000": { "label": "dev server", "onAutoForward": "notify" } },

  "postCreateCommand": "pip install -r requirements.txt 2>/dev/null || true",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "ms-python.debugpy"],
      "settings": { "python.defaultInterpreterPath": "/usr/local/bin/python3" }
    }
  }
}
EOF
```

**⑤ 核对 + 用 Remote-WSL 打开**：

```bash
ls -l .devcontainer/
# -rw-r--r-- 1 xin xin ... Dockerfile
# -rw-r--r-- 1 xin xin ... devcontainer.json
code .
```

- VS Code 打开后右下角状态栏出现 **`WSL: Debian`** 才算连对了。
- 命令面板（`Ctrl+Shift+P`）→ **`Dev Containers: Reopen in Container`** → 等首次构建（拉 `python:3.12-slim` 走 §2.9 加速，几分钟），左下角变 **`Dev Container: py-dev`** 即成功。

> 三个常见拦路虎：
>
> - **`code` 命令不存在** = Windows 侧 VS Code 或 WSL 扩展没装好（回 §3.1）；首次 `code .` 会自动往发行版装 vscode-server，属正常流程。
> - **构建时拉不动镜像** = §2.9 加速配置没写或没生效，`podman run --rm docker.io/library/alpine echo ok` 先验通再回来。
> - **Reopen in Container 弹 "Dev Containers require Docker to run. Do you want to install Docker in WSL?"**（2026-10-07 实战全链路；弹窗一律点 **Cancel**，别点 Install —— Install 会往 WSL 装 Docker CE，与 Podman 方案冲突）。按序排查三层，每改完一步都要 `Ctrl+Shift+P` → `Developer: Reload Window` 再 Reopen：
>
>   **① 确认扩展在窗口里激活**：`Ctrl+Shift+P` 搜得到 `Dev Containers:` 命令 + Local 分组里 Dev Containers 有激活耗时标记 = 已就位。**Dev Containers（0.469+）是 UI 侧扩展，永远不出现在 `WSL: Debian - Installed` 分组，这是正常架构**（WSL 里只有 server 组件 `~/.vscode-remote-containers/`）。曾试过"离线复制扩展目录到 `~/.vscode-server/extensions/`" —— 对 0.469 新架构**无效且不必要**，真正修好弹框的是 ②③。
>
>   **② 设置写进 WSL Machine 侧**（新旧设置名都写 + 绝对路径最稳）：
>
>   ```bash
>   mkdir -p ~/.vscode-server/data/Machine
>   cat > ~/.vscode-server/data/Machine/settings.json <<'EOF'
>   {
>     "dev.containers.dockerPath": "/usr/bin/podman",
>     "remote.containers.dockerPath": "/usr/bin/podman",
>     "dev.containers.dockerComposePath": "podman-compose"
>   }
>   EOF
>   ```
>
>   **③ 日志见 `spawn docker ENOENT` 仍弹框** = 扩展内部 server 初始化硬找 `docker` 命令，`dockerPath` 拦不住这条链路 → 装 podman-docker 垫片（**实测此步后 Reopen 成功开始拉镜像**）：
>
>   ```bash
>   sudo apt install -y podman-docker
>   docker --version    # 应输出 podman version 5.x（垫片转发成功）
>   ```
>
>   取证工具：`Ctrl+Shift+U` 输出面板 → 下拉选 **Dev Containers**，里面能看到扩展实际调用的命令与失败原因。

### 4.1 `.devcontainer/Dockerfile`（带注释版）

```dockerfile
FROM docker.io/library/python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      git curl ca-certificates sudo \
    && rm -rf /var/lib/apt/lists/*

# ★ 关键：容器内建 uid=1000 的用户，与 WSL 登录用户对齐 —— 这是 rootless 权限不翻车的根
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid $USER_GID $USERNAME \
 && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
 && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
 && chmod 0440 /etc/sudoers.d/$USERNAME
USER $USERNAME
```

### 4.2 `.devcontainer/devcontainer.json`（带注释版）

```jsonc
{
  "name": "py-dev",
  "build": { "dockerfile": "Dockerfile", "context": ".." },

  // 工作区挂载：把 VS Code 打开的文件夹绑到 /workspace
  "workspaceMount": "source=${localWorkspaceFolder},target=/workspace,type=bind",
  "workspaceFolder": "/workspace",

  // ★ rootless UID 对齐三件套：keep-id 让容器内 uid 保持 1000（=宿主 uid），
  //   bind mount 里的文件在两侧属主一致，不出现 100999
  "containerUser": "dev",
  "remoteUser": "dev",
  "updateRemoteUserUID": true,
  "runArgs": ["--userns=keep-id:uid=1000,gid=1000"],

  // 端口转发：容器内监听的端口自动在 Windows 的 localhost 上可访问
  "forwardPorts": [8000],
  "portsAttributes": { "8000": { "label": "dev server", "onAutoForward": "notify" } },

  "postCreateCommand": "pip install -r requirements.txt 2>/dev/null || true",
  "customizations": {
    "vscode": {
      "extensions": ["ms-python.python", "ms-python.debugpy"],
      "settings": { "python.defaultInterpreterPath": "/usr/local/bin/python3" }
    }
  }
}
```

### 4.3 Compose 变体要点

多容器才需要：`apt install podman-compose` 后，devcontainer.json 改用 `"dockerComposeFile": "docker-compose.yml"`；已知限制 —— `podman compose` 依赖外部 provider，个别 Compose 特性（如 `depends_on` 条件、部分 `build` 参数）与 docker compose v2 有差异，遇到再说，别一开始就上 Compose。

---

## 5. 常见问题与排查

| 症状 | 根因 | 修法 |
|---|---|---|
| 宿主 `ls -l` 见文件属主 **100999**（或 10xxxx 数字），VS Code 改不动、git 报 unsafe repository | rootless 默认把容器 root 映射到 subuid 区（100000 起），容器内非 0 uid 落到 100999 | devcontainer.json 加 `runArgs --userns=keep-id:uid=1000,gid=1000` + `containerUser`/`remoteUser` 指向 uid=1000 用户（即 §4 三件套） |
| 已经产生一堆 100999 的脏文件 | 历史容器按默认映射写入 | **不要 sudo chown**：`podman unshare rm -rf <dir>` 或 `podman unshare chown -R 0:0 <dir>`（在用户命名空间里操作，等价于宿主的你自己） |
| 挂载 `/mnt/d/...` 报 `bad mount options` / overlay 创建失败，或 IO 慢到怀疑人生 | rootless 不支持对 drvfs/9p 做 overlay；跨系统 IO 本身慢 1–2 个数量级 | 项目搬进 WSL 内部 `~/`；`/mnt/*` 只读访问可以，别做工作区 |
| 启动报 `"/" is not a shared mount` | WSL2 自行挂载根分区、未标 shared（WSL 专属） | `/etc/wsl.conf` 加 `[boot] command = mount --make-rshared /`（§1.1），`wsl --shutdown` |
| `podman run` 报 `controller pids is not available` 类 cgroup 错 | systemd 没开或 cgroup v2 委派不全 | 确认 `ps -p 1` = systemd；真错误看 `journalctl --user -u podman` |
| 容器绑不了 80/443 等低位端口 | rootless 默认 `net.ipv4.ip_unprivileged_port_start=1024` | 用高位端口映射（`8000:80`）；确需低位：`sudo sysctl net.ipv4.ip_unprivileged_port_start=0` |
| 容器内访问宿主服务失败 | rootless 网络经 pasta，不走 `localhost` | 容器内用 `host.containers.internal`；或取 WSL 的 eth0 IP |
| 反过来：Windows 访问容器端口不通 | WSL2 NAT 端口转发未生效 | 依赖 VS Code `forwardPorts`（最稳）；裸 WSL 场景确认 Windows 侧 `localhostForwarding`；别用 mirrored 网络模式叠加 rootless pasta（坑多，未验证不推荐） |
| 拉镜像 500 / denied / 超时 | quay.io 国内不可达、registry 故障 | 换 `docker.io/library/...` 镜像 + registries.conf.d 加速（§2.9） |
| named volume 属主怪异 | 同 100999 问题 | 挂载加 `:U`（`-v myvol:/data:U`）自动 chown，或统一 keep-id |
| `apt install podman` 末尾报 `Job for systemd-binfmt.service failed` | WSL2 与 binfmt 注册表的兼容问题（Debian 13 + WSL 3.0.2 实测遇到） | 不影响使用，可忽略；要干净 → §5.1 |

### 5.1 systemd-binfmt.service failed（apt 装包后的红字，WSL2 已知现象）

**先说结论：不影响 Podman 日常使用，可以不处理。**

- 这个服务管理内核的 binfmt_misc 注册表（"什么格式的可执行文件交给谁跑"），典型用途只有一个：**跨架构模拟**（x86 机器上跑 arm64 容器，靠 qemu）
- WSL2 上为什么失败：WSL 自己在同一张表注册了 `WSLInterop`（WSL 里能跑 `code .`、`explorer.exe` 全靠它），老版本 systemd-binfmt 启动时会清掉别人的注册项、搞坏 WSL 互操作（systemd issue #28126）；WSL 2.5.7 起加了 generator 自动恢复注册，Ubuntu 24.04 起在 WSL 场景预禁用该服务；Debian 13 + WSL 3.0.2 上则表现为「启动失败」被 apt 打出来
- 影响面：仅跨架构模拟 —— x86_64 机器日常全跑 x86_64 镜像，用不到

要处理干净（Ubuntu WSL 官方文档的方案；比 `mask` 优雅，搬到非 WSL 环境自动恢复可用）：

```bash
sudo mkdir -p /etc/systemd/system/systemd-binfmt.service.d
printf '[Unit]\nConditionVirtualization=!wsl\n' | sudo tee /etc/systemd/system/systemd-binfmt.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl reset-failed systemd-binfmt.service   # 清掉当前红字状态
```

验证 WSL 互操作没被波及：WSL 里跑 `explorer.exe .` 能弹出 Windows 资源管理器即正常；万一不行，`wsl --shutdown` 重启后 WSL 会自动恢复注册。

---

## 6. 逐步验证清单（按序跑，全绿即收官）

**引擎层（WSL 终端）：**

1. `podman info` 无报错；§2.8 的 GraphDriver 输出 `overlay true`
2. `systemctl --user is-active podman.socket` → `active`；`ls -l $XDG_RUNTIME_DIR/podman/podman.sock` 存在
3. `podman run --rm docker.io/library/alpine echo ok` → 输出 `ok`
4. `curl -s --unix-socket $XDG_RUNTIME_DIR/podman/podman.sock http://d/v5.0.0/libpod/info | head -c 120` → 返回一段 JSON（API 通道通）
5. （可选，一键体检）`curl -fsSL https://raw.githubusercontent.com/ddev/ddev/main/scripts/linux-podman-rootless.sh -o /tmp/p.sh && bash /tmp/p.sh` —— 检查 subuid、socket、cgroup manager、netavark 配对并实跑一个容器

**编辑层（VS Code）：**

6. WSL 终端 `cd ~/projects/demo && code .` → 状态栏 `WSL: Debian`（目录还没建就回 §4.0 ② 走一遍）
7. 建好 §4 两个文件 → 命令面板 **`Dev Containers: Reopen in Container`** → 构建日志无错，左下角变 `Dev Container: py-dev`
8. 容器内终端 `id` → `uid=1000(dev)`；`touch /workspace/.wtest` 后**回到 WSL 终端** `ls -l ~/projects/demo/.wtest` → 属主是 `xin`（uid 1000），且 VS Code 资源管理器里能删掉它
9. `git status` 无 "dubious ownership" 警告

**调试与互通层：**

10. 容器内 `python3 -m http.server 8000` → **Windows 浏览器**开 `http://localhost:8000` 能看到目录列表（端口转发通）
11. 写个 `main.py` 打断点，F5 启动调试 → 断点命中（调试链路通）
12. 容器内 `curl -s https://www.baidu.com -o /dev/null -w '%{http_code}\n'` → `200`（容器出网通）；容器内 `getent hosts host.containers.internal` 有解析
13. `wsl` 终端 `podman ps` → 能看到这个 dev container 在跑（引擎与扩展用的是同一套）

---

## 相关主题

- 为什么项目必须放 WSL 内部 ext4（跨系统文件 IO 慢 1–2 个数量级）
- `/etc/wsl.conf` 与导入实例的默认用户设置

---

> **可靠性说明**：本文为 2026-10-07 本机实机配置过程的完整记录，环境为 Windows 11 + WSL 3.0.2 + Debian 13（默认 shell zsh）+ Podman 5.x + VS Code 1.140 + Dev Containers 0.469.0。设置项名 `dev.containers.dockerPath`、`podman.socket` 用法、WSL2 make-rshared 均引自官方文档原文；UID 映射修法为多方实测一致结论。**不同发行版 / 扩展版本表现可能有差异** —— 特别是 Dev Containers 扩展的内部实现会随版本变化，若文中"必装垫片"的结论在你的版本上不适用，以 Dev Containers 输出面板（`Ctrl+Shift+U`）里的实际报错为准。
