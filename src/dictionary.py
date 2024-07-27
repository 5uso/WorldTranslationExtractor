from util import full_unescape

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

        normal_text_pattern = ( # Normal text
            re.compile(r'"text" *: *"((?:[^"\\]|\\\\"|\\.)*)"'),
            lambda key: (
                lambda match: f'"translate":"{self.add_entry(full_unescape(match.group(1)), key)}"'
            )
        )
        escaped_text_pattern = ( # Escaped text
            re.compile(r'\\"text\\" *: *\\"((?:[^"\\]|\\\\.)*)\\"'),
            lambda key: (
                lambda match: f'\\"translate\\":\\"{self.add_entry(full_unescape(match.group(1)), key)}\\"'
            )
        )
        plain_text_pattern = ( # Plain text (The game now converts most components to plain strings which is a pain to differentiate them from data)
            re.compile(r'^"([^"]+)"$'),
            lambda key: (
                lambda match: f'{{"translate":"{self.add_entry(match.group(1), key)}"}}'
            )
        )
        bossbar_name_pattern = (
            re.compile(r'bossbar set ([^ ]+) name "(.*)"'),
            lambda key: (
                lambda match: f'bossbar set {match.group(1)} name {{"translate":"{self.add_entry(match.group(2), key)}"}}'
            )
        )
        bossbar_add_pattern = (
            re.compile(r'bossbar add ([^ ]+) "(.*)"'),
            lambda key: (
                lambda match: f'bossbar add {match.group(1)} {{"translate":"{self.add_entry(match.group(2), key)}"}}'
            )
        )

        self.component_patterns = [normal_text_pattern, escaped_text_pattern, plain_text_pattern]
        self.command_patterns = [normal_text_pattern, escaped_text_pattern, bossbar_name_pattern, bossbar_add_pattern]
        self.other_patterns = [normal_text_pattern, escaped_text_pattern]

    def add_entry(self, text: str, key: str) -> str:
        self.current_matches += 1
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
    
    def replace_component(self, nbt: StringTag, key: str) -> tuple[StringTag,int]:
        text = str(nbt)
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.component_patterns:
            text = pattern.sub(string=text, repl=matcher(key))
        return StringTag(text), self.current_matches
    
    def replace_command(self, cmd: str, key: str) -> tuple[str,int]:
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.command_patterns:
            cmd = pattern.sub(string=cmd, repl=matcher(key))
        return cmd, self.current_matches
    
    def replace_other(self, string: str, key: str) -> tuple[str,int]:
        pattern: re.Pattern
        self.current_matches = 0
        for pattern, matcher in self.other_patterns:
            string = pattern.sub(string=string, repl=matcher(key))
        return string, self.current_matches
