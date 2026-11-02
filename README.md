# CLI To-Do List Application

A lightweight, terminal-based To-Do List manager written in Python. It features priority-based sorting, colorized terminal statuses, due date tracking with overdue detection, task statistics with a visual progress bar, keyword search, resilient JSON persistence, and CSV export.

---

## 📸 Preview

```text
 ------------ TO DO APP ------------

No.  Title              | Priority  | Due Date      | Status
-------------------------------------------------------------------
1    Submit proposal    | HIGH      | 15-11-2026    | ❌ PENDING
2    Review pull request| MEDIUM    | 12-11-2026    | ❌ PENDING
3    Buy groceries      | LOW       | No Due Date   | ✅ COMPLETED
```

> _<!-- Screenshot Placeholder: Add a terminal recording or screenshot here (e.g. assets/preview.png) -->_
>
> ![CLI Application Preview](https://via.placeholder.com/800x400?text=CLI+To-Do+List+Application+Preview)

---

## ✨ Features

- **Task Management**:
  - Add tasks with title, priority (`HIGH`, `MEDIUM`, `LOW`), and optional due date (`DD-MM-YYYY`).
  - Update task title, priority, due date, or all fields at once.
  - Delete tasks individually or in bulk (comma-separated) with a safe confirmation prompt (`y/n`).
  - Mark tasks as completed or reopen them back to pending.
  - Clear all tasks with confirmation.
- **Priority-Based Organization**:
  - High, Medium, and Low priorities color-coded in terminal output:
    - **HIGH**: Red
    - **MEDIUM**: Yellow
    - **LOW**: Green
  - Consistent priority sorting across all list views (`HIGH` &rarr; `MEDIUM` &rarr; `LOW`), ensuring displayed numbers correctly map to task records.
- **Smart Due Date Tracking**:
  - Date validation enforcing non-past dates (`DD-MM-YYYY`) or optional skip (`No Due Date`).
  - Automatic overdue detection against current date with visual badges (`⚠️ OVERDUE`, `❌ PENDING`, `✅ COMPLETED`).
- **Resilient Data Persistence**:
  - Automatically loads and saves tasks from/to `tasks.json`.
  - Gracefully handles missing, empty, or corrupted JSON files without crashing or silently destroying user data.
  - Automatically generates timestamped backups (`tasks.json.corrupted_<timestamp>.bak`) if corrupted data is detected.
- **CSV Export**:
  - Export current task records directly to `tasks.csv` in the project root directory.
  - Always synchronizes with the latest task records and statuses.
- **Search & Analytics**:
  - Search tasks by keyword matching title, priority, or due date.
  - View task statistics: total count, completed, overdue, pending, and an ASCII visual progress bar.

---

## 🛠️ Technologies Used

- **Language**: Python 3.8+
- **Terminal Styling**: [colorama](https://pypi.org/project/colorama/) (cross-platform colored terminal text)
- **Built-in Libraries**: `json`, `csv`, `datetime`, `os`, `sys`, `shutil`, `unittest`

---

## 📁 Project Structure

```text
to do app/
│
├── to_do_app.py        # Main CLI application script
├── test_to_do_app.py   # Unit test suite covering all features and bug fixes
├── tasks.json          # Persistent JSON storage for tasks
├── tasks.csv           # Exported CSV file of tasks
├── requirements.txt    # Project dependencies
├── .gitignore          # Git ignore rules for Python artifacts & backups
└── README.md           # Project documentation and guide
```

---

## 🚀 Installation Instructions

### Prerequisites

- Python 3.8 or higher installed on your system.
- `pip` package manager.

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/to-do-app.git
   cd "to-do-app"
   ```

2. **(Optional) Create and activate a virtual environment:**
   - **Windows:**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Execution Instructions

Run the application with:

```bash
python to_do_app.py
```

To run the automated test suite:

```bash
python -m unittest test_to_do_app.py
```

---

## 📖 Usage Examples

### 1. Main Menu
```text
 ------------ MENU ------------
Select the operations you want to perform :
1.Add a task 
2.Update the task  
3.Delete the task 
4.View the tasks 
5.Exit the app 
6.Clear all Tasks 
7.Mark a task as completed 
8.Show Statistics 
9.Search 
10.Export to CSV 
```

### 2. Adding a Task
```text
Enter the new task : Prepare presentation
Enter Day(DD) or press Enter to skip it: 20
Enter Month(MM) or press Enter to skip it: 11
Enter Year(YYYY) or press Enter to skip it: 2026
Select Priority : 
 1.HIGH 
2.MEDIUM 
3.LOW 

Enter priority number : 1
Task Prepare presentation added with priority HIGH successfully.
```

### 3. Updating a Task
```text
 Available tasks are: 
1.Prepare presentation
2.Review PR

Enter the task number you want to update : 1

What do you want to update? 
1.Title 
2.Priority 
3.Due Date 
4.Update ALL
Enter your choice : 2
Select Priority : 
1.HIGH 
2.MEDIUM 
3.LOW 
Enter priority number : 2
Priority updated successfully.
```

### 4. Deleting a Task with Confirmation
```text
 Available tasks are: 
1.Prepare presentation
2.Review PR

Enter task numbers to delete (comma separated): 1
Are you sure you want to delete 1 task(s) (Prepare presentation)? (y/n): y
Task Prepare presentation deleted successfully.
```

### 5. Completing or Reopening a Task
```text
Your tasks are:
         Task 1 :Prepare presentation ❌
         Task 2 :Review PR ✔️

1. Mark as completed 
2. Mark as pending (reopen)
Enter your choice (1 or 2, default 1): 2
Enter the task numbers you want to mark as pending (comma separated): 2
Task number 2 marked as pending.
```

### 6. Showing Statistics
```text
 ---------- STATISTICS ------------
Total tasks : 4 
Completed tasks : 2 
Overdue tasks : 1 
Pending tasks : 2 

Progress : [██████████░░░░░░░░░░] 50.00%
Completion rate of your tasks : 50.00%
```

---

## 📄 License

This project is licensed under the MIT License. Feel free to use and customize it!

