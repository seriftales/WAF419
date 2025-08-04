import re
from app.config import KEYWORDS
from app.utils.logger import logger


class Rules:

    def __init__(self):
        # Burada hem string hem regex gelebilir, regex objelerine çevirelim
        self.blocked_patterns = []
        for pattern in KEYWORDS:
            if isinstance(pattern, str):
                # String ise escape edip regex objesine çevir (case insensitive)
                self.blocked_patterns.append(re.compile(re.escape(pattern), re.IGNORECASE))
            elif isinstance(pattern, re.Pattern):
                self.blocked_patterns.append(pattern)
            else:
                logger.warning(f"[WAF] Desteklenmeyen kural tipi atlandı: {pattern}")

    def is_blocked(self, path: str, body: str) -> bool:
        combined_text = f"{path} {body}"
        for pattern in self.blocked_patterns:
            if pattern.search(combined_text):
                logger.info(f"[WAF] İstek engellendi: '{pattern.pattern}' eşleşti")
                return True
        return False
