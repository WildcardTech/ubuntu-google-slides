import os

def create_autostart_dir():
    """Create the ~/.config/autostart directory."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    try:
        os.makedirs(autostart_dir, exist_ok=True)
        print(f"Created {autostart_dir} directory.")
    except Exception as e:
        print(f"Failed to create directory {autostart_dir}: {e}")

def create_file():
    """Create a test file in the autostart directory."""
    file_path = os.path.expanduser("~/.config/autostart/test_file.txt")
    try:
        with open(file_path, "w") as file:
            file.write("This is a test file.")
        print(f"Created file at: {file_path}")
    except Exception as e:
        print(f"Failed to create file {file_path}: {e}")

if __name__ == "__main__":
    create_autostart_dir()
    create_file()

