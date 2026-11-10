# Scholarly Metadata and Abstract Recovery

## When to Use

The target is a paper (DOI, publisher PII, or a publisher URL), the publisher blocks the HTML, and
the deliverable needs the abstract, authors, venue, OA status or citation count rather than verbatim
body text. Fighting the paywall costs calls and usually loses; the metadata layer is keyless, fast,
and answers abstract-level questions outright.

## Step 0: resolve the identifier

A publisher URL often carries only a PII. Crossref indexes the Elsevier PII as `alternative-id`,
so one call turns a bare `/pii/S...` URL into a DOI, title, journal and date:

```bash
curl -s -m 25 "https://api.crossref.org/works?filter=alternative-id:S0254058424013981&rows=3"
```

With a DOI in hand, every endpoint below takes it directly.

## Step 1: get the abstract, cheapest route first

**OpenAlex**: `https://api.openalex.org/works/doi:<DOI>`. Richest single record: year, venue,
`cited_by_count`, `open_access`, `concepts`, and `abstract_inverted_index`. Reconstruct the text by
sorting the positions:

```python
w = json.loads(resp)
ab = w.get('abstract_inverted_index')
inv = {}
for word, pos in ab.items():
    for p in pos:
        inv[p] = word
text = ' '.join(inv[k] for k in sorted(inv)) if ab else None
```

Expect `None` often, Elsevier titles especially.

**Semantic Scholar**:
`https://api.semanticscholar.org/graph/v1/paper/DOI:<DOI>?fields=title,abstract,year,venue,citationCount,externalIds,tldr`
Frequently holds the abstract where OpenAlex does not, plus `openAccessPdf` with a `CLOSED` status.
Its **search** endpoint 429s within a couple of calls; the single-DOI endpoint tolerates sustained
use. Search the other providers, then resolve the DOI here.

**colab.ws**: `https://colab.ws/articles/<urlencoded DOI>`. The recovery of last resort for
closed-access Elsevier: renders the abstract plus journal metrics (SJR, CiteScore, impact factor)
and the reference list. It is a SPA, so read it with the headless browser, not curl:

```bash
obscura fetch "https://colab.ws/articles/10.1016%2Fj.matchemphys.2024.130269" --dump text
```

**Unpaywall**: `https://api.unpaywall.org/v2/<DOI>?email=<addr>`. Returns `is_oa`,
`oa_status`, `best_oa_location`. Distinguishes "paywalled with nothing public" from "a repository
copy exists and is worth fetching", which decides whether a body-text route is even available. The
email parameter is mandatory.

## Step 2: find the related work

- OpenAlex `filter=title_and_abstract.search:<terms>` for precise recall. The bare `search=` param
  matches full text and buries the target in high-citation noise from adjacent fields; a query for
  transformer-based OPV modelling returns energy-review papers with thousands of citations.
- Add `filter=from_publication_date:YYYY-MM-DD` to drop stale surveys, and
  `sort=cited_by_count:desc` to surface the canonical work first.
- arXiv: read `https://arxiv.org/abs/<id>` pages or the search UI
  (`https://arxiv.org/search/?searchtype=all&query=<terms>`) through the browser. The export API at
  `http://export.arxiv.org/api/query` answers HTTP 406 to browser-ish user agents and its HTTP
  endpoint 301-redirects, so a plain curl loop returns nothing and looks like an empty result set
  rather than a rejected request.

Give every request a `-m` timeout and an `-A` user agent. These APIs are keyless but rate-limit by
IP, and a silent empty body is the usual failure shape.

## Pitfalls

- Distinguish "the API has no abstract" from "the article has no abstract". Report which route
  supplied the text, and do not present an abstract recovered from an aggregator as if the
  publisher's page had been read.
- A recovered abstract is abstract-level evidence only. It cannot support claims about methods,
  numerical results or conclusions that live in the body. State "full text not read" in the
  deliverable and list the paper under a suggested second pass.
- Metadata APIs disagree. A record can be `oa_status: closed` in Unpaywall, `is_oa: false` in
  OpenAlex, and still have an abstract on an aggregator; check more than one before declaring the
  paper unreachable.
- Citation counts are point-in-time. Date them in the write-up.
