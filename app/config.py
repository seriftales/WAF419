#Yapılandırma dosyası 
# Bu dosya, uygulamanın yapılandırma ayarlarını içerir. 


import json 

TARGET_SERVER = "http://172.16.102.35"  # ya da prod url
PROXY_PORT = 8080
LOG_PATH = "logs/app2.log" 
HOST = "0.0.0.0" 

RULES_FILE = "app/filters/rules.json"

try : 
    with open (RULES_FILE, "r") as f:
        KEYWORDS = json.load(f)

except Exception as e:
    print(f"Error loading rules from {RULES_FILE}: {e}")
    KEYWORDS = []