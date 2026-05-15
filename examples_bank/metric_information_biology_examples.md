# Metric Space Applications — Information and Biology (APL-02)

- Source: `AdamsFranzosa2008Topology`
- Sections: §5.2 (Metrics and Information: Error-Correcting Codes, DNA Sequences)
- Version introduced: `v0.2.3`
- Route: `APL-02`
- Rule: Original package explanations only. Book sections guide topic selection and
  fact verification; no problem statements or extended prose are copied verbatim.

---

## Part A — Error-Correcting Codes and the Hamming Metric

### A.1 Setup: Binary Words

**Setting.** Let Vⁿ = {0,1}ⁿ be the set of all binary strings of length n.
Each element is called a **word**. In a transmission channel, a sender
chooses a word c ∈ Vⁿ and the receiver obtains a word f ∈ Vⁿ. Noise in the
channel may flip individual bits: a 0 becomes a 1 or vice versa. The number
of flipped bits is the *error count*.

### A.2 The Hamming Metric

**Definition.** For x, y ∈ Vⁿ the **Hamming distance** is

    D_H(x, y) = |{i : xᵢ ≠ yᵢ}|

the count of positions where x and y differ.

**Metric verification.**
- D_H(x,y) ≥ 0, with equality iff x = y.           ✓ (non-negativity)
- D_H(x,y) = D_H(y,x).                              ✓ (symmetry)
- D_H(x,z) ≤ D_H(x,y) + D_H(y,z).                  ✓ (triangle inequality)

The triangle inequality follows from the observation that any position where
x and z differ must be a position where x and y differ or where y and z
differ (or both).

**Example.** In V⁹:

    x = (0, 0, 1, 1, 0, 0, 0, 1, 0)
    y = (0, 1, 0, 1, 0, 0, 1, 1, 0)

Differences at positions 2, 3, 7: D_H(x,y) = 3.

**Induced topology.** Because Vⁿ is finite, every singleton is open in the
metric topology induced by D_H. Hence D_H induces the **discrete topology**
on Vⁿ. The metric structure carries information not visible from topology alone.

**Pytop module link:** `pytop.metric_spaces`.

---

### A.3 Codes, Codewords, and Minimum Distance

