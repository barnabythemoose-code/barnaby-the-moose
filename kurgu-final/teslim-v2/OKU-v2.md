# B090 "Thanksgiving" — Sıfırdan ses kurgusu (v2)

Bu sürümde **Seedance kaynaklı hiçbir ses kullanılmadı**. Blok (0–1:44), S5 hazır miksleri ve S6–S8 ses dönüştürme (VC) replikleri tamamen atıldı. Her ses tek tek, temiz kaynaklardan yerleştirildi.

## Dosyalar
| Dosya | İçerik |
|---|---|
| B090-TG-FINAL-v2-sifirdan-ses.mp4 | 1080p final, yeni ses (görüntü aynı, yalnız ses değişti) |
| B090-TG-FINAL-v2-onizleme-480p.mp4 | hızlı izleme |
| ses-listesi.csv | 146 satır: her repliğin ve efektin zamanı, kim, metin, dosya |
| stems/diyalog.flac, sfx.flac, ortam.flac, muzik.flac | film boyu hizalı izler (0:00'a koy); kurgudaki seviyede |
| stems/TAM-MIKS.flac | nihai miks (kayıpsız) |
| olcum.json | ölçümler |

## Ne yapıldı
- **Diyalog: 87 replik, hepsi ElevenLabs TTS (eleven_v3), kilitli sesler.** 63 yeni replik üretildi (S3-3…S8-1 Hazel/Barnaby, S8-1 Anne/Baba, D1/E1); 0–40 sn'nin 8 repliği ve S8-2…S9-2b'nin 15 repliği önceki onaylı TTS'ler. Ağız pencereleri Seedance'ın kendi konuşma zamanlarından (kelime zamanlı STT) alındı; her replik pencere başına oturtuldu, gerekirse en fazla ×1,22 (kısa ünlemlerde ×1,3) hız. 14 replik daha hızlı okunmuş ikinci take ile değiştirildi. Dört replik pencereyi 0,26–0,33 sn aşıyor (S3-5 "Promise", S4-4 "Run!", S5-3 "Then we stop and think", S6-5 "Not pie. Mama."): ağız kapanırken ses biter, anlaşılırlık için kabul edildi.
- **STT doğrulama (tüm diyalog izi):** 87 repliğin tamamı birebir okundu; yalnız üç kısa ünlemde STT farklı yazdı ("They're"→"Get", "Oh"→"Ho", "Run!"→"Rat"), kulakla anlaşılır.
- **Efektler, saniye saniye (54 yerleşim):** açılış çanı 0,30; kazlar 17,0 ve 90,2 ve 191,5; iniş/adım 23,3 / 36,1; Papa'nın uzak adımı 30,15; koklamalar 40,55 / 50,7 / 67,9; koku şeridi 41,05 / 177,6 (kopuşu 186,3); şurup damlası 65,15; ağaca yapışma "thwup" 75,26, boğuk "mmf", kurtulma "pop" 77,16; rüzgâr 80,4 ("the wind turned"); ikinci çan "DONG DONG" 85,9; koşu adımları 104,2 ve 183,55; yün hışırtısı 110,3 / 173,95; yaprak düşüşü 120,0; S6-4 yumuşak çan 165,95 / 169,3; Baba'nın adımları 200,1; ding-dong 203,1; S8-2→S9-2b'deki önceki onaylı efektler (adımlar, koklama, burun burna, yapışkan tık, çan, fındık, tabure, tepikler) korundu.
- **Ortam:** gündüz orman döngüsü (0–2:17, gün batımında kısılır) → gece orman döngüsü (2:06'dan sona, 12 sn çapraz). Beyaz gürültü karakteri yok; sessiz pencerelerde 4–12 kHz enerjisi eski mikse göre ~35 dB düşük.
- **Müzik:** yeni açılış parçası M0 (0:00–2:14, 8 sn kuyruk), M1 (2:17–3:18) ve M2 (3:17–son) aynı; diyalog altında −8 dB ducking, sonda +4 dB kalkış.
- **Miks:** diyalog −15,5 LUFS'a sabitlendi; bus kompresör (−30 dB, 1,35), tepe sınırlayıcı (gecikme telafili). Ölçüm: bütün −17,3 LUFS, TP −3,5 dBTP, LRA 4,1, kesimlerde sıçrama yok (en büyük < +6 dB), 1,5 sn'den uzun sessizlik yok. Not: bütün değeri −16'nın altında; diyalog seviyesi doğru, müzik/ortam bilinçli olarak diyaloğun altında tutuldu. İstenirse müzik +2 dB ile −16'ya çekilir.

## Kredi
Bu sürüm için harcanan: ~ kredi (TTS 63+14 retake, 12 efekt, 1 müzik, 3 STT). Proje toplamı: ~20209 kredi (tavan 25.000). Kayıt: ses-log.csv.

## Bilinen sınırlar
- Görüntüdeki ağız hareketleri Seedance'ın orijinal konuşmasına göre; yeni TTS aynı pencereye oturtuldu, kare kare "dudak şekli" eşleşmesi yok (hiçbir dublajda olmaz).
- S1–S2 (0–26 sn) görsel içerik belgesi olmadığından efektler yalnız senaryoda geçen olaylara (çan, kazlar, iniş) kondu.
