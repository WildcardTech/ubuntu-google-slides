import os
import subprocess

def create_autostart_dir():
    """Create the ~/.config/autostart directory."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    try:
        os.makedirs(autostart_dir, exist_ok=True)
        if os.path.exists(autostart_dir):
            print(f"Successfully created or verified {autostart_dir} directory.")
        else:
            print(f"Directory {autostart_dir} does not exist after attempting to create it.")
    except Exception as e:
        print(f"Failed to create directory {autostart_dir}: {e}")

def install_packages():
    """Install necessary packages."""
    try:
        print("Updating package lists...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        print("Installing required packages (Chromium, Unclutter)...")
        packages = ["chromium-browser", "unclutter"]
        subprocess.run(["sudo", "apt", "install", "-y"] + packages, check=True)
        print("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")

def create_slides_script(url):
    """Create the startup shell script for Google Slides."""
    script_content = f"""#!/bin/bash
# Wait for the desktop to load
sleep 10
# Open Chromium in kiosk mode with the Google Slides URL
chromium-browser --kiosk --disable-infobars --disable-restore-session-state "{url}"
"""
    script_path = "/usr/local/bin/start_google_slides.sh"
    try:
        with open("start_google_slides.sh", "w") as script_file:
            script_file.write(script_content)
        subprocess.run(["sudo", "mv", "start_google_slides.sh", script_path], check=True)
        subprocess.run(["sudo", "chmod", "755", script_path], check=True)
        if os.path.exists(script_path):
            print(f"Successfully created startup script at: {script_path}")
        else:
            print(f"Startup script {script_path} does not exist after attempting to create it.")
    except Exception as e:
        print(f"Failed to create script {script_path}: {e}")
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
    try:
        with open("google_slides.desktop", "w") as desktop_file:
            desktop_file.write(desktop_entry_content)
        subprocess.run(["sudo", "mv", "google_slides.desktop", desktop_entry_path], check=True)
        if os.path.exists(desktop_entry_path):
            print(f"Successfully created autostart entry at: {desktop_entry_path}")
        else:
            print(f"Autostart entry {desktop_entry_path} does not exist after attempting to create it.")
    except Exception as e:
        print(f"Failed to create autostart entry {desktop_entry_path}: {e}")
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
    try:
        with open("unclutter.desktop", "w") as unclutter_file:
            unclutter_file.write(unclutter_entry_content)
        subprocess.run(["sudo", "mv", "unclutter.desktop", unclutter_entry_path], check=True)
        if os.path.exists(unclutter_entry_path):
            print(f"Successfully created unclutter autostart entry at: {unclutter_entry_path}")
        else:
            print(f"Unclutter autostart entry {unclutter_entry_path} does not exist after attempting to create it.")
    except Exception as e:
        print(f"Failed to create unclutter autostart entry {unclutter_entry_path}: {e}")

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
    try:
        with open("xsessionrc_temp", "w") as file:
            file.write(commands)
        subprocess.run(["sudo", "mv", "xsessionrc_temp", xsessionrc_path], check=True)
        if os.path.exists(xsessionrc_path):
            print(f"Successfully updated {xsessionrc_path} with xset commands and unclutter.")
        else:
            print(f"{xsessionrc_path} does not exist after attempting to update it.")
    except Exception as e:
        print(f"Failed to update {xsessionrc_path}: {e}")

def main():
    print("Google Slides Auto-Run, Screen Settings, and Unclutter Setup")

    # Step 1: Create ~/.config/autostart directory
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

