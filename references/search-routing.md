# Retrieval routing

Fixed order for every tier: R1 Obscura (MCP plus CLI, each the fallback of the other), then R2 Hound MCP, then R3 Firecrawl and fallbacks. Record which route produced each source in the plan ledger and the provenance sidecar.

Runtime tools named here (Obscura, Hound MCP, Firecrawl-backed web_search and web_extract, the desktop preview pane, portal_x_search, and the browser tools) are external requirements listed in README. A line that names one is a runtime tool, not a file in this repo.

## R1: Obscura (both channels)

MCP browser tools first:

- `browser_navigate` with `networkidle0` for JS-rendered apps, `domcontentloaded` for articles.
- `browser_markdown` for token-dense content, `browser_search` to locate sections before scraping, `browser_links` for link harvests, `browser_evaluate` with a scroll loop for lazy loaders.

Obscura CLI when MCP transport fails or a second channel is needed:

```bash
obscura fetch "URL" --dump markdown     # rendered page as markdown (default)
obscura fetch "URL" --dump text         # plain text, when markdown keeps the nav chrome
obscura fetch "URL" --dump original     # raw body, binary-safe (PDFs, JSON, images)
obscura fetch "URL" --dump assets        # every sub-resource URL the page references
obscura fetch --file urls.txt --dump markdown   # batch mode, one URL per line
```

Useful flags: `--stealth` for fingerprinted gates, `--wait-until networkidle0` for client-rendered pages, `--allow-private-network` for localhost targets.

Output formats bite: `--dump links` prints tab-separated `url<TAB>text`, one hit per line, with status chatter mixed in, so parse lines starting with `http` and split on tab instead of loading it as JSON. `--dump markdown` keeps JavaScript module blobs and heavy whitespace padding, so strip `data:text/javascript,...` sequences and collapse runs of spaces and blank lines before reading or trusting the text.

Channel fallback rule: on an MCP transport Network error, fetch the identical URL through the CLI instead of retrying navigate. When the CLI returns only a gate, render the same URL through MCP. Never retry a captcha wall more than twice; pivot instead (publisher walls go to the metadata APIs below). A 404 from a plain extractor is not proof the page is gone on client-rendered sites; only a failed headless render counts.

Known page-type rules from past sessions:

- Reddit permalinks render through Obscura only on the JS UI: `old.reddit.com` returns a skip-link stub and `.../comments/<id>.json` returns the HTML shell, not JSON. Fetch the `www.reddit.com` permalink with `--dump markdown`, collapse the whitespace, strip the module blobs, and cut at `People also ask about section`; comment text survives, while post bodies and images often do not.
- When `x.com/search` is login-walled for logged-out browsers, discovery runs through DuckDuckGo HTML: `https://html.duckduckgo.com/html/?q=site%3Ax.com+<terms>`, with the same pattern for `site:reddit.com` and `site:github.com`. Result links arrive wrapped as `/l/?uddg=<encoded>`, so unquote before using them. This is usually enough for practitioner posts and threads; Portal is for historical range or broad recall.
- The `browser_navigate` result already carries the post text in its title field, so read that before spending a `browser_markdown` call; markdown is for replies, and the replies often hold the correction (for example, a claimed 248k context on 8 GB that only closes if KV spills to system RAM).
- X status and article pages open logged out via Obscura; `x.com/search` is login-walled for logged-out browsers, so discovery goes through the DuckDuckGo pattern above or `portal_x_search`.
- Space Apps challenge pages (`spaceappschallenge.org/…/challenges/<slug>/`) render as a tab shell: a fetch returns the objectives prose but no Resources list, because tab content is client-side. Treat the Resources tab as an index and take every dataset fact from the linked product landing page, CMR collection metadata (`https://cmr.earthdata.nasa.gov/search/collections.json?short_name=<SHORT_NAME>`), the algorithm theoretical basis document, or the validation literature. Obscura has returned a Network error on that host and plain `curl` exits 000 with no status line, so reach for Hound `smart_fetch` (its auto fetcher escalates to stealthy and clears the page) before concluding the page is down or the host is unavailable.
- Competition and hackathon rubrics: the current edition's site often publishes the judging process (who nominates, who reviews) and withholds the criteria. Take the criteria words from archived editions on the same domain, label them as archived rather than current, and state plainly that the current weights are unpublished, because a rubric quoted from an old edition presented as the live one is a claim the reader cannot check. Fetch the event date page in the same pass: the deadline decides how much report the run can afford.
- Earthdata products: CMR collection and granule search are public and keyless, while `earthaccess.download` and the HDF5 reads behind it need an Earthdata Login. A run without credentials records each product's access route and cost and marks downloads BLOCKED, rather than spending calls on login attempts.

## R2: Hound MCP

`smart_search` first, one broad query before narrow ones. Options: `site` for domain restriction, `exclude_sites` for noise removal, `freshness` (`day`, `week`, `month`, `year`) for the plan freshness window, `max_results` for recall depth. Read the signals: `relevance_score`, `fetch_relevance` (fetch high first), `engines_consensus` (higher means more authoritative), `source_type` (docs, paper, repo, blog, forum, reference, news), `related_queries` (follow-up angles). Semantic Scholar fires automatically for research queries, GitHub search for code, Hacker News for news and howto.

