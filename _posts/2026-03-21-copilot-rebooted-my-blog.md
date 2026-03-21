---
title: "I used Copilot to reboot my blog"
date: 2026-03-21
---


It's 2026 and I wanted to reboot my blog. The problem was my blog has been dead for over a decade. My last post was in January 2013 — a quick write up about distributing scripts as gist micro-gems. Since then, silence. But the content was still out there on the Internet Archive, and I figured it was time to bring it home.

*NOTE:* Real words from Mike: Copilot w/ Claude Opus 4.6 wrote this blog post
with the following prompt and outline. I think the voice is a litte bit cheesy
... I'll try a different model next time. Your slop detector will trigger a
little bit on this reading. But the content is representative of the subject I
cover with some added history I wouldn't have thought to write about.

```
Agent:
Take the outline in today's blog post and fill it out using my voice from _pages and _posts to fill in the information I want to cover in the post.

Outline:
- It's 2026, I wanted to reboot my blog but I had to resurrect it from the Internet Archive
- I saw a copy of plact.cx on the Internet Archive and was reminded how much I liked the The Sun tarot card (Smith-Waite deck) that I used in the page layout template
- Programming this by hand would have taken a lot of effort
- I had Copilot using the Claude Opus 4.6 model rebuild this blog and pages
- It took about five hours to clock time to put this all together
- I'll share the prompts I used to get here
```

## The blog platforms of my life

I've been through a few blog platforms over the years. I started on [Typo](https://github.com/fdv/typo) back in 2006 when I first joined the Rails community. I was blogging all the time about what I was learning — TDD in Rails, decoding MMS messages, Camping microapps, you name it. I ran Typo at blog.mondragon.cc and wrote 24 posts between 2006 and 2007.

