#!/usr/bin/env python3
"""把 OneDrive _posts 的 Markdown 同步到 astro-paper 主题的内容目录。

- 源文件只读，绝不修改 OneDrive 原件
- 自动补齐老 Hexo 文章残缺的 frontmatter（缺开头 --- / 完全没有）
- 字段转换为 astro-paper v6 schema：
    title      -> title（双引号包裹）
    date       -> pubDatetime（ISO 格式，js-yaml 解析为 Date）
    tags       -> tags（统一转数组）
    (新增)     -> description（取正文第一段纯文本，最多 100 字）
    (新增)     -> draft: false
- 幂等：转换结果与仓库现有文件一致就跳过

用法：python sync_posts.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import datetime
from pathlib import Path

SRC = Path(r"C:\Users\xin\OneDrive\_posts")
DST = Path(r"D:\blog\src\content\posts")


def normalize_raw(src: Path, text: str) -> str:
    """保证文件有完整的 --- frontmatter 块。"""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        return text
    for ln in lines[:15]:
        if ln.strip() == "---":
            return "---\n" + text
    mtime = datetime.fromtimestamp(src.stat().st_mtime)
    title = src.stem.replace("-", " ").replace("_", " ").strip() or src.stem
    fm = (
        "---\n"
        f"title: {title}\n"
        f"date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}\n"
        "---\n\n"
    )
    return fm + text


def yq(s: str) -> str:
    """YAML 双引号安全。"""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def parse_tags(fm: str) -> list[str]:
    m = re.search(r"^tags:\s*(.*)$", fm, re.M)
    if not m:
        return []
    inline = m.group(1).strip()
    if inline:
        v = inline.strip("[]")
        return [t.strip().strip("'\"") for t in re.split(r"[,，]", v) if t.strip()]
    # 块列表：tags: 后跟若干 "  - x"
    items = re.findall(r"^\s+-\s*(.+)$", fm[m.end():], re.M)
    return [t.strip().strip("'\"") for t in items if t.strip()]


def parse_date(fm: str, fallback: datetime) -> str:
    m = re.search(r"^date:\s*(.*)$", fm, re.M)
    raw = m.group(1).strip().strip("'\"") if m else ""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw, fmt).strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            continue
    return fallback.strftime("%Y-%m-%dT%H:%M:%S")


def make_desc(body: str, title: str) -> str:
    for line in body.splitlines():
        s = line.strip()
        if not s or s in ("---", "***", "___"):
            continue
        s = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", s)   # 图片 → alt
        s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)    # 链接 → 文字
        s = re.sub(r"^[#>\-*+]+\s*", "", s)               # 行首标记
        s = s.replace("`", "").replace("*", "")
        s = re.sub(r"\s+", " ", s).strip()
        if s:
            return s[:100]
    return title


def convert(src: Path) -> str:
    text = normalize_raw(src, src.read_text(encoding="utf-8", errors="replace"))
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    fm_src, body = m.group(1), m.group(2)

    t = re.search(r"^title:\s*(.*)$", fm_src, re.M)
    title = (t.group(1).strip().strip("'\"") if t else "") or src.stem
    pub = parse_date(fm_src, datetime.fromtimestamp(src.stat().st_mtime))
    tags = parse_tags(fm_src)
    desc = make_desc(body, title)

    lines = ["---", f"title: {yq(title)}", f"description: {yq(desc)}",
             f"pubDatetime: {pub}", "draft: false"]
    if tags:
        lines.append("tags: [" + ", ".join(yq(x) for x in tags) + "]")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.lstrip("\n")


def md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def main() -> int:
    if not SRC.is_dir():
        print(f"[错误] 源目录不存在: {SRC}")
        return 1
    DST.mkdir(parents=True, exist_ok=True)

    copied, skipped = [], 0
    for src in sorted(SRC.glob("*.md")):
        text = convert(src)
        dst = DST / src.name
        if dst.exists() and md5(dst.read_text(encoding="utf-8")) == md5(text):
            skipped += 1
            continue
        dst.write_text(text, encoding="utf-8", newline="\n")
        copied.append(src.name)

    src_names = {p.name for p in SRC.glob("*.md")}
    stale = [p.name for p in DST.glob("*.md") if p.name not in src_names]

    print(f"同步完成：更新 {len(copied)} 篇，未变化 {skipped} 篇，源共 {len(src_names)} 篇")
    if copied:
        print("  本次更新: " + ", ".join(copied[:10]) + (" ..." if len(copied) > 10 else ""))
    if stale:
        print("  ⚠️ 源里已不存在但仓库副本仍有（需手动删或确认）:")
        for name in stale:
            print(f"    {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
