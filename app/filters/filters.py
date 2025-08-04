from app.config import KEYWORDS


class Rules : 

    def __init__(self):
         self.blocked_keywords = KEYWORDS 

    def is_blocked (self, path: str, body: str) -> bool:
        """
        Check if the request should be blocked based on the path and body content.
        """
        for keyword in self.blocked_keywords:            
            if keyword.lower() in path or keyword.lower() in body:
                return True
        return False