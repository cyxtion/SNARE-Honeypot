import re
from typing import Dict, List

class IntelligenceHarvester:
    def __init__(self):
        self.patterns = {
            "upi": re.compile(r"[\w\.\-_]{3,256}@[a-zA-Z]{2,64}"),
            "phone": re.compile(r"(?:\+91[\-\s]?)?[6-9]\d{9}"),
            "url": re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"),
            "bank_account": re.compile(r"\b\d{9,18}\b")
        }
        self.keywords = ["block", "kyc", "verify", "urgent", "lottery"]

    def analyze(self, text: str) -> Dict[str, List[str]]:
        results = {}
        for key, pattern in self.patterns.items():
            matches = pattern.findall(text)
            if matches:
                results[key] = list(set(matches))

        found_kw = [kw for kw in self.keywords if kw in text.lower()]
        if found_kw:
            results["suspicious_keywords"] = found_kw
            
        return results

harvester = IntelligenceHarvester()