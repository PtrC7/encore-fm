from api.exceptions import (
    APIError,
    RateLimitError,
    NotFoundError,
    AuthenticationError
)

from api.models import Song, SetListInfo

from api.setlistfm import SetlistFMClient, SetlistFMError

from api.spotify import SpotifyUserClient, SpotifyAppClient, SpotifyError

from api.musicmeta import MusicMetaClient

__all__ = [
    # Exceptions
    'APIError',
    'RateLimitError',
    'NotFoundError',
    'AuthenticationError',
    # Models
    'Song',
    'SetListInfo',
    # Clients
    'SetlistFMClient',
    'SetlistFMError',
    'SpotifyAppClient',
    'SpotifyUserClient',
    'SpotifyError',
    'MusicMetaClient',
]

__version__ = '0.1.0'