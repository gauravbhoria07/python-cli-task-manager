import os
import sys
import json
import csv
import io
import shutil
import unittest
from datetime import datetime, date, timedelta
from unittest.mock import patch

# Ensure UTF-8 console output
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import to_do_app
from colorama import Fore, Style


class TestToDoApp(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(to_do_app.BASE_DIR, "test_temp")
        os.makedirs(self.test_dir, exist_ok=True)
        self.original_file_name = to_do_app.FILE_NAME
        self.original_csv_file_name = to_do_app.CSV_FILE_NAME

        self.test_json_file = os.path.join(self.test_dir, "test_tasks.json")
        self.test_csv_file = os.path.join(self.test_dir, "test_tasks.csv")

        to_do_app.FILE_NAME = self.test_json_file
        to_do_app.CSV_FILE_NAME = self.test_csv_file

    def tearDown(self):
        to_do_app.FILE_NAME = self.original_file_name
        to_do_app.CSV_FILE_NAME = self.original_csv_file_name
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_empty_title_validation_in_add_task(self):
        """Test that empty or whitespace-only titles are rejected in add_task."""
        tasks = []
        inputs = iter(["", "   ", "Valid Task", "", "", "", "1"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.add_task(tasks)
                output = fake_out.getvalue()

        self.assertIn("Task title cannot be empty", output)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Valid Task")
        self.assertEqual(tasks[0]["priority"], "HIGH")

    def test_empty_title_validation_in_update_task(self):
        """Test that empty or whitespace-only titles are rejected in update_task."""
        tasks = [{"title": "Old Title", "completed": False, "priority": "LOW", "due_date": "No Due Date"}]
        # num=1, choice=1 (Title), empty, spaces, 'New Title'
        inputs = iter(["1", "1", "", "   ", "New Title"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.update_task(tasks)
                output = fake_out.getvalue()

        self.assertIn("Task title cannot be empty", output)
        self.assertEqual(tasks[0]["title"], "New Title")

    def test_update_all_fields(self):
        """Test update_task choice 4 (Update ALL) with empty title validation and priority."""
        tasks = [{"title": "Old Title", "completed": False, "priority": "LOW", "due_date": "No Due Date"}]
        future_year = str(date.today().year + 1)
        # num=1, choice=4 (Update ALL), new title, priority 1 (HIGH), due date (01, 01, future_year)
        inputs = iter(["1", "4", "Brand New Title", "1", "01", "01", future_year])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.update_task(tasks)

        self.assertEqual(tasks[0]["title"], "Brand New Title")
        self.assertEqual(tasks[0]["priority"], "HIGH")
        self.assertEqual(tasks[0]["due_date"], f"01-01-{future_year}")

    def test_all_priority_levels_in_add_task(self):
        """Test adding tasks with HIGH, MEDIUM, and LOW priorities."""
        priorities = [("Task High", "1", "HIGH"), ("Task Med", "2", "MEDIUM"), ("Task Low", "3", "LOW")]
        tasks = []
        for title, p_choice, expected_p in priorities:
            inputs = iter([title, "", "", "", p_choice])
            with patch("builtins.input", lambda prompt="": next(inputs)):
                to_do_app.add_task(tasks)

        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0]["priority"], "HIGH")
        self.assertEqual(tasks[1]["priority"], "MEDIUM")
        self.assertEqual(tasks[2]["priority"], "LOW")

    def test_priority_update_bug_fix(self):
        """Test updating priority to HIGH, MEDIUM, and LOW without invalid-priority error."""
        # Test updating to HIGH
        tasks = [{"title": "Test Task", "completed": False, "priority": "LOW", "due_date": "No Due Date"}]
        inputs = iter(["1", "2", "1"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.update_task(tasks)
                out = fake_out.getvalue()
        self.assertEqual(tasks[0]["priority"], "HIGH")
        self.assertNotIn("Invalid Priority", out)
        self.assertIn("Priority updated successfully.", out)

        # Test updating to MEDIUM
        inputs = iter(["1", "2", "2"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.update_task(tasks)
                out = fake_out.getvalue()
        self.assertEqual(tasks[0]["priority"], "MEDIUM")
        self.assertNotIn("Invalid Priority", out)
        self.assertIn("Priority updated successfully.", out)

        # Test updating to LOW
        inputs = iter(["1", "2", "3"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.update_task(tasks)
                out = fake_out.getvalue()
        self.assertEqual(tasks[0]["priority"], "LOW")
        self.assertNotIn("Invalid Priority", out)
        self.assertIn("Priority updated successfully.", out)

    def test_priority_colors_in_view_task(self):
        """Test that HIGH, MEDIUM, and LOW render with intended Fore colors."""
        tasks = [
            {"title": "Task H", "completed": False, "priority": "HIGH", "due_date": "No Due Date"},
            {"title": "Task M", "completed": False, "priority": "MEDIUM", "due_date": "No Due Date"},
            {"title": "Task L", "completed": False, "priority": "LOW", "due_date": "No Due Date"},
        ]
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            to_do_app.view_task(tasks)
            output = fake_out.getvalue()

        self.assertIn(Fore.RED, output)
        self.assertIn(Fore.YELLOW, output)
        self.assertIn(Fore.GREEN, output)

    def test_task_selection_after_sorting_update(self):
        """
        Verify that updating a displayed task after priority-based sorting
        updates the correct original task record.
        """
        tasks = [
            {"title": "Low Task 1", "completed": False, "priority": "LOW", "due_date": "No Due Date"},
            {"title": "High Task 2", "completed": False, "priority": "HIGH", "due_date": "No Due Date"},
            {"title": "Medium Task 3", "completed": False, "priority": "MEDIUM", "due_date": "No Due Date"},
        ]
        inputs = iter(["1", "1", "Updated High Task"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.update_task(tasks)

        self.assertEqual(tasks[1]["title"], "Updated High Task")
        self.assertEqual(tasks[0]["title"], "Low Task 1")
        self.assertEqual(tasks[2]["title"], "Medium Task 3")

    def test_task_selection_after_sorting_delete(self):
        """
        Verify that deleting a displayed task after priority-based sorting
        deletes the correct original task record.
        """
        tasks = [
            {"title": "Low Task 1", "completed": False, "priority": "LOW", "due_date": "No Due Date"},
            {"title": "High Task 2", "completed": False, "priority": "HIGH", "due_date": "No Due Date"},
            {"title": "Medium Task 3", "completed": False, "priority": "MEDIUM", "due_date": "No Due Date"},
        ]
        inputs = iter(["1", "y"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.delete_task(tasks)

        self.assertEqual(len(tasks), 2)
        titles = [t["title"] for t in tasks]
        self.assertIn("Low Task 1", titles)
        self.assertIn("Medium Task 3", titles)
        self.assertNotIn("High Task 2", titles)

    def test_delete_confirmation_cancellation(self):
        """Test that entering 'n' cancels deletion."""
        tasks = [{"title": "Keep Me", "completed": False, "priority": "HIGH", "due_date": "No Due Date"}]
        inputs = iter(["1", "n"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.delete_task(tasks)
                out = fake_out.getvalue()

        self.assertIn("Deletion cancelled.", out)
        self.assertEqual(len(tasks), 1)

    def test_delete_multiple_tasks_after_sorting(self):
        """Test deleting multiple tasks simultaneously with sorting mapping."""
        tasks = [
            {"title": "Low Task", "completed": False, "priority": "LOW", "due_date": "No Due Date"},
            {"title": "High Task", "completed": False, "priority": "HIGH", "due_date": "No Due Date"},
            {"title": "Med Task", "completed": False, "priority": "MEDIUM", "due_date": "No Due Date"},
        ]
        inputs = iter(["1, 3", "y"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.delete_task(tasks)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["title"], "Med Task")

    def test_json_missing_file(self):
        """Test load_tasks with missing tasks.json."""
        if os.path.exists(self.test_json_file):
            os.remove(self.test_json_file)
        tasks = to_do_app.load_tasks()
        self.assertEqual(tasks, [])

    def test_json_empty_file(self):
        """Test load_tasks with empty (0 bytes) tasks.json."""
        with open(self.test_json_file, "w", encoding="utf-8") as f:
            f.write("")
        tasks = to_do_app.load_tasks()
        self.assertEqual(tasks, [])

    def test_json_corrupted_file_creates_backup(self):
        """Test load_tasks with corrupted tasks.json preserves data via backup."""
        corrupted_content = "{ this is not valid json : [[["
        with open(self.test_json_file, "w", encoding="utf-8") as f:
            f.write(corrupted_content)

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            tasks = to_do_app.load_tasks()
            out = fake_out.getvalue()

        self.assertEqual(tasks, [])
        self.assertIn("Failed to load tasks", out)
        self.assertIn("backup", out.lower())

        # Check backup file was created
        backups = [f for f in os.listdir(self.test_dir) if "corrupted" in f and f.endswith(".bak")]
        self.assertTrue(len(backups) >= 1)

        with open(os.path.join(self.test_dir, backups[0]), "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), corrupted_content)

    def test_json_non_list_type_handling(self):
        """Test load_tasks with valid JSON that is not a list (e.g. dict or integer)."""
        with open(self.test_json_file, "w", encoding="utf-8") as f:
            f.write(json.dumps({"not": "a list"}))

        tasks = to_do_app.load_tasks()
        self.assertEqual(tasks, [])
        backups = [f for f in os.listdir(self.test_dir) if "corrupted" in f and f.endswith(".bak")]
        self.assertTrue(len(backups) >= 1)

    def test_csv_export_consistency(self):
        """Test that tasks.csv is exported to BASE_DIR and matches latest tasks.json."""
        tasks_data = [
            {"title": "Task A", "priority": "HIGH", "due_date": "01-01-2099", "completed": False},
            {"title": "Task B", "priority": "LOW", "due_date": "01-01-2020", "completed": False},
            {"title": "Task C", "priority": "MEDIUM", "due_date": "No Due Date", "completed": True},
        ]
        with open(self.test_json_file, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f)

        to_do_app.export_task_to_csv()

        self.assertTrue(os.path.exists(self.test_csv_file))

        with open(self.test_csv_file, "r", newline="", encoding="utf-8") as f:
            reader = list(csv.reader(f))

        self.assertEqual(reader[0], ["Title", "Priority", "Due Date", "Status"])
        self.assertEqual(reader[1], ["Task A", "HIGH", "01-01-2099", "Pending"])
        self.assertEqual(reader[2], ["Task B", "LOW", "01-01-2020", "Overdue"])
        self.assertEqual(reader[3], ["Task C", "MEDIUM", "No Due Date", "Completed"])

    def test_complete_and_reopen_task(self):
        """Test marking a task completed and reopening it as pending."""
        tasks = [
            {"title": "Task 1", "completed": False, "priority": "HIGH", "due_date": "No Due Date"}
        ]
        # Mark completed: choice 1, task 1
        inputs = iter(["1", "1"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.task_completed(tasks)
        self.assertTrue(tasks[0]["completed"])

        # Reopen as pending: choice 2, task 1
        inputs = iter(["2", "1"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            to_do_app.task_completed(tasks)
        self.assertFalse(tasks[0]["completed"])

    def test_statistics_and_search(self):
        """Test show_statistics and search_tasks functions."""
        tasks = [
            {"title": "Fix search bug", "completed": True, "priority": "HIGH", "due_date": "No Due Date"},
            {"title": "Review docs", "completed": False, "priority": "LOW", "due_date": "01-01-2020"},
        ]
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            to_do_app.show_statistics(tasks)
            stats_out = fake_out.getvalue()
        self.assertIn("Total tasks : 2", stats_out)
        self.assertIn("Completed tasks : 1", stats_out)
        self.assertIn("Overdue tasks : 1", stats_out)

        inputs = iter(["search"])
        with patch("builtins.input", lambda prompt="": next(inputs)):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                to_do_app.search_tasks(tasks)
                search_out = fake_out.getvalue()
        self.assertIn("1 matching task(s) found.", search_out)
        self.assertIn("Fix search bug", search_out)


if __name__ == "__main__":
    unittest.main()
