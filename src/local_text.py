import gettext
import locale
import ctypes
import os

preferred_language_code = 'en'

if os.name == 'nt':
    preferred_language_code = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()]
elif (lc_msgs := os.getenv('LC_MESSAGES')):
    preferred_language_code = lc_msgs

gettext.translation('base', localedir='language', languages=[preferred_language_code,'en']).install()
