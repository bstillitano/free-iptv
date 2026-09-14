"""Build one EPG covering only the channels in playlists/*.m3u.

Pulls Matt Huisman's XMLTV guides (i.mjh.nz), keeps <channel>/<programme> entries whose id
matches a tvg-id in the playlists, and writes epg/epg.xml.gz. The gzip header has no timestamp,
so an unchanged guide produces a byte-identical file and the workflow skips the commit.
"""
import glob
import gzip
import io
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "epg" / "epg.xml.gz"
SOURCES = [
    "https://i.mjh.nz/au/Sydney/epg.xml.gz",
    "https://i.mjh.nz/PlutoTV/us.xml.gz",
    "https://i.mjh.nz/PlutoTV/gb.xml.gz",
    "https://i.mjh.nz/SamsungTVPlus/us.xml.gz",
    "https://i.mjh.nz/SamsungTVPlus/gb.xml.gz",
    "https://i.mjh.nz/Plex/us.xml.gz",
    "https://i.mjh.nz/Plex/gb.xml.gz",
    "https://i.mjh.nz/Roku/all.xml.gz",
]


def playlist_ids():
    ids = set()
    for path in glob.glob(str(ROOT / "playlists" / "*.m3u")):
        ids.update(i for i in re.findall(r'tvg-id="([^"]+)"', Path(path).read_text(encoding="utf-8")) if i)
    return ids


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "free-iptv-epg/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return gzip.decompress(r.read())


def main():
    wanted = playlist_ids()
    channels, programmes, seen = [], [], set()
    for url in SOURCES:
        try:
            data = fetch(url)
        except Exception as e:  # one dead source shouldn't blank the whole guide
            print(f"skip {url}: {e}", file=sys.stderr)
            continue
        kept = 0
        for _, el in ET.iterparse(io.BytesIO(data), events=("end",)):
            if el.tag == "channel":
                cid = el.get("id")
                if cid in wanted and cid not in seen:
                    seen.add(cid)
                    channels.append(ET.tostring(el, encoding="unicode"))
                    kept += 1
                el.clear()
            elif el.tag == "programme":
                if el.get("channel") in wanted:
                    programmes.append(ET.tostring(el, encoding="unicode"))
                el.clear()
        print(f"{url}: {kept} channels", file=sys.stderr)

    if not channels:
        sys.exit("no guide data matched — refusing to overwrite the existing EPG")

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="free-iptv">\n'
           + "".join(channels) + "".join(programmes) + "</tv>\n")
    OUT.parent.mkdir(exist_ok=True)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0, filename="") as gz:
        gz.write(xml.encode("utf-8"))
    OUT.write_bytes(buf.getvalue())
    print(f"wrote {OUT.relative_to(ROOT)}: {len(channels)}/{len(wanted)} channels, "
          f"{len(programmes)} programmes, {OUT.stat().st_size // 1024} KB", file=sys.stderr)


if __name__ == "__main__":
    main()
