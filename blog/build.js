#!/usr/bin/env node
// Builds the blog from blog/posts/*.md into plain HTML.
//   node blog/build.js
// Writes blog/index.html, one blog/<post>.html per post, and the
// "AI news & tip of the day" block on the front page (between the
// ned:latest markers in index.html). No dependencies, no network.
// Fails loudly on a bad post so nothing half-built gets committed.

const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const BLOG = path.join(ROOT, "blog");
const POSTS = path.join(BLOG, "posts");
const HOME = path.join(ROOT, "index.html");
const SITE = "https://webbpageventura.co.uk";
const TYPES = ["AI news", "AI tip"];
const REQUIRED = ["title", "date", "summary", "source", "source_name", "type"];
const MONTHS = ["January", "February", "March", "April", "May", "June", "July",
  "August", "September", "October", "November", "December"];

function fail(msg) {
  console.error("Blog build failed: " + msg);
  process.exit(1);
}

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

function ukDate(iso) {
  const [y, m, d] = iso.split("-").map(Number);
  return `${d} ${MONTHS[m - 1]} ${y}`;
}

function parseFrontMatter(file, text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  if (!m) fail(`${file}: missing front matter between --- lines`);
  const meta = {};
  for (const line of m[1].split(/\r?\n/)) {
    if (!line.trim()) continue;
    const kv = line.match(/^([a-z_]+):\s*(.*)$/);
    if (!kv) fail(`${file}: can't read front matter line "${line}"`);
    meta[kv[1]] = kv[2].trim().replace(/^"(.*)"$/, "$1").replace(/^'(.*)'$/, "$1");
  }
  return { meta, body: m[2] };
}

// Inline Markdown: links, bold, italic. Text is escaped first.
function inline(s) {
  return esc(s)
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g, (_, t, u) => `<a href="${u}">${t}</a>`)
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>");
}

