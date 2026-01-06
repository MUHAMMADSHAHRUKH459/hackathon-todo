# Task T-004: Implement Console Menu
# Spec: specs/features/task-crud.md § All User Stories
# Plan: specs/plan.md § ui.py, Menu Structure

"""
Console user interface for the Todo application.

This module provides the ConsoleUI class which handles all user interactions
through a command-line menu interface. It displays tasks, gets user input,
and shows appropriate feedback messages.
"""

from typing import Optional
from todo_manager import TodoManager
from models import Task


class ConsoleUI:
    """
    Console-based user interface for the Todo application.
    
    Provides a menu-driven interface for managing tasks, handling user input,
    and displaying formatted output with error handling.
    
    Attributes:
        manager: TodoManager instance for task operations
    
    Example:
        >>> storage = TaskStorage()
        >>> manager = TodoManager(storage)
        >>> ui = ConsoleUI(manager)
        >>> ui.run()
    """
    
    def __init__(self, manager: TodoManager) -> None:
        """
        Initialize ConsoleUI with a TodoManager.
        
        Args:
            manager: TodoManager instance for task operations
        """
        self.manager = manager
    
    def run(self) -> None:
        """
        Main application loop displaying menu and handling user choices.
        
        Displays the menu repeatedly until user chooses to exit.
        Catches all exceptions and displays friendly error messages.
        """
        while True:
            self.show_menu()
            choice = input("\nEnter choice (1-6): ").strip()
            
            print()  # Blank line for spacing
            
            try:
                if choice == "1":
                    self.prompt_add_task()
                elif choice == "2":
                    self.prompt_view_tasks()
                elif choice == "3":
                    self.prompt_update_task()
                elif choice == "4":
                    self.prompt_delete_task()
                elif choice == "5":
                    self.prompt_toggle_complete()
                elif choice == "6":
                    print("Thank you for using Todo App!")
                    break
                else:
                    self.display_error("Invalid choice. Please enter 1-6.")
            except ValueError as e:
                self.display_error(str(e))
            except Exception as e:
                self.display_error(f"An unexpected error occurred: {e}")
            
            # Pause before showing menu again (except on exit)
            if choice != "6":
                input("\nPress Enter to continue...")
                print()
    
    def show_menu(self) -> None:
        """
        Display the main menu with all available options.
        """
        print("=" * 30)
        print("        Todo App")
        print("=" * 30)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print("=" * 30)
    
    def prompt_add_task(self) -> None:
        """
        Prompt user to add a new task.
        
        Gets title and description from user, creates the task,
        and displays success message.
        
        Raises:
            ValueError: If validation fails (caught by run() loop)
        """
        print("=== Add New Task ===")
        
        title = input("Enter title: ").strip()
        description = input("Enter description (optional): ").strip()
        
        task = self.manager.create_task(title, description)
        self.display_success(f'Task #{task.id} created successfully: "{task.title}"')
    
    def prompt_view_tasks(self) -> None:
        """
        Display all tasks in a formatted list.
        
        Shows task ID, completion status, and title for each task.
        Displays total count with breakdown of completed and pending tasks.
        Shows friendly message if no tasks exist.
        """
        print("=== Your Tasks ===")
        
        tasks = self.manager.list_tasks()
        
        if not tasks:
            print("No tasks found. Add a task to get started!")
            return
        
        # Display tasks
        self.display_tasks(tasks)
        
        # Display summary
        completed = sum(1 for task in tasks if task.completed)
        pending = len(tasks) - completed
        print(f"\nTotal: {len(tasks)} task{'s' if len(tasks) != 1 else ''} "
              f"({completed} completed, {pending} pending)")
    
    def prompt_update_task(self) -> None:
        """
        Prompt user to update an existing task.
        
        Gets task ID, displays current values, gets new values,
        and updates the task. Empty input keeps original value.
        
        Raises:
            ValueError: If validation fails (caught by run() loop)
        """
        print("=== Update Task ===")
        
        # Get task ID
        task_id_str = input("Enter task ID: ").strip()
        
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
            return
        
        # Get existing task
        task = self.manager.get_task(task_id)
        if task is None:
            self.display_error(f"Task #{task_id} not found")
            return
        
        # Show current values
        print(f"Current title: {task.title}")
        new_title = input("New title (press Enter to keep): ").strip()
        
        print(f"Current description: {task.description}")
        new_description = input("New description (press Enter to keep): ").strip()
        
        # Update task (None if empty input to keep current)
        title_to_update = new_title if new_title else None
        description_to_update = new_description if new_description else None
        
        # Only update if at least one field changed
        if title_to_update is None and description_to_update is None:
            print("No changes made.")
            return
        
        success = self.manager.update_task(task_id, title_to_update, description_to_update)
        if success:
            self.display_success(f"Task #{task_id} updated successfully")
        else:
            self.display_error(f"Failed to update task #{task_id}")
    
    def prompt_delete_task(self) -> None:
        """
        Prompt user to delete a task with confirmation.
        
        Gets task ID, shows task details, asks for confirmation,
        and deletes the task if confirmed.
        """
        print("=== Delete Task ===")
        
        # Get task ID
        task_id_str = input("Enter task ID: ").strip()
        
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
            return
        
        # Get existing task
        task = self.manager.get_task(task_id)
        if task is None:
            self.display_error(f"Task #{task_id} not found")
            return
        
        # Confirm deletion
        confirmation = input(f'Are you sure you want to delete "{task.title}"? (y/n): ').strip().lower()
        
        if confirmation == 'y':
            success = self.manager.delete_task(task_id)
            if success:
                self.display_success(f"Task #{task_id} deleted successfully")
            else:
                self.display_error(f"Failed to delete task #{task_id}")
        else:
            print("Deletion cancelled.")
    
    def prompt_toggle_complete(self) -> None:
        """
        Prompt user to toggle a task's completion status.
        
        Gets task ID, toggles completion status, and displays
        the new status.
        """
        print("=== Toggle Complete ===")
        
        # Get task ID
        task_id_str = input("Enter task ID: ").strip()
        
        try:
            task_id = int(task_id_str)
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
            return
        
        # Toggle completion
        success = self.manager.toggle_complete(task_id)
        if not success:
            self.display_error(f"Task #{task_id} not found")
            return
        
        # Get updated task to show new status
        task = self.manager.get_task(task_id)
        if task.completed:
            self.display_success(f"Task #{task_id} marked as complete")
        else:
            self.display_success(f"Task #{task_id} marked as incomplete")
    
    def display_tasks(self, tasks: list[Task]) -> None:
        """
        Display a formatted list of tasks.
        
        Shows each task with ID, completion status symbol, and title.
        Format: [ID] [✓] Title (completed) or [ID] [ ] Title (incomplete)
        
        Args:
            tasks: List of Task objects to display
        """
        for task in tasks:
            print(task)
    
    def display_success(self, message: str) -> None:
        """
        Display a success message with visual indicator.
        
        Args:
            message: Success message to display
        """
        print(f"✓ {message}")
    
    def display_error(self, message: str) -> None:
        """
        Display an error message with visual indicator.
        
        Args:
            message: Error message to display
        """
        print(f"✗ Error: {message}")
    
    def display_info(self, message: str) -> None:
        """
        Display an informational message.
        
        Args:
            message: Information message to display
        """
        print(f"ℹ {message}")