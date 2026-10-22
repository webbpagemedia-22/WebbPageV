---
title: "PHP2Shell: is your website safe?"
date: 2026-10-22
summary: PHP, the software behind most of the world's websites, has rushed out emergency fixes for two serious security holes that AI helped find. If your site runs on WordPress or similar, check it's been updated.
source: https://www.bleepingcomputer.com/news/security/php-ships-emergency-patches-for-critical-php2shell-flaws/
source_name: BleepingComputer, 21 October 2026 (also reported by The Next Web)
type: AI news
---

PHP is the behind-the-scenes language that powers a huge share of the web, including most WordPress sites. On 21 October its developers released emergency fixes for two critical flaws, nicknamed PHP2Shell.

The flaws let an attacker run their own code on a web server without logging in. PHP's own team called updating "the only safe choice", and the UK's National Cyber Security Centre told organisations to update straight away, or take affected systems offline until they could. Cloudflare said it was already seeing early attacks before the fixes came out.

The AI angle is striking. Researchers at the security firm Calif found the first bug in August using one of OpenAI's models, during an audit of PHP's code. A team at Wiz found the same problems weeks later, also with AI help. It's the second time in a few months that AI-assisted research has forced a mass round of updates, after a batch of WordPress flaws in July.

The fixed versions are PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35. Anything older than 8.2 no longer gets official security updates.

## What this means for your business

If you have a website, ask whoever hosts or looks after it one question this week: "Are we on a patched version of PHP?" Most good hosts will already have done it, but it's worth a two-minute email to be sure. And if your site is running on very old software, now is the time to get it brought up to date.
