import json
import os
import sys
import shutil
from datetime import datetime, date
from colorama import Fore, Style, init
import csv

# Initialize colorama
init(autoreset=True)

# Ensure UTF-8 output encoding in consoles where supported
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_NAME = os.path.join(BASE_DIR, "tasks.json")
CSV_FILE_NAME = os.path.join(BASE_DIR, "tasks.csv")

PRIORITY_ORDER = {
    "HIGH": 1,
    "MEDIUM": 2,
    "LOW": 3
}


def get_sorted_task_indices(tasks):
    """
    Returns a list of tuples (original_index, task) sorted by priority
    (HIGH -> MEDIUM -> LOW). Preserves mapping to original tasks list.
    """
    return sorted(
        enumerate(tasks),
        key=lambda item: PRIORITY_ORDER.get(item[1].get("priority", "MEDIUM"), 2)
    )


def get_valid_due_date():
    while True:
        day = input("Enter Day(DD) or press Enter to skip it: ").strip()
        month = input("Enter Month(MM) or press Enter to skip it: ").strip()
        year = input("Enter Year(YYYY) or press Enter to skip it: ").strip()

        if day == "" and month == "" and year == "":
            return "No Due Date"

        if not (day and month and year):
            print("Please enter valid date or leave all fields blank.")
            continue
        try:
            valid_date = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y").date()
            if valid_date < date.today():
                print("Date cannot be in the past. Please enter a future date.")
                continue
            return valid_date.strftime("%d-%m-%Y")

        except ValueError:
            print("Invalid date. Please enter correct values.")


def add_task(tasks):
    while True:
        new_task = input("Enter the new task : ").strip()
        if not new_task:
            print("Task title cannot be empty. Please enter a valid task title.")
            continue
        break

    due_date = get_valid_due_date()

    print("Select Priority : \n 1.HIGH \n2.MEDIUM \n3.LOW \n")
    while True:
        try:
            choice = int(input("Enter priority number : "))
            if choice == 1:
                priority = "HIGH"
                break
            elif choice == 2:
                priority = "MEDIUM"
                break
            elif choice == 3:
                priority = "LOW"
                break
            else:
                print("Invalid input. Please enter 1 , 2 or 3.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    task = {
        "title": new_task,
        "completed": False,
        "priority": priority,
        "due_date": due_date
    }

    tasks.append(task)
    print(f'Task {new_task} added with priority {priority} successfully.')


