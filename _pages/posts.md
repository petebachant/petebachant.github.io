---
layout: page
title: Posts
permalink: /posts/
exclude_from_navigation: true
comments: false
---

{% for post in site.posts %}
{{ post.date | date: "%b %-d, %Y" }} -- [{{ post.title }}]({{ post.url | prepend: site.baseurl }})
{% endfor %}
