import json
from pathlib import Path
import tempfile
import unittest

from tasks import add_task, complete_task, load_tasks


class TaskTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "tasks.json"

    def test_new_list_is_empty(self):
        self.assertEqual(load_tasks(self.path), [])

    def test_add_and_complete_persist_chinese_title(self):
        add_task(self.path, "  需求访谈  ")
        add_task(self.path, "测试原型")
        complete_task(self.path, 1)
        self.assertEqual(load_tasks(self.path), [
            {"id": 1, "title": "需求访谈", "done": True},
            {"id": 2, "title": "测试原型", "done": False},
        ])

    def test_blank_title_does_not_create_file(self):
        with self.assertRaises(ValueError):
            add_task(self.path, "   ")
        self.assertFalse(self.path.exists())

    def test_missing_id_preserves_file(self):
        add_task(self.path, "已有任务")
        before = self.path.read_bytes()
        with self.assertRaises(ValueError):
            complete_task(self.path, 99)
        self.assertEqual(self.path.read_bytes(), before)

    def test_corrupt_data_is_never_overwritten(self):
        for content in ["broken", "{}", '[{"id":true}]',
                        json.dumps([
                            {"id": 1, "title": "A", "done": False},
                            {"id": 1, "title": "B", "done": False},
                        ])]:
            with self.subTest(content=content):
                self.path.write_text(content, encoding="utf-8")
                before = self.path.read_bytes()
                with self.assertRaises(ValueError):
                    add_task(self.path, "新任务")
                self.assertEqual(self.path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
