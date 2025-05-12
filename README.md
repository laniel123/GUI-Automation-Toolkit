## GUI Automation Toolkit

**GUI Automation Toolkit** is a Python-based automation tool that uses GUI scripting to simulate user interaction on TikTok’s website. By leveraging `pyautogui` and `pyperclip`, it mimics real-time mouse movements and clipboard access to collect video links — useful in environments where traditional browser automation tools may be limited.

> ⚠️ This project is intended for **educational and personal use only**. Please ensure your usage complies with TikTok’s Terms of Service.

---

### Features

- Real cursor movement using `pyautogui`  
- Link grabbing via `pyperclip`  
- Auto scrolls to the next video  
- Centralized screen coordinates managed in `SetUp.py`  
- Telegram integration using `telethon`  

---

### Requirements

Install the required packages before use:

```bash
pip install pyautogui pyperclip requests instaloader telethon
```

- Python 3.7 or higher recommended  
- Ensure the screen coordinates in `SetUp.py` match your screen layout when TikTok is open in a browser

---

## Project Structure

```
- `lib/main.py` – Main automation loop that coordinates link collection and video handling  
- `lib/linkgrabber.py` – Extracts video links from the interface using clipboard logic  
- `lib/lnkgbrfunctions.py` – Low-level helpers for cursor movement and copy automation  
- `lib/getInfo.py` – Formats and organizes TikTok/Instagram links into usable structures  
- `lib/getTTDict.py` – Parses TikTok cookie and token information for deeper scraping  
- `lib/sendT.py` – Sends collected links to a Telegram bot via API  
- `lib/download.py` – Downloads video content from extracted links  
- `lib/launcher.py` – Script launcher that initializes the workflow  
- `lib/SetUp.py` – Defines screen coordinates and setup logic for PyAutoGUI  
- `vids/` – Directory that stores downloaded or copied video files
```

---

### How to Use

1. **Set your screen coordinates**  
   Open `SetUp.py` and edit the coordinate variables to match your screen setup:
   ```python
   url_cords = (x1, y1)  # Coordinates where the link is located
   button_cords = (x2, y2)    # Coordinates for clicking to scroll to the next video
   ```
   Screen coordinate fetcher available in the SetUp Resources.py file.

2. **Install the required packages**  
   Run this in your terminal:
   ```bash
   pip install pyautogui pyperclip requests instaloader telethon
   ```

3. **Open TikTok in your browser**  
   Make sure the TikTok video feed is visible and that your browser is in the same position each time.

4. **Run the main.py script**  
 
5. **What happens next**
   - The script moves your cursor to the video
   - Copies the link
   - Saves it to the vids file
   - Scrolls to the next video and repeats

>  Do not touch your mouse or keyboard while the script is running. It manually controls your system and may interfere with your input.

---

###  Demo

[![Watch the demo](https://img.youtube.com/vi/KPzgZS0lX2U/0.jpg)](https://youtu.be/KPzgZS0lX2U)
---

###  Important

- **This script takes over your mouse**. Avoid using your computer while it runs.
- Intended for **educational and personal use** only.
- Please **respect platform terms of service**.

---

### License

This project is licensed under the [MIT License](LICENSE).
