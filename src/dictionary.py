from amulet_nbt import StringTag

import re

from typing import TYPE_CHECKING
if TYPE_CHECKING: from settings import Settings

class Dictionary():
    def __init__(self, settings: "Settings") -> None:
        self.keepdup = settings.keepdup
        self.data = dict()
        self.keys = dict()
        self.current_matches = 0

    def add_entry(self, text: str, key: str) -> str:
        if text in self.data:
            if not self.keepdup:
                return self.data[text]
            
            key = self.increment_key(key)
            self.data[text].append(key)
            return key
        
        key = self.increment_key(key)
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
    
    def increment_key(self, key: str) -> str:
        if key in self.keys:
            self.keys[key] += 1
            return key + f'.{self.keys[key]}'
        self.keys[key] = 0
        return key
    
    component_patterns = [

    ]
    def replace_component(self, nbt: StringTag, key: str) -> tuple[StringTag,int]:
        text = str(nbt)
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.component_patterns:
            text = pattern.sub(string=text, repl=matcher(key))
        return StringTag(text), self.current_matches
    
    command_patterns = [
        
    ]
    def replace_command(self, cmd: str, key: str) -> tuple[str,int]:
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.command_patterns:
            cmd = pattern.sub(string=cmd, repl=matcher(key))
        return cmd, self.current_matches
    
    other_patterns = [
        
    ]
    def replace_other(self, string: str, key: str) -> tuple[str,int]:
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.other_patterns:
            string = pattern.sub(string=string, repl=matcher(key))
        return string, self.current_matches
