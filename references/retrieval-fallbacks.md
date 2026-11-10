# Retrieval fallbacks

Copied sections for the R3 route. Provenance: README.md.

## Primary pattern: r.jina.ai reader proxy

Prefix any URL with `https://r.jina.ai/` and curl it. Returns clean markdown, and in
many cases passes Cloudflare that blocks both curl and the browser.

```bash
# Render a blocked page as markdown (e.g. Cloudflare-protected blog)
curl -s "https://r.jina.ai/https://blog.example.com/the-best-list/"

# Search WITH snippets and dates via lite DuckDuckGo through jina (best quality)
curl -s "https://r.jina.ai/https://lite.duckduckgo.com/lite/?q=Brand+holiday+cookies+2025"
```

Lite DDG results come back as numbered markdown:

```
1.[Title](https://duckduckgo.com/l/?uddg=...)
snippet text...
display-url.com/path
date
```

Parse with: `re.split(r'\n(?=\d+\.\[)', raw)` then
`re.match(r'\d+\.\[([^\]]+)\]\((http[^)]+)\)\n?(.*)', block, re.S)`: lines[0] is the
snippet, lines[1] the display URL, and a `\d{4}-\d{2}-\d{2}` scan finds dates (crucial
for "as of <date>" questions and for telling 2025-season products from evergreen listings).

## Archive fallback: Wayback Machine CDX

When the live URL is blocked and jina also fails:

```bash
# Find snapshots (exact URL)
curl -s "http://web.archive.org/cdx/search/cdx?url=<url>&output=json&limit=5&from=2024"
# Domain-wide scan with URL filter
curl -s "http://web.archive.org/cdx/search/cdx?url=blog.example.com&matchType=domain&output=json&collapse=urlkey&filter=original:.*brands.*"
# Then fetch a snapshot: http://web.archive.org/web/<timestamp>/<url>
```

Notes: the availability API (`archive.org/wayback/available`) 429s easily: sleep 3-5s
and retry, or skip straight to CDX. `[]` from CDX means no snapshot exists; don't
conclude the page never existed from one CDX call alone: try the trailing-slash and
no-slash variants.

## Direct curl fallback (no proxy, when jina is also throttled/unavailable)

Desktop UA plus direct curl beats bare curl on many sites:

```bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
curl -sL --max-time 30 -A "$UA" "<url>" -o out.html
```

- **Keep `-L`, and check what came back.** A raw-file or release URL often answers with a redirect. Without `-L`, curl saves the redirect body and still exits 0, so the file looks fetched but is empty or wrong. Print `-w '%{http_code} %{size_download} %{url_effective}\n'` once to tell a redirect (3xx, near-zero bytes) from a real empty file.
- **Wikipedia REST API is rarely blocked**: `https://en.wikipedia.org/api/rest_v1/page/html/<Page_Title>`
  returns full page HTML. Strip tags with python (`re.sub(r'<[^>]+>',' ',raw)`, `html.unescape`,
  collapse whitespace), then print context windows around keywords (names, "resigned",
  "succeeded by", "assumed office"): great for roster/membership-date checks and succession facts.
  The **plain article URL** (`https://en.wikipedia.org/wiki/<Title>` with a desktop UA) also works
  directly and is simpler: same strip-then-grep approach with `re.finditer(kw, text, re.I)` and a
  ±250-char window per hit, first hit per keyword is usually enough.
- **Raw lite DDG without jina** also works directly: `https://lite.duckduckgo.com/lite/?q=<query>`
  returns HTML whose results are `<a href="//duckduckgo.com/l/?uddg=<urlencoded>&rut=...">Title</a>`:
  extract with `re.findall(r'href="([^"]*uddg[^"]*)"[^>]*>(.*?)</a>', html, re.S)` to recover real
  target URLs (this surfaced a direct `2023_BPI_Senate.pdf` download link).
- **Direct Brave HTML (no jina) also works** (tested 2026-08): with a desktop UA,
  `https://search.brave.com/search?q=<urlencoded>` returns titles + snippets in plain anchors:
  extract with `re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S)`, dedupe
  by URL, skip empty titles. Same session: Bing → Cloudflare "Verify you are human" iframe, Google
  → /sorry redirect, DDG html/lite and Mojeek → empty, so Brave was the only engine that answered.
- **Some sites emit single-quoted href attributes** (e.g. thelugarcenter.org after relaunch):
  grep `href='...'`, not `href="..."`, or you'll conclude "no links on page".
