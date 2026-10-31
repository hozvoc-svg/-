"""List every upload of the channel owner's YouTube channels with views/likes/comments.
The API key is injected by the environment's network secret (header X-goog-api-key), so no key here.

    python3 tools/yt_channels.py [out.json]
"""
import json, re, sys, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3/"
CHANNELS = {"Stickman Unsolved": "UCuhwDfyLEBp6z_Wpi_3rjqg", "Bounce Lab": "UCH3fur3y79RowK8v_XvYDkg",
            "Sleepy Cosmos": "UCzKx2K9QkE7oSym8z0aHgQw"}


def get(path, **params):
    with urllib.request.urlopen(API + path + "?" + urllib.parse.urlencode(params), timeout=30) as r:
        return json.load(r)


def seconds(iso):
    h, m, s = (int(x or 0) for x in re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso).groups())
    return h * 3600 + m * 60 + s


def uploads(channel_id):
    ids, token = [], None
    playlist = "UU" + channel_id[2:]
    while True:
        p = dict(part="contentDetails", playlistId=playlist, maxResults=50)
        if token:
            p["pageToken"] = token
        d = get("playlistItems", **p)
        ids += [it["contentDetails"]["videoId"] for it in d.get("items", [])]
        token = d.get("nextPageToken")
        if not token:
            return ids


def details(ids):
    out = []
    for i in range(0, len(ids), 50):
        d = get("videos", part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50]))
        for it in d.get("items", []):
            st = it["statistics"]
            out.append(dict(id=it["id"], title=it["snippet"]["title"], published=it["snippet"]["publishedAt"][:10],
                            seconds=seconds(it["contentDetails"]["duration"]), views=int(st.get("viewCount", 0)),
                            likes=int(st.get("likeCount", 0)), comments=int(st.get("commentCount", 0))))
    return sorted(out, key=lambda v: v["published"])


if __name__ == "__main__":
    data = {name: details(uploads(cid)) for name, cid in CHANNELS.items()}
    if len(sys.argv) > 1:
        json.dump(data, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
    for name, vids in data.items():
        print(f"\n== {name}: {len(vids)} videos, {sum(v['views'] for v in vids)} views")
        for v in vids:
            kind = "SHORT" if v["seconds"] <= 180 else "LONG "
            print(f"{v['published']}  {kind} {v['seconds']:>5}s  {v['views']:>6} views  {v['likes']:>4} likes  {v['title'][:70]}")
