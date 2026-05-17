"""
GUI Automation Toolkit - TikTok Downloader
Warm, earthy UI inspired by SpiceRack.

Supports: macOS + Windows
Modes:    Single Link | Multi-Link (batch)

Original idea by Daniel Larson, hash coded by Geo on github.
Updated: May 2026
"""

import tkinter as tk
from tkinter import filedialog
import pyautogui
import pyperclip
import time
import platform
import os
import threading

from lnkgbrfucntions import launch_2
from browser_control import get_current_url, click_next_video, set_coords
from download import set_output_dir

# ── OS ────────────────────────────────────────────────────────────────────────
IS_MAC  = platform.system() == "Darwin"
IS_WIN  = platform.system() == "Windows"
OS_NAME = "macOS" if IS_MAC else "Windows" if IS_WIN else platform.system()

# ── SpiceRack-inspired palette ────────────────────────────────────────────────
BG        = "#f5f3ee"
SURFACE   = "#faf9f6"
SURFACE2  = "#ede9e0"
BORDER    = "#d4cfc3"
ACCENT    = "#b83232"
TEXT      = "#1c1a16"
TEXT2     = "#5a5650"
TEXT3     = "#8a857c"
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
download_count_entry = None
single_url_entry     = None
output_dir           = None
log_text             = None
start_btn            = None
url_x_entry          = None
url_y_entry          = None
btn_x_entry          = None
btn_y_entry          = None


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
    global download_count_entry, single_url_entry, current_mode
    global output_dir, log_text, start_btn
    global url_x_entry, url_y_entry, btn_x_entry, btn_y_entry

    root = tk.Tk()
    root.title("TikTok Downloader")
    root.configure(bg=BG)
    root.resizable(False, False)

    # ── Header ────────────────────────────────────────────────────────────────
    hdr = tk.Frame(root, bg=SURFACE, pady=14)
    hdr.pack(fill="x")
    tk.Label(hdr, text="TikTok Downloader", bg=SURFACE, fg=TEXT,
             font=FONT_TITLE).pack(side="left", padx=20)
    tk.Label(hdr, text=OS_NAME, bg=SURFACE, fg=TEXT3,
             font=FONT_SMALL).pack(side="right", padx=20)
    tk.Frame(root, height=2, bg=ACCENT).pack(fill="x")

    # ── Download mode ─────────────────────────────────────────────────────────
    _section_label(root, "DOWNLOAD MODE")
    current_mode = tk.StringVar(value="multi")
    single_panel = tk.Frame(root, bg=BG)
    multi_panel  = tk.Frame(root, bg=BG)

    def show_single():
        multi_panel.pack_forget()
        single_panel.pack(fill="x", padx=20, pady=(4, 0))

    def show_multi():
        single_panel.pack_forget()
        multi_panel.pack(fill="x", padx=20, pady=(4, 0))

    _radio(root, "Single Link — paste one URL and download immediately",
           current_mode, "single", command=show_single)
    _radio(root, "Multi-Link — automatically collects N videos in a row",
           current_mode, "multi",  command=show_multi)

    # Single panel
    tk.Label(single_panel, text="TikTok URL", bg=BG, fg=TEXT3,
             font=FONT_SMALL).pack(anchor="w", pady=(6, 2))
    single_url_entry = _entry(single_panel, width=52)
    single_url_entry.pack(fill="x", ipady=6)

    # Multi panel
    tk.Label(multi_panel, text="Number of videos", bg=BG, fg=TEXT3,
             font=FONT_SMALL).pack(anchor="w", pady=(6, 2))
    download_count_entry = _entry(multi_panel, width=10)
    download_count_entry.pack(anchor="w", ipady=6)
    tk.Label(multi_panel,
             text="Switch to your browser within 10 s after clicking Download.",
             bg=BG, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", pady=(4, 0))

    multi_panel.pack(fill="x", padx=20, pady=(4, 0))

    _divider(root)

    # ── Coordinates ───────────────────────────────────────────────────────────
    _section_label(root, "SCREEN COORDINATES")
    tk.Label(root, text="Run SetUp Resources/x,y.py to find your coordinates.",
             bg=BG, fg=TEXT3, font=FONT_SMALL).pack(anchor="w", padx=20)

    coords_frame = tk.Frame(root, bg=BG)
    coords_frame.pack(fill="x", padx=20, pady=(4, 0))

    tk.Label(coords_frame, text="URL bar  X", bg=BG, fg=TEXT3,
             font=FONT_SMALL).grid(row=0, column=0, padx=(0, 4), pady=3)
    url_x_entry = _entry(coords_frame, width=6)
    url_x_entry.grid(row=0, column=1, padx=(0, 12), ipady=4)

    tk.Label(coords_frame, text="Y", bg=BG, fg=TEXT3,
             font=FONT_SMALL).grid(row=0, column=2, padx=(0, 4))
    url_y_entry = _entry(coords_frame, width=6)
    url_y_entry.grid(row=0, column=3, ipady=4)

    tk.Label(coords_frame, text="Next btn X", bg=BG, fg=TEXT3,
             font=FONT_SMALL).grid(row=1, column=0, padx=(0, 4), pady=3)
    btn_x_entry = _entry(coords_frame, width=6)
    btn_x_entry.grid(row=1, column=1, padx=(0, 12), ipady=4)

    tk.Label(coords_frame, text="Y", bg=BG, fg=TEXT3,
             font=FONT_SMALL).grid(row=1, column=2, padx=(0, 4))
    btn_y_entry = _entry(coords_frame, width=6)
    btn_y_entry.grid(row=1, column=3, ipady=4)

    _divider(root)

    # ── Save location ─────────────────────────────────────────────────────────
    _section_label(root, "SAVE LOCATION")
    output_dir = tk.StringVar(value=_default_output_dir())

    row = tk.Frame(root, bg=BG)
    row.pack(fill="x", padx=20, pady=(0, 4))

    _entry(row, textvariable=output_dir, width=36).pack(
        side="left", ipady=6, fill="x", expand=True)
    tk.Button(
        row, text="Browse", command=_pick_folder,
        bg=SURFACE2, fg=TEXT2,
        activebackground=BORDER, activeforeground=TEXT,
        relief="flat", font=FONT_SMALL, cursor="hand2",
        padx=10, pady=5, bd=0,
        highlightthickness=1, highlightbackground=BORDER,
    ).pack(side="left", padx=(6, 0))

    _divider(root)

    # ── Download button ───────────────────────────────────────────────────────
    start_btn = tk.Button(
        root, text="Download",
        command=start_download,
        bg=ACCENT, fg="white",
        activebackground="#9a2020", activeforeground="white",
        font=("Georgia", 11, "bold"),
        relief="flat", cursor="hand2",
        padx=0, pady=11, bd=0,
    )
    start_btn.pack(fill="x", padx=20, pady=(0, 6))

    # ── Status log ────────────────────────────────────────────────────────────
    _section_label(root, "STATUS LOG")

    log_outer = tk.Frame(root, bg=BORDER, padx=1, pady=1)
    log_outer.pack(fill="both", expand=True, padx=20, pady=(0, 4))

    log_inner = tk.Frame(log_outer, bg=SURFACE)
    log_inner.pack(fill="both", expand=True)

    log_text = tk.Text(
        log_inner, height=8,
        bg=SURFACE, fg=TEXT,
        font=FONT_MONO, relief="flat", bd=8,
        state="disabled", wrap="word",
        insertbackground=TEXT, selectbackground=SURFACE2,
    )
    log_text.pack(side="left", fill="both", expand=True)

    for tag, col in [(TEXT, TEXT), (TEXT3, TEXT3), (SUCCESS, SUCCESS),
                     (WARNING, WARNING), (ERROR_COL, ERROR_COL), (INFO, INFO)]:
        log_text.tag_config(tag, foreground=col)

    sb = tk.Scrollbar(log_inner, command=log_text.yview,
                      bg=SURFACE2, troughcolor=SURFACE2,
                      activebackground=BORDER, relief="flat", bd=0)
    sb.pack(side="right", fill="y")
    log_text.config(yscrollcommand=sb.set)

    # ── Footer ────────────────────────────────────────────────────────────────
    tk.Frame(root, height=1, bg=BORDER).pack(fill="x", pady=(6, 0))
    tk.Label(root, text="For personal use only — respect platform Terms of Service.",
             bg=BG, fg=TEXT3, font=FONT_SMALL).pack(pady=(4, 10))

    log(f"Ready on {OS_NAME}.", INFO)
    log("Configure your settings above and click Download.", TEXT3)

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
            log("Single link mode started.", INFO)
            with open(_data_path(), "w") as f:
                f.write(url + "\n\n")
            log(f"URL: {url}")
            set_output_dir(output_dir.get())
            log("Downloading…")
            launch_2()
            log("Download complete.", SUCCESS)
        except Exception as e:
            log(f"Error: {e}", ERROR_COL)
        finally:
            _set_busy(False)

    threading.Thread(target=job, daemon=True).start()


def _start_multi():
    try:
        n = int(download_count_entry.get().strip())
        if n <= 0:
            raise ValueError
    except ValueError:
        log("Enter a valid positive number.", ERROR_COL)
        return

    def job():
        _set_busy(True)
        try:
            log(f"Collecting {n} link(s).", INFO)
            log("Switch to your TikTok tab now! (10 s…)", WARNING)
            launch_1(n)
            log("Links collected. Downloading…", INFO)
            set_output_dir(output_dir.get())
            launch_2()
            log(f"Done — {n} video(s) saved.", SUCCESS)
        except Exception as e:
            log(f"Error: {e}", ERROR_COL)
        finally:
            _set_busy(False)

    threading.Thread(target=job, daemon=True).start()


# ── Cursor automation ─────────────────────────────────────────────────────────
def launch_1(total: int):
    try:
        ux = int(url_x_entry.get().strip())
        uy = int(url_y_entry.get().strip())
        bx = int(btn_x_entry.get().strip())
        by = int(btn_y_entry.get().strip())
    except ValueError:
        log("Enter valid coordinates before collecting.", ERROR_COL)
        return

    set_coords(ux, uy, bx, by)
    log(f"URL bar ({ux},{uy})  Next btn ({bx},{by})", TEXT3)

    time.sleep(10)
    with open(_data_path(), "w") as f:
        for i in range(total):
            url = get_current_url()
            log(f"  [{i+1}/{total}] {url}")
            f.write(url + "\n\n")
            time.sleep(0.1)
            click_next_video()
            time.sleep(0.4)
    log("Link collection complete.")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    setup_gui()