- Bing raw HTML returns no parseable anchors (consent wall); skip it outside jina.
- Akamai-gated sites (senate.gov, openthebooks.com) and cookie-gated React (plannedparenthoodaction.org)
  still need a real browser: curl shows only the gate. Mark those "unverified", never "unavailable".

## Long pages and whole repositories

- `web_extract` returns the head and tail of a page that exceeds its character budget (observed: about 9 KB and 3 KB of a 65 KB spec page) and saves the full text to the path named in its footer. Read that file in pages (`read_file` with offset and limit) instead of fetching again to see the middle.
- For a repository, `git clone --depth 1 <url> <dir>` and read the files directly. The clone holds the whole tree, including `references/` and `scripts/` folders that a page render drops, and `git log -1 --format=%cd` gives the commit date to cite.
- For a single raw file, `curl -fsSL -m 30 -o <file> <url>` into the run folder keeps a copy that a verifier can open later.
- A marketplace page (skills.sh, a plugin listing) or a GitHub `blob` page can truncate in `web_extract`: the copy stops partway through. Read the repository instead. Fetch its file list once with `curl -fsS https://api.github.com/repos/<owner>/<repo>/git/trees/HEAD?recursive=1` (confirm the response's `truncated` field is false; the unauthenticated API allows about 60 calls an hour, so reuse the list), filter the paths by the skill's directory name, then fetch each file from `https://raw.githubusercontent.com/<owner>/<repo>/HEAD/<path>`. Match on the directory name, not the expected path: skills sit under plugin, package or category folders.
- A repository can rename a skill after its marketplace page was captured. When the expected name is missing from the tree, search the tree for keyword stems before concluding the skill is absent, and record the rename in the output.
- A truncated `web_extract` can hide the section that answers the question, so read the full text before reporting a default or a limit as undocumented.
- A verifier can check only files it can open, so a source kept as a file beats a figure quoted from a scrolled page.

## Obscura: MCP transport versus CLI

Obscura has two channels and the MCP one is the fragile side. A navigation chain in the MCP server
capped at ten documents fails with `Too many client-initiated navigations, the chain reached its
limit of 10 documents`, and after the third rejection the server pauses itself for about 45 seconds
and rejects every call with "MCP server 'obscura' rejected the last 3 calls".

- **On the first chain-limit error, switch channel instead of retrying.** Close pages first if the
  session has them open, but do not spend three calls proving the pause: the CLI has neither the
  chain cap nor the pause.
- The CLI is the same engine with no chain state:

```bash
obscura fetch --dump markdown https://example.com/page   # prints markdown to stdout
```

- Treat an MCP pause as channel state, not a per-URL verdict: the URL the MCP refused usually fetches
  fine through the CLI one call later.
- Retry the MCP channel only after the pause clears, and only for what the CLI cannot do
  (interaction, screenshots). A run whose sources all came through the CLI records the CLI as its R1
  route.

## Order of preference

1. `r.jina.ai/https://lite.duckduckgo.com/lite/?q=...`: search with snippets + dates
2. `r.jina.ai/https://search.brave.com/search?q=...`: **best second engine when lite DDG
   returns empty or a CAPTCHA** (tested 2026-08): keeps result titles, snippets, AND target
   URLs; surfaced an exact article slug plus a sibling article when DDG was captcha'd,
   Google abuse-blocked, Mojeek captcha'd, Bing Cloudflare'd. URL-encode the query; strip
   the `Showing results for <spellcheck>` noise lines; `grep -iE "domain|term"` on the
   jina output extracts the result links.
3. `r.jina.ai/https://<target-url>`: direct page render (primary-source pages, press
   releases with dates, brand official sites)
4. Wayback CDX + snapshot: archived copies of blocked pages
5. `r.jina.ai/https://www.bing.com/search?q=...`: works but titles/domains only (no
   snippets), quotes get stripped, multi-word brand queries return junk; last resort
6. Mojeek, do NOT use: 403s automated queries ("network appears to be sending automated queries")
7. Obscura local headless browser: when the page needs JavaScript, or the paths above return only
   the gate; see the Obscura section above for the invocation. This is the user's stated preference
   when the configured web backends are unavailable, and whenever the user names the Obscura MCP for a search.
8. For a **scholarly paper** rather than a page: skip straight to the metadata APIs
   (references/scholarly-metadata-apis.md): Crossref, OpenAlex, Semantic Scholar, Unpaywall,
   before spending any call on publisher HTML.