Anti-patterns: never search for a URL already in hand (fetch it); never run one search per sub-fact (one broad search plus 1 to 2 targeted fetches); never fetch every result.

`smart_fetch` with focus is the default extractor for long pages and PDFs:

- `focus='question'` keeps only BM25-relevant paragraphs (post-cache, no re-fetch; re-pass the same focus when paginating).
- `pages='1-5,9-12'` grabs known PDF ranges (the returned table of contents gives ranges).
- `urls=['u1','u2']` bulk-fetches in parallel instead of sequential calls.
- `include_links=true` harvests citations and primary-source links.

Check response signals before trusting content: `content_ok` False means shell or wall (do not cite); `next_action` tells the optimal next call; `page_type` `list` means fetch the linked pages or crawl; `auth_wall` or `paywall` means switch sources; `network.fragments` holds XHR-loaded data; `quality_score` flags garbled PDFs; `content_age_days` matters for current-state questions.

`smart_crawl` for multi-page doc sites: two-phase (map with `sitemap=true`, then fetch only the needed pages via `crawl_urls`), `focus=` to prioritize and filter, caps on pages, depth, and total chars.

## R3: Firecrawl and fallbacks

Hermes: `web_search` and `web_extract` on the configured Firecrawl backend (other agents: their search and extract tools). Then the fallbacks in `references/retrieval-fallbacks.md`: r.jina.ai reader proxy, lite DDG with dates, Wayback CDX snapshots, direct curl with a desktop user agent, Wikipedia REST API. Scholarly metadata APIs live in `references/scholarly-metadata-apis.md`.

Package registries: read the version from the package manager, not from a fetched page, because `web_extract` on a registry document can return a cached copy that is already behind (`npm view <pkg> dist-tags --json`, `npm view <pkg>@<v> version`, `pip index versions <pkg>` all hit the registry live). License text and wheel or platform matrices come from the registry JSON. When a pack pins a version and a live read disagrees, keep the pin, cite it, and record the newer one rather than silently moving.

## X as P0 source

Discovery order: Obscura first, internal browser second, desktop preview pane third, Portal tool last.

1. Obscura: MCP `browser_navigate` plus `browser_markdown` on status, article, profile, and search URLs, with the CLI (`obscura fetch --dump markdown`) as the mutual fallback per the R1 rule. Status and article pages open logged out; `x.com/search` is login-walled for logged-out browsers, so a login redirect means moving to step 2, not retrying.
2. Internal browser (dynamo-chrome MCP, persistent Chrome): `new_page` or `navigate_page` for the X URL, `take_snapshot` to read the accessibility tree, `evaluate_script` for scroll loops that trigger lazy loading. Pages in the same `isolatedContext` share cookies and storage, so an existing logged-in session carries over; confirm login (home timeline or account switcher present) before treating search renders as complete.
3. Desktop preview pane, when the runtime has one: the desktop app's own browser, so it carries the user's real X login even when a managed browser cannot start on that profile. Mechanics: the portal-x-search skill (external requirement, see README).
Hermes: runtime tool: `desktop_preview` open, then read; `drive_preview` for clicks and typing. The app's pane holds the profile, which is the normal state, not a fault. `action=read` returns the rendered visible text with `start`, `end` and `total_chars` for paging, and it includes handles, relative timestamps and engagement counts but no status URLs, so resolve every candidate through fxtwitter before citing. Refs from `drive_preview action=elements` die on navigation.
4. Portal tool (runtime tool: `portal_x_search`; if the runtime defers tools, load it first) when direct browsing is walled or needs broad historical recall. Server-side search works on the OpenRouter-routed Grok models (`x-ai/grok-4.20`, `x-ai/grok-4.3`); a `degraded: true` answer is unsourced model knowledge and must never be cited. Handles and date filters are available; a call takes 30 to 120 seconds.
Hermes: `tool_search`, then `tool_describe`, then `tool_call` load the portal tool when the runtime defers tools.

Verification before quoting: resolve every cited post through fxtwitter (`https://api.fxtwitter.com/i/status/<id>` gives created_at, likes, views, author, full text) or Obscura on the status URL. Search snippets carry no dates and stale counts. Artifact links often sit in the first reply or a follow-up post, so walk the author's next posts before concluding a link is missing. Full discovery recipe: the portal-x-search skill (external requirement, see README).

## Paper search chain (all tiers)

1. Hound `smart_search` (Semantic Scholar auto-fires) plus Scholar queries through Obscura stealth render when bot-walled; Scholar cluster links expose alternate versions.
2. Record APIs for metadata and OA status: OpenAlex (works, citations, OA locations), Crossref (DOI metadata), Unpaywall (OA PDF URL), Semantic Scholar single-DOI lookup (its search endpoint rate-limits, use sparingly).
3. arXiv through `abs` pages via fetch; the export API has returned 406 and 429 in past sessions, so never depend on it. PDFs through Hound `smart_fetch` with `pages=` ranges.
4. Publisher HTML through R1. On captcha walls (ScienceDirect and similar), stop fetching HTML and pull the abstract plus OA status from the APIs or colab.ws instead.
5. Closed-access PDFs: when the paper is load-bearing and Unpaywall shows no OA copy. Fetch through R1 or R2. If unreachable, cite the OA record plus abstract and mark full text BLOCKED. Never present an unread PDF as consulted.