**Definition.** A **code** C ⊆ Vⁿ is any chosen subset. Its elements are
**codewords**. The **minimum distance** δ(C) is

    δ(C) = min{D_H(c, c') : c, c' ∈ C, c ≠ c'}

A code with minimum distance δ satisfies:
- **Error detection:** any received word f with up to δ−1 errors differs
  from every codeword, so the receiver knows an error occurred.
- **Error correction:** any received word f with up to ⌊(δ−1)/2⌋ errors
  has a unique closest codeword (Theorem 5.10 below).

**Example.** Code of length 6 with minimum distance 3:

    C = { (0,0,1,0,0,0),
          (1,0,0,1,1,1),
          (1,1,1,0,1,1),
          (0,1,0,0,1,0) }

Any single-bit error in a transmitted codeword can be corrected: the received
word is within distance 1 of exactly one codeword.

---

### A.4 Error-Correction Theorem (Metric Ball Argument)

**Metric ball.** For c ∈ Vⁿ and integer r ≥ 0 define

    B(c, r) = {f ∈ Vⁿ : D_H(f, c) ≤ r}

**Theorem (Adams & Franzosa §5.2, Th. 5.10).** If C has minimum distance δ,
then every word with at most ⌊(δ−1)/2⌋ errors can be corrected uniquely.

*Proof sketch.* Set t = ⌊(δ−1)/2⌋. If the received word f satisfies
D_H(f,c) ≤ t for some codeword c, and also D_H(f,c') ≤ t for a different
codeword c', then by the triangle inequality:

    D_H(c,c') ≤ D_H(c,f) + D_H(f,c') ≤ t + t = 2t ≤ δ−1

This contradicts the minimum distance being δ. So c is the unique closest
codeword and the error is corrected.

**Geometric picture.** The open balls B(c, t) around distinct codewords are
**disjoint**. The receiver maps each received word f to the unique codeword
c for which f ∈ B(c, t).

---

### A.5 The Hamming Bound (Sphere-Packing Bound)

The size of a code correcting t errors is constrained by how many disjoint
balls of radius t fit inside Vⁿ.

**Ball size.** The number of words in B(c, t) (i.e. words differing from c in
at most t positions) is

    |B(c, t)| = Σ_{k=0}^{t} C(n, k)

where C(n,k) = n! / (k!(n−k)!) is the binomial coefficient.

**Hamming bound.** For any code C ⊆ Vⁿ correcting t errors:

    |C| · Σ_{k=0}^{t} C(n,k) ≤ 2ⁿ

A code achieving equality is called a **perfect code**: the disjoint balls
of radius t around its codewords partition all of Vⁿ exactly.

**Example: Hamming(7,4) code.** The binary Hamming code with n=7, t=1
has 2⁴ = 16 codewords. Ball size = C(7,0)+C(7,1) = 1+7 = 8. Check:
16 × 8 = 128 = 2⁷. It achieves the Hamming bound — it is a perfect
single-error-correcting code.

**Example: Binary Golay code.** The extended binary Golay code has n=24,
|C| = 2¹², t = 3. Ball size = C(24,0)+C(24,1)+C(24,2)+C(24,3) = 1+24+276+2024 = 2325.
Check: 2¹² × 2325 = 4096 × 2325 = 9,523,200 ≠ 2²⁴ = 16,777,216. The Golay
code does not meet the Hamming bound; it corrects 3 errors but is not perfect.
(The perfect Golay code is the ternary Golay code over F₃.)

---

### A.6 Comparison: Rate vs. Distance

A code designer faces a fundamental trade-off:

| Goal | Effect on code |
|---|---|
| Larger |C| (more messages) | Codewords are closer together → smaller δ |
| Larger δ (more error correction) | Fewer codewords → smaller |C| |
| Shorter n (faster transmission) | Less room for redundancy |

The **rate** R = log₂|C| / n measures information per transmitted bit. A
rate-1 code (R=1) has no redundancy and corrects nothing. A rate-0 code
corrects everything but conveys nothing. Real codes balance both.

**Pytop module link:** `pytop.metric_spaces`.

---

## Part B — DNA Sequence Metrics

### B.1 DNA as a Metric Space

**Biological structure.** A DNA molecule encodes genetic information as a
sequence over the alphabet Σ = {A, C, G, T} (adenine, cytosine, guanine,
thymine). The two complementary strands wind into a double helix, but the
information content is carried by one strand's sequence.

Let W = ⋃_{n≥1} Σⁿ be the set of all finite DNA sequences. Two natural
metrics arise in computational biology.

---

### B.2 Hamming Distance for Same-Length Sequences

When two sequences x, y ∈ Σⁿ have the same length and differences arise
only from **nucleotide substitutions** (one base replaced by another with
no insertions or deletions), the Hamming distance counts substitutions
directly:

    D_H(x, y) = |{i : xᵢ ≠ yᵢ}|

**Example.**

    x = A C G T T G A A T A C
    y = A G G G T T G A A T A

Differences at positions 2, 4, 6, 7, 8, 9, 10, 11: D_H(x, y) = 8.

**Limitation.** When sequences differ by **insertions or deletions (indels)**,
Hamming distance is misleading. A single insertion shifts all subsequent
positions, causing many apparent mismatches even when the actual sequences
are very similar.

---

### B.3 Levenshtein (Edit) Distance

**Definition.** The **Levenshtein distance** D_L(x, y) between sequences
x, y ∈ W is the minimum number of single-character operations needed to
transform x into y, where allowed operations are:

- **Substitution:** replace one character with another
- **Insertion:** insert a new character at any position
- **Deletion:** remove one character at any position

    D_L(x, y) = min over all operation sequences S { insertions(S) + deletions(S) + substitutions(S) }

**Metric verification.**

- D_L(x,y) ≥ 0 with equality iff x = y.            ✓
- D_L(x,y) = D_L(y,x): every insertion has a reverse deletion.  ✓
- Triangle inequality: any path from x to z via y gives an upper bound. ✓

**Example (from Adams & Franzosa §5.2, Ex. 5.7).**

    x = AGTTCGAATCC
    y = AGCTCAGGAATC

Transform x → y in 4 operations:
1. Substitute T→C at position 3:  AGCTCGAATCC
2. Insert A after position 6:     AGCTCAGAATCC
3. Insert G after position 7:     AGCTCAGGAATCC
4. Delete C at position 13:       AGCTCAGGAATC  = y

D_L(x, y) = 4.

**Comparison with Hamming on equal-length sequences.** For the same-length pair:

    x = ACGTTGAATAC
    y = AGGGTTGAATA

D_L(x, y) = 3  (the shared segment GTTGAATA is recognized)
D_H(x, y) = 7  (many apparent differences due to offset)

The Levenshtein distance is always ≤ the Hamming distance when both are
defined (same-length sequences), because substitutions are a subset of the
allowed operations. When indels are present, D_L can be dramatically smaller
than D_H.

---

### B.4 Dynamic Programming Computation of D_L

The Levenshtein distance is computed efficiently by the **Wagner–Fischer
dynamic programming algorithm** in O(|x|·|y|) time and O(min(|x|,|y|))
space.

**Algorithm sketch.** Build a (|x|+1)×(|y|+1) matrix M where M[i][j] is
the edit distance between x[1..i] and y[1..j]:

    M[0][j] = j     (delete j characters from x to match empty prefix of y)
    M[i][0] = i     (insert i characters to match x[1..i] from empty y)

    M[i][j] = M[i−1][j−1]                      if xᵢ = yⱼ  (no operation)
             min( M[i−1][j]   + 1,              (delete xᵢ)
                  M[i][j−1]   + 1,              (insert yⱼ)
                  M[i−1][j−1] + 1 )             (substitute)   otherwise

The answer is M[|x|][|y|].

**Small example.** D_L("ACG", "AG"):

       ""  A  G
    ""  0   1  2
    A   1   0  1
    C   2   1  1
    G   3   2  1

D_L("ACG","AG") = 1 (delete C).

---

### B.5 Biological Interpretations and Applications

**Evolutionary distance.** Two DNA sequences that diverged from a common
ancestor accumulate substitutions and indels over time. D_L provides a proxy
for evolutionary distance: species with small D_L between homologous gene
sequences are more closely related.

**Phylogenetics.** Distance matrices built from pairwise D_L values are used
to construct phylogenetic trees via algorithms such as UPGMA (Unweighted Pair
Group Method with Arithmetic Mean) and Neighbor Joining.

**Sequence alignment.** Global alignment (Needleman–Wunsch algorithm) and
local alignment (Smith–Waterman algorithm) are refinements of the edit
distance framework that allow weighted costs for different operation types and
find optimal alignments between subsequences.

**Spell checking and NLP.** The same Levenshtein framework applies to text
processing: a spell checker replaces a misspelled word with the dictionary
word of minimum Levenshtein distance.

---

### B.6 Metric Topology on W

The Levenshtein metric D_L makes W = ⋃_{n≥1} Σⁿ a metric space. Topological
consequences:

- **Open balls** B(x, r) = {y ∈ W : D_L(x,y) < r} group sequences that are
  "biologically close" to x — reachable by fewer than r edit operations.
- Since W is countably infinite and D_L takes only non-negative integer values,
  B(x, 1) is always finite (there are finitely many single-edit neighbours of x).
- The metric topology on W is **discrete** (every singleton is open) because
  B(x, 1/2) = {x} for all x.
- Despite inducing the discrete topology, D_L carries geometric information:
  the *sizes* of balls encode evolutionary reachability and biological proximity.

**Contrast with Hamming on Vⁿ.** Both Hamming and Levenshtein induce the
discrete topology on their respective domains. Their utility lies not in the
topology they induce but in the metric structure they impose, which enables
nearest-neighbour search, clustering, and error-correction decoding.

**Pytop module link:** `pytop.metric_spaces`, `pytop.metric_completeness`.

---

## Part C — Metric Summary Table

| Metric | Domain | Operation counted | Handles indels? | Topology induced |
|---|---|---|---|---|
| Hamming D_H | Vⁿ (fixed length) | Bit/symbol substitutions | No | Discrete |
| Levenshtein D_L | W (variable length) | Substitution + insertion + deletion | Yes | Discrete |
| Euclidean d_E | ℝⁿ | — | N/A | Standard (non-discrete) |

**Key principle.** A metric space (X, d) carries two levels of structure:
the **topological** level (open sets, continuity, convergence) and the
**metric** level (distances, balls, rates). For finite or countable discrete
spaces, the metric level contains far more information than the topological
level alone.

---

## Cross-reference to Pilot Examples

| Pilot example (adams_franzosa_pilot_examples.md) | Expanded here |
|---|---|
| Example 4 (Hamming metric, error-correcting codes) | §A.2, A.3, A.4, A.5, A.6 |
| Example 5 (DNA edit distance) | §B.1, B.2, B.3, B.4, B.5, B.6 |
