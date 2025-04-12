## 📥 TikTok Video Downloader

**TikTok Video Downloader** is a Python automation project that **controls your computer’s mouse in real-time** to mimic human interaction on TikTok’s website. It bypasses bot detection systems that block tools like Selenium by using manual `pyautogui` movements and clipboard access.

This project is ideal for collecting video links in environments where browser automation is restricted or flagged.

---

### ⚙️ Features

- 🖱️ Real cursor movement using `pyautogui`  
- 📋 Link grabbing via `pyperclip`  
- 🔁 Auto-scrolls to the next video  
- 🧩 Centralized screen coordinates managed in `SetUp.py`  
- 📸 Optional Instagram link downloading with `instaloader`  
- 📤 Telegram integration using `telethon`  

---

### 🛠 Requirements

Install the required packages before use:

```bash
pip install pyautogui pyperclip requests instaloader telethon
```

- Python 3.7 or higher recommended  
- Ensure the screen coordinates in `SetUp.py` match your screen layout when TikTok is open in a browser

---

### 🗂 Project Structure

```
├── lib/
│   ├── main.py             # Main automation loop
│   ├── linkgrabber.py      # Grabs and handles links
│   ├── lnkgbrfucntions.py  # Low-level cursor and copy helpers
│   ├── getInfo.py          # Organizes TikTok and Instagram links
│   ├── getTTDict.py        # Parses TikTok cookies/token info
│   ├── sendT.py            # Sends collected links to Telegram
│   ├── download.py         # Downloads video content
│   ├── launcher.py         # Entry point launcher
│   ├── SetUp.py            # Contains coordinate values and setup logic
├── vids/                   # Directory for saved video files
```

---

### 🚀 How to Use

1. **Set your screen coordinates**  
   Open `SetUp.py` and edit the coordinate variables to match your screen setup:
   ```python
   link_box_coords = (x1, y1)  # Coordinates where the link is located
   button_coords = (x2, y2)    # Coordinates for clicking to scroll to the next video
   ```

2. **Install the required packages**  
   Run this in your terminal:
   ```bash
   pip install pyautogui pyperclip requests instaloader telethon
   ```

3. **Open TikTok in your browser**  
   Make sure the TikTok video feed is visible and your browser is in the same position each time.

4. **Run the main script**  
   In your terminal:
   ```bash
   python lib/main.py
   ```

5. **What happens next**
   - The script moves your cursor to the video
   - Copies the link
   - Saves it to a file
   - Scrolls to the next video and repeats

> ⚠️ Do not touch your mouse or keyboard while the script is running. It manually controls your system and may interfere with your input.

---

### ⚠️ Important

- **This script takes over your mouse** — avoid using your computer while it runs.
- Intended for **educational and personal use** only.
- Please **respect platform terms of service**.

---

### 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

### 📄 License

This project is licensed under the [MIT License](LICENSE).
