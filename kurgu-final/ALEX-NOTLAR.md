# Alex için notlar — B090 "Thanksgiving" kurgu/ses sürecinden çıkarılan dersler

Bu dosya, B090 bölümünün final kurgu, ses tasarımı, miks, VFX düzeltmesi ve teslim sürecini bulutta yürüten asistanın (Fable) kendi çalışmasını analiz ederek yerel üretim asistanı Alex için yazdığı notlardır. Amaç: aynı kaliteyi daha az sürtünmeyle, 7/24 ve seri biçimde üretmek.

Dürüst sınır: Bu süreçte **video üretilmedi**. Seedance klipleri ve kilitli S1–S4 bloğu daha önce üretilmişti; burada yapılan iş görüntü kurgusu, sıfırdan ses (TTS diyalog, efekt, ortam, müzik, miks), dudak uyumu, bir VFX düzeltmesi ve teslimdi. Karakter tutarlılığı görüntü tarafında üretim prompt disiplininden geldi; o kısımdaki gözlemler 2. bölümde ayrı verilmiştir.

---

## 1. Neyi doğru yaptım — ilkeler (öncelik sırasıyla)

### 1.1 Önce ölç, sonra karar ver
Kulak ve göz yokken tek doğruluk kaynağı sayıdır. Her iddia bir ölçümle doğrulandı:
- Ses: LUFS (ebur128), true peak, kesim noktalarında seviye sıçraması, 1,5 sn üstü sessizlik, stem başına RMS.
- Dudak uyumu: ağız açılış/kapanış **kare numarası** (24 fps kontak sayfası), replik başlangıcı = ağız açılış karesi.
- Anlaşılırlık: bitmiş diyalog izinin kelime zamanlı STT'si ile senaryo metninin birebir karşılaştırması.
- Görüntü: kare sayısı (6034), parça başına kare, anahtar kare bayrağı, birleştirme testi.
"Bence iyi oldu" yerine "diyalog −15,5 LUFS, TP −3,4, sıçrama yok" yazıldı. Yönetmen de böyle konuşuyor (zaman kodlu notlar); aynı dili kullanmak geri dönüşü hızlandırdı.

### 1.2 Deterministik, tek dosyadan yeniden üretilebilir boru hattı
Tüm ses kararları tek bir cue dosyasında (kur.py → cues.json) tutuldu. Değişiklik = bir satır düzenle, boru hattını baştan çalıştır: cue → stem render → miks → remux → stem FLAC → CSV → notlar → zip. Tam tur ~5 dakika.
Sonuç: Yönetmenin her notu (örn. "3:06 fren gereksiz", "Mama 0,3 sn öne") birkaç dakikada uygulanıp yeniden teslim edildi. Manuel düzenleme hiç yapılmadı; bu yüzden hata birikmedi ve her sürüm tekrar üretilebilir kaldı.
Kural: **Elle dokunulan hiçbir çıktı yok.** Çıktı yanlışsa kaynak kural düzeltilir, her şey yeniden üretilir.

### 1.3 Küçük, geri alınabilir adımlar; her adım commit + push + log
Her sürüm (v2 → v2.1 → … → v2.4c) ayrı commit. Ücretli her çağrı tek satır log (zaman, işlem, varyant sayısı, kredi). Hata olduğunda (örn. 24-bit ses, zip boyutu) geri dönüş ucuzdu.

