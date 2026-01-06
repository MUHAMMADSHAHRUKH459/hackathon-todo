# Task T-005: Create Main Entry Point
# Spec: specs/plan.md § main.py

"""
Main entry point for the Todo application.

This module wires up all components (storage, manager, UI) and starts
the application with proper exception handling.
"""

from storage import TaskStorage
from todo_manager import TodoManager
from ui import ConsoleUI


def main() -> None:
    """
    Initialize and run the Todo application.
    
    Creates all necessary components, wires them together with dependency
    injection, and starts the console UI loop. Handles interruptions and
    unexpected errors gracefully.
    """
    try:
        # Initialize components with dependency injection
        storage = TaskStorage()
        manager = TodoManager(storage)
        ui = ConsoleUI(manager)
        
        # Display welcome message
        print("=== Todo App - Phase I ===\n")
        
        # Start application
        ui.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()