---
title: "WP-Notable In a Typo 4.0 Theme"
date: 2006-10-25
categories: [Typo, Rails]
tags: [rails, typo]
---

Here are some quick notes on getting WP-Notable style book marking into the [Scribbish](./pages/scribbish/index.html) Typo 4.0 Theme. This pattern would apply to other themes as well.

I saw post on John Wang’s Dev411 article [Notable social bookmarking/networking for Typo](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo#comments/index.html) and wanted to get the Notable book marks into my Typo 4.0 blog. I’m using the [Scribbish theme](./pages/scribbish/index.html) so there are slightly different steps to getting the John’s Notable mods applied to a theme.

I followed his steps [1, 2, and 3](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo#comments/index.html) . I skipped step 4 because I couldn’t figure out what the equivalent file/location to `app/views/articles/read.rhtml` was for a theme.

Here are a summary of my steps:

Note: When I checked up on John’s page his server was having a 500. [Here is the tar file](./tutorials/ruby/typo_notable.tgz) that he published with the png icons and `_article_notable.rhtml` partial.

**Step 1.** I copied John’s `_article_notable.rhtml` to `themes/scribbish/views/articles/`

**Step 2.** I followed John’s instructions on how to download and install his icons in the images directory. I did notice that his `_article_notable.rhtml` creates an absolute URI to the image, for instance the Newsvine image will be **/images/notable/newsvine.png**. Change the absolute url to your images if you deviate from his example.

**Step 3.**
John shows a code snippet in his step 3

```erb
<%= render :partial=>"article_notable",:locals=>{:article=>article} %>
```

Place that snippet of code inside the div with the class name “content” in the `themes/scribbish/views/articles/_article.rhtml` file. Place it at the end of the div after the end of the *if article.extended?* block.

**Step 4 (mine).** In the cache section of the admin page click “Rebuild cached HTML” link and then check to make sure the Notable bookmarks show in your articles.

**Extra (from me)** Add Notable bookmarks to the Pages view

Change your `app/views/articles/view_page.rhtml` to look like this:

```erb
<div id="viewpage" >
  <%= @page.full_html %>
</div>
<%= render :partial=>"page_notable",:locals=>{:article=>@page} %>
```

Copy `_article_notable.rhtml` into a new partial named `app/views/articles/_page_notable.rhtml`

Now all your pages have Notable buttons like [My Homepage in my Blog](./pages/home)

I saw post on John Wang’s Dev411 article [Notable social bookmarking/networking for Typo](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo#comments/index.html) and wanted to get the Notable book marks into my Typo 4.0 blog. I’m using the [Scribbish theme](./pages/scribbish/index.html) so there are slightly different steps to getting the John’s Notable mods applied to a theme.

I followed his steps [1, 2, and 3](./blog/2006/09/02/notable-social-bookmarking-networking-for-typo#comments/index.html) . I skipped step 4 because I couldn’t figure out what the equivalent file/location to `app/views/articles/read.rhtml` was for a theme.

Here are a summary of my steps:

Note: When I checked up on John’s page his server was having a 500. [Here is the tar file](./tutorials/ruby/typo_notable.tgz) that he published with the png icons and `_article_notable.rhtml` partial.

**Step 1.** I copied John’s `_article_notable.rhtml` to `themes/scribbish/views/articles/`

**Step 2.** I followed John’s instructions on how to download and install his icons in the images directory. I did notice that his `_article_notable.rhtml` creates an absolute URI to the image, for instance the Newsvine image will be **/images/notable/newsvine.png**. Change the absolute url to your images if you deviate from his example.

**Step 3.**
John shows a code snippet in his step 3

```erb
<%= render :partial=>"article_notable",:locals=>{:article=>article} %>
```

Place that snippet of code inside the div with the class name “content” in the `themes/scribbish/views/articles/_article.rhtml` file. Place it at the end of the div after the end of the *if article.extended?* block.

**Step 4 (mine).** In the cache section of the admin page click “Rebuild cached HTML” link and then check to make sure the Notable bookmarks show in your articles.

**Extra (from me)** Add Notable bookmarks to the Pages view

Change your `app/views/articles/view_page.rhtml` to look like this:

```erb
<div id="viewpage" >
  <%= @page.full_html %>
</div>
<%= render :partial=>"page_notable",:locals=>{:article=>@page} %>
```

Copy `_article_notable.rhtml` into a new partial named `app/views/articles/_page_notable.rhtml`

Now all your pages have Notable buttons like [My Homepage in my Blog](./pages/home)
