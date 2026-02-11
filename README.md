

# 🔍 EzFix - Steam DRM & Online-Fix Checker

<p align="center">
  <img src="https://capsule-render.vercel.app/render?type=soft&color=2ecc71&height=150&section=header&text=EzFix%20Bot&fontSize=50&animation=fadeIn" alt="EzFix Header" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Prototype-yellow?style=for-the-badge" alt="Prototype Status" />
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/Library-BeautifulSoup4-orange?style=for-the-badge" alt="BeautifulSoup" />
  <img src="https://img.shields.io/badge/API-Steam_Web_API-blue?style=for-the-badge&logo=steam" alt="Steam API" />
</p>

---

## 🌐 Project Evolution: From Bot to Web App
> **Note:** This Discord bot served as the **foundational prototype** logic before being re-engineered and fully integrated into my personal platform.

You can now experience the enhanced, high-performance version of **EzFix Tool** directly on my website:
👉 **[Visit EzplaystoreTh.xyz](https://ezplaystoreth.xyz/ezfix)**

<p align="center">
<img width="1909" height="987" alt="image" src="https://github.com/user-attachments/assets/ef6f0b3f-30f0-46c8-87c4-a1ae3a9525fe" width="90%" alt="EzFix Web Version" />
  <br>
  <i>The evolved EzFix Tool running on Next.js at EzplaystoreTh</i>
</p>

---

## 🚀 Overview
**EzFix** is a specialized Discord bot designed for gamers and software enthusiasts. It allows users to quickly verify if a specific Steam game has third-party DRM (like **Denuvo**) and checks its availability on **Online-Fix.me** for multiplayer bypasses.

## 🛠️ Key Features
* **Steam Integration:** Fetches real-time game data using Steam AppID.
* **DRM Detection:** Automatically scrapes Steam store pages to identify Denuvo and other 3rd-party DRM systems.
* **Availability Checker:** Scans Online-Fix.me to see if a multiplayer fix is available for the searched game.
* **Visual Embeds:** Dynamic UI that changes color based on availability (Green for available, Red for unavailable).
* **Always-On:** Integrated with `keep_alive` to ensure the bot stays online 24/7 on hosting platforms like Replit.

## 📦 Requirements
* `discord.py`
* `aiohttp`
* `beautifulsoup4`

## ⚙️ Configuration

1. **Bot Token:** Securely store your Discord Token in an environment variable named `BOT_TOKEN`.
2. **Setup:**
   ```bash
   pip install discord.py aiohttp beautifulsoup4



3. **Run:** Execute the script, and the bot will automatically sync slash commands.

## 🎮 Commands

* `/ezfix [steam_appid]` - Checks the DRM status and fix availability for the provided Steam AppID.

---

## ⚠️ Disclaimer

This tool is for educational purposes and personal information gathering regarding software protection systems.

---

<p align="center">
Developed by <a href="https://www.google.com/search?q=https://github.com/novterss">novterss</a> | <b>Computer Science Student</b>
</p>

