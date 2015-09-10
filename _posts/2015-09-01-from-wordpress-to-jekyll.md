---
layout: post
title:  "From WordPress to Jekyll"
date:   2015-09-09 19:04:55
---

After reading many articles and comments extolling the virtues of static HTML
(speed, efficiency, simplicity, etc.) and being a very happy GitHub user for a
while now, I decided to migrate my personal website from WordPress to Jekyll and
use GitHub Pages for hosting.

After an unsuccessful attempt to use
[`jekyll-import`](http://import.jekyllrb.com/docs/wordpress/) with my old
database credentials, I used the export tool built into WordPress to generate an
XML version of the site and ran that through
[`jekyll-import`](http://import.jekyllrb.com/docs/wordpressdotcom/), but didn't
like that posts didn't translate to Markdown. I finally ended up using
[Exitwp](https://github.com/thomasf/exitwp), which generated Markdown with YAML
front matter. Exitwp did a reasonable job, though the amount of tweaking I had
to do would have been prohibitive for anything above ~20 posts. I manually
downloaded and replaced all images, tweaked YAML metadata, had to reformat all
tables (originally generated with a WordPress plugin), and had to change some
LaTeX syntax, but got it done in a few hours.

One unexpected snag was that Kramdown, the default Markdown renderer, would not
allow for GitHub-flavored syntax highlighting in fenced code blocks, e.g.,

    ```python
    print("hello world")
    ```

This was remedied by switching over to Redcarpet, which was as simple as editing
the `markdown` entry in `_config.yml`.

I've only made a couple visual tweaks to the default Jekyll theme so far and I'm
actually quite pleased with it. So far Jekyll seems like a winner, allowing me
to easily work offline in Markdown, ditch my old web host, and hopefully write
more frequently!
