from werkzeug.contrib.cache import SimpleCache

BASE_URL_EMAIL = 'https://ask.fm/login/recover/'
BASE_URL_ACCOUNT = 'https://ask.fm/'
TITLE_ACCOUNT = '<title>Page Not Found - ASKfm</title>'


CACHE = SimpleCache(threshold=500, default_timeout=3600)
