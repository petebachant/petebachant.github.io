#!/usr/bin/env python
"""Crude script to make make a post from a Jupyter Notebook."""

import subprocess
import os

yaml_template = \
'''---
title: "{title}"
date: {date}
layout: post
comments: true
---
'''

fpath_in = os.path.join(
    os.path.expanduser("~"),
    "Google Drive",
    "Research",
    "Reverse numerics",
    "heat-equation",
    "notebook.ipynb"
)

date = "2016-12-03"

cmd = 'jupyter nbconvert "{fpath_in}" --to markdown --output-dir .'

def convert_to_jekyll(input_md_fpath):
    """Replace title, add YAML block, and rename."""
    with open(input_md_fpath) as f:
        txt = ""
        title = None
        for line in f.readlines():
            if line.startswith("# ") and title is None:
                title_line = line
                title = line.replace("#", "").strip()
            elif title is not None:
                txt += line
    txt = yaml_template.format(title=title, date=date) + "\n" + txt
    post_fname = date + "-" + "-".join(title.lower().split()) + ".md"
    post_fname = post_fname.replace("'", "")
    with open(os.path.join("_posts", post_fname), "w") as f:
        f.write(txt)
    os.remove(input_md_fpath)

# Convert to Markdown
subprocess.call(cmd.format(fpath_in=fpath_in), shell=True)
# Convert to Jekyll Markdown
convert_to_jekyll("notebook.md")
