from markupsafe import Markup, escape
import re

# Define allowed tags and attributes (e.g., for a basic RTE)
ALLOWED_TAGS = {
    'b', 'i', 'u', 'strong', 'em', 'p', 'br', 'ul', 'ol', 'li', 'a', 'span',
    'table', 'tr', 'th', 'td', 'thead', 'tbody', 'tfoot', 'caption',
    'blockquote', 'pre', 'code', 'sub', 'sup', 'hr', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'div', 'dl', 'dt', 'dd', 's'
}
ALLOWED_ATTRS = {'href', 'title', 'style'}

# Regex to match tags and attributes
TAG_RE = re.compile(r'(</?)(\w+)([^>]*)(>)')
ATTR_RE = re.compile(r'(\w+)\s*=\s*(".*?"|\'.*?\')')


def safe_escape(value):
    def replace_tag(match):
        tag_open, tag_name, attrs, tag_close = match.groups()
        tag_name = tag_name.lower()

        if tag_name not in ALLOWED_TAGS:
            # Escape entire tag if not allowed
            return escape(match.group(0))

        # Process allowed attributes
        safe_attrs = ''
        for attr_match in ATTR_RE.finditer(attrs):
            attr_name, attr_value = attr_match.groups()
            attr_name = attr_name.lower()
            if attr_name in ALLOWED_ATTRS:
                # Ensure the attribute value is safely quoted
                safe_attrs += f' {attr_name}={attr_value}'

        # Return the sanitized tag
        return f'{tag_open}{tag_name}{safe_attrs}{tag_close}'

    # Use regex to process the tags first and then escape the remaining content
    escaped_content = TAG_RE.sub(replace_tag, value)
    return Markup(escaped_content)
