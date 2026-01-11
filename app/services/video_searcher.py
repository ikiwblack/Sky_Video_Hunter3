from ddgs import DDGS
import yt_dlp
import logging

# Konfigurasi logging agar terminal tetap bersih
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_videos_logic(keyword, max_results=5, page=1, site=""):
    """
    Mencari video menggunakan library ddgs (DuckDuckGo Search).
    Menyaring link artikel secara otomatis agar hanya video yang tampil.
    """
    results = []
    
    # 1. Normalisasi input situs
    clean_site = site.lower().replace("site:", "").replace("https://", "").replace("http://", "").strip().split('/')[0]
    
    # 2. Susun Query yang kuat (menekankan hasil video)
    if clean_site:
        query = f"{keyword} site:{clean_site}"
    else:
        # Jika mencari global, tambahkan intent video agar tidak muncul artikel berita
        query = f"{keyword} (video OR clip OR watch) -article -news"
    
    logger.info(f"Query Utama: {query}")

    try:
        # 3. Ambil link dari DuckDuckGo
        with DDGS() as ddgs:
            # Kita ambil cadangan hasil lebih banyak (fetch_limit) 
            # karena banyak link web biasa yang harus dibuang
            fetch_limit = 20 if clean_site else 40
            search_results = ddgs.text(
                query, 
                region="wt-wt", 
                safesearch="moderate", 
                max_results=fetch_limit
            )
            
            all_links = list(search_results)
            
            # Hitung offset untuk pagination
            start_index = (page - 1) * max_results
            # Kita mulai memproses dari start_index sampai mendapatkan 5 video valid
            potential_targets = all_links[start_index:]

        # 4. Filter & Ambil Metadata dengan yt-dlp
        ydl_opts = {
            'quiet': True, 
            'extract_flat': True, 
            'no_warnings': True,
            'skip_download': True,
            'allowed_extractors': ['default', 'generic']
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for item in potential_targets:
                if len(results) >= max_results:
                    break
                
                video_url = item.get('href')
                
                # Filter Cepat: Hindari domain berita/artikel yang sudah pasti bukan video player
                blacklist = ['detik.com', 'kompas.com', 'tribunnews.com', 'wikipedia.org']
                if any(domain in video_url for domain in blacklist):
                    continue

                try:
                    # Cek apakah yt-dlp mengenali URL ini sebagai video
                    info = ydl.extract_info(video_url, download=False)
                    
                    if info:
                        # Jika berhasil, masukkan ke daftar hasil
                        results.append({
                            "title": info.get("title") or item.get("title"),
                            "url": video_url,
                            "duration": info.get("duration") or 0,
                            "uploader": info.get("uploader") or clean_site or "Web Source",
                            "thumbnail": info.get("thumbnail") or (info.get("thumbnails")[0]['url'] if info.get("thumbnails") else None),
                        })
                except Exception:
                    # Jika link tidak didukung (Unsupported URL), abaikan saja
                    continue
                    
        return results

    except Exception as e:
        logger.error(f"Koneksi DDGS Bermasalah: {e}")
        return []

def get_direct_download_url(video_url):
    """
    Ekstraksi link MP4 langsung.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url') or (info.get('formats')[-1].get('url') if info.get('formats') else None)
    except:
        return None