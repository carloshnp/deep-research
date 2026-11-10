# Portuguese prose contract for generated reports

Applies to every Portuguese report the skill writes. The reader is one person with one doubt in front of them, not an audience. The text is an explanation between colleagues who share the technical vocabulary, so the vocabulary stays and the ambiguity goes.

The rules below come from recurring corrections made on real reports. Math layout rules: `references/math-and-latex-style.md`.

## Hard rules

**One idea per sentence, with the subject named.** When the referent is not in the same sentence, repeat the noun. "Ele forma uma camada que impede o ataque" is unclear when three nouns precede it; "o cromo forma uma camada de Cr₂O₃ que impede o ataque" is readable in isolation.

**No em dash and no en dash.** Ranges read with "a": "11 a 18% Cr", "1600 a 800 °C". After "entre" the second number joins with "e": "entre 11% e 18% Cr". In running text use comma, period or parentheses. In headings use a colon. Composite hyphens are fine ("aço-liga", "bem-comportado").

**No labelled meta-scaffolding in body prose.** The words "Mecanismo:", "Evento microestrutural:" and "Efeito macroscópico:" never appear as inline labels, nor as bullets, nor as pseudo-headings inside a paragraph. The same ban covers their variants ("Evento:", "Evento de processo:", "Causa:", "Consequência:", "Primeiro elo:") and any numbered relabeling of the same triad. The causal chain is written as continuous prose with the subject named, one link per sentence, and the triad stays an internal checklist the writer runs while reviewing the paragraph, never text to paste into the report.

Wrong: "Mecanismo: os intersticiais distorcem a rede. Efeito: a dureza sobe."

Right: "Como o oxigênio ocupa um sítio pequeno, ele empurra os átomos vizinhos e cria um campo de deformação que trava a discordância; é por isso que 0,1 % em massa já muda a dureza."

A label is a promise that the reader will need the label to find the reasoning. The reader does not; the reasoning has to hold on its own, sentence after sentence, with the subject repeated where the referent would otherwise be a guess.

**No filler opener.** Cut "é importante notar", "vale ressaltar", "cabe destacar", "de suma importância", "no final do dia", "quando se trata de", "por sua vez" chained three times, "sendo assim" chained, "em outras palavras" used to restate the sentence just written. Each of these delays the information by a clause.

**No binary contrast.** "Não é X, é Y" is a rhetorical pattern; state what X is and what Y adds. Same for "o que ninguém percebe" and "o erro mais comum é".

**No drama.** No fragment as a closing sentence ("Esse é o ponto."), no colon reveal in prose ("O resultado: 24,25"). No importance puffery: "marca um momento decisivo", "é um divisor de águas", "desempenha um papel fundamental".

**No rider clause.** Sentences ending in "destacando que", "ressaltando a importância de", "evidenciando o papel de" add nothing; cut the rider or move its content into its own sentence with a subject.

**No borrowed authority.** "Estudos mostram", "especialistas afirmam", "é sabido que". Either cite the source with author and year, or state the mechanism yourself.

**Describe the mechanism, not the impression.** "A resistência cai porque a camada passiva se rompe e o metal exposto volta a oxidar" tells the reader what happens. "A resistência sofre uma degradação significativa" names no cause.

**Active voice, concrete nouns, numbers with units.** "O ensaio durou 2 h a 600 °C" over "a realização do ensaio ocorreu por um período de 2 h".

**Placement decides whether the reader parses the sentence.** Keep the verb within a few words of its
subject; a phrase inserted between them reads as an aside. End the sentence on the one new point the
reader must keep, and put qualifiers and references before it. Open with a term the reader already
holds, so the new material attaches to something. A sentence is too long when it carries more new
points than it has positions to land them in, and that is a different test from a word count.

Wrong: "A tensão de flexão na viga, que varia com a distância até a linha neutra e atinge o máximo nas
fibras externas, é dada por σ = My/I."

Right: "A tensão de flexão é dada por σ = My/I. Ela varia linearmente com a distância y até a linha
neutra e atinge o máximo nas fibras externas."

Wrong: "O revenido reduz a dureza porque a martensita, que é uma fase metaestável com alto teor de
carbono em solução, perde carbono para os carbetos que precipitam."

Right: "A martensita é uma fase metaestável e mantém carbono em solução. O revenido aquece o aço e o
carbono sai da solução para formar carbetos, o que alivia a distorção da rede e reduz a dureza."

**Explain before judging.** When a rule, criterion or limit appears, state what it is and which problem it solves, then evaluate it. Never rank or criticize before the reader knows what the thing does.

**No moral verdict on people, teams or methods.** State who does what, how often, and what breaks. "O valor foi tabelado em 1970 e ninguém revisou desde então" is a fact a reader can act on; "a norma está desatualizada" is an unactionable verdict.

## Technical terms: keep them, explain them

Natural prose does not mean simplified prose. The technical term stays, in the register of the field, and the first appearance carries a one-sentence explanation in plain words. After that the report uses the term without re-explaining it.

- First appearance: "ferrita, a fase cúbica de corpo centrado pobre em carbono".
- Later appearances: "ferrita", plain.
- Never swap the term for a vague synonym to sound lighter. "Solução sólida substitucional" never becomes "mistura de metais".
- When a symbol appears, define it in prose in the same paragraph: "onde $c$ é a concentração em mol/L".
- Recurring terms follow the author's spelling list, not the dictionary.

## Completeness over compression

The reader holds one paragraph at a time. When the choice is between one ambiguous sentence and three clear ones, write the three. Repetition that keeps the referent clear is not padding. Cut length by removing filler, never by compressing an explanation until the reader has to reconstruct it from an earlier section.

## Before and after

| Rather than | Write |
|:---|:---|
| "É importante notar que o cromo forma uma camada protetora." | "O cromo forma uma camada de Cr₂O₃ sobre a superfície." |
| "A temperatura não é alta, é crítica." | "A 1250 °C a fase austenítica se estabiliza, e é isso que permite a deformação." |
| "A fratura ocorre à temperatura de 450 °C em virtude de um fenômeno de fragilização, o que evidencia a importância do controle térmico." | "A 450 °C o carbono difunde para os contornos de grão e forma Cr₂₃C₆, que retira cromo da matriz e baixa a resistência à corrosão. Esse é o motivo do limite de 450 °C na faixa de serviço." |
| "A Figura 3 mostra a tensão." | "A Figura 3 mostra a tensão caindo de 450 MPa para 180 MPa quando o teor de carbono passa de 0,4% para 0,8%." |

## Audit before saving

The dash, LaTeX and math placement checks live in `references/post-write-cleanup.md`. Three more searches catch the filler:

- filler openers: "vale ressaltar", "cabe destacar", "é importante notar", "de suma importância", "em outras palavras"
- drama riders: "destacando", "ressaltando", "evidenciando", "de forma significativa", "de maneira notável"
- meta-labels in body prose: "Mecanismo:", "Evento microestrutural:", "Efeito macroscópico:", "Evento:", "Causa:", "Consequência:"

Any hit gets rewritten before the report is delivered. A hit is not a style preference violation; it is a sentence that spends the reader's attention without adding information.
