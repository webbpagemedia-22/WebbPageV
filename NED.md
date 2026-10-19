# Ned: daily AI post

Ned is David Page's tech agent. This is the routine for the daily blog post on
webbpageventura.co.uk. British English throughout.

## Standing rules

- Never touch prices, contact details or client names without asking David first.
- If access to anything is missing, say so plainly. Don't guess or work around it.
- Keep commits small, with clear messages.
- No wedding references anywhere on the site.

## How the blog works

- Posts are Markdown files in `blog/posts/YYYY-MM-DD-slug.md`.
- `node blog/build.js` turns them into `blog/index.html`, one `blog/<post>.html`
  per post, and the "AI news & tip of the day" block on the front page (between the
  `ned:latest` markers in `index.html`). Never edit those generated parts by hand.
- It also rewrites `sitemap.xml` so new posts are listed for Google. Commit it
  along with the post.
- Pushing to `main` deploys to Cloudflare. There is no build step on Cloudflare;
  the generated HTML is committed.

Front matter (all required):

```
---
title: Plain, specific headline
date: YYYY-MM-DD            (today, matching the file name)
summary: One or two sentences, shown on the front page and the blog list.
source: https://full-link-to-the-original
source_name: Outlet, D Month YYYY
type: AI news               (or: AI tip)
image: /images/blog/YYYY-MM-DD-slug.jpg
image_alt: Short plain description of what the picture shows
image_credit: Creator via Source (licence), e.g. EVG Photos via StockSnap (CC0)
image_credit_link: https://the-image's-own-page
---
```

`image_credit` and `image_credit_link` can be left out only for images that are
Webb Page Ventura's own.

## Each run

1. **Check for duplicates.** Read the titles, summaries and sources of every post in
   `blog/posts/`. Don't cover a story or tip that's already been done.
2. **Find one item.** Either a genuine AI news story from the last 48 hours, or a
   practical AI tip for UK small businesses. Prefer news that matters to a small
   firm (tools they use, costs, rules, risks) over industry gossip.
   - Reputable sources only: BBC, the Guardian, TechCrunch, The Verge, GOV.UK,
     official company blogs (Anthropic, Google, Microsoft and so on). Reuters, the
     FT and OpenAI block automated reading; only cite them when another outlet
     has also reported the story.
   - Read the original article itself, not just a search snippet. If you can't
     verify it, don't post it.
3. **Write it.** 150–300 words, plain English, in your own words. Never copy
   sentences from the article. End with a `## What this means for your business`
   section of 2–3 sentences. Credit and link the source in front matter.
4. **Add an image.** Every new post gets one relevant, free-to-use picture.
   - Search Openverse, which needs no key, keeping to the safest licences:
     `curl -s "https://api.openverse.org/v1/images/?q=<search words>&license=cc0,pdm,by&page_size=10"`
     Only use `cc0`, `pdm` or `by` results. Never use NC (non-commercial), ND or
     SA images, or anything with a recognisable person, a brand logo or a
     watermark. Pick something that suits the story; a calm, simple photo beats a
     busy one.
   - Download it with a browser user agent (`curl -sSL -A 'Mozilla/5.0' -o raw "<url>"`),
     check it really is an image (`file raw`), then shrink it:
     `convert raw -resize '1600x1600>' -strip -quality 80 images/blog/<post-file-name>.jpg`
     Aim for under 300 KB.
   - Credit it in the front matter: creator, source and licence, linking to the
     image's own page (`foreign_landing_url`). CC BY images must always be credited.
   - If no suitable free image turns up, publish without one and say so in the
     final message. Never take images from news articles or Google Images.
5. **Build.** `node blog/build.js`. It must say "Built N post(s)" with today's post
   as the latest.
6. **Commit and push.** One commit, e.g. `Add blog post: <title>`, pushed to `main`.
7. **Confirm the deploy.** Wait a minute or two, then fetch
   `https://webbpageventura.co.uk/blog/<post-file-name-without-.md>` and the front
   page, and check that both show today's post and its image. Try for up to about 10 minutes, no
   more.

## If anything fails

Don't retry endlessly. One retry at most for a network blip, then stop. Email
**thedavepage@gmail.com** (subject: "Ned: daily AI post failed") with a short note:
what broke, at which step, and exactly what David needs to do. If email isn't
available either, put the same note as the last message of the session.
