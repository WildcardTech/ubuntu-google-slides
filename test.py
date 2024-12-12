import os

autostart_dir = os.path.expanduser("~/.config/autostart")

try:
    os.makedirs(autostart_dir, exist_ok=True)
    print(f"Successfully created {autostart_dir} directory.")
except Exception as e:
    print(f"Failed to create directory {autostart_dir}: {e}")

