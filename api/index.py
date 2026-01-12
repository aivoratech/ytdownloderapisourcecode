from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

# STEP 1: ANALYZE VIDEO
def analyze(url):
    r = requests.post(
        "https://www.y2mate.com/mates/en68/analyze/ajax",
        data={"url": url, "q_auto": 0},
        headers=HEADERS,
        timeout=15
    )
    return r.json()

# STEP 2: CONVERT FORMAT
def convert(vid, k):
    r = requests.post(
        "https://www.y2mate.com/mates/en68/convert",
        data={"vid": vid, "k": k},
        headers=HEADERS,
        timeout=15
    )
    return r.json()

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "url missing"}), 400

    data = analyze(url)
    if not data.get("status"):
        return jsonify({"error": "analyze failed"}), 500

    title = re.sub(r'[\\/:*?"<>|]', '', data.get("title", "video"))
    links = []

    # videos
    for q, v in data.get("links", {}).get("mp4", {}).items():
        res = convert(data["vid"], v["k"])
        if res.get("status"):
            links.append({
                "type": "video",
                "quality": q,
                "url": res["dlink"]
            })

    # audios
    for q, v in data.get("links", {}).get("mp3", {}).items():
        res = convert(data["vid"], v["k"])
        if res.get("status"):
            links.append({
                "type": "audio",
                "quality": q,
                "url": res["dlink"]
            })

    return jsonify({
        "success": True,
        "title": title,
        "formats": len(links),
        "media": links,
        "developer": "@anshapi"
    })

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "developer": "@anshapi",
        "endpoint": "/download?url="
    })
