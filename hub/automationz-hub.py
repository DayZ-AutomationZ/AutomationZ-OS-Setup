#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

AUTOMATIONZ_DIR = Path(os.environ.get("AUTOMATIONZ_DIR", "/opt/automationz"))
UPDATER = Path("/opt/automationz-os/updater/automationz-update.sh")

# Your real structure:
# - Most tools: /opt/automationz/<ToolFolder>/app/main.py
# - Exception: /opt/automationz/AutomationZ_Mod_Update_Auto_Deploy/main.py
TOOLS = [
    ("Admin Orchestrator",        AUTOMATIONZ_DIR / "AutomationZ_Admin_Orchestrator" / "app" / "main.py"),
    ("Log Cleanup Scheduler",     AUTOMATIONZ_DIR / "AutomationZ_Log_Cleanup_Scheduler" / "app" / "main.py"),
    ("Mod Update Auto Deploy",    AUTOMATIONZ_DIR / "AutomationZ_Mod_Update_Auto_Deploy" / "main.py"),  # special case
    ("Restart Companion",         AUTOMATIONZ_DIR / "AutomationZ-Restart-Companion" / "app" / "main.py"), 
    ("AutomationZ Scheduler",     AUTOMATIONZ_DIR / "AutomationZ_Scheduler" / "app" / "main.py"),
    ("Server Backup Scheduler",   AUTOMATIONZ_DIR / "AutomationZ_Server_Backup_Scheduler" / "app" / "main.py"),
    ("Server Health",             AUTOMATIONZ_DIR / "AutomationZ_Server_Health" / "app" / "main.py"),
    ("Uploader",                  AUTOMATIONZ_DIR / "AutomationZ_Uploader" / "app" / "main.py"), 
    ("Config Diff",               AUTOMATIONZ_DIR / "AutomationZ-Config-Diff-LOCAL" / "app" / "main.py"),
    ("Restart Loop Guard",        AUTOMATIONZ_DIR / "AutomationZ_Restart_Loop_Guard" / "app" / "main.py"),
]

def run_cmd(cmd: list[str]) -> None:
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        messagebox.showerror("Launch failed", str(e))

def run_python(script_path: Path) -> None:
    if not script_path.exists():
        messagebox.showwarning("Not found", f"Tool entry not found:\n{script_path}")
        return
    run_cmd(["python3", str(script_path)])

def open_folder(path: Path) -> None:
    if not path.exists():
        messagebox.showwarning("Not found", f"Folder not found:\n{path}")
        return
    run_cmd(["xdg-open", str(path)])

def update_now() -> None:
    if not UPDATER.exists():
        messagebox.showerror("Updater missing", f"Updater not found:\n{UPDATER}")
        return
    # GUI password prompt on KDE
    run_cmd(["pkexec", str(UPDATER)])

def open_steam() -> None:
    run_cmd(["steam"])

def open_editor() -> None:
    run_cmd(["codium"])

def open_filezilla() -> None:
    run_cmd(["filezilla"])

def build_ui(root: tk.Tk) -> None:
    root.title("AutomationZ Hub")
    root.geometry("600x520")
    root.minsize(600, 520)

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    title = ttk.Label(frm, text="AutomationZ Hub", font=("Arial", 18, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(frm, text=f"Tools path: {AUTOMATIONZ_DIR}")
    subtitle.pack(anchor="w", pady=(4, 12))

    tools_box = ttk.LabelFrame(frm, text="Tools", padding=12)
    tools_box.pack(fill="x")

    for label, path in TOOLS:
        row = ttk.Frame(tools_box)
        row.pack(fill="x", pady=4)
        ttk.Label(row, text=label).pack(side="left")
        ttk.Button(row, text="Launch", command=lambda p=path: run_python(p)).pack(side="right")

    sys_box = ttk.LabelFrame(frm, text="System", padding=12)
    sys_box.pack(fill="x", pady=(12, 0))

    sys_row1 = ttk.Frame(sys_box)
    sys_row1.pack(fill="x", pady=4)
    ttk.Button(sys_row1, text="Update AutomationZ now", command=update_now).pack(side="left")
    ttk.Button(sys_row1, text="Open AutomationZ folder", command=lambda: open_folder(AUTOMATIONZ_DIR)).pack(side="left", padx=8)

    sys_row2 = ttk.Frame(sys_box)
    sys_row2.pack(fill="x", pady=4)
    ttk.Button(sys_row2, text="Steam", command=open_steam).pack(side="left")
    ttk.Button(sys_row2, text="VSCodium", command=open_editor).pack(side="left", padx=8)
    ttk.Button(sys_row2, text="FileZilla", command=open_filezilla).pack(side="left")

    # Quick sanity check button
    def check_paths():
        missing = [str(p) for _, p in TOOLS if not p.exists()]
        if not missing:
            messagebox.showinfo("OK", "All tool entrypoints found ✅")
        else:
            messagebox.showwarning("Missing", "These entrypoints were not found:\n\n" + "\n".join(missing))

    ttk.Button(frm, text="Check tool paths", command=check_paths).pack(anchor="w", pady=(12, 0))

if __name__ == "__main__":
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
