#!/usr/bin/env python

import datetime
import fileinput
from pathlib import Path
import sys

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
  <h1>{path}</h1>
  <ul>{files}</ul>
</div>
<div id="footer">Generated {timestamp} by generate-html-indexes.py</div>
</body>
</html>
"""

subdirs_to_files = {}

for line in sys.stdin.readlines():
    path = Path(line)
    parent = path.parent

    prev = path
    while parent != Path("."):
        if parent in subdirs_to_files:
            if prev.name not in subdirs_to_files[parent]:
                subdirs_to_files[parent].append(prev.name)
        else:
            subdirs_to_files[parent] = [prev.name]
        prev = parent
        parent = parent.parent

    if path.parent in subdirs_to_files:
        if path.name not in subdirs_to_files[path.parent]:
            subdirs_to_files[path.parent].append(path.name)
    else:
        subdirs_to_files[path.parent] = [path.name]


for path, files in subdirs_to_files.items():
    diskpath = OUTDIR / path
    diskpath.mkdir(parents=True, exist_ok=True)
    lis = []
    for filename in files:
        lis.append(f'<li><a href="{filename}">{filename}</a></li>')
    with open(diskpath / "index.html", "w") as f:
        f.write(
            TEMPLATE.format(
                path=path,
                files="".join(sorted(lis)),
                timestamp=str(datetime.datetime.now()).split(".")[0],
            )
        )
