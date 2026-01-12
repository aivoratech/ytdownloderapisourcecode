from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def safe_title_from_html(html):
    t = re.search(r"<title>(.*?)<\/title>", html, re.I | re.S)
    if not t:
        return "media_download"
    title = t.group(1).replace("\n", " ").replace("\r", " ").strip()
    return re.sub(r'[\\\/:*?"<>|]', "", title)

def extract_encrypted_links(html):
    matches = re.findall(r'href="([^"]*#url=([^"]+))"', html, re.I)
    return [{"encrypted": m[1], "text": m[0].lower()} for m in matches]

def decrypt_direct_url(encrypted):
    try:
        r = requests.get(
            "https://downloader.twdown.online/load_url",
            params={"url": encrypted},
            headers=HEADERS,
            timeout=10
        )
        res = r.text.strip()
        if res.startswith("http"):
            return res
    except:
        pass
    return None

def get_content_length(url):
    try:
        h = requests.head(url, headers=HEADERS, allow_redirects=True, timeout=8)
        return int(h.headers.get("content-length", "0"))
    except:
        return 0

def process_url(video_url):
    r = requests.get(
        "https://www.videofk.com/search",
        params={"url": video_url},
        headers=HEADERS,
        timeout=12
    )
    html = r.text

    title = safe_title_from_html(html)
    encrypted_links = extract_encrypted_links(html)

    if not encrypted_links:
        return {"error": "Download links not found"}

    media = []
    best_video = {"size": 0}
    best_audio = None
    no_watermark = None

    for item in encrypted_links:
        final = decrypt_direct_url(item["encrypted"])
        if not final:
            continue

        is_audio = re.search(r"mp3|m4a|aac|kbps|audio", item["text"])
        quality = (re.search(r"(\d+p|\d+kbps)", item["text"]) or ["unknown"])[0]

        if is_audio:
            best_audio = best_audio or {
                "url": final,
                "bitrate": quality,
                "title": title
            }
            media.append({"type": "audio", "url": final, "quality": quality})
            continue

        size = get_content_length(final)

        if re.search(r"no watermark|without water", item["text"], re.I):
            no_watermark = {
                "url": final,
                "size": size,
                "quality": quality,
                "title": title
            }

        if size > best_video.get("size", 0):
            best_video = {
                "url": final,
                "size": size,
                "quality": quality,
                "title": title
            }

        media.append({
            "type": "video",
            "url": final,
            "quality": quality,
            "size": size
        })

    out = {
        "success": True,
        "title": title,
        "original_url": video_url,
        "formats": len(media),
        "media": media
    }

    if no_watermark:
        out["video_no_watermark"] = no_watermark
    else:
        out["video_best"] = best_video

    if best_audio:
        out["audio_best"] = best_audio

    return out

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url missing"}), 400
    return jsonify(process_url(url))

@app.route("/info")
def info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url missing"}), 400
    r = process_url(url)
    if "error" in r:
        return jsonify(r), 400
    return jsonify({
        "success": True,
        "title": r["title"],
        "formats": r["formats"],
        "has_video": "video_best" in r or "video_no_watermark" in r,
        "has_audio": "audio_best" in r,
        "qualities": list({v["quality"] for v in r["media"]})
    })

@app.route("/")
def home():
    return jsonify({
        "endpoints": {
            "/download?url=": "Full data",
            "/info?url=": "Only info"
        }
    })
