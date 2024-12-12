import os
import subprocess

def run_command(command, use_sudo=False):
    """Run a shell command with optional sudo and log output."""
    if use_sudo:
        command.insert(0, 'sudo')
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running command: {' '.join(command)}\n{result.stderr}")
    return result.returncode

def create_autostart_dir():
    """Create the ~/.config/autostart directory."""
    autostart_dir = os.path.expanduser("~/.config/autostart")
    run_command(["mkdir", "-p", autostart_dir], use_sudo=True)

def install_packages():
    """Install necessary packages."""
    print("Updating package lists...")
    run_command(["apt", "update"], use_sudo=True)
    print("Installing required packages (Chromium, Unclutter)...")
    run_command(["apt", "install", "-y", "chromium-browser", "unclutter"], use_sudo=True)

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
        with open(script_path, "w") as script_file:
            script_file.write(script_content)
        run_command(["chmod", "755", script_path], use_sudo=True)
        print(f"Successfully created startup script at: {script_path}")
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
        with open(desktop_entry_path, "w") as desktop_file:
            desktop_file.write(desktop_entry_content)
        print(f"Successfully created autostart entry at: {desktop_entry_path}")
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
        with open(unclutter_entry_path, "w") as unclutter_file:
            unclutter_file.write(unclutter_entry_content)
        print(f"Successfully created unclutter autostart entry at: {unclutter_entry_path}")
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
        with open(xsessionrc_path, "w") as file:
            file.write(commands)
        print(f"Successfully updated {xsessionrc_path} with xset commands and unclutter.")
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
