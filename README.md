# 🚀 Video Downloader API (Web Scraping)

**Developer:** @anshapi
**Platform:** Render (Python Web Service)
**Tech:** Flask + Requests (Pure Web Scraping)

---

## 📌 Project Overview

This API extracts **video & audio download links** using **web scraping only** (no yt-dlp, no binaries).

It works by:

* Scraping a third‑party search page
* Extracting **encrypted URLs** from HTML
* Decrypting them via helper endpoint
* Returning **best video, best audio & all formats** in JSON

⚠️ Educational purpose only.

---

## ✨ Features

* ✅ Pure web scraping (requests + regex)
* ✅ Best video selection (by size)
* ✅ Best audio selection
* ✅ No-watermark detection (if available)
* ✅ Render deployable (long‑running service)
* ✅ CORS enabled

---

## 🔁 Flowchart (How It Works)

```
User Video URL
      ↓
/download endpoint
      ↓
Fetch Search Page HTML
      ↓
Extract Encrypted Links (#url=)
      ↓
Decrypt Each Link
      ↓
Audio / Video Filter
      ↓
HEAD request → file size
      ↓
Pick Best Quality
      ↓
Return JSON Response
```

---

## 🔗 API Endpoints

### 🔹 GET `/download?url=VIDEO_URL`

Returns full data + direct links

### 🔹 GET `/info?url=VIDEO_URL`

Returns only metadata (no direct URLs)

### 🔹 GET `/direct/{type}?url=ENCRYPTED`

Decrypt a single encrypted URL

---

## 📂 Project Structure

```
project/
├── app.py
├── requirements.txt
├── Procfile
└── README.md
```

---

## 🚀 Deploy on Render (Step‑by‑Step)

1. Push this project to **GitHub**
2. Go to **Render → New Web Service**
3. Select your GitHub repo
4. Environment: **Python**
5. Build Command:

```
pip install -r requirements.txt
```

6. Start Command:

```
gunicorn app:app
```

7. Deploy 🎉

---

## ⚠️ Notes & Limitations

* Web scraping sites may change HTML anytime
* Some links may expire
* Respect platform Terms of Service

---

## 👨‍💻 Developer Credit

**Built & Maintained by:**

### 🔥 @anshapi

APIs • Bots • Scraping • Automation

---

⭐ If you like this project, share & follow @anshapi
