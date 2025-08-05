#Filtreleme işlemleri
# Bu modül, gelen istekleri filtreler

import re
from app.config import KEYWORDS
from app.utils.logger import logger
from urllib.parse import parse_qs,urlparse

class Rules:
    
    def __init__(self):
        # Kuralları yükle ve işle
        self.blocked_patterns = []
        self.load_patterns()

    def load_patterns(self):
        """Kuralları KEYWORDS'den yükleyip regex objelerine dönüştür."""
        for rule_category, rules in KEYWORDS.items():
            for rule in rules:
                if isinstance(rule, dict) and "pattern" in rule:
                    if isinstance(rule["pattern"], str):
                        self.blocked_patterns.append({
                            "regex": re.compile(re.escape(rule["pattern"]), re.IGNORECASE),
                            "category": rule_category,  
                            "level": rule["level"],
                            "message": rule["message"],
                            "target": rule["target"]
                        })
                    else:
                        logger.warning(f"[WAF] Kuralın 'pattern' alanı doğru formatta değil: {rule['pattern']}")
                else:
                    logger.warning(f"[WAF] Desteklenmeyen kural tipi veya eksik pattern: {rule}")

    
    def check_pattern(self, combined_text: str) -> bool:
        """Gelen text üzerinde kuralları kontrol eder."""
        for rule in self.blocked_patterns:
            if rule["regex"].search(combined_text):
                #logger.info(f"[WAF] İstek engellendi: '{rule['pattern']}' - {rule['message']} ({rule['category']})")
                return True
        return False
    
    
    def is_blocked(self, path: str, body: str,query:str) -> bool:
        combined_text = f"{path}" 
        if self.check_pattern(combined_text):
            return True
        
        if query : 
            parsed_query = parse_qs(query)
            query_string = ' '.join([f"{k}={v[0]}" for k, v in parsed_query.items()])                                             
      
            if self.check_pattern(query_string):
                return True

        combined_text = f" {body}"
        if self.check_pattern(combined_text):
            return True

        return False


