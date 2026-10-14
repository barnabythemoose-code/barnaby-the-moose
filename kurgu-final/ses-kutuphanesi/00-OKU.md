# B090 "Thanksgiving" — Ses Kütüphanesi (kendi miksini yapmak için)

Bu paket, filmin ses kurgusunda kullanılan **her ögeyi tek tek**, zaman koduyla adlandırılmış ve ham (işlenmemiş) halde içerir. Hiçbir şey birbirine yapıştırılmamıştır; hangi sesi açıp kapatacağına, seviyesine ve yerine sen karar verirsin.

## Standart
- Zaman çizelgesi: **24 fps**, filmin ilk karesi 00:00:00:00, toplam süre **4:11,417** (6034 kare, son kare 00:04:11:10). Tüm süreler film başından itibaren.
- Ses: **48 kHz, 24 bit, FLAC**, stereo. MP3/WAV kaynaklar FLAC'e çevrildi; kalite kaybı yok. Sekansı 48 kHz açarsan dönüştürme (conform) olmaz.
- Dosya adı öneki = kurgudaki başlangıç zamanı, milisaniye hassasiyetinde: `02m18s750_...` → 2 dk 18,750 sn. `cue-sheet.csv`'de aynı zaman `film_t0_sn` (sn), `film_tc` (SS:DD:SS:KK) ve `kare` olarak da var. **`kare`/`film_tc` en yakın kareye yuvarlamadır (≤ 21 ms fark)**; hassas yer için `film_t0_sn` kullan (ses izleri karelerden bağımsız yerleşebilir).
- **Tekil dosyalar HAM seviyededir** (benim kazancım uygulanmadı). Kullandığım kazanç `kurguda_kullanilan_kazanc_dB` sütununda sayı olarak durur, başlangıç noktası diye. İstisnalar `not` sütununda **BÜYÜK HARFLE** yazılıdır: `03-ortam/..._esinti-yatak-..._kazancli` (+14,6 dB uygulandı), `06/..._SADECE-YENI-REPLIKLER` (kurgudaki seviyede) ve `08-tam-uzunluk-izler` (kurgudaki haliyle).
- `tempo` sütunu 1,0'dan farklıysa (1,05 / 1,08 / 1,1 / 1,2 / 0,92 / 1,12) o hız değişimi dosyaya **uygulanmıştır**; süre kurgudaki süredir.
- 7 dosyanın kaynağı 0 dBFS'i aşıyordu; bunlar −0,5 dBFS tepeye normalize edildi, miktarı `not`ta ("DIKKAT: … normalize") yazar; kazancı o kadar artır.

