# REMO_OX Downloader Web (v0.1) 🌐⚡

A modern, responsive, and high-performance web application designed to download videos and audio in high quality from popular social media platforms (**Instagram, TikTok, Facebook, Twitter/X, Pinterest, Vimeo, and 1000+ sites**).

Built using **Python**, **Streamlit**, and **yt-dlp**, and engineered to run seamlessly across all devices: **Mobile Phones (iPhone via Safari, Android via Chrome)** and **Desktops (Mac, Windows, Linux)**.

---

## 🌟 Key Features (v0.1)

1. **Cross-Platform & Mobile-First:**
   * Runs directly inside any modern web browser without requiring software installation on mobile devices.
   * Responsive layout optimized for smartphones, tablets, and desktops.

2. **Mobile Home Screen App Shortcut (PWA):**
   * Users can easily add the app as a standalone icon on their **iPhone (Safari)** or **Android (Chrome)** home screens.
   * Launches in full-screen standalone mode without browser bars, providing a native app experience.

3. **100% Cloud-Optimized Platforms:**
   * Fast, reliable video and audio extraction from:
     * 🟣 **Instagram (Reels, Stories & Posts)**
     * ⚫ **TikTok (Watermark-free HD)**
     * 🔵 **Facebook (Videos & Reels)**
     * ⚪ **Twitter / X**
     * 🔴 **Pinterest**
     * 🌐 **1000+ Online Media Platforms**

4. **Smart YouTube Handling:**
   * Because YouTube restricts downloads originating from datacenter/cloud hosting server IPs (AWS), the web app detects YouTube links and provides an immediate one-click direct download button for the free, restriction-free Windows Desktop App:  
     `REMO_OX_Downloader_v2.exe`

5. **Clean & Private Interface:**
   * Streamlit headers, GitHub fork buttons, and repository links are completely hidden.
   * Server management widgets and log access are hidden from public visitors, ensuring privacy and security.

6. **Direct Device Download:**
   * Once processing finishes, a direct download button allows instant saving to **Files / Photos** on iOS, and the **Downloads** directory on Android, Windows, and Mac.

7. **Bilingual Support (Arabic & English):**
   * Real-time language switching with full Right-to-Left (RTL) layout support for Arabic and Left-to-Right (LTR) for English.

8. **Format & Resolution Control:**
   * Download high-definition video (MP4) or extract pure audio (MP3 192kbps).

9. **Automatic Server Maintenance:**
   * Background temp file cleaner automatically purges processed files to preserve disk space and ensure privacy.

---

## 🏗️ Architecture & OOP Design

The project is structured according to **Object-Oriented Programming (OOP)** principles:

```text
Remo_ox_downloader_web_app/
│
├── app.py                      # Main Application Controller (RemoOxWebApp)
├── requirements.txt            # Python dependencies (streamlit, yt-dlp, requests)
├── packages.txt                # Linux system dependencies (ffmpeg)
├── README.md                   # Official GitHub repository documentation (English)
│
├── .streamlit/
│   └── config.toml             # Dark theme styling, server settings, and UI customization
│
└── core/
    ├── __init__.py
    ├── config.py               # Application configurations and path management (AppConfig)
    ├── downloader.py           # Core media extraction and conversion engine (MediaDownloader)
    ├── translations.py         # Bilingual localization and direction manager (TranslationManager)
    └── cleaner.py              # Server temporary file garbage collection (TempCleaner)
```

### Module Responsibilities:
* **`RemoOxWebApp` (`app.py`):** Central controller managing app lifecycle, session state (`st.session_state`), UI rendering, event handling, and PWA setup.
* **`MediaDownloader` (`core/downloader.py`):** Interfaces with `yt-dlp` and `FFmpeg` for media extraction, format handling, and smart YouTube desktop redirection.
* **`TranslationManager` (`core/translations.py`):** Bilingual dictionary managing Arabic and English text resources with dynamic text-direction alignment.
* **`AppConfig` (`core/config.py`):** Holds application constants, supported resolutions, and locates `FFmpeg` on Linux and Windows.
* **`TempCleaner` (`core/cleaner.py`):** Periodically purges stale files from the server's temporary downloads cache.

---

## 📲 Installing as a Mobile Home Screen App (PWA)

### 🍏 iPhone & iPad (Safari):
1. Open the application link in **Safari**.
2. Tap the **Share** button `⎋` (the square with an upward arrow at the bottom).
3. Scroll down and select **"Add to Home Screen"** `➕`.
4. Tap **"Add"** in the top right corner.  
*The app icon will appear on your home screen and open in full-screen standalone mode.*

### 🤖 Android Devices (Chrome):
1. Open the application link in **Google Chrome**.
2. Tap the **three dots menu** `⋮` in the top right corner.
3. Tap **"Install app"** or **"Add to Home screen"** `➕`.
4. Confirm by tapping **"Install"**.  
*The app will be installed directly to your app launcher and home screen.*

---

## 💾 Choosing the Download Folder

Web browsers run within a strict security sandbox that prevents websites from accessing or modifying local disk directories directly. However, users can configure their browsers to prompt for the target directory:
* **Desktop (Chrome / Edge):** Go to **Settings ➡️ Downloads ➡️ Enable "Ask where to save each file before downloading"**.
* **iOS (iPhone / iPad):** After downloading, tap the file in Safari downloads and choose **"Save to Files"** to pick any local or iCloud folder, or select **"Save Video"** to export directly to the Camera Roll.

---

## 💻 Local Development

To run the application locally on your computer:

```bash
# Navigate to the project directory
cd Remo_ox_downloader_web_app

# Launch the Streamlit server
streamlit run app.py
```

The app will open automatically in your default browser at:  
`http://localhost:8501`

---

## 🌐 Live Web Application

Access the deployed cloud version here:  
**[remodownloader.streamlit.app](https://remodownloader.streamlit.app)**

---

<p align="center" style="color: #00d2ff; font-weight: bold; font-size: 1.2rem;">
⚡ Developed By REMO_OX
</p>
