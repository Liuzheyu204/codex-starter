# Codex 中文起步仓库

用于练习让 Codex 阅读项目、实现功能、运行测试和交付修改。附带一个可以立即运行的命令行任务清单。这里只是开发起点，不是完成的挑战杯参赛项目。

## 开始使用

需要 Python 3.10 或更高版本，无需安装第三方库。在本目录打开终端：

```sh
python tasks.py add "确定项目的目标用户"
python tasks.py add "完成第一次需求访谈"
python tasks.py list
python tasks.py done 1
python -m unittest discover -s tests -v
```

macOS/Linux 如未提供 `python` 命令，可改用 `python3`。
数据默认保存在当前目录的 `tasks.json`，该文件不会提交到 Git。
可通过 `python tasks.py --file 路径 add "任务"` 指定其他数据文件。

## 给 Codex 的第一条任务

> 阅读 README.md 和 AGENTS.md，运行已有测试，说明当前程序如何工作。然后添加按关键词搜索任务的功能，补充能验证搜索行为的测试，运行测试并解释修改。保持现有命令兼容。

## 仓库内容

| 文件 | 用途 |
| --- | --- |
| AGENTS.md | 给代码助手的项目工作约定 |
| tasks.py | 可运行的任务清单示例 |
| tests/test_tasks.py | 验证存储、完成任务和错误处理 |
| docs/START_HERE.md | 从空仓库到第一次开发任务 |
| docs/PROMPTS.md | 可复制的开发任务指令 |
| docs/PROJECT_BRIEF.md | 填写真实项目需求 |
| .github/ISSUE_TEMPLATE/task.md | 开发任务模板 |

没有预设第三方服务、付费 API 或自动部署。需要这些能力时，再围绕项目需求添加。

## 发布和数据

任务清单是本地明文 JSON，不适合保存密码、密钥或敏感访谈记录。示例没有登录、云同步或多人协作。当前未选择开源许可证；如果要公开授权他人使用代码，请先决定许可证。