## Klasörler
| Klasör | İçerik |
|---|---|
| `01-diyalog/` | 39 replik (S6–S9): ElevenLabs ses dönüştürme/TTS, kilitli Hazel/Barnaby/Anne/Baba sesleri. Ad: zaman_replikKodu_karakter_metin. `S1-S4-yeni-dublaj/`: 0–44 sn için 8 yeni replik (kırpılmış, hızı uygulanmış, ham seviye). |
| `02-efekt/yerlesim/` | Her efekt, kurgudaki **her yerleşim için ayrı dosya** (3 kaz sesi = 3 dosya, 9 tepik = 9 dosya). `kaynak/`: 11 tek kopya. `kaynak/alternatifler/`: 13 kullanılmayan varyant (3 ek tepik, çan/yün/fındık v1-v2 vb.). |
| `03-ortam/` | 7 sahne "ortam" dosyası + S8-2→son için esinti yatağı. **Dikkat:** S6-1, S6-2-D2, S6-3-E2, S6-4, S6-5, S8-1-B2 ortam dosyaları Seedance klip sesinin konuşma pencereleri sessize alınmış halidir, **sürekli oda tonu değildir** (büyük kısmı sessiz). Sürekli yatak istersen `alternatifler/` içindeki 12 sn esinti dosyalarını veya `esinti-sakin-dongu-ham`ı döngüle. |
| `04-muzik/` | M1 (S6–S7, **2:17,250**'de başlar, 0–60,883 sn kullanıldı) ve M2 (S8–S9, **3:16,833**'te başlar, 0–54,584 sn kullanıldı) ham tam parçalar + kullandığım **ducking otomasyonu** CSV (film zamanı → toplam dB, zaman sıralı). İstersen hiç kullanma, kendin duck'la. |
| `05-hazir-miksler-B-efektli/` ve `-A-efektsiz/` | S5-1a…S5-3b, S6-2-D1, S6-3-E1 için sahibin önceki aşamadaki hazır diyalog+efekt miksleri. Kurgudaki kesimle aynı uzunluk. **B veya A'dan birini kullan.** A seçersen bu 9 sahnede hiç efekt kalmaz; bu sahnelerin ayrı efekt kaynağı pakette yok (referans B ile yapıldı). S5-3b'nin ilk 2,5 sn'si kurguda −5→0 dB rampayla girdi (dosyada yok, cue-sheet `zarf_otomasyon`). |
| `06-S1-S4-blok/` | İlk 104,042 sn (kilitli blok). Aşağıya bak. |
| `07-orijinal-klip-sesleri/` | Her Seedance klibinin kendi ham sesi, kurguda kullanılan kare aralığına kesilmiş ve film zamanına adlandırılmış (17 dosya; 6 klipte ses izi yok). **Çoğunda makine konuşması var**; `not` sütunu söyler. S5 ve S6-2-D1/S6-3-E1 klipleri 05 hazır mikslerle **aynı konuşmayı** içerir, üst üste koyma. Ortam/efekt kaynağı olarak kullanırsan konuşma pencerelerini sustur. |
| `08-tam-uzunluk-izler/` | Kategori başına **film boyu (4:11,417) hizalı** izler: S1-S4-blok, diyalog, efekt, ortam, müzik, hazır-miks B, hazır-miks A. 0:00'a koy, yerleşim bitti. Kurgudaki kazanç/zarf/fade uygulanmış. + `REFERANS_tam-miks-B-efektli` (benim son miksim). |
| `09-referans/` | 480p görüntü, benim son miksimle. Hizalama kontrolü için. |
| `cue-sheet.csv` | 161 satır: paketteki **her** ses dosyası (kaynak/alternatifler dahil). Zaman, süre, sahne, karakter, metin, kazanç, tempo, kaynak, not. UTF-8, virgül ayraçlı. `cue-sheet_excel-tr.csv`: aynı tablo, noktalı virgül ayraçlı ve ondalık virgüllü (Türkçe Excel). `cue-sheet.json`: aynı veri. |
| `zaman-cizelgesi.csv` | Sahne giriş/çıkış zamanları ve kareleri. |

## Hızlı başlangıç (iki yol)
1. **Hazır hizalı izlerle:** `08-tam-uzunluk-izler/` içinden S1-S4-blok, diyalog, efekt, ortam, müzik ve hazır-miks **B** *veya* **A** izlerini 0:00'a at; her şey yerinde. Beğenmediğin ögeyi o izden kesip `01–07`'deki ham tekiliyle değiştir veya sustur.
2. **Sıfırdan:** `01–07`'deki tekil dosyaları ad önekindeki zamana at. `cue-sheet.csv` zaman sıralıdır; satır satır git.

**Referans miks hakkında:** `REFERANS_tam-miks-B-efektli` = 08 izlerinin toplamı (B) + bus kompresör (eşik −30 dB, oran 1,35, atak 40 ms, bırakma 700 ms) + +7 dB + tepe sınırlayıcı −3,9 dBFS. İzleri olduğu gibi toplarsan ≈ −16,5 LUFS, LRA ≈ 12 çıkar; −15,6 LUFS / LRA 8 için bus işlemi gerekir. Referans ve 09 videosu izlerle örnek hassasiyetinde hizalıdır (sınırlayıcı gecikmesi telafi edildi).

