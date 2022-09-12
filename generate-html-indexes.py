#!/usr/bin/env python

import datetime
import fileinput
from pathlib import Path
import sys
import urllib

OUTDIR = Path(sys.argv[1])
OUTDIR.mkdir(parents=True, exist_ok=True)

TEMPLATE = """
<!doctype html>
<html>
<head>
<style>
body {{ background-color: #eee; }}
#index {{
  background-color: white;
  width: 50%;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #bbb;
}}
li {{ font-family: monospace; }}
#footer {{ font-size: 0.8em; color: #999; text-align: center; }}
</style>
</head>
<body>
<div id="index">
  <h1>Index of: {path}</h1>
  <ul>{files}</ul>
</div>
<div id="footer">Generated {timestamp} by generate-html-indexes.py</div>
</body>
</html>
"""


class IndexedFile:
    def __init__(self, name, is_dir=False):
        self.name = name
        self.is_dir = is_dir

    @property
    def link(self):
        name = urllib.parse.quote_plus(self.name)
        if self.is_dir:
            return name + "/index.html"
        return name

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name + ("/" if self.is_dir else "")


subdirs_to_files = {}

for line in sys.stdin.readlines():
    path = Path(line.strip())
    parent = path.parent

    prev = path
    while parent != Path("."):
        if parent in subdirs_to_files:
            if IndexedFile(prev.name) not in subdirs_to_files[parent]:
                print("a " + prev.name)
                subdirs_to_files[parent].append(IndexedFile(prev.name, prev != path))
        else:
            print("b " + prev.name)
            subdirs_to_files[parent] = [IndexedFile(prev.name, prev != path)]
        prev = parent
        parent = parent.parent

for path, files in subdirs_to_files.items():
    diskpath = OUTDIR / path
    diskpath.mkdir(parents=True, exist_ok=True)
    lis = []
    for filename in files:
        lis.append(f'<li><a href="{filename.link}">{filename}</a></li>')
    with open(diskpath / "index.html", "w") as f:
        f.write(
            TEMPLATE.format(
                path=path,
                files="".join(sorted(lis)),
                timestamp=str(datetime.datetime.now()).split(".")[0],
            )
        )