// Block Markdown: ## and ### headings, - and 1. lists, paragraphs.
function markdown(md) {
  const out = [];
  for (const block of md.trim().split(/\r?\n\s*\r?\n/)) {
    const lines = block.split(/\r?\n/).map((l) => l.trim());
    const h = lines[0].match(/^(#{2,3})\s+(.*)$/);
    if (h && lines.length === 1) {
      out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`);
    } else if (lines.every((l) => /^[-*]\s+/.test(l))) {
      out.push("<ul>" + lines.map((l) => `<li>${inline(l.replace(/^[-*]\s+/, ""))}</li>`).join("") + "</ul>");
    } else if (lines.every((l) => /^\d+\.\s+/.test(l))) {
      out.push("<ol>" + lines.map((l) => `<li>${inline(l.replace(/^\d+\.\s+/, ""))}</li>`).join("") + "</ol>");
    } else {
      out.push(`<p>${inline(lines.join(" "))}</p>`);
    }
  }
  return out.join("\n");
}

function loadPosts() {
  const files = fs.readdirSync(POSTS).filter((f) => f.endsWith(".md")).sort();
  const posts = files.map((file) => {
    const slug = file.replace(/\.md$/, "");
    if (!/^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) {
      fail(`${file}: name must look like YYYY-MM-DD-some-slug.md`);
    }
    const { meta, body } = parseFrontMatter(file, fs.readFileSync(path.join(POSTS, file), "utf8"));
    for (const k of REQUIRED) if (!meta[k]) fail(`${file}: front matter is missing "${k}"`);
    if (!TYPES.includes(meta.type)) fail(`${file}: type must be one of ${TYPES.join(" / ")}`);
    if (meta.date !== slug.slice(0, 10)) fail(`${file}: date ${meta.date} doesn't match the file name`);
    if (!/^https?:\/\//.test(meta.source)) fail(`${file}: source must be a full link`);
    if (!/What this means for your business/.test(body)) fail(`${file}: needs a "What this means for your business" section`);
    return { ...meta, slug, url: `/blog/${slug}`, html: markdown(body) };
  });
  // Newest first; same-day posts by file name, last one first.
  return posts.reverse();
}

function page({ title, description, canonical, current, main }) {
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="${esc(description)}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:type" content="website">
<meta property="og:image" content="${SITE}/images/brand/share.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:url" content="${SITE}${canonical}">
<link rel="canonical" href="${SITE}${canonical}">
<link rel="icon" href="/images/brand/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/images/brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<style>html{scroll-behavior:smooth}body{margin:0}img{max-width:100%}@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}</style>
<title>${esc(title)} | Webb Page Ventura</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Instrument+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/styles.css">

</head>
<body>
<header class="site">
  <div class="wrap site-row">
    <a class="wordmark" href="/"><img class="logo-mark" src="/images/brand/logo-mark.png" width="169" height="172" alt=""><span class="wordmark-text">Webb Page <span>Ventura</span></span></a>
    <nav class="site-nav" aria-label="Main">
      <a href="/services">Services</a>
      <a href="/how-it-works">How it works</a>
      <a href="/experience">Experience</a>
      <a href="/blog/"${current ? ' aria-current="page"' : ""}>Blog</a>
      <a href="/#about">About us</a>
      <a href="/#contact">Contact</a>
    </nav>
  </div>
</header>

<main class="wrap">
${main}
</main>

<footer class="site">
  <div class="wrap site-row">
    <span>© 2026 Webb Page Ventura</span>
    <span>AI setup, social media and customer service training for small businesses</span>
  </div>
</footer>
</body>
</html>
`;
}

function meta(p) {
  return `<p class="eyebrow post-meta"><span class="tag">${esc(p.type)}</span> <time datetime="${p.date}">${ukDate(p.date)}</time></p>`;
}

function postPage(p) {
  return page({
    title: p.title,
    description: p.summary,
    canonical: p.url,
    current: true,
    main: `
  <article class="post">
    <header class="page-head stack">
      ${meta(p)}
      <h1>${esc(p.title)}</h1>
      <p class="lede">${esc(p.summary)}</p>
    </header>
    <div class="prose">
${p.html}
    </div>
    <p class="source-credit">Source: <a href="${esc(p.source)}">${esc(p.source_name)}</a>. This is our own summary; read the original for the full story.</p>
    <p><a class="text-link" href="/blog/">All posts</a></p>
  </article>
`,
  });
}

function indexPage(posts) {
  const items = posts.map((p) => `      <li>
        ${meta(p)}
        <h2><a href="${p.url}">${esc(p.title)}</a></h2>
        <p>${esc(p.summary)}</p>
      </li>`).join("\n");
  return page({
    title: "AI news and tips",
    description: "One useful bit of AI news or a practical AI tip each day, written in plain English for UK small businesses.",
    canonical: "/blog/",
    current: true,
    main: `
  <section class="page-head stack">
    <p class="eyebrow">Blog</p>
    <h1>AI news and tips, in plain English.</h1>
    <p class="lede">One useful bit of AI news or a practical tip each day, and what it means for a small business.</p>
  </section>

  <section aria-label="All posts">
    <ul class="post-list">
${items}
    </ul>
  </section>
`,
  });
}

function homeBlock(posts) {
  const [latest, ...rest] = posts;
  const earlier = rest.slice(0, 3).map((p) => `          <li><a href="${p.url}">${esc(p.title)}</a> <time datetime="${p.date}">${ukDate(p.date)}</time></li>`).join("\n");
  return `<!-- ned:latest:start (generated by blog/build.js, don't edit by hand) -->
  <section id="ai-today" aria-labelledby="ai-today-h">
    <div class="section-head">
      <p class="eyebrow">AI news &amp; tip of the day</p>
      <h2 id="ai-today-h">One useful AI thing a day.</h2>
    </div>
    <div class="today">
      <article class="today-latest">
        ${meta(latest)}
        <h3><a href="${latest.url}">${esc(latest.title)}</a></h3>
        <p class="today-summary">${esc(latest.summary)}</p>
        <a class="text-link" href="${latest.url}">Read more</a>
      </article>
      <div class="today-earlier">
        <p class="eyebrow">Earlier</p>
${earlier ? `        <ul>\n${earlier}\n        </ul>` : `        <p>More posts coming soon.</p>`}
        <a class="text-link" href="/blog/">See all posts</a>
      </div>
    </div>
  </section>
  <!-- ned:latest:end -->`;
}

const posts = loadPosts();
if (!posts.length) fail("no posts in blog/posts");

// Remove pages for posts that no longer exist, then write the rest.
const keep = new Set(posts.map((p) => p.slug + ".html").concat("index.html"));
for (const f of fs.readdirSync(BLOG)) {
  if (f.endsWith(".html") && !keep.has(f)) fs.unlinkSync(path.join(BLOG, f));
}
for (const p of posts) fs.writeFileSync(path.join(BLOG, p.slug + ".html"), postPage(p));
fs.writeFileSync(path.join(BLOG, "index.html"), indexPage(posts));

const home = fs.readFileSync(HOME, "utf8");
const marker = /<!-- ned:latest:start[\s\S]*?<!-- ned:latest:end -->/;
if (!marker.test(home)) fail("index.html is missing the ned:latest markers");
fs.writeFileSync(HOME, home.replace(marker, homeBlock(posts)));

console.log(`Built ${posts.length} post(s). Latest: ${posts[0].date} ${posts[0].title}`);
