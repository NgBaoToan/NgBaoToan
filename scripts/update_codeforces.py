#!/usr/bin/env python3
"""Refresh a locally hosted Codeforces card using only Python's standard library."""
from __future__ import annotations

import argparse
import datetime as dt
from html import escape
import json
from pathlib import Path
import time
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data' / 'codeforces.json'
CARD = ROOT / 'assets' / 'codeforces-live.svg'
HANDLE = 'toan149'


def api(method: str, **params):
    url = 'https://codeforces.com/api/' + method + '?' + urllib.parse.urlencode(params)
    error = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'NgBaoToan-profile/1.0'})
            with urllib.request.urlopen(request, timeout=25) as response:
                payload = json.load(response)
            if payload.get('status') != 'OK':
                raise ValueError(payload.get('comment', 'API did not return OK'))
            return payload['result']
        except (OSError, ValueError, KeyError) as exc:
            error = exc
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
    raise RuntimeError(f'{method} unavailable: {error}')


def color_for_rating(rating):
    if rating is None: return '#98B2B8'
    if rating < 1200: return '#A8B3BC'
    if rating < 1400: return '#71E5CE'
    if rating < 1600: return '#61DCEC'
    if rating < 1900: return '#88A6FF'
    if rating < 2100: return '#CF9CFF'
    if rating < 2400: return '#FFBC71'
    return '#FF8796'


def t(x, y, value, size=18, color='#EBF5F2', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def format_date(value):
    if not value: return 'Awaiting first sync'
    return dt.datetime.fromisoformat(value).astimezone(dt.timezone(dt.timedelta(hours=7))).strftime('%d %b %Y, %H:%M UTC+7')


def render(cache):
    info = cache.get('info') or {}
    history = cache.get('history')
    rating = info.get('rating')
    accent = color_for_rating(rating)
    b = '<rect x=".5" y=".5" width="1279" height="419" rx="18" fill="#0B141B" stroke="#263D46"/>'
    b += t(32,38,'CODEFORCES / '+HANDLE,14,'#98B2B8',400,'letter-spacing="2"')
    b += t(32,98,str(rating) if rating is not None else '—',55,accent,700)
    rank = info.get('rank', 'Unrated' if info else 'Awaiting sync').upper()
    b += t(32,132,rank,18,accent,700)
    b += '<path d="M570 61 V146 M905 61 V146" stroke="#263D46"/>'
    b += t(608,83,'BEST RATING',12,'#98B2B8',400,'letter-spacing="1"')
    b += t(608,129,info.get('maxRating','—'),32,'#EBF5F2',700)
    b += t(946,83,'RATED CONTESTS',12,'#98B2B8',400,'letter-spacing="1"')
    b += t(946,129,len(history) if history is not None else '—',32,'#EBF5F2',700)
    b += '<path d="M32 166 H1248" stroke="#263D46"/>'
    b += t(32,200,'RATING HISTORY',12,'#98B2B8',400,'letter-spacing="1.5"')
    if history:
        values=[row['newRating'] for row in history]
        # Keep a readable range even for one rated contest or a flat history.
        low, high = min(values)-70, max(values)+70
        low = max(0,low)
        span = max(1,high-low)
        coords=[(68 + i*1140/max(1,len(values)-1), 329-(v-low)*100/span) for i,v in enumerate(values)]
        if len(coords)==1: coords=[(638,coords[0][1])]
        for y in [229,279,329]: b += f'<path d="M68 {y} H1208" stroke="#1C333E" stroke-dasharray="4 7"/>'
        b += t(32,235,high,11,'#6F8E98') + t(32,334,low,11,'#6F8E98')
        points=' '.join(f'{x:.2f},{y:.2f}' for x,y in coords)
        b += f'<polyline points="{points}" fill="none" stroke="{accent}" stroke-width="3" stroke-linejoin="round"/>'
        for x,y in coords:
            b += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#0B141B" stroke="{accent}" stroke-width="2"/>'
        first=dt.datetime.fromtimestamp(history[0]['ratingUpdateTimeSeconds'],dt.timezone.utc).strftime('%b %Y')
        last=dt.datetime.fromtimestamp(history[-1]['ratingUpdateTimeSeconds'],dt.timezone.utc).strftime('%b %Y')
        b += t(68,357,first,12,'#98B2B8') + t(1208,357,last,12,'#98B2B8',extra='text-anchor="end"')
    else:
        message='No rated contests yet.' if history == [] else 'Rating history will appear after a successful sync.'
        b += t(640,284,message,19,'#98B2B8',extra='text-anchor="middle"')
    b += t(32,397,'Profile: '+format_date(cache.get('info_updated_at')),11,'#98B2B8')
    b += t(1248,397,'History: '+format_date(cache.get('history_updated_at')),11,'#98B2B8',extra='text-anchor="end"')
    title=f'Codeforces {HANDLE}: rating {rating if rating is not None else "unavailable"}, {rank.lower()}; best {info.get("maxRating","unavailable")}; {len(history) if history is not None else "unknown"} rated contests. Last profile sync: {format_date(cache.get("info_updated_at"))}.'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="420" viewBox="0 0 1280 420" role="img" aria-label="{escape(title,quote=True)}"><title>{escape(title)}</title><g font-family="DejaVu Sans Mono, monospace">{b}</g></svg>'


def atomic_write(path, content):
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp')
    temp.write_text(content,encoding='utf-8')
    temp.replace(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline',action='store_true',help='Render the stored snapshot without calling the API.')
    args=parser.parse_args()
    cache=json.loads(CACHE.read_text()) if CACHE.exists() else {'handle':HANDLE}
    errors=[]
    if not args.offline:
        try:
            users=api('user.info',handles=HANDLE)
            info=users[0]
            # Deliberately store only the public fields used by the profile.
            cache['info']={key:info[key] for key in ['handle','rank','rating','maxRank','maxRating'] if key in info}
            cache['info_updated_at']=dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')
        except (RuntimeError,IndexError,KeyError) as exc: errors.append(str(exc))
        time.sleep(2.1)
        try:
            rows=api('user.rating',handle=HANDLE)
            cache['history']=sorted([{k:row[k] for k in ['contestId','ratingUpdateTimeSeconds','newRating']} for row in rows],key=lambda row:row['ratingUpdateTimeSeconds'])
            cache['history_updated_at']=dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')
        except (RuntimeError,KeyError) as exc: errors.append(str(exc))
    atomic_write(CACHE,json.dumps(cache,ensure_ascii=False,indent=2)+'\n')
    atomic_write(CARD,render(cache))
    for error in errors: print('Warning: '+error+'; retained the last successful snapshot and its timestamp.')
    print('Codeforces card rendered from public, timestamped data.')


if __name__=='__main__': main()
