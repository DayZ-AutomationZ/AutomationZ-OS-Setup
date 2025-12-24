#!/usr/bin/env python3
from __future__ import annotations

import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

AUTOMATIONZ_DIR = Path(os.environ.get("AUTOMATIONZ_DIR", "/opt/automationz"))
UPDATER = Path("/opt/automationz-os/updater/automationz-update.sh")

# Try common entrypoints you may have across tools
CANDIDATE_TOOLS = [
    ("AutomationZ (main.py)", AUTOMATIONZ_DIR / "main.py"),
    ("Mod Auto-Deploy",       AUTOMATIONZ_DIR / "mod_auto_deploy" / "main.py"),
    ("Server Health Monitor", AUTOMATIONZ_DIR / "server_health" / "main.py"),
    ("Uploader",              AUTOMATIONZ_DIR / "uploader" / "main.py"),
    ("Config Diff Tool",      AUTOMATIONZ_DIR / "config_diff" / "main.py"),
]

def run_cmd(cmd: list[str]) -> None:
    try:
        subprocess.Popen(cmd)
    except Exception as e:
        messagebox.showerror("Launch failed", str(e))

def run_python(script_path: Path) -> None:
    if not script_path.exists():
        messagebox.showwarning("Not found", f"Tool not found:\n{script_path}")
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
    # pkexec gives a GUI password prompt on KDE instead of terminal sudo
    run_cmd(["pkexec", str(UPDATER)])

def open_steam() -> None:
    run_cmd(["steam"])

def open_editor() -> None:
    run_cmd(["codium"])

def open_filezilla() -> None:
    run_cmd(["filezilla"])

def build_ui(root: tk.Tk) -> None:
    root.title("AutomationZ Hub")
    root.geometry("560x460")
    root.minsize(560, 460)

    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)

    title = ttk.Label(frm, text="AutomationZ Hub", font=("Arial", 18, "bold"))
    title.pack(anchor="w")

    subtitle = ttk.Label(frm, text=f"AutomationZ path: {AUTOMATIONZ_DIR}")
    subtitle.pack(anchor="w", pady=(4, 12))

    tools_box = ttk.LabelFrame(frm, text="Tools", padding=12)
    tools_box.pack(fill="x")

    for label, path in CANDIDATE_TOOLS:
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

    footer = ttk.Label(frm, text="Tip: put tools in /opt/automationz/<tool>/main.py for auto-detection.")
    footer.pack(anchor="w", pady=(14, 0))

if __name__ == "__main__":
    root = tk.Tk()
    build_ui(root)
    root.mainloop()
