---
title: "vscode配置"
description: "按f1输入task,调出运行配置文件"
pubDatetime: 2017-04-17T12:52:37
draft: false
tags: ["软件"]
---

+ 按f1输入task,调出运行配置文件
    输入

```
{
    "version": "0.1.0",
    "command": "python",
    "isShellCommand": true,
    "args": ["${file}"],
    "showOutput": "always",
    "options":
        {
        "env":
            {
            "PYTHONIOENCODING": "UTF-8"
            }
        }
}
```

+ 常用插件
    进辅助线 Guides
    文件图标 vscode-icons
    缩进线 Indenticator

+ 设置

```
// 将设置放入此文件中以覆盖默认设置
{
    "window.zoomLevel": 2,
    //字号
    "editor.fontSize": 14,
    // 字体
    "editor.fontFamily": "Hack, Menlo, Monaco, 'Courier New', monospace",
    //80个字符的提示线
    "editor.rulers": [80],
    "editor.acceptSuggestionOnEnter": true,
    // Arguments passed in. Each argument is a separate item in the array.
    //pep8自动格式化
    "python.formatting.autopep8Args":[
        "--max-line-length=80",
        "--indent-size=4"
    ],

    // Format the document upon saving. 保存文件后自动格式化
    "python.formatting.formatOnSave": true,
    // 忽略的pep8提示
    "python.linting.pylintArgs": [
        "--include-naming-hint=n",
        "--disable=W0311",
        "--disable=C0103",
        "--disable=E1101",
        "--disable=C0111",
        "--disable=W0621"
    ],
    //去除尾部的空格
    "files.trimTrailingWhitespace": true,
    //失去焦点时自动保存
    "files.autoSave": "onFocusChange",
    //显示缩进空格
      "editor.renderWhitespace": "boundary",
    "editor.renderLineHighlight": "line",
   //忽略的文件
  "files.exclude": {
    "**/.git": true,
    "**/.svn": true,
    "**/.hg": true,
    "**/.DS_Store": true,
        ".vscode": true,
        "**/__pycache__": true,
        "**/**/*.pyc": true
  },
  //关闭显示打开的文件
  "explorer.openEditors.visible": 0,
  //关闭回车的自动补全
    "editor.acceptSuggestionOnEnter": false


}
```

需要安装pylint和auto pep8;

+  自己需要的快捷键
```
[
    { "key": "f6",                    "command": "workbench.action.debug.continue",
                                     "when": "inDebugMode" },

{ "key": "f6",                    "command": "workbench.action.debug.start",
                                     "when": "!inDebugMode" },
{ "key": "f5",           "command": "workbench.action.tasks.build" }
]

```

+ 不出现自动补全提示的时候,
在`~/.vscode/extensions/donjayamanne.python-0.5.5/pythonFiles/preview/jedi/parser`目录下复制一份grammar3.5.txt,并将其改名为grammar3.6.txt