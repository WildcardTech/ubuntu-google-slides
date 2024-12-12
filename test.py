import os

def create_autostart_dir():
    """Ensure the ~/.config/autostart directory exists."""
    config_dir = os.path.expanduser("~/.config")
    autostart_dir = os.path.join(config_dir, "autostart")

    try:
        if not os.path.exists(config_dir):
            os.makedirs(config_dir, exist_ok=True)
            print(f"Ensured {config_dir} directory exists.")
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir, exist_ok=True)
            print(f"Ensured {autostart_dir} directory exists.")
        else:
            print(f"Directory {autostart_dir} already exists.")
    except Exception as e:
        print(f"Failed to create directory {autostart_dir}: {e}")

if __name__ == "__main__":
    create_autostart_dir()
