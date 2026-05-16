"""
GUI Automation Toolkit - TikTok Downloader
Dark, polished native UI. App never closes on its own.

Supports: macOS + Windows
Modes:    Single Link | Multi-Link (batch)
Coord:    Smart (DOM-based) | Manual (pixel coords from SetUp.py)

Original idea by Daniel Larson, hash coded by Geo on github.
Updated: May 2026
"""

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
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
IS_MAC = platform.system() == "Darwin"
IS_WIN = platform.system() == "Windows"
OS_NAME = "macOS" if IS_MAC else "Windows" if IS_WIN else platform.system()

# ── Color palette ─────────────────────────────────────────────────────────────
BG          = "#0f0f0f"
SURFACE     = "#1a1a1a"
SURFACE2    = "#242424"
BORDER      = "#2e2e2e"
TIKTOK_RED  = "#fe2c55"
TIKTOK_CYAN = "#25f4ee"
TEXT        = "#f1f1f1"
TEXT_DIM    = "#888888"
TEXT_MUTED  = "#444444"
SUCCESS     = "#4ade80"
WARNING     = "#facc15"
ERROR_COL   = "#f87171"

FONT_TITLE  = ("SF Pro Display", 15, "bold") if IS_MAC else ("Segoe UI", 13, "bold")
FONT_BODY   = ("SF Pro Text",    10)         if IS_MAC else ("Segoe UI",  10)
FONT_SMALL  = ("SF Pro Text",     9)         if IS_MAC else ("Segoe UI",   9)
FONT_MONO   = ("SF Mono",         9)         if IS_MAC else ("Consolas",   9)

# ── Globals ───────────────────────────────────────────────────────────────────
current_mode         = None
control_mode         = None
download_count_entry = None
single_url_entry     = None
output_dir           = None
log_text             = None
start_btn            = None
root_ref             = None


# ── Helpers ───────────────────────────────────────────────────────────────────
def log(msg: str, color: str = TEXT):
    if log_text is None:
        return
    ts = time.strftime("%H:%M:%S")
    log_text.config(state="normal")
    log_text.insert("end", f"[{ts}] ", TEXT_MUTED)
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
        log(f"Output folder set: {folder}", TIKTOK_CYAN)


def _set_busy(busy: bool):
    if start_btn:
        start_btn.config(
            state="disabled" if busy else "normal",
            text="⏳  Running…" if busy else "▶   Start Download",
            bg=BORDER if busy else TIKTOK_RED,
        )


def _sep(parent):
    tk.Frame(parent, height=1, bg=BORDER).pack(fill="x", padx=0, pady=6)


def _section(parent, label: str):
    f = tk.Frame(parent, bg=BG)
    f.pack(fill="x", padx=20, pady=(10, 4))
    tk.Label(f, text=label.upper(), bg=BG, fg=TEXT_MUTED,
             font=FONT_SMALL).pack(side="left")


def _radio(parent, text, var, value, command=None):
    f = tk.Frame(parent, bg=SURFACE2, cursor="hand2")
    f.pack(fill="x", padx=20, pady=2)
    tk.Radiobutton(
        f, text=text, variable=var, value=value,
        bg=SURFACE2, fg=TEXT, selectcolor=SURFACE2,
        activebackground=SURFACE2, activeforeground=TIKTOK_CYAN,
        font=FONT_BODY, bd=0, highlightthickness=0,
        command=command,
    ).pack(anchor="w", padx=12, pady=8)
    return f


