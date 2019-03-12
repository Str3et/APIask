from werkzeug.contrib.cache import SimpleCache

BASE_URL = 'https://ask.fm/login/recover/'

CACHE = SimpleCache(threshold=500, default_timeout=3600)