### 1.4 Kalite kapıları sayısal ve otomatik; "inceleme" ayrı ve nadir
İki farklı şey karıştırılmamalı:
- **Kapı (gate):** scriptin kendi içinde, her çalıştırmada, ücretsiz, saniyeler. Eşik aşıldıysa durur. (LUFS hedefi, TP ≤ −1, sıçrama ≤ 6 dB, sessizlik ≤ 1,5 sn, tempo ≤ 1,22, pencere aşımı ≤ 0,33 sn, kare sayısı eşitliği…)
- **İnceleme (review):** ajanlı, pahalı, dakikalar. Yalnızca kendi gözümün yetmeyeceği yerde ve yalnızca kilometre taşlarında.
Bu projede yüzlerce kapı çalıştırması, toplam **4 ajanlı inceleme** vardı: kare kare efekt taraması (üretim girdisi, 11+5 ajan), iki ağız/göz zamanlaması doğrulaması (6 ajan), VFX kompozit QA (3 tur: 3+3+2 ajan). Hepsi üretimle **paralel** çalıştı; hiçbiri boru hattını bekletmedi.

### 1.5 İncelemenin sözleşmesi: şema + somut düzeltme + üçlü karar
Her inceleme ajanı şu şemayla döndü: `verdict ∈ {ship, minor_fix, redo}`, `score`, `issues[] {frame, issue, severity, viewer_visible, fix}`, `notes`. Kurallar:
- `fix` sayısal ve uygulanabilir olmak zorunda ("daha doğal olsun" geçersiz; "k1843'te yaprak 8 px yukarı, 4 px sağa" geçerli).
- Yalnızca `viewer_visible=true` olanlar düzeltilir; "piksel bakıcı" bulguları loglanır, uygulanmaz.
- Aynı konu için en fazla 3 tur. İki ajan "ship" dediğinde durulur.
- Farklı mercekler (hareket / entegrasyon / şüpheci), aynı prompt'un 3 kopyası değil. Fikir ayrılıklarında ölçüm kazanır.

### 1.6 Yönetmen geri bildirimi > kendi kendine QA
En değerli kalite kapısı yönetmenin zaman kodlu notlarıydı. Erken ve sık teslim (önizleme + zip), notları **aynen** uygulama, ama kareye bakarak: Yönetmen "Mama 0,25–0,3 sn öne" dedi; kare ağız açılışını 0,44 sn önce gösterdi; kare uygulandı ve fark raporlandı. Tahmin yok, kare var.

### 1.7 Dürüst raporlama
Doğrulanmayan şey doğrulandı denmedi; yanlışlar açıkça yazıldı (kaynakların 720p olduğu, 24-bit sesin telefonda çalmadığı, daha önce "1080p" yazılmış notun düzeltilmesi). Yönetmen güvenini bu sağlar; "mükemmel" demek değil.

### 1.8 Kredi/bütçe disiplini
- Her üretimde `generations_count=1` (varyant seçme lüksü yok; gerekirse ikinci tek üretim).
- Tavan (25.000) ve kalan yüzdesi her turda hesaplandı; iki ardışık hatada durma kuralı.
- Pahalı STT yalnızca kısa kesitlerde; tam film STT'si (1.383 kredi) bir kez yapıldı ve bir daha yapılmadı.
- Sınıflandırıcı reddi aldığında aynı çağrı **bir kez** tekrarlandı; ikinci reddi kural ihlali say.

---