## 06-S1-S4-blok: ilk 44 saniye için seçenekler
Blok sesi tek kanaldır (Seedance konuşma + yaprak/ayak + ortam aynı izde). Bu yüzden birkaç halini verdim; **hepsi 0:00'a konur**:
- `..._ORIJINAL_mobil-v2` — dokunulmamış mobil kurgu sesi, kurgudaki kesim noktasında (104,042 sn) 40 ms fade ile kesildi. Eski konuşmalar ve yüksek yaprak sesi içinde.
- `..._0-44_YATAK_eski-konusma-susturulmus` — orijinal; yalnız eski konuşma pencerelerinde −30 dB kısılmış, bloğun kendi ortam döngüsüyle doldurulmuş, 13,6–16,4 sn −8 dB ve 25,4–27,0 sn −10 dB gürültü kısması uygulanmış. **Yeni replik yok.** Üstüne `01-diyalog/S1-S4-yeni-dublaj/` tekillerini (ham) veya `..._SADECE-YENI-REPLIKLER`i (kurgudaki seviyede) koy. 44,5 sn'den 104,042'ye kadar `ORIJINAL` ile devam et; ek yapısı aynıdır, geçiş gerekmez.
- `..._0-44_KALINTI_...` — ses ayırma ile konuşması çıkarılmış hal; eski konuşma kısmen duyulur, yalnız alternatif.
- `..._0-44_IZOLE-ESKI-KONUSMA` — yalnız eski konuşmalar (zamanlama referansı, mikse koyma).
- `..._KURGUDAKI_yeni-dublaj-miks_rev3` — finaldeki hal (= 08/S1-S4-blok izi). 0–44 yeni dublaj; 44,5 sn sonrası orijinal.
- `eski-konusma-pencereleri.json` — eski konuşma aralıkları (sn): 1,57–5,13 · 18,87–21,48 · 23,77–26,13 · 30,92–31,93 · 37,62–39,03 ve şikâyet ettiğin gürültü bölgeleri: **13,6–16,4** (gürültü benzeri yaprak/rüzgâr) ve **25,4–27,0** (yüksek yaprak). Orijinali kullanıyorsan buraları kıs/kes.
- `ortam-dongusu_blok-6-9sn` — bloğun kendi temiz ortamından 3 sn; boşluk doldurmak için.

## Dudak uyumu / kayma kontrol listesi
1. Sekans 24 fps, 48 kHz; FLAC'ler zaten 48 kHz (dönüştürme yok).
2. Her dosyayı ad önekindeki zamana (veya `film_t0_sn`) koy; `kare` sütunu yuvarlamadır.
3. Replik başlangıçları ağız pencerelerine oturtulmuştur; kaydıracaksan ±2 kareyi geçme. Bir replik sahne kesiminden **önce** başlıyorsa bu bilerek yapılmış **ses-önce (J-cut)** kesimdir, `not`ta yazar (ör. Anne'nin S8-1 repliği kesimden 9 kare önce başlar); kesime çekme.
4. Kontrol: filmin sonu 00:04:11:10'da bitmeli; `02m45s967` el çanı (S6-4) ve `03m53s442` çan (S9-1) 09 videosundaki çanla üst üste düşmeli.

## Seviye başlangıç noktaları (görevdeki hedefler)
- Bütün: −16…−14 LUFS entegre, tepe ≤ −1 dBTP, LRA ≤ 8.
- Diyalog ≈ −16 LUFS (fısıltı/yakın replikler −18…−20), müzik diyalog altında −8…−9 dB duck, ortam ≈ −38…−40 LUFS.
- Kullandığım tüm kazançlar cue-sheet'te; müzik otomasyonu 04-muzik CSV'lerinde.

## Notlar
- Bu paket için yeni ses üretilmedi; sıfır ElevenLabs kredisi. Her şey mevcut üretimlerden.
- Ses kimlikleri kilitli: Barnaby, Hazel, Anne, Baba (yeni ses yok).
- Finalde "Is that maple?" (S8-4) dudak uyumu için çıkarıldı; pakette de yok. Barnaby'nin "I followed Papa's pie. It was a tree." repliği iki dosyadır (B74a / B74b).
- Kullanılan kaynak yolları (`kaynak_dosya`) benim çalışma kopyama göredir; sadece iz sürmek için.
