#!/usr/bin/env python3
"""Scaffold work/<name>/ from a library prompt. Usage: new_project.py <slug> [name]"""
import json, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug = sys.argv[1]; name = sys.argv[2] if len(sys.argv) > 2 else slug
v = next((x for x in json.load(open(os.path.join(root, 'data', 'videos.json'))) if x['slug'] == slug), None)
if not v: sys.exit('slug not found')
p = os.path.join(root, 'work', name); os.makedirs(os.path.join(p, 'out'), exist_ok=True)
open(os.path.join(p, 'prompt.txt'), 'w').write(v['prompt'] + '\n')
open(os.path.join(p, 'brief.txt'), 'w').write(
f"""source slug: {slug}
source post: {v['post_url']}
category: {v['category']}
tech tags: {', '.join(v['tech_tags'])}
prompt partial: {v['prompt_partial']}

our adaptation (fill in): topic / brand / duration / aspect ratio (1920x1080 or 1080x1920) / palette / audio
""")
print(p)
