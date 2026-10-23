"""Local task list; Python standard library only."""

import argparse
import json
import os
from pathlib import Path
import tempfile


def load_tasks(path):
    path = Path(path)
    if not path.exists():
        return []
    try:
        tasks = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ValueError("数据文件无法读取为 JSON，原文件未修改") from exc
    valid = isinstance(tasks, list)
    ids = set()
    if valid:
        for task in tasks:
            if not isinstance(task, dict):
                valid = False
                break
            task_id = task.get("id")
            if (type(task_id) is not int or task_id < 1 or task_id in ids
                    or not isinstance(task.get("title"), str)
                    or not task["title"].strip()
                    or type(task.get("done")) is not bool):
                valid = False
                break
            ids.add(task_id)
    if not valid:
        raise ValueError("任务数据格式不正确，原文件未修改")
    return tasks


def save_tasks(path, tasks):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent,
            prefix=path.name + ".", delete=False
        ) as handle:
            temporary = handle.name
            json.dump(tasks, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def add_task(path, title):
    title = title.strip()
    if not title:
        raise ValueError("任务标题不能为空")
    tasks = load_tasks(path)
    task = {"id": max((t["id"] for t in tasks), default=0) + 1,
            "title": title, "done": False}
    tasks.append(task)
    save_tasks(path, tasks)
    return task


def complete_task(path, task_id):
    tasks = load_tasks(path)
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(path, tasks)
            return task
    raise ValueError(f"找不到编号为 {task_id} 的任务")


def main():
    parser = argparse.ArgumentParser(description="本地任务清单")
    parser.add_argument("--file", default="tasks.json", help="JSON 数据文件")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list", help="列出所有任务")
    add = commands.add_parser("add", help="新增任务")
    add.add_argument("title")
    done = commands.add_parser("done", help="标记完成")
    done.add_argument("id", type=int)
    args = parser.parse_args()
    try:
        if args.command == "add":
            task = add_task(args.file, args.title)
            print(f"已添加 #{task['id']}：{task['title']}")
        elif args.command == "done":
            task = complete_task(args.file, args.id)
            print(f"已完成 #{task['id']}：{task['title']}")
        else:
            tasks = load_tasks(args.file)
            if not tasks:
                print("暂无任务。使用 add 添加第一项。")
            for task in tasks:
                marker = "x" if task["done"] else " "
                print(f"[{marker}] #{task['id']} {task['title']}")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"错误：{exc}\n")


if __name__ == "__main__":
    main()