Then Typo became over featured for my needs. I endured as Frédéric de Villamil refactored and modernized the code base, but it became a burden to maintain my fork. In 2012, I switched to [Obtvse](https://github.com/NateW/obtvse), a minimal Rails blog app that fit how I wanted to blog. I ran that at plasti.cx and wrote another 6 posts between 2012 and 2013. I was also maintaining some personal pages there — an about page, my bowfishing for carp page that has existed in one form or another since 1995, and a ThinkPad T42 Linux setup guide.

And then life happened and I stopped blogging entirely.

## Resurrecting from the Internet Archive

I found copies of both blog.mondragon.cc and plasti.cx on the Internet Archive and downloaded the HTML. That gave me about 30 blog posts across two completely different blog platforms, plus three static pages, and about 60 images. The Typo pages were XHTML 1.0 Strict with `<div class="atomentry">` wrappers, comments sections, and carrier-injected social sharing markup. The Obtvse pages were HTML5 with `<section id="post-N">` elements and `<time>` tags for dates. Completely different structures.

Programming the conversion by hand would have taken a lot of effort. Each platform had its own HTML structure, its own way of storing dates and categories and tags and code blocks. I would have needed to write parsers for each, strip out the junk (comments, social sharing widgets, tracking markup), extract the real content, convert it to Markdown, and generate proper Jekyll front matter. Then there were the broken links, the missing images, the relative paths pointing to dead domains.

## Enter Copilot

I had GitHub Copilot using the Claude Opus 4.6 model rebuild this whole blog. I opened VS Code, started a conversation, and let it drive.

Here's roughly what happened:

1. **Explored the old content** — Copilot dug through the downloaded Internet Archive HTML to understand the structure of both Typo and Obtvse pages. It identified the content divs, date formats, category and tag markup, and code blocks for each platform.

2. **Wrote Python import scripts** — It built two separate Python scripts using BeautifulSoup and markdownify. One for the 24 Typo blog posts from blog.mondragon.cc, one for the 6 Obtvse posts and 3 pages from plasti.cx. Each script handled the specifics of its platform — stripping comments and tracking markup from Typo, parsing `<time>` elements from Obtvse, detecting code languages from CSS classes, fixing image paths.

3. **Set up the Jekyll site** — Built out the `_config.yml`, layouts, includes, navigation, the whole thing. Permalink structure matches my old Typo URLs (`/:year/:month/:day/:title/`) so existing links from the internet still work.

4. **Fixed broken content** — Updated dead Ruby doc links in my old posts to point to ruby-doc.org/3.4.1. Fixed double-encoded HTML entities in titles. Converted relative image paths from `./files/` to `/assets/images/`.

5. **Restructured pages** — Imported my old plasti.cx about page (the one with Linus signing my plate at LinuxWorld '99 and me doing a frontside at Rotary Skateboard Park), then when I decided I wanted a cleaner about page, moved that content to `/old-about/` and set up a simple about page linking to the sub-pages.

6. **Added SEO** — Dropped in the jekyll-sitemap plugin for a proper sitemap.xml.

## I was reminded how much I like The Sun

While I was looking at plasti.cx on the Internet Archive I was reminded how much I like The Sun tarot card from a Smith-Waite deck. I had used it as the visual identity for plasti.cx. That kind of thing — rediscovering bits of your past self in old website layouts — is what made this project feel worthwhile.

## Five hours

It took about five hours of clock time to put this all together. That includes the back and forth of reviewing what Copilot was doing, answering questions about my preferences (yes preserve categories and tags, yes use Python, yes auto-detect code languages), tracking down images that weren't in the Internet Archive download, and iterating on the page structure.

For context, the import scripts alone dealt with two different HTML parsers, custom Markdown converters with language-aware code block handling, front matter generation with dates and categories and tags, and image path rewriting. The kind of thing that would have been a weekend project if I was coding it by hand. Copilot had working scripts on the first pass, and when things broke (markdownify's API had changed between versions — `convert_as_inline` became `parent_tags`) it figured out the fix.

## The prompts

```
Ask:
This is the repo is for my github user "monde"'s github pages site monde.github.io.
I want to turn the repo into a static file blog site with the source of the articles rendered from markdown.
What are the most commonly used static content management tool/library's currently used? I would prefer to use an opensource project.

Ask:
I have an old blog site but the content for it only exists in the Internet Archive's Wayback Machine. How can we download my old content quickly? Like with curl or other API calls?

Ask:
what is common page structure and navigation for a jekyll site with many pages

Agent:
Apply all of your recommendations and examples into the current project.
I also would like two example blog posts that have the following structure:
their URIs are "/blog/{YYYY}/{MM}/{DD}/{slug}" wehre the URI path is year, month, day, and the slug for the page from the blog post's title.
Add two example blog posts one on the path "/2003/12/01/hello" with a short bit of lorem ipsum content. And the other with the path "/2004/09/05/world" in the same format as the hello blog post.

Agent:
The footer needs css padding for the left side of the text

Agent:
modify the for link loop that produces <li> elements. If the object is a "link" fill in the correct <a> values if the object is a "image" fill in the correct <img> values

Agent:
modify the for post loop to only iterate on the first three items from site.posts

Plan:
I want you to verify this command to import my old blog content:

run this command in this repo's root `find _old-blog-content/websites/blog.mondragon.cc | grep "\d\{4\}\/\d\{2\}\/\d\{2\}\/[a-z,A-Z,0-9,-]\+\/index.html"`
to find my old blog posts

- Each file found is an old blog post.
- The path to file has a date embedded into it YYYY/MM/DD and then the slug for the page.
- Turn each of this pages into a jekyll github formatted markdown  file with meta data "title" which is the <title> from the index.html and the "data" meta data is the date from the from the original post
- Some of the input index.html has comments from a blogging platform, we want those scrubbed out.

Tell me if you think this is a good plan and do you have any other recomendations or modifications to the plan.

Agent:
Run your plan

Plan:
This is a follow on from your previous plan.
The directory _old-blog-content/websites/plasti.cx holds content from my newer blog. You'll find duplicate content of old blog posts to blog.mondragon.cc imported to _posts in this repo, ignore that old content.
I think there are only these blog posts to import

distribute-scripts-as-gist-micro-gems
maintaining-my-copy-of-obtvse
report-resque-exceptions-to-honeybadger
seattle-dot-rb-irb-presentation
seattle-dot-rb-refactoring-talk
switched-my-blog-to-obtvse-from-typo

There are also three pages websites/plasti.cx/pages home, carp, and tp-t42 from my earliest website, I want to import those pages also but not as blog posts. They should get their own navigation in the side bar.

Agent:
Run your plan

Agent:
- Take the content from the current about.md and call it an old about page.
- Revert to the pervious version of the about.md
- Remove "Carp" and "ThinkPad T42" links from the left hand navigation
- Add links to the old about page, "Carp" and "ThinkPad T42", in the current about.md

Ask:
Are sitemaps to benefit webcrawlers still a thing?

Agent:
Run your suggestions on sitemaps. If .github/workflows/jekyll.yml needs to be updated for sitemap generation do so.
```