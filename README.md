# AutomationZ OS Setup (Fedora KDE)

This repo turns a fresh Fedora KDE install into an "AutomationZ Admin OS" style workstation:

- AutomationZ Hub in the KDE menu
- AutomationZ installed to `/opt/automationz`
- Auto-updater via systemd timer (git pull)
- Includes Steam, VSCodium, Firefox, FileZilla, and admin tooling

## Install

```bash
sudo dnf install -y git
git clone https://github.com/DayZ-AutomationZ/AutomationZ-OS-Setup.git
cd AutomationZ-OS-Setup
chmod +x install.sh
sudo ./install.sh
```

## Override AutomationZ repo URL/branch

```bash
sudo AUTOMATIONZ_GIT_URL="https://github.com/DayZ-AutomationZ/AutomationZ.git" AUTOMATIONZ_BRANCH="main" ./install.sh
```

## Update manually

From GUI: open **AutomationZ Hub** -> **Update AutomationZ now**

Or terminal:

```bash
sudo /opt/automationz-os/updater/automationz-update.sh
```

## Auto-updater status

```bash
systemctl status automationz-updater.timer
journalctl -u automationz-updater.service --no-pager -n 50
```

## Notes

- The Hub tries common tool entrypoints like `/opt/automationz/<tool>/main.py`.

## Credits

---
🧩 AutomationZ 
These tools are part of the AutomationZ Admin Toolkit:

- AutomationZ Mod Update Auto Deploy (steam workshop)
- AutomationZ Uploader
- AutomationZ Scheduler
- AutomationZ Server Backup Scheduler
- AutomationZ Server Health
- AutomationZ Config Diff 
- AutomationZ Admin Orchestrator
- AutomationZ Log Cleanup Scheduler

Together they form a complete server administration solution.

### 💚 Support the project

AutomationZ tools are built for server owners by a server owner.  
If these tools save you time or help your community, consider supporting development.

☕ Support me [Ko-fi](https://ko-fi.com/dannyvandenbrande) 