def update_task(tasks):
    if not tasks:
        print("No tasks found. Please add some tasks first.")
        return

    sorted_tasks = get_sorted_task_indices(tasks)
    print("\n Available tasks are: ")
    for i, (orig_idx, task) in enumerate(sorted_tasks, 1):
        print(f"{i}.{task['title']}")

    try:
        num = int(input("Enter the task number you want to update : "))
        if num < 1 or num > len(sorted_tasks):
            print(f"Task number {num} is Invalid.")
            return

    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    orig_idx, task = sorted_tasks[num - 1]

    print("\nWhat do you want to update? \n1.Title \n2.Priority \n3.Due Date \n4.Update ALL")

    try:
        choice = int(input("Enter your choice : "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    if choice == 1:
        while True:
            new_title = input("Enter the new title : ").strip()
            if not new_title:
                print("Task title cannot be empty. Please enter a valid task title.")
                continue
            break
        task['title'] = new_title
        print(f"Title of task {task['title']} updated successfully.")

    elif choice == 2:
        print("Select Priority : \n1.HIGH \n2.MEDIUM \n3.LOW ")
        try:
            p_choice = int(input("Enter priority number : "))
            if p_choice == 1:
                task['priority'] = 'HIGH'
            elif p_choice == 2:
                task['priority'] = 'MEDIUM'
            elif p_choice == 3:
                task['priority'] = 'LOW'
            else:
                print("Invalid Priority. Please enter 1, 2 or 3.")
                return
            print("Priority updated successfully.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

    elif choice == 3:
        due_date = get_valid_due_date()
        task['due_date'] = due_date
        print("Due date updated successfully.")

    elif choice == 4:
        while True:
            new_title = input("Enter the new title : ").strip()
            if not new_title:
                print("Task title cannot be empty. Please enter a valid task title.")
                continue
            break
        task['title'] = new_title
        print("\nSelect Priority : \n1.HIGH \n2.MEDIUM \n3.LOW")

        try:
            p = int(input("Enter priority number : "))
            if p == 1:
                task['priority'] = 'HIGH'
            elif p == 2:
                task['priority'] = 'MEDIUM'
            elif p == 3:
                task['priority'] = 'LOW'
            else:
                print("Invalid Priority. Please enter 1, 2 or 3.")
                return
        except ValueError:
            print("Invalid input. Please enter a number.")
            return

        due_date = get_valid_due_date()
        task['due_date'] = due_date

        print("Task updated successfully.")

    else:
        print("Invalid input. Please enter 1,2,3 or 4.")
        return


def delete_task(tasks):
    if not tasks:
        print("No tasks found. Please add some tasks first.")
        return

    sorted_tasks = get_sorted_task_indices(tasks)
    print("\n Available tasks are: ")
    for i, (orig_idx, task) in enumerate(sorted_tasks, 1):
        print(f"{i}.{task['title']}")

    user_input = input("Enter task numbers to delete (comma separated): ")

    try:
        numbers = [int(num.strip()) for num in user_input.split(",") if num.strip()]
        if not numbers:
            print("Invalid input. Please enter numbers separated by commas.")
            return

        valid_orig_indices = []
        invalid_numbers = []

        for num in numbers:
            if 1 <= num <= len(sorted_tasks):
                orig_idx = sorted_tasks[num - 1][0]
                if orig_idx not in valid_orig_indices:
                    valid_orig_indices.append(orig_idx)
            else:
                invalid_numbers.append(num)

        for num in invalid_numbers:
            print(f"Task number {num} is invalid.")

        if not valid_orig_indices:
            return

        # Optional improvement: confirmation prompt before deleting
        task_titles = [tasks[idx]['title'] for idx in valid_orig_indices]
        confirm = input(f"Are you sure you want to delete {len(valid_orig_indices)} task(s) ({', '.join(task_titles)})? (y/n): ").strip().lower()
        if confirm not in ("y", "yes"):
            print("Deletion cancelled.")
            return

        # Delete tasks by original indices in descending order to avoid index shifting
        for orig_idx in sorted(valid_orig_indices, reverse=True):
            del_task = tasks.pop(orig_idx)
            print(f"Task {del_task['title']} deleted successfully.")

    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")


def view_task(tasks):
    if tasks:
        title_width = max(len(task.get("title", "")) for task in tasks) + 2
        title_width = max(title_width, 7)
        print(f"\n{'No.':<4} {'Title':<{title_width}} | {'Priority':<9} | {'Due Date':<13} | Status")
        print("-" * (title_width + 49))

        sorted_tasks = get_sorted_task_indices(tasks)
        for i, (orig_idx, task) in enumerate(sorted_tasks, 1):
            due_date = task.get("due_date") or "No Due Date"

            if task.get("completed"):
                status = Fore.GREEN + "✅ COMPLETED" + Style.RESET_ALL
            else:
                due_date_str = task.get("due_date") or "No Due Date"

                if due_date_str != "No Due Date":
                    try:
                        task_date = datetime.strptime(due_date_str, "%d-%m-%Y").date()
                        if task_date < date.today():
                            status = Fore.YELLOW + "⚠️  OVERDUE" + Style.RESET_ALL
                        else:
                            status = Fore.RED + "❌ PENDING" + Style.RESET_ALL

                    except (ValueError, TypeError):
                        status = Fore.RED + "❌ PENDING" + Style.RESET_ALL
                else:
                    status = Fore.RED + "❌ PENDING" + Style.RESET_ALL

            priority = task.get("priority", "MEDIUM")
            formatted_priority = f"{priority:<9}"
            if priority == "HIGH":
                colored_priority = Fore.RED + formatted_priority + Style.RESET_ALL
            elif priority == "MEDIUM":
                colored_priority = Fore.YELLOW + formatted_priority + Style.RESET_ALL
            elif priority == "LOW":
                colored_priority = Fore.GREEN + formatted_priority + Style.RESET_ALL
            else:
                colored_priority = formatted_priority

            print(f"{i:<4} {task.get('title', ''):<{title_width}} | {colored_priority} | {due_date:<13} | {status}")

    else:
        print("No tasks found. Please add some tasks first.")


def task_completed(tasks):
    if not tasks:
        print("No tasks found. Please add some tasks first.")
        return

    sorted_tasks = get_sorted_task_indices(tasks)
    print("\nYour tasks are:")
    for i, (orig_idx, task) in enumerate(sorted_tasks, 1):
        status = "✔️" if task.get("completed") else "❌"
        print(f'         Task {i} :{task["title"]} {status}')

    print("\n1. Mark as completed \n2. Mark as pending (reopen)")
    action_choice = input("Enter your choice (1 or 2, default 1): ").strip()

    if "," in action_choice or (action_choice.isdigit() and int(action_choice) > 2):
        # Support passing comma-separated numbers directly
        user_input = action_choice
        action_type = "completed"
    elif action_choice == "2":
        action_type = "pending"
        user_input = input("Enter the task numbers you want to mark as pending (comma separated): ")
    else:
        action_type = "completed"
        user_input = input("Enter the task numbers you want to mark as completed (comma separated): ")

    try:
        numbers = [int(num.strip()) for num in user_input.split(",") if num.strip()]

        for num in numbers:
            if 1 <= num <= len(sorted_tasks):
                orig_idx, task = sorted_tasks[num - 1]
                if action_type == "completed":
                    task["completed"] = True
                    print(f"Task number {num} marked as completed.")
                else:
                    task["completed"] = False
                    print(f"Task number {num} marked as pending.")
            else:
                print(f"Task number {num} is invalid.")

    except ValueError:
        print("Invalid input. Please enter numbers separated by commas.")


def show_statistics(tasks):
    if not tasks:
        print("No tasks found. Please add some tasks first.")
        return

    total_tasks = len(tasks)
    completed = 0
    overdue = 0

    for task in tasks:
        if task.get("completed"):
            completed += 1
        else:
            due_date = task.get("due_date") or "No Due Date"

            if due_date != "No Due Date":
                try:
                    task_date = datetime.strptime(due_date, "%d-%m-%Y").date()
                    if task_date < date.today():
                        overdue += 1
                except (ValueError, TypeError):
                    pass
    pending = total_tasks - completed
    completion_rate = (completed / total_tasks) * 100

    progress_unit = 20
    filled = int((completed / total_tasks) * progress_unit)
    bar = "█" * filled + "░" * (progress_unit - filled)

    print("\n ---------- STATISTICS ------------")

    print(f"Total tasks : {total_tasks} ")
    print(f"Completed tasks : {completed} ")
    print(f"Overdue tasks : {overdue} ")
    print(f"Pending tasks : {pending} ")
    print(f"\nProgress : [{bar}] {completion_rate :.2f}%")
    print(f"Completion rate of your tasks : {completion_rate:.2f}%")


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []

    try:
        if os.path.getsize(FILE_NAME) == 0:
            return []

        with open(FILE_NAME, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValueError(f"Expected JSON list of tasks, but got {type(data).__name__}")
            return data

    except (json.JSONDecodeError, ValueError, OSError) as e:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{FILE_NAME}.corrupted_{timestamp}.bak"
        try:
            shutil.copyfile(FILE_NAME, backup_filename)
            print(Fore.RED + f"Error: Failed to load tasks from '{FILE_NAME}': {e}" + Style.RESET_ALL)
            print(Fore.YELLOW + f"A backup of the corrupted file was created at: {backup_filename}" + Style.RESET_ALL)
        except Exception as copy_err:
            print(Fore.RED + f"Error loading tasks and creating backup: {e} ({copy_err})" + Style.RESET_ALL)
        return []


def export_task_to_csv(tasks=None):
    # Always generate the CSV using the latest task data from tasks.json
    latest_tasks = load_tasks()
    if not latest_tasks:
        print("No tasks found to export. Please add some tasks first.")
        return

    try:
        with open(CSV_FILE_NAME, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(["Title", "Priority", "Due Date", "Status"])

            for task in latest_tasks:
                if task.get("completed"):
                    status = "Completed"
                else:
                    due_date = task.get("due_date") or "No Due Date"

                    if due_date != "No Due Date":
                        try:
                            task_date = datetime.strptime(due_date, "%d-%m-%Y").date()
                            if task_date < date.today():
                                status = "Overdue"
                            else:
                                status = "Pending"
                        except (ValueError, TypeError):
                            status = "Pending"
                    else:
                        status = "Pending"

                due_date_str = task.get("due_date") or "No Due Date"
                writer.writerow([
                    task.get("title", ""),
                    task.get("priority", "MEDIUM"),
                    due_date_str,
                    status
                ])

        print(f"Tasks exported to {CSV_FILE_NAME} successfully.")
    except OSError as e:
        print(f"Error exporting tasks to CSV: {e}")


def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=4)
    except OSError as e:
        print(f"Error saving tasks to '{FILE_NAME}': {e}")


def search_tasks(tasks):
    if not tasks:
        print("No tasks found. Please add some tasks first.")
        return

    keyword = input("Enter the keyword to search : ").strip().lower()
    result = []

    for task in tasks:
        due_val = task.get('due_date') or ""
        combined_text = (
            str(task.get('title', '')).lower() + " " +
            str(task.get('priority', "")).lower() + " " +
            str(due_val).lower()
        )
        if keyword in combined_text:
            result.append(task)

    if result:
        print("\n ------------ SEARCH RESULTS ------------")
        print(f"\n{len(result)} matching task(s) found.")
        view_task(result)
    else:
        print("No matching tasks found.")


def main():
    tasks = load_tasks()

    print("\n ------------ TO DO APP ------------")

    if not tasks:
        while True:
            try:
                total_tasks = int(input("Enter the total number of tasks : "))

                if total_tasks <= 0 or total_tasks > 10:
                    print("Invalid input. Please enter a positive number between 1 and 10.")
                elif total_tasks > 0:
                    for i in range(1, total_tasks + 1):
                        print(f"\nEntering details for task {i}: ")
                        add_task(tasks)
                    save_tasks(tasks)
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

    while True:
        print("\n ------------ MENU ------------")
        print("Select the operations you want to perform :")
        print("1.Add a task \n2.Update the task  \n3.Delete the task \n4.View the tasks \n5.Exit the app \n6.Clear all Tasks \n7.Mark a task as completed \n8.Show Statistics \n9.Search \n10.Export to CSV ")

        try:
            choice = int(input("Enter the operation you want to perform : "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            add_task(tasks)
            save_tasks(tasks)
        elif choice == 2:
            update_task(tasks)
            save_tasks(tasks)
        elif choice == 3:
            delete_task(tasks)
            save_tasks(tasks)
        elif choice == 4:
            view_task(tasks)
        elif choice == 5:
            break
        elif choice == 6:
            print("Do you really want to clear all tasks ?")
            print("1.Yes \n2.No")
            try:
                confirm = int(input("Enter your choice : "))
            except ValueError:
                print("Invalid input. Please enter 1 or 2.")
                continue
            if confirm == 1:
                tasks.clear()
                save_tasks(tasks)
                print("All tasks cleared successfully.")
            elif confirm == 2:
                pass
            else:
                print("Invalid input. Please enter 1 or 2.")

        elif choice == 7:
            task_completed(tasks)
            save_tasks(tasks)

        elif choice == 8:
            show_statistics(tasks)
        elif choice == 9:
            search_tasks(tasks)
        elif choice == 10:
            export_task_to_csv(tasks)

        elif choice <= 0 or choice > 10:
            print("Invalid Choice. Please enter a valid choice.")


if __name__ == "__main__":
    main()