# ── GUI ───────────────────────────────────────────────────────────────────────
def setup_gui():
    global download_count_entry, single_url_entry, current_mode, control_mode
    global output_dir, log_text, start_btn, root_ref

    root = tk.Tk()
    root_ref = root
    root.title("TikTok Downloader")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ── Header ────────────────────────────────────────────────────────────────
    header = tk.Frame(root, bg=BG)
    header.pack(fill="x", padx=20, pady=(18, 4))
    tk.Label(header, text="TikTok", bg=BG, fg=TIKTOK_RED,
             font=FONT_TITLE).pack(side="left")
    tk.Label(header, text=" Downloader", bg=BG, fg=TEXT,
             font=FONT_TITLE).pack(side="left")
    tk.Label(header, text=f"  {OS_NAME}", bg=BG, fg=TEXT_MUTED,
             font=FONT_SMALL).pack(side="left", pady=(4, 0))

    _sep(root)

    # ── Browser control ───────────────────────────────────────────────────────
    _section(root, "Browser Control")
    control_mode = tk.StringVar(value="smart")
    _radio(root, "🧠  Smart  — auto-finds URL + next button (recommended)",
           control_mode, "smart")
    _radio(root, "📐  Manual — use pixel coords from SetUp.py",
           control_mode, "manual")
    tk.Label(root, text="  Smart works on any screen size, no coordinate setup needed.",
             bg=BG, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", padx=20)

    _sep(root)

    # ── Download mode ─────────────────────────────────────────────────────────
    _section(root, "Download Mode")
    current_mode = tk.StringVar(value="multi")

    single_panel = tk.Frame(root, bg=BG)
    multi_panel  = tk.Frame(root, bg=BG)

    def show_single():
        multi_panel.pack_forget()
        single_panel.pack(fill="x", padx=20, pady=(4, 0))

    def show_multi():
        single_panel.pack_forget()
        multi_panel.pack(fill="x", padx=20, pady=(4, 0))

    _radio(root, "Single Link  — paste one URL and download immediately",
           current_mode, "single", command=show_single)
    _radio(root, "Multi-Link   — cursor automation collects N videos in a row",
           current_mode, "multi",  command=show_multi)

    # Single panel
    tk.Label(single_panel, text="TikTok URL", bg=BG, fg=TEXT_DIM,
             font=FONT_SMALL).pack(anchor="w", pady=(6, 2))
    single_url_entry = tk.Entry(
        single_panel, width=52, bg=SURFACE2, fg=TEXT,
        insertbackground=TEXT, relief="flat", font=FONT_BODY,
        bd=0, highlightthickness=1,
        highlightbackground=BORDER, highlightcolor=TIKTOK_CYAN,
    )
    single_url_entry.pack(fill="x", ipady=7)

    # Multi panel
    tk.Label(multi_panel, text="Number of videos to collect", bg=BG, fg=TEXT_DIM,
             font=FONT_SMALL).pack(anchor="w", pady=(6, 2))
    download_count_entry = tk.Entry(
        multi_panel, width=10, bg=SURFACE2, fg=TEXT,
        insertbackground=TEXT, relief="flat", font=FONT_BODY,
        bd=0, highlightthickness=1,
        highlightbackground=BORDER, highlightcolor=TIKTOK_CYAN,
    )
    download_count_entry.pack(anchor="w", ipady=7)
    tk.Label(multi_panel,
             text="Switch to your browser within 10 s after clicking Start.",
             bg=BG, fg=TEXT_MUTED, font=FONT_SMALL).pack(anchor="w", pady=(4, 0))

    multi_panel.pack(fill="x", padx=20, pady=(4, 0))

    _sep(root)

    # ── Save location ─────────────────────────────────────────────────────────
    _section(root, "Save Location")
    output_dir = tk.StringVar(value=_default_output_dir())

    folder_row = tk.Frame(root, bg=BG)
    folder_row.pack(fill="x", padx=20, pady=(0, 4))

    tk.Entry(
        folder_row, textvariable=output_dir, width=38,
        bg=SURFACE2, fg=TEXT, insertbackground=TEXT,
        relief="flat", font=FONT_BODY, bd=0,
        highlightthickness=1, highlightbackground=BORDER,
        highlightcolor=TIKTOK_CYAN,
    ).pack(side="left", ipady=7, fill="x", expand=True)

    tk.Button(
        folder_row, text="Browse", command=_pick_folder,
        bg=SURFACE2, fg=TEXT_DIM,
        activebackground=SURFACE, activeforeground=TEXT,
        relief="flat", font=FONT_SMALL, cursor="hand2",
        padx=10, pady=6, bd=0,
        highlightthickness=1, highlightbackground=BORDER,
    ).pack(side="left", padx=(6, 0))

    _sep(root)

    # ── Start button ──────────────────────────────────────────────────────────
    start_btn = tk.Button(
        root, text="▶   Start Download",
        command=start_download,
        bg=TIKTOK_RED, fg="white",
        activebackground="#e0203f", activeforeground="white",
        font=("SF Pro Display", 12, "bold") if IS_MAC else ("Segoe UI", 11, "bold"),
        relief="flat", cursor="hand2",
        padx=0, pady=12, bd=0,
    )
    start_btn.pack(fill="x", padx=20, pady=(0, 6))

    # ── Status log ────────────────────────────────────────────────────────────
    _section(root, "Status Log")

    log_frame = tk.Frame(root, bg=SURFACE, highlightthickness=1,
                         highlightbackground=BORDER)
    log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    log_text = tk.Text(
        log_frame, height=9, bg=SURFACE, fg=TEXT,
        font=FONT_MONO, relief="flat", bd=8,
        state="disabled", wrap="word",
        insertbackground=TEXT, selectbackground=SURFACE2,
    )
    log_text.pack(side="left", fill="both", expand=True)

    log_text.tag_config(TEXT,        foreground=TEXT)
    log_text.tag_config(TEXT_MUTED,  foreground=TEXT_MUTED)
    log_text.tag_config(TIKTOK_CYAN, foreground=TIKTOK_CYAN)
    log_text.tag_config(SUCCESS,     foreground=SUCCESS)
    log_text.tag_config(WARNING,     foreground=WARNING)
    log_text.tag_config(ERROR_COL,   foreground=ERROR_COL)

    sb = tk.Scrollbar(log_frame, command=log_text.yview,
                      bg=SURFACE, troughcolor=SURFACE,
                      activebackground=BORDER, relief="flat", bd=0)
    sb.pack(side="right", fill="y")
    log_text.config(yscrollcommand=sb.set)

    # ── Footer ────────────────────────────────────────────────────────────────
    tk.Label(root, text="For personal use only. Respect platform ToS.",
             bg=BG, fg=TEXT_MUTED, font=FONT_SMALL).pack(pady=(0, 10))

    log(f"App started on {OS_NAME}", TIKTOK_CYAN)
    log("Ready. Configure your settings and click Start.", TEXT_DIM)

    root.mainloop()


# ── Download entry point ──────────────────────────────────────────────────────
def start_download():
    if current_mode.get() == "single":
        _start_single()
    else:
        _start_multi()


def _start_single():
    url = single_url_entry.get().strip()
    if not url:
        log("No URL entered.", ERROR_COL)
        return
    if not (url.startswith("https://www.tiktok.com") or
            url.startswith("https://m.tiktok.com")):
        log("Invalid URL — must start with https://www.tiktok.com", ERROR_COL)
        return

    def job():
        _set_busy(True)
        try:
            log("Single link mode started…", TIKTOK_CYAN)
            with open(_data_path(), "w") as f:
                f.write(url + "\n\n")
            log(f"URL saved: {url}")
            set_output_dir(output_dir.get())
            log("Downloading…")
            launch_2()
            log("✓ Download complete!", SUCCESS)
        except Exception as e:
            log(f"Error: {e}", ERROR_COL)
        finally:
            _set_busy(False)

    threading.Thread(target=job, daemon=True).start()


def _start_multi():
    try:
        n = int(download_count_entry.get())
        if n <= 0:
            raise ValueError
    except ValueError:
        log("Enter a valid positive number.", ERROR_COL)
        return

    use_smart  = control_mode.get() == "smart"
    mode_label = "Smart (DOM)" if use_smart else "Manual (coords)"

    def job():
        _set_busy(True)
        try:
            log(f"Collecting {n} link(s) — {mode_label}", TIKTOK_CYAN)
            log("Switch to your TikTok tab now! (10 s countdown…)", WARNING)
            launch_1(n, smart=use_smart)
            log("Links collected. Downloading…", TIKTOK_CYAN)
            set_output_dir(output_dir.get())
            launch_2()
            log(f"✓ {n} video(s) downloaded!", SUCCESS)
        except Exception as e:
            log(f"Error: {e}", ERROR_COL)
        finally:
            _set_busy(False)

    threading.Thread(target=job, daemon=True).start()


# ── Cursor automation ─────────────────────────────────────────────────────────
def launch_1(total: int, smart: bool = True):
    time.sleep(10)
    with open(_data_path(), "w") as f:
        for i in range(total):
            if smart:
                url = get_current_url()
                log(f"  [{i+1}/{total}] {url}")
                f.write(url + "\n\n")
                time.sleep(0.1)
                click_next_video(use_js=True, fallback_scroll=True)
                time.sleep(0.4)
            else:
                pyautogui.moveTo(url_cords)
                highlight_link()
                copy()
                time.sleep(0.1)
                f.write(pyperclip.paste() + "\n\n")
                time.sleep(0.05)
                pyautogui.moveTo(button_cords)
                click()
    log("Link collection complete.")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_gui()