# file: app.py
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)  # Simple CORS for demo

HEADERS = {"User-Agent": "Mozilla/5.0"}

def json_response(obj, code=200):
    return Response(response=requests.utils.requote_uri(jsonify(obj).get_data(as_text=True)),
                    status=code,
                    mimetype="application/json")

def safe_title_from_html(html):
    t = re.search(r"<title>(.*?)<\/title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not t:
        return "media_download"
    title = t.group(1).replace("\n", " ").replace("\r", " ").strip()
    # remove filesystem-illegal chars
    title = re.sub(r'[\\\/:*?"<>|]', "", title)
    return title

def extract_encrypted_links(html):
    # match href="...#url=ENCODED"
    matches = re.findall(r'href="([^"]*#url=([^"]+))"', html, flags=re.IGNORECASE)
    # returns list of tuples (full_href, encrypted_part)
    return [{"encrypted": m[1], "text": m[0].lower()} for m in matches]

def decrypt_direct_url(encrypted):
    try:
        resp = requests.get("https://downloader.twdown.online/load_url", params={"url": encrypted}, headers=HEADERS, timeout=10)
        final = resp.text.strip()
        if final.startswith("http"):
            return final
    except Exception:
        pass
    return None

def get_content_length(url):
    try:
        h = requests.head(url, headers=HEADERS, timeout=8, allow_redirects=True)
        size = int(h.headers.get("content-length", "0"))
        return size
    except Exception:
        return 0

def process_url(video_url):
    try:
        # 1) fetch search page that contains encrypted links
        r = requests.get("https://www.videofk.com/search", params={"url": video_url}, headers=HEADERS, timeout=12)
        html = r.text

        # 2) title extraction & sanitization
        title = safe_title_from_html(html)

        # 3) find encrypted links like href="...#url=ENCODED"
        encrypted_links = extract_encrypted_links(html)
        if not encrypted_links:
            return {"error": "Download links not found"}

        media_items = []
        best_video = {"size": 0, "url": None, "quality": "unknown"}
        best_audio = {"url": None, "bitrate": "unknown", "title": title}
        no_watermark = None

        for item in encrypted_links:
            encrypted = item["encrypted"]

            # 4) call decrypt endpoint to get final url
            final = decrypt_direct_url(encrypted)
            if not final:
                continue

            is_audio = bool(re.search(r"mp3|m4a|aac|kbps|audio", item["text"], flags=re.IGNORECASE))
            quality = (re.search(r"(\d+p|\d+kbps)", item["text"]) or ["unknown"])[0]

            if is_audio:
                if not best_audio["url"]:
                    best_audio = {"url": final, "bitrate": quality, "title": title}
                media_items.append({"type": "audio", "url": final, "quality": quality})
                continue

            # 5) try HEAD to get size (to pick best video)
            size = get_content_length(final)

            if re.search(r"no watermark|without water", item["text"], flags=re.IGNORECASE):
                no_watermark = {"url": final, "size": size, "quality": quality, "title": title}

            if size > best_video["size"]:
                best_video = {"url": final, "size": size, "quality": quality, "title": title}

            media_items.append({"type": "video", "url": final, "quality": quality, "size": size})

        out = {
            "success": True,
            "title": title,
            "original_url": video_url,
            "formats": len(media_items),
            "media": media_items
        }
        if no_watermark:
            out["video_no_watermark"] = no_watermark
        elif best_video["url"]:
            out["video_best"] = best_video

        if best_audio["url"]:
            out["audio_best"] = best_audio

        return out

    except Exception as e:
        return {"error": "unexpected: " + str(e)}


@app.route("/download")
def download_route():
    link = request.args.get("url")
    if not link:
        return jsonify({"error": "url missing"}), 400
    return jsonify(process_url(link))


@app.route("/info")
def info_route():
    link = request.args.get("url")
    if not link:
        return jsonify({"error": "url missing"}), 400
    r = process_url(link)
    if r.get("error"):
        return jsonify(r), 400
    return jsonify({
        "success": True,
        "title": r["title"],
        "formats": r["formats"],
        "has_video": bool(r.get("video_best") or r.get("video_no_watermark")),
        "has_audio": bool(r.get("audio_best")),
        "qualities": list({v["quality"] for v in r["media"]})
    })


@app.route("/direct/<path:typ>")  # kept same route shape
def direct_route(typ):
    encrypted = request.args.get("url")
    if not encrypted:
        return jsonify({"error": "encrypted url missing"}), 400
    final = decrypt_direct_url(encrypted)
    if not final:
        return jsonify({"error": "decrypt failed"}), 400
    return jsonify({"success": True, "direct_url": final})


@app.route("/")
def root():
    return jsonify({
        "endpoints": {
            "/download?url=": "Full result + links",
            "/info?url=": "Only information",
            "/direct/{type}?url=": "Decrypt encrypted URL"
        }
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
