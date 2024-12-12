import os
import subprocess

def create_autostart_dir():
    """Ensure the ~/.config/autostart directory exists."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    print(f"Ensured {autostart_dir} directory exists.")

def install_packages():
    """Ensure necessary packages are installed."""
    print("Checking for required packages (Chromium, Unclutter)...")
    packages = ["chromium-browser", "unclutter"]
    for package in packages:
        try:
            subprocess.run([package, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"{package} is already installed.")
        except FileNotFoundError:
            print(f"{package} is not installed. Installing {package}...")
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", package], check=True)

def create_slides_script(url):
    """Create the startup shell script for Google Slides."""
    script_content = f"""#!/bin/bash
# Wait for the desktop to load
sleep 10
# Open Chromium in kiosk mode with the Google Slides URL
chromium-browser --kiosk --disable-infobars --disable-restore-session-state "{url}"
"""
    script_path = "/usr/local/bin/start_google_slides.sh"

    # Write the script content
    with open(script_path, "w") as script_file:
        script_file.write(script_content)
    os.chmod(script_path, 0o755)
    print(f"Startup script created at: {script_path}")
    return script_path

def create_autostart_entry(script_path):
    """Create the autostart .desktop file for Google Slides."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    desktop_entry_content = f"""[Desktop Entry]
Type=Application
Exec={script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Start Google Slides
Comment=Automatically run Google Slides on boot
"""
    desktop_entry_path = os.path.join(autostart_dir, "google_slides.desktop")

    # Write the desktop entry content
    with open(desktop_entry_path, "w") as desktop_file:
        desktop_file.write(desktop_entry_content)
    print(f"Autostart entry created at: {desktop_entry_path}")
    return desktop_entry_path

def create_unclutter_autostart():
    """Create an autostart entry for Unclutter."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    unclutter_entry_content = """[Desktop Entry]
Type=Application
Exec=unclutter -idle 0
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Unclutter
Comment=Hide the mouse cursor when idle
"""
    unclutter_entry_path = os.path.join(autostart_dir, "unclutter.desktop")

    # Write the unclutter entry content
    with open(unclutter_entry_path, "w") as unclutter_file:
        unclutter_file.write(unclutter_entry_content)
    print(f"Unclutter autostart entry created at: {unclutter_entry_path}")

def update_xsessionrc():
    """Add xset commands and unclutter to ~/.xsessionrc."""
    xsessionrc_path = os.path.expanduser("~/.xsessionrc")
    commands = """
# Prevent screen blanking and power saving
xset s off
xset -dpms
xset s noblank

# Run unclutter to hide the mouse cursor when idle
unclutter -idle 0
"""

    if os.path.exists(xsessionrc_path):
        with open(xsessionrc_path, "r") as file:
            content = file.read()
        if commands.strip() not in content:
            content += commands
    else:
        content = commands

    with open(xsessionrc_path, "w") as file:
        file.write(content)
    print(f"xset commands and unclutter added to {xsessionrc_path}")

def main():
    print("Google Slides Auto-Run, Screen Settings, and Unclutter Setup")

    # Step 1: Ensure ~/.config/autostart directory exists
    create_autostart_dir()

    # Step 2: Get the Google Slides URL
    url = input("Enter the published URL of your Google Slides presentation: ").strip()
    if not url:
        print("URL cannot be empty. Exiting.")
        return

    # Step 3: Install required packages
    install_packages()

    # Step 4: Create the startup script for Google Slides
    script_path = create_slides_script(url)

    # Step 5: Create the autostart entry for Google Slides
    create_autostart_entry(script_path)

    # Step 6: Create the autostart entry for Unclutter
    create_unclutter_autostart()

    # Step 7: Update the ~/.xsessionrc file to prevent screen blanking and run unclutter
    update_xsessionrc()

    print("\nSetup complete! Reboot your system to test the setup.")

if __name__ == "__main__":
    main()
