import requests
import logging
from typing import Optional
from api.models import Song
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MusicMetaClient:
    ITUNES_SEARCH = "https://itunes.apple.com/search"
    MUSICBRAINZ_SEARCH = "https://musicbrainz.org/ws/2/artist/"
    HEADERS = {"User-Agent": os.getenv('MUSIC_BRAINZ_HEADER')}

    def search_track(self, song: Song) -> Optional[dict]:
        query = f"{song.name} {song.original_artist}"
        logger.info(f"[iTunes] Searching: {query}")
        try:
            resp = requests.get(self.ITUNES_SEARCH, params={
                "term": query,
                "media": "music",
                "entity": "song",
                "limit": 5
            }, timeout=5)
            resp.raise_for_status()
            results = resp.json().get("results", [])
            if not results:
                return None

            match = next(
                (r for r in results if song.original_artist.lower() in r.get("artistName", "").lower()),
                results[0]
            )

            artwork = match.get("artworkUrl100", "").replace("100x100", "500x500")

            return {
                "album": match.get("collectionName"),
                "album_image": artwork or None,
                "artist_image": None, 
            }
        except Exception as e:
            logger.warning(f"[iTunes] Search failed for '{query}': {e}")
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