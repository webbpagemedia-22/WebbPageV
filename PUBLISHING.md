# How agents' work goes live

This is the one home for how queued work reaches webbpageventura.co.uk and
foresthounds.co.uk. Agent prompts and the `ogd` skill link here instead of
repeating it. If the process changes, change it here only.

## The route

1. **Queue.** Scheduled agents never push to GitHub and never write through the
   GitHub connector. Why: scheduled runs have no push access, and one audited
   route keeps mistakes off the live sites. They queue their work instead (below).
2. **Audit.** Ned's website audit runs every night at about 04:41 UK time. It reads
   everything queued and writes "Ned verdict YYYY-MM-DD" in the Queue folder, with
   one APPROVE or REJECT line per item.
3. **Publish.** OGD publishes what Ned approved **when David says "Morning OGD"
   at about 07:30** (or any later "Hi OGD" check-in). There is no automatic
   publishing run, so queued work waits until then. Never tell David something is
   live because it was queued.

## The daily rhythm (from 19 Nov 2026)

All times UK. The night shift runs in the cloud while David sleeps; nothing
needs his Mac.

| Time | Who | What |
|---|---|---|
| Mon 01:13 | Napoleon | SEO plan and Ned's blog ideas |
| 02:13 | Ned | Writes the daily post, queues it as a Gmail draft |
| 02:43 | Forest Hounds developer | Queues an "FH dev" patch |
| 02:57 | WPV developer | Queues a "WPV dev" patch |
| Weekdays 03:23 | Sully | Sales emails as Gmail drafts only |
| 04:41 | Ned | Audit: writes "Ned verdict YYYY-MM-DD" |
| Weekdays 06:13 | Forest Hounds admin | Enquiries and calendar summary email |
| 06:41 | OGD roll-up | Checks every run, John's housing sweep, Sterling, writes the hub briefing |
| ~07:30 | David: "Morning OGD" | OGD plans the LEGO route (Tue–Thu), publishes, briefs, Sully review |
| 08:13 | OGD nudge | Only if David hasn't checked in |

Developers and Ned build on whatever is still waiting in the queue, so a missed
morning only delays publishing; nothing is lost.
   - Webb Page Ventura: approved work goes to `main`, which deploys live.
   - Forest Hounds: approved work goes to a branch `web-dev/YYYY-MM-DD-<topic>`
     and a pull request. Nothing goes to `main` except David's own merges.

## The Queue

Google Drive folder "Queue" inside "OGD publishing queue", id
`11uTZRsR-Pr33Y00SiJXgdjXD-VlDLC7d`.

- A file whose title contains DONE has been published. One whose title contains
  REJECTED will not be. Anything else is still waiting.
- Ned's daily post is queued differently: a Gmail draft with the subject
  "OGD QUEUE: Ned post YYYY-MM-DD". Its format is in Ned's own prompt.

## Queueing a patch

1. Commit locally with clear messages that say what each change did and why, so
   Ned can check the patch against them.
2. `git format-patch --binary --stdout origin/main > work.patch` (or against the
   commit you started from).
3. Upload it with `mcp__Google_Drive__create_file`: the title your prompt gives,
   textContent = the patch, contentMimeType "text/plain",
   disableConversionToGoogleType true, parentId = the Queue folder id above.
4. Keep the patch under about 1 MB. Leave big images out and say so in your report.
5. If you changed nothing, upload nothing.

## Reading pages with WebFetch

WebFetch puts a "---" block of the page's head tags (canonical:, meta-og:title:
and so on) at the top of every page it reads. That is WebFetch's own summary, not
part of the page; it appears on every site. Ignore it, and only report a display
problem if the page's real HTML or a real browser shows it. WebFetch also strips
scripts, so confirm things like the Google tag from the repository and say how you
checked. Add a `?v=<anything>` query to dodge its cache.
