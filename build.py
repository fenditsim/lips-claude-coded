#!/usr/bin/env python3
import argparse
import json
import os
import re


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content without external libraries."""
    if not content.startswith('---'):
        return {}, content

    end = content.find('\n---', 3)
    if end == -1:
        return {}, content

    frontmatter_text = content[3:end].strip()
    body = content[end + 4:].strip()

    fields = {}
    lines = frontmatter_text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        match = re.match(r'^([\w_]+):\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            # List value: next lines start with '- '
            if value == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('-'):
                items = []
                i += 1
                while i < len(lines) and lines[i].strip().startswith('-'):
                    item = lines[i].strip()[1:].strip()
                    if (item.startswith('"') and item.endswith('"')) or \
                       (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    items.append(item)
                    i += 1
                fields[key] = items
                continue
            else:
                # Strip surrounding quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                fields[key] = value
        i += 1

    return fields, body


def generate_snippet(body, max_chars=220):
    """Generate a short snippet from the body text."""
    text = ' '.join(body.split())
    if len(text) <= max_chars:
        return text
    snippet = text[:max_chars]
    last_space = snippet.rfind(' ')
    if last_space > 0:
        snippet = snippet[:last_space]
    return snippet + '\u2026'


def process_posts(posts_dir, output_file):
    md_files = sorted(f for f in os.listdir(posts_dir) if f.endswith('.md'))
    posts = []

    for filename in md_files:
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        frontmatter, body = parse_frontmatter(content)

        post = {
            'slug': filename[:-3],
            'title': frontmatter.get('title', ''),
            'source_title': frontmatter.get('source_title', ''),
            'source_url': frontmatter.get('source_url', ''),
            'linkedin_url': frontmatter.get('linkedin_url', ''),
            'keywords': frontmatter.get('keywords', []),
            'body': body,
            'snippet': generate_snippet(body),
        }
        posts.append(post)

    js_content = 'const POSTS = ' + json.dumps(posts, ensure_ascii=False, indent=2) + ';\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f'\u2713 Built {len(posts)} posts \u2192 {output_file}')


def main():
    parser = argparse.ArgumentParser(description='Build posts.js from markdown files')
    parser.add_argument('--dir', default='./posts', help='Directory containing .md files')
    parser.add_argument('--out', default='posts.js', help='Output JS file')
    args = parser.parse_args()
    process_posts(args.dir, args.out)


if __name__ == '__main__':
    main()
