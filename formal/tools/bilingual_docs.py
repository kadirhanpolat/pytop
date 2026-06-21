#!/usr/bin/env python3
"""
bilingual_docs.py — Lean 4 topoloji teoremlerinden API'siz ikidilli belge üretici.

Yaklaşım:
  - Rol-yuvası şablonları: {cond}, {concl}, {lhs}, {rhs} slotları
    bağımsız varyant havuzlarından doldurulur → N×M kombinasyon
  - Deterministik çeşitlilik: hash(teorem_adı) % len(şablonlar)
  - Üç katman: ad (mevcut) · sözel ifade (otomatik) · yorum (elle yazılı)
  - Fazlalık engeli: teorem adını kelimeye döken cümleler yerine yorum katmanı öne çıkar

Kullanım:
    py -3.14 formal/tools/bilingual_docs.py
    py -3.14 formal/tools/bilingual_docs.py --lean PATH --out PATH
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ── Paths ───────────────────────────────────────────────────────────────────
TOOL_DIR = Path(__file__).parent
DATA_DIR  = TOOL_DIR / "data"
REPO_ROOT = TOOL_DIR.parent.parent

LEAN_DEFAULT = REPO_ROOT / "formal" / "Formal" / "SetTopology.lean"
OUT_DEFAULT  = REPO_ROOT / "docs"  / "SetTopology_Bilingual.md"

# ── Data model ──────────────────────────────────────────────────────────────

@dataclass
class TheoremEntry:
    name:      str
    section:   str
    doc_tr:    Optional[str]   # Turkish docstring already in the file
    hyp_preds: list[str]       # predicate names from h* hypotheses
    concl:     str             # raw conclusion text
    kind:      str             # iff | existence | subset | equality | implication | other

# ── Lean parser ─────────────────────────────────────────────────────────────

_SECTION_RE = re.compile(
    r'--\s*[-─]{10,}\s*\n--\s*\d+\.\s*(.+?)\s*\n'
)
_DOC_RE  = re.compile(r'/--\s*(.*?)\s*-/', re.DOTALL)
_HYPH_RE = re.compile(r'\(\s*h\w*\s*:\s*([\w.]+)')

_KIND_PATTERNS = [
    ('iff',         re.compile(r'↔|⟺')),
    ('existence',   re.compile(r'∃')),
    ('subset',      re.compile(r'⊆')),
    ('equality',    re.compile(r'(?<![<>!:])=(?!=)')),
]


def _classify_kind(concl: str) -> str:
    for name, pat in _KIND_PATTERNS:
        if pat.search(concl):
            return name
    return 'implication'


def _find_return_colon(text: str) -> Optional[int]:
    """Return index of the outermost ':' separating params from return type."""
    depth = 0
    for i, c in enumerate(text):
        if c in '([{':
            depth += 1
        elif c in ')]}':
            depth -= 1
        elif c == ':' and depth == 0:
            if i + 1 < len(text) and text[i + 1] in ('=', ':'):
                continue
            return i
    return None


def parse_lean(path: Path) -> list[TheoremEntry]:
    src = path.read_text(encoding='utf-8')

    # Index section headings: (char-position, title)
    section_idx: list[tuple[int, str]] = [
        (m.start(), m.group(1).strip()) for m in _SECTION_RE.finditer(src)
    ]

    def section_at(pos: int) -> str:
        title = "Genel / General"
        for sp, t in section_idx:
            if sp <= pos:
                title = t
        return title

    entries: list[TheoremEntry] = []
    search_start = 0

    while True:
        idx = src.find('\ntheorem ', search_start)
        if idx == -1:
            break

        # Grab a 3000-char window for the signature
        window = src[idx: idx + 3000]
        # Match: theorem name <params> : <conclusion> (until := or where or end)
        m = re.match(
            r'\ntheorem\s+(\w+)\s*'
            r'((?:\s*\{[^}]*\}|\s*\([^)]*\)|\s*\[[^\]]*\])*)'
            r'\s*:\s*'
            r'((?:[^\n]|\n[ \t]+[^\n]+)*?)(?=\s*:=|\s*\bwhere\b|\Z)',
            window,
            re.DOTALL,
        )
        if not m:
            search_start = idx + 1
            continue

        name   = m.group(1)
        params = m.group(2)
        concl  = re.sub(r'\s+', ' ', m.group(3)).strip()
        concl  = re.sub(r'\s*:=.*$', '', concl, flags=re.DOTALL).strip()

        # Extract preceding docstring (look back up to 500 chars)
        pre = src[max(0, idx - 500): idx]
        doc_tr: Optional[str] = None
        doc_ms = list(_DOC_RE.finditer(pre))
        if doc_ms:
            last = doc_ms[-1]
            gap  = pre[last.end():]
            if not re.search(r'\b(theorem|def|lemma|abbrev|structure|end)\b', gap):
                raw = last.group(1).strip()
                # Collapse internal whitespace from multi-line docstrings
                doc_tr = re.sub(r'\s*\n\s*', ' ', raw).strip()

        entries.append(TheoremEntry(
            name      = name,
            section   = section_at(idx),
            doc_tr    = doc_tr,
            hyp_preds = _HYPH_RE.findall(params),
            concl     = concl,
            kind      = _classify_kind(concl),
        ))

        search_start = idx + len(m.group(0))

    return entries

# ── Generator ───────────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def _pick(choices: list[str], seed: str) -> str:
    """Deterministic, varied selection: same seed → same choice, different seeds → varied."""
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return choices[h % len(choices)]


def _safe_format(template: str, **kwargs: str) -> str:
    """Format template; leave unknown {slots} intact rather than raising KeyError."""
    result = template
    for k, v in kwargs.items():
        result = result.replace('{' + k + '}', v)
    return result


class Generator:
    def __init__(self) -> None:
        self.terms   = _load_json(DATA_DIR / 'terms.json')
        self.tmpls   = _load_json(DATA_DIR / 'templates.json')
        self.remarks = _load_json(DATA_DIR / 'remarks.json')

    # ── Low-level helpers ────────────────────────────────────────────────────

    def _pred_phrase(self, pred: str, lang: str, seed: str) -> Optional[str]:
        variants = self.terms['predicates'].get(pred, {}).get(lang)
        return _pick(variants, seed + pred + lang) if variants else None

    def _concl_phrase(self, concl: str, lang: str, seed: str) -> str:
        """Map conclusion text to a natural-language phrase via keyword lookup."""
        for kw, entry in self.terms['conclusions'].items():
            if kw in concl:
                variants = entry.get(lang)
                if variants:
                    return _pick(variants, seed + kw + lang)
        return self._subst(concl, lang)

    def _subst(self, text: str, lang: str) -> str:
        """Apply Lean → natural-language substitutions."""
        for lean_str, nl in self.terms['substitutions'].get(lang, {}).items():
            text = text.replace(lean_str, nl)
        return text.strip()

    # ── Condition phrase ─────────────────────────────────────────────────────

    def _cond_str(self, hyps: list[str], lang: str, seed: str) -> str:
        phrases = [
            p for h in hyps
            if (p := self._pred_phrase(h, lang, seed)) is not None
        ]
        if not phrases:
            return (
                'verilen koşullar altında' if lang == 'tr'
                else 'under the given conditions'
            )
        if len(phrases) == 1:
            return phrases[0]
        sep_last = ' ve ' if lang == 'tr' else ' and '
        return ', '.join(phrases[:-1]) + sep_last + phrases[-1]

    # ── Sentence builder ─────────────────────────────────────────────────────

    def sentence(self, thm: TheoremEntry, lang: str) -> str:
        k    = thm.kind
        seed = thm.name
        bank = self.tmpls.get(k, self.tmpls['other'])
        tmpl = _pick(bank.get(lang, bank.get('en', ['{content}'])), seed + k + lang)

        cond  = self._cond_str(thm.hyp_preds, lang, seed)
        Cond  = cond[0].upper() + cond[1:] if cond else cond
        concl = self._concl_phrase(thm.concl, lang, seed)

        if k == 'iff':
            parts = re.split(r'↔', thm.concl, 1)
            lhs = self._subst(parts[0].strip(), lang)
            rhs = self._subst(parts[1].strip() if len(parts) > 1 else '', lang)
            return _safe_format(tmpl, lhs=lhs, rhs=rhs, content=f"{lhs} ↔ {rhs}")

        if k == 'subset':
            parts = thm.concl.split('⊆', 1)
            lhs = self._subst(parts[0].strip(), lang)
            rhs = self._subst(parts[1].strip() if len(parts) > 1 else '', lang)
            return _safe_format(tmpl, lhs=lhs, rhs=rhs, content=thm.concl)

        if k == 'equality':
            parts = re.split(r'(?<![<>!:])=(?!=)', thm.concl, 1)
            lhs = self._subst(parts[0].strip(), lang)
            rhs = self._subst(parts[1].strip() if len(parts) > 1 else '', lang)
            return _safe_format(tmpl, lhs=lhs, rhs=rhs, content=thm.concl)

        if k == 'existence':
            m = re.search(r'∃\s*\w+\s*:\s*(\w+)', thm.concl)
            obj_raw = m.group(1) if m else 'object'
            obj  = self._subst(obj_raw, lang)
            prop = self._subst(thm.concl, lang)
            return _safe_format(
                tmpl,
                obj=obj, prop=prop,
                cond=cond,
                content=prop,
            )

        # implication / other
        return _safe_format(
            tmpl,
            cond=cond,
            Cond=Cond,
            concl=concl,
            content=concl,
        )

    def remark(self, name: str, lang: str) -> Optional[str]:
        return self.remarks.get(name, {}).get(lang)

    # ── Redundancy check ─────────────────────────────────────────────────────

    @staticmethod
    def _redundant(sentence: str, thm_name: str) -> bool:
        """True if the sentence merely restates the theorem name in words."""
        name_words = set(re.sub(r'[_\W]', ' ', thm_name).lower().split())
        sent_words = set(re.sub(r'[^\w]', ' ', sentence).lower().split())
        stop = {'is', 'of', 'the', 'a', 'an', 'in', 'to', 'and', 'or',
                'bir', 've', 'ile', 'için', 'da', 'de', 'ni', 'nın'}
        name_words -= stop
        sent_words -= stop
        if not name_words:
            return False
        overlap = len(name_words & sent_words) / len(name_words)
        return overlap > 0.75


# ── Markdown output ──────────────────────────────────────────────────────────

def write_markdown(entries: list[TheoremEntry], gen: Generator, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)

    header = (
        "# SetTopology — İkidilli Teorem Kılavuzu\n"
        "# Bilingual Theorem Reference\n\n"
        "> Bu dosya `formal/tools/bilingual_docs.py` tarafından otomatik üretilir.  \n"
        "> This file is auto-generated by `formal/tools/bilingual_docs.py`.  \n"
        "> Yorum satırları (`>`) elle yazılmıştır — `data/remarks.json`.  \n"
        "> Remarks (`>`) are hand-curated — `data/remarks.json`.\n\n"
        "---\n"
    )

    lines: list[str] = [header]
    current_section: Optional[str] = None

    for e in entries:
        if e.section != current_section:
            current_section = e.section
            lines.append(f"\n## {e.section}\n")

        lines.append(f"\n### `{e.name}`\n\n")

        en = gen.sentence(e, 'en')
        tr = gen.sentence(e, 'tr')

        # Redundancy check: if auto-sentence just restates the name, fall back to raw concl
        if gen._redundant(en, e.name):
            en = f"`{e.concl}`"
        if gen._redundant(tr, e.name):
            tr = f"`{e.concl}`"

        lines.append(f"**EN:** {en}  \n")
        lines.append(f"**TR:** {tr}\n")

        rem_en = gen.remark(e.name, 'en')
        rem_tr = gen.remark(e.name, 'tr')
        if rem_en or rem_tr:
            lines.append("\n")
            if rem_en:
                lines.append(f"> *{rem_en}*  \n")
            if rem_tr:
                lines.append(f"> *{rem_tr}*\n")

    out.write_text(''.join(lines), encoding='utf-8')
    print(f"✓ {len(entries)} teorem işlendi / theorems processed")
    print(f"  → {out}")


# ── Entry point ──────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description='Lean topoloji teoremlerinden ikidilli belge üretici')
    ap.add_argument('--lean', type=Path, default=LEAN_DEFAULT,
                    help='Lean kaynak dosyası (varsayılan: formal/Formal/SetTopology.lean)')
    ap.add_argument('--out',  type=Path, default=OUT_DEFAULT,
                    help='Çıktı markdown dosyası (varsayılan: docs/SetTopology_Bilingual.md)')
    args = ap.parse_args()

    lean = args.lean if args.lean.is_absolute() else Path.cwd() / args.lean
    out  = args.out  if args.out.is_absolute()  else Path.cwd() / args.out

    if not lean.exists():
        raise SystemExit(f"Dosya bulunamadı / File not found: {lean}")

    print(f"Ayrıştırılıyor / Parsing: {lean.name}")
    entries = parse_lean(lean)
    print(f"  {len(entries)} teorem bulundu / theorems found")

    gen = Generator()
    write_markdown(entries, gen, out)


if __name__ == '__main__':
    main()
