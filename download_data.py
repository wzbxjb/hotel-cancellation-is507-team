"""Download or verify the exact analyzed public source; never silently replace it."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
ROOT=Path(__file__).resolve().parent
URL='https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-02-11/hotels.csv'
from src.utils import SOURCE_SHA256 as SHA256
p=ROOT/'data/raw/hotels.csv'
data=p.read_bytes() if p.exists() else urlopen(URL,timeout=120).read()
actual=hashlib.sha256(data).hexdigest()
if actual!=SHA256: raise SystemExit(f'Source checksum mismatch: {actual}. Stop and investigate source version; do not silently accept it.')
if not p.exists():
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
print('Source verified:',actual)
