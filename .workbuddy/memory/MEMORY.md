# MEMORY.md — cpp-python-review 项目长期备忘

## 工作区约定
- 所有工程统一在 `D:\Learning Documents\WorkFinding\` 下，目录英文命名。
- C/C++ 通过 `.vscode/settings.json` + `C/C++ Runner` 扩展统一管理，常用工具链：mingw64 `D:/mingw64/bin/gcc.exe`、`g++.exe`、`gdb.exe`；MSVC 批处理 `C:/Program Files/Microsoft Visual Studio/VR_NR/Community/VC/Auxiliary/Build/vcvarsall.bat`。
- QT 工具链保留 MinGW 8.1.0 at `C:\Program Files\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin`。

## VSCode 推荐扩展与 Python 联想通用配置
- 在每个工程根 `.vscode/extensions.json` 推荐：`ms-python.python` + `ms-python.vscode-pylance`。
- 关键 settings.json 段（追加在 C++ 段之后即可）：
  - `python.languageServer = "Pylance"`
  - `editor.quickSuggestions.{strings, other} = true`
  - `editor.suggest.snippetsPreventQuickSuggestions = false`
  - `files.associations: {"*.py": "python"}`
- 验证方法：状态栏右下角出现 Python 版本 → 输入 `os.pa` 弹出 `os.path` → 鼠标悬停函数出 docstring。

## 学习节奏
- 中文回复，步骤化 + 表格化 + 改动汇总 + 验证步骤，是默认输出风格。
- 处理报错流程：先根因诊断 → 再给出跨项目通用修复方案 → 最后给出可执行的验证步骤。
