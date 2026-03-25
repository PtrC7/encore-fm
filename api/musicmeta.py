import requests
import logging
import time
from typing import Optional
from api.models import Song
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def _is_valid_album(album_name: str) -> bool:
    name_lower = album_name.lower()
    invalid_keywords = ["live", "compilation", "greatest hits", "remaster", "karaoke", "tribute", "cover", "re-record"]
    return not any(word in name_lower for word in invalid_keywords)


class MusicMetaClient:
    ITUNES_SEARCH = "https://itunes.apple.com/search"
    MUSICBRAINZ_SEARCH = "https://musicbrainz.org/ws/2/artist/"
    HEADERS = {"User-Agent": os.getenv('MUSIC_BRAINZ_HEADER')}

    REQUEST_DELAY = 0.3
    MAX_RETRIES = 3

    def search_track(self, song: Song) -> Optional[dict]:
        query = f"{song.name} {song.original_artist}"
        
        for attempt in range(self.MAX_RETRIES):
            try:
                time.sleep(self.REQUEST_DELAY)
                resp = requests.get(self.ITUNES_SEARCH, params={
                    "term": query,
                    "media": "music",
                    "entity": "song",
                    "limit": 10
                }, timeout=5)

                if resp.status_code == 403:
                    wait = 2 ** attempt  # 1s, 2s, 4s
                    logger.warning(f"[iTunes] 403 on attempt {attempt + 1}, retrying in {wait}s...")
                    time.sleep(wait)
                    continue

                resp.raise_for_status()
                results = resp.json().get("results", [])
                if not results:
                    return None

                def score(r):
                    s = 0
                    if song.original_artist.lower() == r.get("artistName", "").lower():
                        s += 10
                    elif song.original_artist.lower() in r.get("artistName", "").lower():
                        s += 5
                    if song.name.lower() == r.get("trackName", "").lower():
                        s += 5
                    if not _is_valid_album(r.get("collectionName", "")):
                        s -= 8
                    if r.get("kind") == "song":
                        s += 2
                    return s

                best = max(results, key=score)
                artwork = best.get("artworkUrl100", "").replace("100x100", "600x600")

                return {
                    "album": best.get("collectionName"),
                    "album_image": artwork or None,
                    "artist_image": None,
                }

            except Exception as e:
                logger.warning(f"[iTunes] Search failed for '{query}': {e}")
                return None

        logger.warning(f"[iTunes] All retries exhausted for '{query}'")
        return None

    def get_artist_image(self, artist_name: str) -> Optional[str]:
        """Fetch artist image from MusicBrainz + fanart.tv fallback."""
        try:
            resp = requests.get(self.MUSICBRAINZ_SEARCH, params={
                "query": artist_name,
                "fmt": "json",
                "limit": 1
            }, headers=self.HEADERS, timeout=5)
            resp.raise_for_status()
            artists = resp.json().get("artists", [])
            if not artists:
                return None

            mbid = artists[0]["id"]

            adb_resp = requests.get(
                f"https://www.theaudiodb.com/api/v1/json/2/artist-mb.php?i={mbid}",
                timeout=5
            )
            adb_resp.raise_for_status()
            adb_artists = adb_resp.json().get("artists")
            if adb_artists:
                return adb_artists[0].get("strArtistThumb") or adb_artists[0].get("strArtistFanart")

        except Exception as e:
            logger.warning(f"[MusicBrainz/AudioDB] Artist image failed for '{artist_name}': {e}")
        return None