import tkinter as tk
from tkinter import ttk


class Application(tk.Tk):
    """Main application window for the EyeChart application."""

    def __init__(self):
        """Initialize the application."""
        super().__init__()

        self.title("EyeChart")
        self.geometry("800x600")

        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a simple label
        self.label = ttk.Label(self.main_frame, text="EyeChart Application")
        self.label.pack(pady=20)

        # Create a simple button
        self.button = ttk.Button(self.main_frame, text="Click Me", command=self.on_button_click)
        self.button.pack(pady=10)

    def on_button_click(self):
        """Handle button click event."""
        print("Button clicked!")


def run_application():
    """Run the application."""
    app = Application()
    app.mainloop()
