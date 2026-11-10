# Math and LaTeX style

## Inline vs display

- Inline stays as it was: $...$ for symbols and short expressions inside a sentence, like $O(n \log n)$ or $p = 0{,}95$.
- Anything that is a standalone equation, a derivation step, a system, or a chain of steps is display math, and display math always sits on its own line, never mid-sentence. The fix for hard-to-read formulas is more display math, not denser inline.

## Decimal comma

Numbers in Portuguese prose and in math use the comma as decimal separator: 2,7, 0,85, 1,587, 1,74 g/cm³. Never the point. In math mode the comma goes braced, as in $2{,}7$ or $0{,}85$, so that the renderer does not add the spacing it uses for the comma as an operator in a list.

Correct:

- $p = 0{,}95$, $k = 1{,}5$, $\rho = 1{,}74 \, \text{g/cm}^3$
- prose: "a densidade do alumínio é 2,7 g/cm³", "o c/a vale 1,587"

Wrong, and never written in the report:

```
$p = 0.95$   "2.7 g/cm³"   $c/a = 1.587$
```

The point survives in exactly three places: inside code blocks, in machine-readable values (CSV, JSON, script arguments, file names), and as the thousands separator, which Portuguese writes with a point: 3.000 rpm, 40.000 psi. That is not a decimal point and does not become a comma.

## Display layout

Single equation, its own line, blank line before and after:

$$
\epsilon_{\text{maq}} = 2^{1-p}
$$

Multi-line derivations and solved examples use an aligned environment inside the display: one step per row, aligned at the relation with &:

$$
\begin{align}
x_{n+1} &= x_n - \frac{f(x_n)}{f'(x_n)} \\
        &= 2 - \frac{4 - 2}{4} \\
        &= 1{,}5
\end{align}
$$

Rules:

- one relation per row; the solving chain (formula, substitution, arithmetic result) belongs in a single align block, not three separate displays;
- & goes at the relation (=, \approx, \leq);
- short \text{...} annotations at row ends are fine; keep them brief;
- \text{...} is not reserved for row-end annotations. It is the way roman text enters display math at all, and it is expected for units and for words inside a formula: $\sigma = 250 \, \text{MPa}$, $\rho = 1{,}74 \, \text{g/cm}^3$, $\epsilon_{\text{maq}}$, $\sigma_{\text{limite}}$. Put a thin space (`\,` or `\;`) between the number and its unit, and never write the unit as italic math variables: $MPa$ reads as the product of three symbols;
- a quantity that carries a unit keeps the unit through the whole derivation and the unit of the result is checked at the end (dimensional analysis);
- if a renderer rejects align inside $$, fall back to \begin{aligned}; both follow the same layout rules;
- a display inside a callout keeps the quote marker on every line: `> $$`, then the environment, then `> $$`, with a `>` blank line before and after. A `> \begin{align}` with no `> $$` around it ships as literal LaTeX text, and a writer copying the callout shape from prose reproduces it in every worked example.

## Hard rules

- Never \(...\) or \[...\]; always $...$ and $$...$$.
- No currency $ in prose (write "USD 104" or the HTML entity).
- No $ inside a display block.
- Balanced $ per line (the lint checks it).
- Ranges read "N a M" (PT) or "N to M" (EN), never with a dash.
- Decimal comma in Portuguese prose and in math ($2{,}7$, $0{,}85$, $1{,}587$), never the point; the point stays inside code blocks, machine-readable formats and the thousands grouping (3.000).
- Standard KaTeX/MathJax commands only (\sin, \cos, \ln, \log, \lim, \det, \boxed). Never \sen, \tg, \cosec.
- Passing LaTeX through tool calls and JSON: commands starting with b, t, r, f, n need the backslash doubled (\b, \t, \r, \f, \n are escape sequences); the rest are safe.
- Python scientific notation must never leak into math mode ({:.2e} values become \times 10^{N}; the cleanup rules are in references/post-write-cleanup.md).

## Checks

The lint, which this repo does not ship, checks: display math alone on its line (flags $$ mixed with text), $ parity per line, align block count. references/post-write-cleanup.md covers dash stripping, currency and scientific notation. Two greps catch the separator: a point between digits in prose (`[0-9]\.[0-9]`) must resolve to a code block, a CSV or a thousands grouping, and a bare comma decimal outside `{,}` in math is a rendering bug waiting to happen.

Read the file for residual cases: for each `> \begin{align}` insert `> $$` before it and `> $$` after `> \end{align}`, split a `> $$formula$$` line into three quoted lines, and re-read the file until no environment is bare. A report that passes the lint with 0 errors can still ship two dozen bare environments, because the count of `$$` stays even in prose.