## 2. Karakter/sahne tutarlılığı — üretim prompt'larında gördüğüm iyi uygulamalar
(Video üretimini ben yapmadım; `ciktilar/*/payload.json` dosyalarındaki prompt'larda tutarlılığı sağlayan kalıplar şunlardı.)
1. **Değişmez karakter kartı:** Her klipte aynı cümlelerle, aynı sırada: boy oranı ("frame yüksekliğinin %42–50'si"), boynuz oranı ("kafa genişliğinin 1,8 katı"), renk, burun, gözler, kazak detayı. Kart kelimesi kelimesine kopyalanıyor; "benzer" yazılmıyor.
2. **Referans görsel slotları sabit:** @Image 1 = Barnaby kafa, @Image 6 = tam vücut profil, @Image 2 = Hazel, … Her klipte aynı eşleme. Ve kritik cümle: "Every Barnaby reference gives identity only, never size or crop."
3. **Negatif kısıtlar baştan:** "Exactly four characters", "Only one Barnaby is in the frame", "Subtitle-free, no logo, no watermark."
4. **Zaman kodlu aksiyon:** "At about second 3.4 Barnaby says … his lips moving to the words" — bu, sonradan dudak uyumu için ağız penceresi tahmini sağlıyor.
5. **Kilitli blok:** Onaylanan S1–S4 bloğu dokunulmaz kaynak olarak kullanıldı; yalnızca ses üstüne yazıldı. Tek istisna (yaprak ışınlanması) ayrı bir VFX olarak, görüntü üretmeden kompozitle çözüldü.
Öneri: Her klip üretiminden sonra tek otomatik kontrol: 4 fps kontak sayfası + **bir** okuyucu ajan, yalnızca "kırmızı çizgi" ihlallerini (ikinci Barnaby, altyazı, boynuz/renk kaybı, karakter sayısı) işaretlesin. Estetik yorum istenmesin; o yönetmenin işi.

---

## 3. Ses reçetesi (bu bölümde işe yarayan sayılar)

### 3.1 Diyalog
- Tüm replikler TTS, kilitli ses kimlikleri; orijinal üretim sesi hiç kullanılmadı (hışırtı/mikrofon tonu sorunu böyle bitti).
- Ağız penceresi: orijinal konuşmanın kelime zamanlı STT'sinden (varsa) ya da 24 fps kontak sayfasından. Replik **ağız açılış karesinde** başlar.
- TTS kırpma: −40 dBFS eşik; 30 ms ön, 80–100 ms kuyruk; 60 ms çıkış fade.
- Hız: en fazla ×1,22 (1 sn altı ünlemlerde ×1,30); tek tek istisnalar listede (CAP). Pencereyi 0,33 sn'den fazla aşan replik kabul edilmez; aşanlar raporlanır.
- Seviye: her replik −23 dBFS RMS'e normalize (bus öncesi); gece sahnelerinde −1,5 dB, Hazel −0,5 dB.
- Çakışma kuralı: Sonraki replikten en az 60 ms önce bit; kesilecek kısım sessiz kuyruksa kırp, konuşmaysa sonraki repliği en fazla 0,4 sn geciktir.
- Görünen her ağız hareketinin sesi olmalı; senaryoda yoksa kısa bir "Um…" bile ekle (yönetmen bunu fark ediyor).
- Doğrulama: bitmiş diyalog izi STT → senaryo ile birebir; farklar listelenir ("Oh"→"Ho" gibi kulakla anlaşılır üç istisna kabul edildi).

### 3.2 Efektler
- Kare kare tarama: 1 sn = 1 kontak sayfası (24 kare, üstünde zaman + kare no). Okuyucu ajanlar JSON olay listesi döndürür: `{t, ad, tepe_dBFS, tür, güven, açıklama}`. Eşleme kuralları (regex) kütüphane adına çevirir; 0,25 sn aynı ad / 0,5 sn çapraz kaynak tekilleştirme; koşu döngüleri aralık olarak birleştirilir.
- Seviyeler tepe dBFS ile verilir; `sfx()` gain = tepe + 6 dB (normalize kaynaklar −1 dBFS).
- Her görünür fiziksel olaya ses; kesme/dissolve'a ses **yok**.

### 3.3 Ortam ve müzik
- Gündüz orman döngüsü (RMS −42,5) → gece orman döngüsü (−43,5), 12 sn çapraz; gün batımında kısılır.
- Müzik hedefi −29 dBFS (ilk −25 çok yüksek bulundu), diyalog altında −8 dB ducking (0,3 sn öncesi, 0,5 sn sonrası).

### 3.4 Miks ve ölçüm kapıları
- Stem toplamı → bus kompresör (eşik −30 dB, oran 1,35) → kazanç, **diyalog stem'i −15,5 LUFS olacak şekilde** (bütün değil, diyalog sabitlenir) → limiter (lookahead gecikmesi telafili).
- Kapılar: TP ≤ −1 dBTP; kesimlerde sıçrama ≤ +6 dB; sessizlik ≤ 1,5 sn; bütün −18…−16 LUFS aralığı yalnızca bilgi.
- Teslim: 4 stem FLAC + tam miks FLAC, zaman kodlu CSV (zaman, tür, kim, metin, dosya, not), ölçüm JSON, OKU notu, kredi logu.

### 3.5 Yönetmenin bu bölümde öğrettiği zevk kuralları (bir sonraki bölümde baştan uygula)
- Fren/lastik kayması sesi **yok**; ani duruş = yaprak üstünde kayan toynak hışırtısı.
- "Çın/ping" aksanları en aza; göz açılması, uyanış gibi yerlerde bile tartışmalı. Doink yalnızca net gag anlarında.
- Çan sesi çan gibi olmalı (çın-çın el çanı); karakterin tepkisinden **0,5–1 sn önce** çalmalı ki izleyici önce sesi algılasın.
- Müzik diyalogun altında, sahnede değil arkada.
- Yaprak hışırtıları hafif; koşu döngüleri olabilir ama arka planda.
- Kaz sürüsü geçişi gibi "dünya" sesleri sevildi; yakın tek korna sevilmedi.
- Replik 0,25 sn geç başlarsa fark ediliyor; her replik ağız açılışında.

---

## 4. Görüntü teslimi (öğrenilenler)
- Tüm kaynaklar 1280x720; master bu çözünürlükte CRF 14 (≈4 Mb/s). Büyütme detay eklemez; önerme, istenirse yönetmen kendi aracıyla yapar.
- Paylaşım sınırı varsa: 20 sn'lik MOV parçalar, zorlanmış anahtar kare (`force_key_frames` 20n), `-c copy` ile bölme, ses dilimi **ayrı ve örnek-hassas** (atrim) eklenir; birleştirme testi ile kare sayısı doğrulanır.
- Ses: 16-bit PCM (`sowt`). 24-bit (`in24`) telefon ve tarayıcıda sessiz çalar. Yönetmen önce telefondan izliyor; ilk izlenim orada oluşur.
- Tek dosya arşiv için 100 MB altı MP4 (CRF 17 + AAC 256k).
- Küçük VFX (ışınlanan nesne vb.) için görüntü üretme: sprite'ı filmin kendi karesinden al, yama için statik kameradan bir sonraki çekimin gerçek piksellerini kullan, hareket bulanıklığını shutter ortalamasıyla (≥32 örnek, dönüş dahil) yap, parlaklık rampasıyla hedef kareye bağla.

---

## 5. QA'da boğulmadan 7/24 üretim — çalışma düzeni önerisi

Sorun tanımı: Her adımda insan gibi inceleme yapmak üretimi durduruyor; inceleme bulguları elle uygulanınca her tur yeniden iş çıkarıyor.

Düzen:
1. **Üç katman:** (a) her çalıştırmada otomatik sayısal kapılar (ücretsiz, saniye); (b) kilometre taşında bir kez bağımsız ajan incelemesi (şemalı, paralel, zaman kutulu); (c) yönetmen notu (gerçek kalite kapısı). Üretim sırasında (b) yok.
2. **İnceleme tetikleyicileri (sadece bunlar):** kendi gözünün yetmediği kare okumaları; tek seferlik görsel risk (VFX, yeni geçiş); yönetmene gidecek sürümden hemen önce. Bir efekt seviyesini 1 dB değiştirmek için inceleme çağrılmaz.
3. **Şemalı inceleme sözleşmesi:** `verdict/score/issues[frame, issue, severity, viewer_visible, fix]/notes`. `fix` sayısal değilse bulgu geçersiz. Yalnızca `viewer_visible` olanlar uygulanır. En fazla 3 tur; iki "ship" = dur.
4. **Zaman kutusu ve paralellik:** inceleme en fazla N dakika; o sırada boru hattının geri kalanı (kodlama, paketleme) çalışır; inceleme kötü çıkarsa yalnızca etkilenen parça yeniden üretilir (bu projede 13 parçadan 1'i).
5. **Deterministik yeniden üretim olmadan QA yapma.** Önce "tek komutla her şey yeniden üretilir" durumuna gel; sonra QA bulguları ucuzlar.
6. **Kuyruk + checkpoint:** 7/24 için her sahne/bölüm bağımsız iş; her işin durumu (üretildi / kapıdan geçti / incelemede / yönetmende) dosyada; süreç yeniden başladığında kaldığı yerden devam.
7. **Üretim ve karar ayrımı:** Mekanik işler (kontak sayfası okuma, CSV, transkript karşılaştırma, kodlama) ucuz ve hızlı modele/alt ajanlara; planlama, yönetmen notu yorumlama, inceleme kararı ve VFX gibi muhakeme işleri en güçlü modele ve yüksek "effort" ayarına. Alt ajanlara şemalı tek görev ver; prompt'ta neyi **ölçeceğini** söyle, nasıl düşüneceğini değil.
8. **Prompt uzunluğu:** Çok kuralcı, uzun QC prompt'ları yeni modellerde kaliteyi düşürüyor. Her ajan prompt'u: bağlam (3–5 cümle) + ölçüm yöntemi + çıktı şeması. Gerisi gürültü.
9. **Flake yok, kök neden var:** Aynı bulgu ikinci kez gelirse kural düzeltilir (efekt eşleme regex'i, tempo sınırı), tek tek düzeltme yapılmaz.

---

## 6. Araç tuzakları (zaman kaybettirenler)
- `pgrep -f`/`pkill -f` kendi kabuk satırını da yakalar; kalıbı `crf 1[4]` gibi köşeli parantezle yaz.
- ffmpeg `-ss` girişten önce + `-vf drawtext=%{pts}` → etiketler sayfa başına göre sıfırlanır; film zamanı = ofset + etiket. Okuyucu ajanlara bunu açıkça yaz.
- ElevenLabs flow: büyük sonuçlar dosyaya düşer; indirip prompt metniyle eşle. STT'yi ham URL ile bağla, kısa kesit ver.
- Sınıflandırıcı reddi: bir kez tekrar.
- Teslim dosyası sınırı (~30 MiB): video parçalarını DaVinci'de art arda dizilecek şekilde böl; zip-split yerine bunu tercih et (yönetmen DaVinci kullanıyor).
- GitHub 100 MB dosya sınırı: tek dosya MP4'ü CRF 17 ile 95 MB'a sığdır.
- Limiter lookahead gecikmesi (239 örnek) telafi edilmezse dudak uyumu 5 ms kayar; küçük ama ölçülebilir.

---

## 7. Kısa kontrol listesi (bir sonraki bölüm için)
- [ ] Karakter kartı ve referans slotları her klipte birebir aynı mı?
- [ ] Her ağız hareketine replik var mı; replikler ağız açılış karesinde mi?
- [ ] Bitmiş diyalog STT'si senaryoyla birebir mi?
- [ ] Her görünür fiziksel olaya efekt var mı; kesmelere yok mu?
- [ ] Fren/çın/doink zevk kuralları uygulandı mı?
- [ ] Çanlar tepkiden 0,5–1 sn önce mi?
- [ ] Diyalog −15,5 LUFS, TP ≤ −1, sıçrama ≤ 6 dB, sessizlik ≤ 1,5 sn?
- [ ] Müzik diyalog altında (−29 hedef, −8 dB ducking)?
- [ ] Parçalar anahtar karede, ses 16-bit PCM, birleştirme testi kare sayısı tutuyor mu?
- [ ] Kredi logu güncel, tavan altında mı?
- [ ] OKU notunda doğrulanmayan şey "doğrulandı" diye yazılmadı mı?
