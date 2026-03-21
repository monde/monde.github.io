---
title: Blog
permalink: /blog/
nav_order: 2
---

{% for post in site.posts %}
<time>{{ post.date | date: "%B %d, %Y" }}</time>
<section>
  <div class="contain">
    <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
    <p>{{ post.excerpt | strip_html | truncatewords: 30 }}</p>
  </div>
</section>
{% endfor %}
