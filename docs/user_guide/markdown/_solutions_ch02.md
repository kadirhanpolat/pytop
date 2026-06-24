## Bölüm 2: Önermeler Mantığı

### Alıştırma 6 — Dağılma Yasası (∧ üzerinden ∨)

(ch02 6. alıştırmasına dön)

İki değişkenli `check_tautology` deseni üç değişkene genişletilir: artık sekiz
`(p, q, r)` atamasının tümünü gezeriz. `iff` her atamada `True` dönerse ifade
bir tautolojidir.

```python
from pytop import Proposition, conjunction, disjunction, iff

triples = [(a, b, c) for a in (True, False)
                     for b in (True, False)
                     for c in (True, False)]

def check_tautology3(name, func):
    ok = all(
        func(Proposition("p", tp), Proposition("q", tq), Proposition("r", tr)).truth_value
        for tp, tq, tr in triples
    )
    print(f"{name}: {'tautoloji' if ok else 'DEGIL'}")

check_tautology3("p&(q|r) <-> (p&q)|(p&r)",
    lambda p, q, r: iff(conjunction(p, disjunction(q, r)),
                        disjunction(conjunction(p, q), conjunction(p, r))))
```

```text
p&(q|r) <-> (p&q)|(p&r): tautoloji
```

Sekiz satırın tamamında sol taraf `p & (q | r)` ile sağ taraf
`(p & q) | (p & r)` aynı doğruluk değerini alır. Sezgisel olarak: `p` yanlışsa
iki taraf da yanlıştır; `p` doğruysa her iki taraf da `q | r`'ye indirgenir.
Dolayısıyla `∧`, `∨` üzerinde dağılır. (Simetrik biçimde `∨`, `∧` üzerinde de
dağılır — `q` ile `r`'yi `∨`/`∧` rollerini değiştirerek aynı yöntemle
doğrulayabilirsiniz.)

### Alıştırma 7 — Kontrapozitif ≠ Tersi (Teori)

(ch02 7. alıştırmasına dön)

İddia yanlıştır: `p → q` doğru olduğunda `q → p` (tersi / converse) doğru olmak
**zorunda değildir**. `p → q`'nin gerçekten denk olduğu ifade kontrapozitif
`¬q → ¬p`'dir, tersi değil.

**Somut karşı-örnek.** `p` = "tam sayı 4'e bölünür", `q` = "tam sayı çifttir"
olsun.

- `p → q` **doğrudur**: 4'e bölünen her sayı çifttir (ör. 4, 8, 12).
- Tersi `q → p` **yanlıştır**: çift olan her sayı 4'e bölünmez — `6` çifttir
  ama 4'e bölünmez, yani `q` doğru iken `p` yanlıştır. Bu tek karşı-örnek
  `q → p`'yi çürütür.
- Kontrapozitif `¬q → ¬p` **doğrudur**: "çift değilse (tek ise) 4'e de bölünmez"
  — bu, `p → q` ile mantıksal olarak aynı içeriği taşır.

Genel kural: bir içerme her zaman kontrapozitifine denktir
(`(p → q) ↔ (¬q → ¬p)`, Bölüm 4'teki doğruluk tablosu kanıtı), ama tersine veya
 inverse'üne (`¬p → ¬q`) denk değildir. Öncül ile sonucu yer değiştirmek mantığın
yönünü tersine çevirir; yalnızca her ikisini birden olumsuzlayıp yer değiştirmek
(yani kontrapozitif) anlamı korur.
