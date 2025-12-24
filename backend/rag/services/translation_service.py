from typing import Dict, Any
from backend.shared.types import TranslationRequest
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re


class FormattingPreserver:
    """Helper class to preserve formatting during translation"""

    def parse_markdown(self, content: str) -> list:
        """Parse markdown content into structured blocks"""
        blocks = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for headings
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                content = line.lstrip('# ').strip()
                blocks.append({
                    'type': 'heading',
                    'level': level,
                    'content': content,
                    'original_line': line
                })
            # Check for code blocks
            elif line.startswith('```'):
                code_block = [line]
                i += 1
                while i < len(lines) and not lines[i].startswith('```'):
                    code_block.append(lines[i])
                    i += 1
                if i < len(lines):
                    code_block.append(lines[i])  # Add closing ```
                blocks.append({
                    'type': 'code',
                    'content': '\n'.join(code_block),
                    'original_lines': code_block
                })
            # Check for list items
            elif line.strip().startswith(('- ', '* ', '1. ', '2. ', '3. ')):
                blocks.append({
                    'type': 'list_item',
                    'content': line.strip(),
                    'original_line': line
                })
            # Check for bold/italic markers - store separately to preserve
            elif line.strip().startswith(('**', '*')) and line.strip().endswith(('**', '*')):
                blocks.append({
                    'type': 'formatted',
                    'content': line.strip(),
                    'original_line': line
                })
            # Regular paragraph
            else:
                if line.strip():
                    blocks.append({
                        'type': 'text',
                        'content': line.strip(),
                        'original_line': line
                    })
                else:
                    blocks.append({
                        'type': 'empty',
                        'content': '',
                        'original_line': line
                    })

            i += 1

        return blocks

    def reconstruct_markdown(self, blocks: list) -> str:
        """Reconstruct markdown from structured blocks"""
        result = []
        for block in blocks:
            if block['type'] == 'heading':
                result.append(f"{'#' * block['level']} {block['content']}")
            elif block['type'] == 'code':
                result.append(block['content'])
            elif block['type'] == 'list_item':
                result.append(block['content'])
            elif block['type'] == 'formatted':
                result.append(block['content'])
            elif block['type'] == 'text':
                result.append(block['content'])
            elif block['type'] == 'empty':
                result.append('')

        return '\n'.join(result)


class UrduTranslationService:
    def __init__(self):
        # Initialize the translation pipeline for English to Urdu
        # Using a pre-trained model for English to Urdu translation
        try:
            self.translator = pipeline(
                "translation",
                model="Helsinki-NLP/opus-mt-en-ur",
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Warning: Could not load translation model: {e}")
            print("Falling back to mock translation service")
            self.translator = None

        self.formatter_preserver = FormattingPreserver()

    def translate_content(self, content: str, preserve_formatting: bool = True) -> str:
        """Translate content to Urdu while preserving formatting"""
        if not content.strip():
            return content

        if preserve_formatting:
            # Parse and preserve markdown structure
            parsed_content = self.formatter_preserver.parse_markdown(content)
            translated_blocks = []

            for block in parsed_content:
                if block['type'] == 'text':
                    # Translate text blocks
                    translated_text = self._translate_text(block['content'])
                    translated_blocks.append({
                        **block,
                        'content': translated_text
                    })
                elif block['type'] == 'heading':
                    # Translate heading content but preserve structure
                    translated_text = self._translate_text(block['content'])
                    translated_blocks.append({
                        **block,
                        'content': translated_text
                    })
                elif block['type'] == 'list_item':
                    # Translate list item content but preserve structure
                    translated_text = self._translate_text(block['content'])
                    translated_blocks.append({
                        **block,
                        'content': translated_text
                    })
                else:
                    # Preserve non-translatable elements (code, etc.) as-is
                    translated_blocks.append(block)

            return self.formatter_preserver.reconstruct_markdown(translated_blocks)
        else:
            return self._translate_text(content)

    def _translate_text(self, text: str) -> str:
        """Internal translation method"""
        if not text.strip():
            return text

        if self.translator:
            try:
                # Use the translation pipeline
                result = self.translator(text, max_length=1000)
                return result[0]['translation_text']
            except Exception as e:
                print(f"Translation error: {e}")
                return f"[TRANSLATION ERROR: {text}]"
        else:
            # Fallback translation for demo purposes
            return f"URDU TRANSLATION: {text}"