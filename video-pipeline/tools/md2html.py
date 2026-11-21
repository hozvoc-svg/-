"""Tiny Markdown -> phone-friendly HTML (headings, tables, lists, code blocks with Copy buttons, bold, inline code).
    python3 tools/md2html.py IN.md OUT.html"""
import html, re, sys

CSS = """:root{--bg:#fbfaf7;--fg:#1d1d22;--mut:#6b6b76;--card:#fff;--line:#e6e3dc;--acc:#0b7a5c;--code:#f3f1ec}
@media (prefers-color-scheme:dark){:root{--bg:#141418;--fg:#ececf1;--mut:#9a9aa6;--card:#1d1d23;--line:#2d2d36;--acc:#45d4a5;--code:#25252d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,system-ui,Segoe UI,Roboto,sans-serif}
main{max-width:760px;margin:0 auto;padding:20px 16px 60px}h1{font-size:24px;line-height:1.25}h2{font-size:20px;margin-top:34px;border-top:1px solid var(--line);padding-top:20px}
h3{font-size:17px}code{background:var(--code);padding:1px 5px;border-radius:5px;font-size:.92em}
.tw{overflow-x:auto;margin:12px 0}table{border-collapse:collapse;width:100%;font-size:14px}th,td{border:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}
th{background:var(--code)}.pre{position:relative;margin:12px 0}pre{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px;white-space:pre-wrap;word-break:break-word;font-size:14px;margin:0}
button.cp{position:absolute;top:8px;right:8px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:8px;padding:5px 10px;font-size:13px}
button.ci{margin-left:6px;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:6px;padding:2px 7px;font-size:12px}
li{margin:4px 0}a{color:var(--acc)}hr{border:0;border-top:1px solid var(--line);margin:28px 0}"""
JS = """function cp(b,t){navigator.clipboard.writeText(t).then(()=>{const o=b.textContent;b.textContent='✓';setTimeout(()=>b.textContent=o,1200)})}
document.querySelectorAll('.pre').forEach(d=>{const b=d.querySelector('button');b.onclick=()=>cp(b,d.querySelector('pre').innerText)});
document.querySelectorAll('button.ci').forEach(b=>b.onclick=()=>cp(b,b.previousElementSibling.innerText));"""


def inline(s, copy=False):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<i>\1</i>", s)
    s = re.sub(r"`([^`]+)`", (r"<code>\1</code><button class=ci>Копіювати</button>" if copy else r"<code>\1</code>"), s)
    return s


def convert(md, title):
    out, lines, i = [], md.split("\n"), 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append(f"<div class=pre><button class=cp>Копіювати</button><pre>{html.escape(chr(10).join(lines[i+1:j]))}</pre></div>")
            i = j + 1; continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                if not re.match(r"^\|[\s:|-]+\|$", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip("|").split("|")])
                i += 1
            h = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{inline(c, True)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f"<div class=tw><table><tr>{h}</tr>{b}</table></div>"); continue
        m = re.match(r"^(#{1,3}) (.*)", ln)
        if m:
            out.append(f"<h{len(m.group(1))}>{inline(m.group(2))}</h{len(m.group(1))}>")
        elif re.match(r"^\s*([-*]|\d+\.) ", ln):
            tag = "ol" if re.match(r"^\s*\d+\.", ln) else "ul"
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.) ", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i])); i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x, True)}</li>" for x in items) + f"</{tag}>"); continue
        elif ln.strip() == "---":
            out.append("<hr>")
        elif ln.strip():
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return (f"<!doctype html><html lang=uk><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>{''.join(out)}</main><script>{JS}</script></body></html>")


if __name__ == "__main__":
    md = open(sys.argv[1], encoding="utf-8").read()
    t = re.search(r"^# (.*)", md, re.M)
    open(sys.argv[2], "w", encoding="utf-8").write(convert(md, t.group(1) if t else "Bounce Lab"))
