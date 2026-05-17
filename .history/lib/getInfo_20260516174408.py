import os

def _data_path() -> str:
    return os.path.join(os.path.expanduser("~"), "Documents", "TikTok Downloader", "data.txt")

def getList() -> list:
    with open(_data_path()) as f:
        return [item.strip() for item in f.read().split("\n")]

def getLinkDict() -> dict:
    values = {"tiktok": [], "instagram": []}
    for item in getList():
        if item.startswith("https://www.instagram.com"):
            values["instagram"].append(item)
        elif item.startswith(("https://www.tiktok.com", "https://m.tiktok.com")):
            values["tiktok"].append(item)
    return values