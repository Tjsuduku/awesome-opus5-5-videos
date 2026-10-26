#!/usr/bin/env python3
"""Search data/videos.json. Usage: find_prompt.py [keywords...] [--cat motion|3d|explainer|interactive] [--tag canvas] [--full] [--limit N]"""
import json, sys, os, argparse
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('kw', nargs='*'); ap.add_argument('--cat'); ap.add_argument('--tag')
ap.add_argument('--full', action='store_true'); ap.add_argument('--limit', type=int, default=15)
ap.add_argument('--complete', action='store_true', help='skip partial prompts')
a = ap.parse_args()
d = json.load(open(os.path.join(root, 'data', 'videos.json')))
n = 0
for v in d:
    if a.cat and v['category'] != a.cat: continue
    if a.tag and a.tag not in v['tech_tags']: continue
    if a.complete and v['prompt_partial']: continue
    t = v['prompt'].lower()
    if not all(k.lower() in t for k in a.kw): continue
    n += 1
    if n > a.limit: break
    print(f"{v['slug']} | {v['category']} | {','.join(v['tech_tags'])} | partial={v['prompt_partial']}")
    print('   ' + (v['prompt'] if a.full else v['prompt'][:160].replace('\n', ' ')))
