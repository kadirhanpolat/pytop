# pytop Notebooks

Her notebook beş bölümden oluşur:

| Bölüm | İçerik |
|-------|--------|
| **1. Konu** | Sezgisel açıklama + formal tanımlar |
| **2. Teoremler** | Anahtar teoremler + tam ispat |
| **3. API** | pytop fonksiyonları, tag sistemi, `Result` nesnesi |
| **4. Örnekler** | 4+ örnek, Basit → Karmaşık |
| **5. Alıştırmalar** | Kodlama görevi + Teori sorusu + Karşılaştırma |

## Mevcut Notebook'lar

### Çekirdek Topoloji

| Notebook | Modül(ler) | Konu |
|----------|-----------|------|
| [spaces_and_predicates.ipynb](spaces_and_predicates.ipynb) | `pytop.spaces`, `pytop.predicates` | Topolojik uzay tanımı, açık/kapalı kümeler, yoğunluk |
| [compactness.ipynb](compactness.ipynb) | `pytop.compactness` | Kompaktlık, Lindelöf, sayılabilir kompaktlık, Heine-Borel |
| [metric_spaces.ipynb](metric_spaces.ipynb) | `pytop.metric_spaces` | Metrik uzaylar, açık toplar, indüklenen topoloji, Baire |
| [maps.ipynb](maps.ipynb) | `pytop.maps` | Süreklilik, homeomorfizma, gömme, bölüm fonksiyonu |

### İleri Topoloji

| Notebook | Modül | Konu |
|----------|-------|------|
| [persistent_homology.ipynb](persistent_homology.ipynb) | `pytop.persistent_homology` | TDA, filtrasyonlar, kalıcılık diyagramları, kararlılık teoremi |

## Kurulum

```bash
pip install -e .
pip install jupyter
jupyter notebook notebooks/
```

## Hedef Kitle

Notebooklar iki katmanlıdır:
- **Matematikçi**: Teorem ifadeleri, ispat iskeletleri, formal tanımlar
- **Python kullanıcısı**: pytop API'si, tag sistemi, `Result` nesnesiyle çalışma
