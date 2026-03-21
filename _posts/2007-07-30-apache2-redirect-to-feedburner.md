---
title: "Apache2 Redirect To Feedburner"
date: 2007-07-30
categories: [Apache]
tags: [apache]
---

This is how I’m doing a 302 redirect to Feedburner from my Apache2 virtual host settings for this blog. Its only for the main articles syndication in [RSS](./xml/rss20/feed.xml) and [Atom](./xml/atom/feed.xml) . Everyone is redirected to Feedburner except for their web crawling bot. I’m doing this so people can see Feedburner’s shiny widget (  ) in the sidebar showing that only 1 or 2 people subscribe to my blog.

I put the following in between the **RewriteEngine On** statement and the static maintenance statement **RewriteCond %{DOCUMENT\_ROOT}/system/maintenance.html -f** covered [in this post describing an Apache vhosts setup for a Rails app](./articles/2007/04/08/maintaining-your-own-typo-4-0-3)

```bash
# 302 temporary, 301 permanent
RewriteCond %{HTTP_USER_AGENT}  !^FeedBurner/.*
RewriteRule ^/xml/rss20/feed.xml$ http://feeds.feedburner.com/mondragon/PQVR [R=302,L]
RewriteRule ^/xml/atom/feed.xml$ http://feeds.feedburner.com/mondragon/PQVR [R=302,L]
```
