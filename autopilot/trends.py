"""Free trend scout: finds psychology Shorts that hugely outperform their channel size (YouTube Data API).
Shorts and Reels share the same viral topics, so this stands in for Instagram trend research.
Usage: python3 autopilot/trends.py [days=7]"""
import json, sys, urllib.request, urllib.parse, datetime, math

API = 'https://www.googleapis.com/youtube/v3/'
def get(ep, **p):
    url = API + ep + '?' + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={'X-goog-api-key': 'dummy'})  # key injected by the proxy
    return json.load(urllib.request.urlopen(req, timeout=30))

days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)).strftime('%Y-%m-%dT%H:%M:%SZ')
QUERIES = ['psychology facts', 'psychology says', 'dark psychology', 'relationship psychology', 'why do we',
           'overthinking psychology', 'attachment style', 'body language psychology', 'human behavior facts', 'brain facts']
ids = {}
for q in QUERIES:
    d = get('search', part='id', type='video', videoDuration='short', order='viewCount', maxResults=25,
            q=q, publishedAfter=since, relevanceLanguage='en')
    for it in d.get('items', []): ids[it['id']['videoId']] = q
vids = []
idl = list(ids)
for k in range(0, len(idl), 50):
    d = get('videos', part='snippet,statistics,contentDetails', id=','.join(idl[k:k + 50]))
    vids += d.get('items', [])
chs = {}
cl = list({v['snippet']['channelId'] for v in vids})
for k in range(0, len(cl), 50):
    d = get('channels', part='statistics', id=','.join(cl[k:k + 50]))
    for c in d.get('items', []): chs[c['id']] = int(c['statistics'].get('subscriberCount', 0) or 0)
rows = []
for v in vids:
    sn = v['snippet']; st = v['statistics']
    lang = (sn.get('defaultAudioLanguage') or sn.get('defaultLanguage') or 'en')[:2]
    if lang != 'en': continue
    views = int(st.get('viewCount', 0)); subs = chs.get(sn['channelId'], 0)
    if views < 50000: continue
    rows.append(dict(id=v['id'], title=sn['title'], channel=sn['channelTitle'], views=views, subs=subs,
                     ratio=round(views / max(subs, 1000), 1), likes=int(st.get('likeCount', 0)),
                     comments=int(st.get('commentCount', 0)), published=sn['publishedAt'][:10],
                     url='https://www.youtube.com/shorts/' + v['id']))
rows.sort(key=lambda r: r['ratio'] * math.log10(r['views']), reverse=True)
for r in rows[:25]:
    print(f"{r['ratio']:>7}x  {r['views']:>10,} views  {r['subs']:>9,} subs  {r['published']}  {r['title'][:90]}  {r['url']}")
json.dump(rows[:25], open('/tmp/trends.json', 'w'), indent=1)
