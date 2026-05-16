"""
download.py — Video download logic for TikTok and Instagram.
Cross-platform: resolves data.txt and vids/ using absolute paths.
"""

import requests
import os
import instaloader
from getTTDict import getDict
from getInfo import getLinkDict

# ── Path helpers ──────────────────────────────────────────────────────────────
def _project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_custom_output_dir = None

def set_output_dir(path: str):
    global _custom_output_dir
    _custom_output_dir = path
    os.makedirs(path, exist_ok=True)

def _vids_dir() -> str:
    if _custom_output_dir:
        return _custom_output_dir
    path = os.path.join(_project_root(), "vids")
    os.makedirs(path, exist_ok=True)
    return path


# ── TikTok download ───────────────────────────────────────────────────────────
def createHeader(parseDict: dict):
    cookies = {"PHPSESSID": parseDict.get("PHPSESSID", "")}
    headers = {
        "authority": "ttdownloader.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://ttdownloader.com",
        "referer": "https://ttdownloader.com/",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/108.0.0.0 Safari/537.36"
        ),
        "x-requested-with": "XMLHttpRequest",
    }
    data = {"url": "", "format": "", "token": parseDict.get("token", "")}
    return cookies, headers, data


def TDL(cookies, headers, data, name: str) -> None:
    response = requests.post(
        "https://ttdownloader.com/search/",
        cookies=cookies, headers=headers, data=data
    )
    link_parse = [i for i in str(response.text).split() if i.startswith("href=")][0]
    video_response = requests.get(link_parse[6:-10])
    out_path = os.path.join(_vids_dir(), f"tiktok_{name}.mp4")
    with open(out_path, "wb") as f:
        f.write(video_response.content)
    print(f"  Saved: {out_path}")


def TDLALL() -> None:
    parse_dict = getDict()
    cookies, headers, data = createHeader(parse_dict)
    link_list = getLinkDict()["tiktok"]
    for i, link in enumerate(link_list):
        try:
            data["url"] = link
            TDL(cookies, headers, data, str(i))
        except IndexError:
            parse_dict = getDict()
            cookies, headers, data = createHeader(parse_dict)
        except Exception as err:
            print(f"TikTok download error: {err}")
            raise


# ── Instagram download ────────────────────────────────────────────────────────
def IDL(url: str, name: str) -> None:
    obj = instaloader.Instaloader()
    shortcode = url.split("p/")[1].strip("/ ")
    post = instaloader.Post.from_shortcode(obj.context, shortcode)
    out_path = None
    if post.video_url:
        response = requests.get(post.video_url)
        out_path = os.path.join(_vids_dir(), f"insta_{name}.mp4")
        with open(out_path, "wb") as f:
            f.write(response.content)
    elif post.url:
        response = requests.get(post.url)
        out_path = os.path.join(_vids_dir(), f"insta_{name}.jpg")
        with open(out_path, "wb") as f:
            f.write(response.content)
    if out_path:
        print(f"  Saved: {out_path}")


def IDLALL() -> None:
    link_list = getLinkDict()["instagram"]
    for i, link in enumerate(link_list):
        try:
            IDL(link, str(i))
        except Exception as err:
            print(f"Instagram download error: {err}")
            raise


if __name__ == "__main__":
    pass