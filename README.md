# 🚀 YouTube Video Download API (Web Scraping)

**Developer:** @anshapi
**Language:** Python (Flask)
**Deploy:** Vercel (Serverless)

---

## 📌 About This Project

This project is a **YouTube / Video Download API** built using **web scraping logic**.
It does **NOT** directly download videos from YouTube servers. Instead, it:

* Scrapes a third‑party search page
* Extracts **encrypted download URLs**
* Decrypts them using a helper service
* Returns **best video, best audio, and all formats** in clean JSON

⚠️ This project is for **educational purposes only**.

---

## 🔥 Features

* ✅ Serverless Flask API (Vercel ready)
* 🔐 Encrypted URL decryption
* 🎵 Best audio detection
* 🎥 Best video quality detection (by file size)
* 🚫 No‑watermark video detection (if available)
* 🌐 CORS enabled
* 📦 Clean JSON response

---

## 🧠 How It Works (High Level)

```
User URL
   ↓
API Endpoint (/download)
   ↓
Scrape Search Page HTML
   ↓
Extract Encrypted Links (#url=)
   ↓
Decrypt Each Link
   ↓
Filter Audio / Video
   ↓
Pick Best Quality
   ↓
Return JSON Response
```

---

## 📊 Detailed Flowchart

```
┌──────────────┐
│   USER URL   │
└──────┬───────┘
       ↓
┌────────────────────┐
│  /download API     │
└──────┬─────────────┘
       ↓
┌──────────────────────────┐
│ Scrape Search Page HTML  │
│ videofk.com/search       │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ Extract Encrypted Links  │
│ href="#url=XXXX"        │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ Decrypt Encrypted URL    │
│ downloader.twdown.online │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ Audio / Video Detection  │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ HEAD Request (Size)      │
│ Pick Best Quality        │
└──────┬───────────────────┘
       ↓
┌──────────────────────────┐
│ JSON Response to Client  │
└──────────────────────────┘
```

---

## 🧩 API Endpoints

### 🔹 GET `/download?url=VIDEO_URL`

Returns **full media details + direct links**

```json
{
  "success": true,
  "title": "Video Title",
  "video_best": {},
  "audio_best": {},
  "media": []
}
```

---

### 🔹 GET `/info?url=VIDEO_URL`

Returns **only information** (no direct links)

```json
{
  "success": true,
  "title": "Video Title",
  "formats": 5,
  "has_video": true,
  "has_audio": true,
  "qualities": ["360p", "720p"]
}
```

---

## 🗂 Project Structure

```
yt-download-api/
├── api/
│   └── index.py
├── requirements.txt
├── vercel.json
└── README.md
```

---

## 🚀 Deploy on Vercel

1. Upload ZIP to **Vercel Dashboard**
2. Framework: **Other**
3. Build handled automatically
4. Done 🎉

---

## ⚠️ Disclaimer

* This project uses **web scraping**
* External services may change or block requests
* Respect **YouTube Terms of Service**
* Use for **learning & experimentation only**

---

## 👨‍💻 Developer Credit

**Built & Maintained by:**

### 🔥 @anshapi

* Telegram / GitHub / API Projects
* Follow for more **API, Bots & Scraping content**

---

⭐ If this project helped you, give it a star and share!
