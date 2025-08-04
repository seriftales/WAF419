#Yapılandırma dosyası 
# Bu dosya, uygulamanın yapılandırma ayarlarını içerir. 

import re

TARGET_SERVER = "http://127.0.0.1:5000"  # ya da prod url
PROXY_PORT = 8080
LOG_PATH = "logs/app.log" 
HOST = "0.0.0.0" 

KEYWORDS= [

    re.compile(r"(?i)admin"),  # case insensitive admin kelimesi    
    re.compile(r"(?i)password"),  # case insensitive password kelimesi
    re.compile(r"(?i)secret"),  # case insensitive secret kelimesi

]