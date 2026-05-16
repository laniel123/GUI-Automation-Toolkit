"""
GUI Automation Toolkit - TikTok Downloader
Warm, earthy UI inspired by SpiceRack.

Supports: macOS + Windows
Modes:    Single Link | Multi-Link (batch)
Coord:    Smart (DOM-based) | Manual (pixel coords from SetUp.py)

Original idea by Daniel Larson, hash coded by Geo on github.
Updated: May 2026
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import pyautogui
import pyperclip
import time
import platform
import os
import threading

from lnkgbrfucntions import click, highlight_link, copy, launch_2
from browser_control import get_current_url, click_next_video
from SetUp import url_cords, button_cords
from download import set_output_dir

# ── OS ────────────────────────────────────────────────────────────────────────
IS_MAC  = platform.system() == "Darwin"
IS_WIN  = platform.system() == "Windows"
OS_NAME = "macOS" if IS_MAC else "Windows" if IS_WIN else platform.system()

# ── SpiceRack-inspired palette ────────────────────────────────────────────────
BG        = "#f5f3ee"   # warm parchment
SURFACE   = "#faf9f6"   # card white
SURFACE2  = "#ede9e0"   # slightly deeper card
BORDER    = "#d4cfc3"   # warm grey border
ACCENT    = "#b83232"   # SpiceRack red
ACCENT2   = "#2d6e4a"   # SpiceRack green
TEXT      = "#1c1a16"   # near-black warm
TEXT2     = "#5a5650"   # medium warm grey
TEXT3     = "#8a857c"   # muted warm grey
SUCCESS   = "#2d6e4a"
WARNING   = "#9a6000"
ERROR_COL = "#b83232"
INFO      = "#1a4e8a"

FONT_TITLE = ("Georgia", 14, "bold")
FONT_BODY  = ("Helvetica", 10) if IS_WIN else ("Helvetica Neue", 10)
FONT_SMALL = ("Helvetica", 9)  if IS_WIN else ("Helvetica Neue", 9)
FONT_MONO  = ("Courier New", 9)

# ── Globals ───────────────────────────────────────────────────────────────────
current_mode         = None
control_mode         = None
download_count_entry = None
single_url_entry     = None
output_dir           = None
log_text             = None
start_btn            = None


# ── Helpers ───────────────────────────────────────────────────────────────────
def log(msg: str, color: str = TEXT):
    if log_text is None:
        return
    ts = time.strftime("%H:%M:%S")
    log_text.config(state="normal")
    log_text.insert("end", f"[{ts}] ", TEXT3)
    log_text.insert("end", msg + "\n", color)
    log_text.see("end")
    log_text.config(state="disabled")


def _data_path() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data.txt")


def _default_output_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "vids")


def _pick_folder():
    folder = filedialog.askdirectory(title="Choose download folder")
    if folder:
        output_dir.set(folder)
        log(f"Save location: {folder}", INFO)


def _set_busy(busy: bool):
    if start_btn:
        start_btn.config(
            state="disabled" if busy else "normal",
            text="Running…" if busy else "Download",
            bg=BORDER if busy else ACCENT,
            fg=TEXT2 if busy else "white",
        )


def _divider(parent):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", pady=8)


def _section_label(parent, text):
    tk.Label(parent, text=text, bg=BG, fg=TEXT3,
             font=("Helvetica", 8, "bold") if IS_WIN else ("Helvetica Neue", 8, "bold")
             ).pack(anchor="w", padx=20, pady=(10, 3))


def _entry(parent, textvariable=None, width=40, **kwargs):
    return tk.Entry(
        parent,
        textvariable=textvariable,
        width=width,
        bg=SURFACE,
        fg=TEXT,
        insertbackground=TEXT,
        relief="flat",
        font=FONT_BODY,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        **kwargs,
    )


def _radio(parent, text, var, value, command=None):
    f = tk.Frame(parent, bg=SURFACE2, cursor="hand2")
    f.pack(fill="x", padx=20, pady=2)
    tk.Radiobutton(
        f, text=text, variable=var, value=value,
        bg=SURFACE2, fg=TEXT, selectcolor=SURFACE2,
        activebackground=SURFACE2, activeforeground=ACCENT,
        font=FONT_BODY, bd=0, highlightthickness=0,
        command=command,
    ).pack(anchor="w", padx=12, pady=8)
    return f


# ── GUI ───────────────────────────────────────────────────────────────────────
def setup_gui():
    global download_count_entry, single_url_entry, current_mode, control_mode
    global output_dir, log_text, start_btn

    root = tk.Tk()
    root.title("TikTok Downloader")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ── Header ────────────────────────────────────────────────────────────────
    hdr = tk.F