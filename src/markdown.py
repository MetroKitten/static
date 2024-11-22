import re
from enums import *
from htmlnode import *
from textnode import *
from splitter import *

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n\n"):
        cleaned_line = line.strip()
        if cleaned_line:
            blocks.append(cleaned_line)
    return blocks

def block_to_block_type(block):
        if re.match(r"#+", block):
            if re.match(r"^#{1}\s", block):
                return BlockType.HEADING1
            elif re.match(r"^#{2}\s", block):
                return BlockType.HEADING2
            elif re.match(r"^#{3}\s", block):
                return BlockType.HEADING3
            elif re.match(r"^#{4}\s", block):
                return BlockType.HEADING4
            elif re.match(r"^#{5}\s", block):
                return BlockType.HEADING5
            elif re.match(r"^#{6}\s", block):
                return BlockType.HEADING6
            else:
                return BlockType.PARAGRAPH
        elif block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
        elif re.match(r"> ", block):
            return BlockType.QUOTE
        elif re.match(r"^(?:\s*[-*+]\s.*(?:\n|$))+\Z", block):
            return BlockType.UNORDERED_LIST
        elif block.startswith("1. "): 
            is_ordered_list = True
            lines = block.strip().split("\n")
            number = 1
            for line in lines:
                if line.startswith(f"{number}. "):
                    number += 1
                else:
                    is_ordered_list = False
                    break
            if is_ordered_list:
                return BlockType.ORDERED_LIST
            else:
                return BlockType.PARAGRAPH
        else:
            return BlockType.PARAGRAPH
