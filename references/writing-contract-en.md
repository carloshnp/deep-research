# Writing contract for research reports

This contract sets what each section of a research report must carry and how its sentences must read. Where a script can check a rule, the gate scripts do; the rest is judged by a reader.

## Why these rules

The rules target four failures: a reader who holds too much or too little for a passage, a sentence whose placement hides its point, a causal link left unstated, and a claim that rests on authority rather than mechanism. Readability formulas are not used as a gate, because their recommended edits often make a passage harder to follow.

## Reader

The reader is one colleague with one doubt. They know the field's vocabulary and its basic methods, and they have not read the sources. Write for that person, not for an audience.

The misremembered part matters more than what the reader already knows. Three misreadings are common. A correct fact is taken as an explanation when no link connects it to the claim before it. An event listed before another is taken as its cause. A qualifier dropped in a summary is taken as never having existed. A correct sentence does not remove a wrong model unless it is set against that model. Every section therefore names the misconception it displaces (see Limit below).

## Placement

Placement decides whether the reader parses a sentence. These rules apply to every sentence.

- Keep the verb within a few words of its subject. A phrase inserted between them reads as an aside.
- End the sentence on the one new point the reader must keep. Put qualifiers and references before it.
- Open with a term the reader already holds, so the new material attaches to something.
- A sentence is too long when it carries more new points than it has places to land them. That is a different test from word count: ten words can be hard to parse and a hundred can flow.
- When you split a sentence, keep the connective (because, so, therefore). A removed causal link forces the reader to supply the inference.
- Use one term for one thing. Use a pronoun only when a single antecedent is possible.

The first version below buries the formula under a clause. The second states the formula, then adds the qualifier.

The bending stress in the beam, which varies with distance from the neutral axis and peaks at the outer fibers, is given by σ = My/I.

Bending stress is given by σ = My/I. It varies linearly with the distance y from the neutral axis and peaks at the outer fibers.

## Chain before point

A claim in a report is either a mechanism or a definition. A mechanism is written as A, then B, therefore C, with a cause given for each link. A definition gives the reason it is definitional. A list of facts joined by "and" or "also" is not a chain, and a point that cannot be chained is a fact for a clause, not a section.

Worked chain (illustrative, not sourced): a cache holds recently used data close to the processor. A request that finds its data in the cache is a hit, and a hit returns in a few nanoseconds. A request that misses goes to main memory, which is far slower, so the processor stalls while it waits. A workload whose working set exceeds the cache misses more often, so its average time per request rises even when the code is unchanged.

Write the chain as continuous prose, one link per sentence, with the subject named. Words such as "Mechanism", "Cause", "Effect" and "Consequence" stay out of the text; they belong to the writer's review checklist.

## The twelve-field plan

Before a writer drafts a section, the plan states twelve fields for it. A field with nothing to say states that and why, for example "qualitative: the trace shows the shape of the curve and gives no value".

- question: the one question the section answers, as one sentence. If it needs two, it is two sections.
- reader: what the reader is assumed to know, and what they are likely to misremember. The second half matters more.
- entry: what the reader must already hold for the section to work, naming the earlier section that supplied it.
- point: the one sentence the reader should keep. Two points mean two sections.
- chain: the mechanism, link by link, each link with its cause.
- principle: the rule or principle each step instantiates, named.
- instance: the worked example with numbers and units and its named source, or a statement that the section is qualitative and why.
- limit: the exception or wrong model the section displaces. "None" is allowed only with a reason.
- budget: words for the section, a number between 250 and 800.
- boundary: what the section excludes and where that material lives.
- source: the research file and the page, slide or line range the claims come from.
- file: the output path for the section.

Rules for filling the plan:

- Write the question first. If it cannot be one question, split the section.
- Write reader before point, because the point depends on what the reader already holds.
- Write chain before point. A point that cannot be chained is a fact, not a section.
- Set the budget from the chain length. Four links with numbers run 350 to 500 words; one definition and one figure run 250 to 300 words.
- Set the report's word target as the sum of the section budgets, never as a round number chosen first.
- Mark the boundary in the plan, not in a later cleanup pass.
- Copy numbers from the source range with their units, and name the source.

## Instance and limit

An instance is a worked example with numbers, units and a named source. Illustrative example (not sourced): a loop reads a 4 MB array on a machine with a 2 MB cache. Every pass misses, so each access takes the main-memory time. Shrink the array to 1 MB and the loop fits the cache after its first pass.

A limit names the wrong model the passage displaces. For the same example: the wrong model is that a faster processor always runs the same loop faster. Once the data misses the cache, a faster clock only waits longer on the same memory. A section with no limit says "none" and gives the reason.

## Numbers and units

Give every number its unit and a named source. Use decimal points. Write ranges as "N to M" in tables and lists, and as "between N and M" in English prose: "between 150 and 275 °C" in a sentence, "150 to 275 °C" in a table cell.

