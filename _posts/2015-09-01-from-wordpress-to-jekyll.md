---
layout: post
title:  "From WordPress to Jekyll"
date:   2015-09-01 22:04:55
---

After reading many articles and comments extolling the virtues of static HTML
and being a very happy GitHub user for a while now, I decided to migrate my
personal website from WordPress to Jekyll with GitHub Pages for hosting.

I tried to use Jekyll's importer with my old database credentials but for some
reason that wouldn't work. I ended up using the export tool built into WordPress
to generate an XML version of the site. This was then converted into Jekyll
posts and pages using [exitwp](https://github.com/thomasf/exitwp). Exitwp did a
reasonable job, though the amount of tweaking I had to do would have been
prohibitive for anything above ~20 posts. I manually downloaded and replaced all
images, had to reformat all tables (they were generated with a WordPress
plugin), and had to change some LaTeX syntax, but got it done in a few hours.

I've only made a couple visual tweaks to the default Jekyll theme so far and I'm
actually quite pleased with it.

## Markdown renderer

Kramdown would not allow for syntax highlighting in fenced code blocks, e.g.,

    ```python
    print("hello world")
    ```

so I switched over to Redcarpet (as simple as editing the `markdown` entry in
`_config.yml`), and all is well.
