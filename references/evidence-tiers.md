# Evidence tiers

Fixed hierarchy for every depth tier. X and community threads are searched first-class (P0 signal) and quoted as evidence, but load-bearing technical claims are corroborated against authority tiers before delivery.

| Tier | Class | Role | Rules |
|---|---|---|---|
| P0 signal | X threads, Reddit threads, HN discussions | Practitioner signal and discovery | Search alongside web, quote representative posts, verify each cited post (fxtwitter or permalink fetch), corroborate technical claims with P1 before they carry load |
| P1 authority | Official docs, release notes, specs, standards, primary papers | Every fact and number | Read the version cited; cite by section when numbering is unstable |
| P2 teaching | University notes, textbooks, established explainers | Intuition and framing | Do not reuse their figures (licensing); draw or describe independently |
| P3 context | Independent comparisons, press, vendor blogs | Landscape and positioning | Label vendor claims as vendor claims |
| P4 mirrors | Aggregators, trend reports, SEO category pages | Never the sole source | Evergreen pages prove nothing dated; a GitHub trend report is not a week ranking |

## Labels (mandatory per source)

- `(read)`: content claims may come from it.
- `(URL verified, not read in full)`: the link may be listed; no content claims.
- Discovery-only: titles or snippets that pointed at a better source; never cited for facts.

## Code and machine-readable indexes

A vendor's source tree is the authority for what the product does, and its docs are the authority for what the vendor says it does. When the two disagree, cite both, state which one you observed, and let the code decide any behavior claim.

Cite code by commit hash, file path, and line range, because line numbers move between commits. Record the commit in the pack, and read the file at that commit.

When the tree carries a machine-readable index (a catalog JSON, a registry file, a generated manifest), count from the index rather than from a docs page that summarizes it, since docs can lag the index. Triggers, gates, and defaults are set in workflow and config files; a docs sentence describing them is a claim to check against those files.

## Pack discipline (Standard and Deep)

One excerpt file per source under `research/<area>/`: title, URL, author or org, date, which questions it serves, 2 to 6 key claims with direct quotes when wording is load-bearing, and a quality note (class, currency, coverage, limits, conflicts with other sources). Numbers appear exactly as the source states them. Nothing is quoted that was not read.

Probe every URL in the final report and record the outcome. Reuse existing captures before fetching (keep a reuse inventory of capture plus used-for). When a gap survives, record what was searched instead of filling it with a weak source. The Deep coverage map lists every planned subsection against its sources with gaps explicit.
