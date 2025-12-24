from typing import Dict, List, Tuple
import re


class MarkdownPreserver:
    """Preserves markdown formatting during translation processes"""

    def __init__(self):
        self.placeholder_pattern = r'\[PLACEHOLDER_(\d+)\]'
        self.placeholders = {}

    def extract_and_preserve_formatting(self, content: str) -> Tuple[str, Dict[str, str]]:
        """Extract markdown elements and replace with placeholders"""
        processed_content = content
        self.placeholders = {}

        # Extract and preserve code blocks
        code_blocks = re.findall(r'```.*?```', processed_content, re.DOTALL)
        for i, block in enumerate(code_blocks):
            placeholder = f"[PLACEHOLDER_CODE_{i}]"
            self.placeholders[placeholder] = block
            processed_content = processed_content.replace(block, placeholder, 1)

        # Extract and preserve inline code
        inline_codes = re.findall(r'`[^`]*`', processed_content)
        for i, code in enumerate(inline_codes):
            placeholder = f"[PLACEHOLDER_INLINE_CODE_{len(code_blocks) + i}]"
            self.placeholders[placeholder] = code
            processed_content = processed_content.replace(code, placeholder, 1)

        # Extract and preserve links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', processed_content)
        for i, (text, url) in enumerate(links):
            placeholder = f"[PLACEHOLDER_LINK_{i}]"
            self.placeholders[placeholder] = f"[{text}]({url})"
            processed_content = processed_content.replace(f"[{text}]({url})", placeholder, 1)

        # Extract and preserve images
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', processed_content)
        for i, (alt, src) in enumerate(images):
            placeholder = f"[PLACEHOLDER_IMAGE_{i}]"
            self.placeholders[placeholder] = f"![{alt}]({src})"
            processed_content = processed_content.replace(f"![{alt}]({src})", placeholder, 1)

        # Extract and preserve headings
        headings = re.findall(r'^(#+\s.*?)(?=\n|$)', processed_content, re.MULTILINE)
        for i, heading in enumerate(headings):
            placeholder = f"[PLACEHOLDER_HEADING_{i}]"
            self.placeholders[placeholder] = heading
            processed_content = processed_content.replace(heading, placeholder, 1)

        # Extract and preserve bold text
        bolds = re.findall(r'\*\*([^*]+)\*\*', processed_content)
        for i, bold in enumerate(bolds):
            placeholder = f"[PLACEHOLDER_BOLD_{i}]"
            self.placeholders[placeholder] = f"**{bold}**"
            processed_content = processed_content.replace(f"**{bold}**", placeholder, 1)

        # Extract and preserve italic text
        italics = re.findall(r'\*([^*]+)\*', processed_content)
        for i, italic in enumerate(italics):
            placeholder = f"[PLACEHOLDER_ITALIC_{i}]"
            self.placeholders[placeholder] = f"*{italic}*"
            processed_content = processed_content.replace(f"*{italic}*", placeholder, 1)

        # Extract and preserve lists
        list_items = re.findall(r'^(\s*[-*+]\s.*?)(?=\n\s*[-*+]\s|\n\n|\Z)', processed_content, re.MULTILINE)
        for i, item in enumerate(list_items):
            placeholder = f"[PLACEHOLDER_LIST_{i}]"
            self.placeholders[placeholder] = item
            processed_content = processed_content.replace(item, placeholder, 1)

        return processed_content, self.placeholders

    def restore_formatting(self, translated_content: str) -> str:
        """Restore markdown formatting from placeholders"""
        restored_content = translated_content

        # Replace placeholders with original markdown elements
        for placeholder, original in self.placeholders.items():
            restored_content = restored_content.replace(placeholder, original)

        return restored_content

    def parse_markdown_blocks(self, content: str) -> List[Dict[str, str]]:
        """Parse markdown into structured blocks"""
        blocks = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                blocks.append({'type': 'empty', 'content': line})
                i += 1
                continue

            # Check for headings
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                content = line.lstrip('# ').strip()
                blocks.append({
                    'type': 'heading',
                    'level': level,
                    'content': content
                })
                i += 1
                continue

            # Check for code blocks
            if line.startswith('```'):
                code_block = [line]
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_block.append(lines[i])
                    i += 1
                if i < len(lines):
                    code_block.append(lines[i])  # Add closing ```
                blocks.append({
                    'type': 'code_block',
                    'content': '\n'.join(code_block)
                })
                i += 1
                continue

            # Check for list items
            if line.startswith(('- ', '* ', '+ ')) or re.match(r'^\d+\.\s', line):
                blocks.append({
                    'type': 'list_item',
                    'content': line
                })
                i += 1
                continue

            # Regular paragraph
            blocks.append({
                'type': 'paragraph',
                'content': line
            })
            i += 1

        return blocks

    def reconstruct_markdown(self, blocks: List[Dict[str, str]]) -> str:
        """Reconstruct markdown from structured blocks"""
        result_lines = []

        for block in blocks:
            if block['type'] == 'heading':
                result_lines.append(f"{'#' * block['level']} {block['content']}")
            elif block['type'] == 'code_block':
                result_lines.append(block['content'])
            elif block['type'] == 'list_item':
                result_lines.append(block['content'])
            elif block['type'] == 'paragraph':
                result_lines.append(block['content'])
            elif block['type'] == 'empty':
                result_lines.append(block['content'])

        return '\n'.join(result_lines)


class UrduTranslationService:
    """Enhanced translation service with markdown preservation"""

    def __init__(self):
        self.markdown_preserver = MarkdownPreserver()

    def translate_content_preserving_formatting(self, content: str) -> str:
        """Translate content while preserving markdown formatting"""
        # Extract and preserve formatting
        clean_content, placeholders = self.markdown_preserver.extract_and_preserve_formatting(content)

        # Translate the cleaned content (in a real implementation, this would call the translation API)
        # For demo purposes, we'll just add a prefix
        translated_content = f"URDU TRANSLATION: {clean_content}"

        # Restore the formatting
        final_content = self.markdown_preserver.restore_formatting(translated_content)

        return final_content

    def translate_by_blocks(self, content: str) -> str:
        """Translate content by parsing into blocks and translating text-only blocks"""
        # Parse into blocks
        blocks = self.markdown_preserver.parse_markdown_blocks(content)

        # Translate text blocks while preserving code and other blocks
        translated_blocks = []
        for block in blocks:
            if block['type'] in ['paragraph', 'heading']:
                # Translate these blocks
                translated_content = f"URDU: {block['content']}"
                translated_blocks.append({
                    **block,
                    'content': translated_content
                })
            else:
                # Keep other blocks as is (code, lists, etc.)
                translated_blocks.append(block)

        # Reconstruct the markdown
        return self.markdown_preserver.reconstruct_markdown(translated_blocks)


# Global instance
markdown_preservation_service = UrduTranslationService()