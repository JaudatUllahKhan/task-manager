import os
import pickle  # INSECURE: Snyk isko security issue count karega (Insecure Deserialization)

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority, due_date):
        """Task add karne ka function"""
        # BUG 1: Empty title check nahi ho raha (Validation Bug)
        # BUG 2: Invalid priority input (e.g., 'ABC') check nahi ho rahi
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority, # Expected: High, Medium, Low
            "due_date": due_date,
            "status": "Pending"
        }
        self.tasks.append(task)
        print(f"\n[+] Task '{title}' successfully added!")

    def view_tasks(self, filter_priority=None):
        """Tasks ko display aur filter karne ka function (Loops ka use)"""
        if not self.tasks:
            print("\n[-] No tasks found.")
            return

        print("\n--- TASK LIST ---")
        for task in self.tasks:
            if filter_priority and task["priority"].lower() != filter_priority.lower():
                continue  # Filter condition
            
            print(f"ID: {task['id']} | Title: {task['title']} | Priority: {task['priority']} | Due: {task['due_date']} | Status: {task['status']}")

    def update_status(self, task_id, new_status):
        """Task status update karne ka function (If-Else ka use)"""
        # BUG 3: Agar user string enter kar de task_id ki jagah to crash ho jayega (Data Type Bug)
        for task in self.tasks:
            if task["id"] == int(task_id):
                task["status"] = new_status
                print(f"\n[+] Task ID {task_id} updated to {new_status}.")
                return
        print("\n[-] Task ID not found.")

    def save_data_insecurely(self, filename="tasks.dat"):
        """Data ko save karne ka function"""
        # SECURITY VULNERABILITY: Using pickle.dump() on unvalidated data
        with open(filename, "wb") as f:
            pickle.dump(self.tasks, f)
        print(f"\n[+] Data saved to {filename}")

def main_menu():
    manager = TaskManager()
    
    # Fake hardcoded credentials for Snyk to catch
    ADMIN_PASSWORD = "SuperSecretPassword123" # SECURITY VULNERABILITY: Hardcoded Secret

    while True:
        print("\n=== TASK MANAGER MENU ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Filter Tasks by Priority")
        print("4. Update Task Status")
        print("5. Save Backup")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            title = input("Enter Task Title: ")
            priority = input("Enter Priority (High/Medium/Low): ")
            due_date = input("Enter Due Date (DD-MM-YYYY): ")
            manager.add_task(title, priority, due_date)

        elif choice == "2":
            manager.view_tasks()

        elif choice == "3":
            prio = input("Enter priority to filter (High/Medium/Low): ")
            manager.view_tasks(filter_priority=prio)

        elif choice == "4":
            t_id = input("Enter Task ID to update: ")
            status = input("Enter New Status (Pending/In-Progress/Completed): ")
            manager.update_status(t_id, status)

        elif choice == "5":
            manager.save_data_insecurely()

        elif choice == "6":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main_menu()