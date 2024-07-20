from typing import TYPE_CHECKING
if TYPE_CHECKING: from settings import Settings

class Dictionary():
    def __init__(self, settings: "Settings") -> None:
        self.keepdup = settings.keepdup
        self.data = dict()

    def add_entry(self, text: str, key: str) -> str:
        if text in self.data:
            if not self.keepdup:
                return self.data[text]
            
            self.data[text].append(key)
            return key
        
        self.data[text] = [key] if self.keepdup else key
        return key
    
    def reverse(self) -> dict[str,str]:
        r = dict()
        for text in self.data:
            if not self.keepdup:
                r[self.data[text]] = text
                continue
            
            for k in self.data[text]:
                r[k] = text

        return r