## Prose rules

Hard rules:

- One idea per sentence, with the subject named. When the referent sits outside the sentence, repeat the noun. "It forms a layer that blocks attack" is unclear when three nouns come before it; "the oxide layer blocks attack" reads alone.
- No em dash and no en dash. Use commas, full stops or parentheses in running text, and a colon in headings. Hyphens inside compounds are fine.
- No labelled scaffolding in body prose. Labels such as "Mechanism:", "Event:", "Cause:", "Consequence:" and "Effect:" never appear inline, as bullets or as pseudo-headings. The reasoning has to hold on its own, with the subject repeated wherever a referent would be a guess.

Instead of "Mechanism: cache lines bounce between cores. Effect: throughput falls.", write: "Because two cores write to the same cache line, each write forces the other core to reload it, which is why the counter slows as cores are added."

- No filler opener. Delete on sight: "It is worth noting", "It should be emphasized", "It is important to note", "Importantly", and "In other words" when it only restates the sentence before. Each one delays the information by a clause.
- No binary contrast. "It is not X, it is Y" is a rhetorical pattern. State what X is and what Y adds. The same applies to "what nobody notices" and "the most common mistake is".
- No drama. No fragment as a closing sentence ("That is the point."), no colon reveal in prose ("The result: 24.25"), and no importance puffery such as "marks a decisive moment" or "plays a fundamental role".
- No rider clause. Sentences ending in "highlighting that", "underscoring the importance of" or "emphasizing the role of" add nothing. Cut the rider, or give its content a sentence with its own subject.
- No borrowed authority. "Studies show" and "experts agree" are not sources. Cite the work with author and year, or state the mechanism.
- Describe the mechanism, not the impression. "Throughput falls because the lines bounce between cores" says what happens. "Performance degrades significantly" names no cause.
- Active voice, concrete nouns, numbers with units. "The test ran 2 h at 600 °C" beats "the test was carried out over a period of 2 h".
- Explain before judging. When a rule or limit appears, say what it is and which problem it solves, then evaluate it.
- No moral verdict on people, teams or methods. State who does what, how often, and what breaks.

The table below shows the rewrites. The numbers are illustrative.

| Rather than | Write |
|:---|:---|
| It is worth noting that the cache speeds up reads. | A read that hits the cache returns in a few nanoseconds. |
| The size is not large, it is critical. | A 2 MB cache holds the loop's working set, so the loop runs without misses. |
| Performance degrades significantly at scale, which highlights the importance of memory layout. | At 4 MB the loop misses on every pass, so the average access takes the main-memory time. Keeping hot data together is what the fix changes. |
| Figure 3 shows the timing. | Figure 3 shows the average access time falling from 90 ns to 12 ns as the array shrinks from 4 MB to 1 MB. |

Technical terms stay, and the first appearance carries a one-sentence plain explanation, such as "hash table, a structure that maps keys to slots so a lookup takes about one step on average". Later uses are plain. Never swap a term for a vaguer word to sound lighter: "hash table" never becomes "lookup structure". Define any symbol in prose in the same paragraph, as in "where c is the concentration in mol/L".

Completeness over compression: the reader holds one paragraph at a time. When the choice is between one ambiguous sentence and three clear ones, write the three. Repetition that keeps the referent clear is not padding. Cut length by removing filler, never by compressing an explanation until the reader must rebuild it from an earlier section.

## Audit before saving

Three searches catch most of the filler: the openers listed above; drama riders such as "highlighting", "underscoring", "emphasizing", "remarkably" and "significantly"; and meta-labels such as "Mechanism:", "Event:", "Cause:", "Consequence:" and "Effect:" in body text. Each hit is rewritten before the report is delivered. A hit is not a style preference; it is a sentence that spends the reader's attention without adding information.

What can be checked, and by what:

- Script-detectable: number provenance with its unit, term coverage, formatting, the report-level rules below.
- Judge-detectable, binary with a quoted span, one section per call: missing causal step, term used before definition, claim with no source line, topic jump.
- Human only: reversed causal direction, factual error against the source, whether a reader can use the section.
- Report-only until calibrated: question answerability. Generate questions from the section, answer them with and without it, and count what the text alone supports.

## Report-level rules

- One level-1 title at the top, and a status line near the top that names the checks that did not run.
- No internal section IDs in reader-facing text, such as codes taken from the plan.
- No process words in reader-facing text: names of planning steps, review passes, worker rounds or numbered waves.
- No paragraph over 180 words.
- A sentence over 40 words is a warning; split it at its connective.
- No line begins with a label such as Confidence, Basis, Verdict, Decision or Status followed by a colon.

The two gate scripts are scripts/check_plan.py, the plan gate run before writers start, and scripts/check_report_style.py, the report gate run on the assembled report.
