# π-base Tümdengelimli Çıkarım ve Atlas (deneysel) -- PIBASE-01

- Sürüm: `v0.6.0`
- Hat: `PIBASE-01`
- Kaynak odağı: π-base (topology.pi-base.org), Clontz & Dabbs — **CC BY 4.0**
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Ne Sağlıyor?

`pytop.experimental.pi_base`, π-base veritabanını (243 özellik, 902 implikasyon
teoremi, 222 uzay / 2099 trait) **gerçek bir tümdengelimli motora** dönüştürür:
bilinen trait'lerin implikasyon grafı altındaki kapanışını hesaplar
(forward chaining + contrapositive, `and`/`or`/`not` bileşik formülleriyle) ve
**çelişki** tespit eder. Veri stdlib `json` ile yüklenir (çalışma-zamanı bağımlılığı yok).

> Atıf: Veri π-base'den türetilmiştir (CC BY 4.0). `PI_BASE_ATTRIBUTION` sabitine bakınız.

## 2. Tümdengelimli Kapanış

```python
from pytop.experimental.pi_base import deduce, consequences, property_uid

# Bir tek trait'ten çıkarım: kompakt => sayılabilir kompakt (T000001)
print(consequences("Compact")[property_uid("Countably compact")])  # True

# Çoklu hipotez: kompakt + Hausdorff => normal
closure = deduce({property_uid("Compact"): True, property_uid("Hausdorff"): True})
print(closure[property_uid("Normal")])  # True
```

## 3. Çelişki (Tutarlılık) Denetimi

```python
from pytop.experimental.pi_base import is_consistent, InconsistentTraitsError, deduce, property_uid

# Kompakt, sayılabilir-kompaktlığı zorlar; tersini iddia etmek tutarsızdır
print(is_consistent({property_uid("Compact"): True, property_uid("Countably compact"): False}))  # False
```

## 4. Karşı-Örnek Bulma (Atlas)

```python
from pytop.experimental.pi_base_atlas import find_counterexamples, space_name, steen_seebach_index

# "Kompakt ama Hausdorff olmayan bir uzay var mı?"
ce = find_counterexamples(has=["Compact"], lacks=["Hausdorff"])
print(len(ce), [space_name(u) for u in ce[:3]])

# Steen–Seebach "Counterexamples in Topology" numarasıyla bağlantı
print(steen_seebach_index()[1])  # S000001: Discrete topology on {0,1}
```

## 5. Çapraz Doğrulama (pytop ↔ π-base)

`compare_traits`, pytop'un (veya herhangi bir dış kaynağın) özellik yargılarını
π-base'in tümdengelimli kapanışıyla karşılaştırır; uyuşmazlıkları döndürür:

```python
from pytop.experimental.pi_base import compare_traits, property_uid

# known'dan türet, claims'i denetle
conflicts = compare_traits({"P000016": True}, {property_uid("Countably compact"): False})
print(conflicts)  # bir TraitConflict: deduced=True vs expected=False
```

## 6. Köprü

Bu motor, ilk denetimde pytop'un en büyük yapısal zayıflığı olarak belirlenen
**elle-kodlanmış etiket-tabanlı çıkarımı**, referanslı ve makine-doğrulanabilir
bir implikasyon grafıyla güçlendirir. `tests/experimental/test_pi_base_crossvalidation.py`,
pytop'un kodladığı klasik implikasyonları bu grafa karşı sabitler.
