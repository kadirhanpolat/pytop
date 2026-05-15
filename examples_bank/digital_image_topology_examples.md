# Dijital Görüntü İşleme Topolojisi -- EMB-02

- Sürüm: `v0.2.203`
- Hat: `EMB-02`
- Kaynak odağı: Adams & Franzosa Bölüm 11.3
- Dil ilkesi: Bu dosya Türkçedir; Python API adları paket standardı gereği
  İngilizce tutulmuştur.

## 1. Dijital Görüntü Neden Topolojik Bir Nesnedir?

Bir dijital görüntü yalnızca renk değerlerinden oluşan bir tablo değildir. Hangi
piksellerin komşu sayıldığı da modelin parçasıdır. Bu komşuluk seçimi,
görüntüdeki nesnelerin bağlı olup olmadığını, sınırın kopuk görünüp
görünmediğini ve arka planın kaç bileşene ayrıldığını değiştirir.

Bu yüzden dijital görüntü işleme topolojisinde temel soru şudur:

```text
Pikseller hangi komşuluk kuralıyla okunuyor?
```

## 2. 4-Bağlılık ve 8-Bağlılık

4-bağlılıkta bir piksel yalnızca yatay ve dikey komşularıyla bitişik sayılır.
8-bağlılıkta ise çapraz komşular da bitişik kabul edilir.

```text
4-bağlılık:  üst, alt, sol, sağ
8-bağlılık:  üst, alt, sol, sağ + dört çapraz komşu
```

Nesne pikselleri için 4-bağlılık seçmek, köşeden temas eden iki parçayı ayrı
tutabilir. Nesne pikselleri için 8-bağlılık seçmek ise aynı iki parçayı tek
bileşen sayabilir. Aynı görüntü, farklı komşuluk sözleşmeleri altında farklı
topolojik sonuçlar verir.

## 3. Nesne-Arka Plan İkiliği

Dijital görüntüde nesne ve arka planı aynı komşuluk kuralıyla okumak bazen
paradoks üretir. Bu yüzden sık kullanılan öğretim kuralı şudur:

```text
Nesne 4-bağlı okunuyorsa arka plan 8-bağlı okunur.
Nesne 8-bağlı okunuyorsa arka plan 4-bağlı okunur.
```

Bu ikili seçim, dijital Jordan sezgisini daha tutarlı hale getirir: nesnenin
sınırı, arka planın ayrımını beklenmedik şekilde bozmaz.

## 4. Dijital Eğri ve Jordan Sezgisi

Sürekli düzlemde basit kapalı bir Jordan eğrisi düzlemi iç ve dış olmak üzere
iki bileşene ayırır. Dijital düzlemde ise bu sezgi komşuluk kuralına bağlıdır.
Köşeden temas eden pikseller, seçilen kurala göre bağlı veya ayrı sayılabilir.

EMB-02'nin ana uyarısı budur: dijital eğri teorisinde "eğri kapalı mı" sorusu,
yalnızca piksel kümesine değil, komşuluk sözleşmesine de bağlıdır.

## 5. Bölütleme İçin Topolojik Kontrol

Görüntü bölütleme sırasında topolojik sinyaller kullanılabilir:

- bağlı bileşen sayısı,
- delik sayısı,
- sınırın kopuk olup olmadığı,
- nesne ve arka plan komşuluklarının uyumlu seçilip seçilmediği.

Gürültülü bir görüntüde tek piksellik köprüler iki nesneyi yanlışlıkla
birleştirebilir. Tek piksellik boşluklar ise bir nesneyi yanlışlıkla iki bileşen
gibi gösterebilir. Topolojik kontrol, bu hataları fark etmek için öğretim
amaçlı güçlü bir araçtır.

## 6. Paket Bağlantısı

Bu örnek dosyası şu modülle birlikte okunmalıdır:

```text
src/pytop/digital_image_topology.py
```

Önceki EMB-01 sürümü `src/pytop/embeddings.py` ile Jordan eğrisi ve gömü
profillerini açmıştı. EMB-02 bu hattı dijital görüntü işleme örneklerine taşır.
