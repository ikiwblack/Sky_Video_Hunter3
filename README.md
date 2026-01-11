# 🎬 SKY VIDEO HUNTER 3 - [EKSPERIMENTAL] 🚀
## *Video Search via Localhost*

> **STATUS:** Proyek ini dalam tahap **EKSPERIMENTAL**. Fokus utama versi ini adalah integrasi **DuckDuckGo Search (DDGS)** untuk mencari dan mengimpor aset video langsung dari internet ke dalam timeline.

Sky Video Hunter 3 bukan sekadar editor video biasa. Ini adalah ekosistem di mana Anda bisa mencari aset melalui DDGS, mentranskripsinya dengan AI Whisper, dan mengeditnya secara real-time dalam satu antarmuka berbasis web.

## 🌟 Fitur Baru: DDGS Video Browser
- [x] **Live Video Search**: Cari video dari web langsung.
- [x] **CUSTOM URL filter**: Filter URL.
- [x] **Thumbnail**: Lihat hasil pencarian sebelum memutuskan untuk mendownload.

## 📁 Struktur Proyek

    hunter/
    ├── app/
    │   ├── main.py                 # Endpoint API (Termasuk Search Logic)
    │   ├── templates/              # UI dengan Modal Browser Video
    │   │   └── index.html 
    │   └── services/               
    │       └── search_engine.py    # DuckDuckGo Search Wrapper
    ├── requirements.txt            # Ditambahkan: duckduckgo_search
    └── README.md
