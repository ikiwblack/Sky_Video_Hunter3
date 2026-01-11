from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from app.services.video_searcher import search_videos_logic, get_direct_download_url
import uvicorn

# Inisialisasi aplikasi
app = FastAPI(title="VideoHunter v3.0 - Global Search Engine")

# Setup folder templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def home(request: Request):
    """Menampilkan antarmuka pencarian"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search")
async def search(
    q: str = Query(..., min_length=1), 
    page: int = Query(1, ge=1), 
    site: str = Query("")
):
    """
    Endpoint pencarian menggunakan DuckDuckGo.
    Mendukung ribuan situs (TikTok, Vimeo, IG, dll) tanpa bias YouTube.
    """
    try:
        # Panggil logika pencarian global dari video_searcher
        results = search_videos_logic(q, max_results=5, page=page, site=site)
        
        return {
            "status": "success", 
            "results": results, 
            "current_page": page,
            "engine": "DuckDuckGo Global"
        }
    except Exception as e:
        return {"status": "error", "message": f"Terjadi kesalahan: {str(e)}"}

@app.get("/get_download")
async def get_download(url: str = Query(..., description="Link video asli")):
    """
    Mengambil link file video mentah (.mp4) menggunakan yt-dlp.
    """
    try:
        download_url = get_direct_download_url(url)
        if download_url:
            return {"status": "success", "download_url": download_url}
        return {"status": "error", "message": "Format video tidak didukung atau link mati."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # Jalankan di localhost port 8000
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)