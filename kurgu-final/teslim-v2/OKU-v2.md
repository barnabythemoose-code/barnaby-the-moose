# B090 "Thanksgiving" — Sıfırdan ses kurgusu (v2.2, yönetmen düzeltmeleri)

Bu sürümde **Seedance kaynaklı hiçbir ses kullanılmadı**. Blok (0–1:44), S5 hazır miksleri ve S6–S8 ses dönüştürme (VC) replikleri tamamen atıldı. Her ses tek tek, temiz kaynaklardan yerleştirildi.

## Dosyalar
| Dosya | İçerik |
|---|---|
| B090-TG-FINAL-v2-sifirdan-ses.mp4 | 1080p final, yeni ses (görüntü aynı, yalnız ses değişti) |
| B090-TG-FINAL-v2-onizleme-480p.mp4 | hızlı izleme |
| ses-listesi.csv | 354 satır: her repliğin ve efektin zamanı, kim, metin, dosya |
| stems/diyalog.flac, sfx.flac, ortam.flac, muzik.flac | film boyu hizalı izler (0:00'a koy); kurgudaki seviyede |
| stems/TAM-MIKS.flac | nihai miks (kayıpsız) |
| olcum.json | ölçümler |

## Ne yapıldı
- **Diyalog: 89 replik, hepsi ElevenLabs TTS (eleven_v3), kilitli sesler.** 64 yeni replik üretildi (S3-3…S8-1 Hazel/Barnaby, S8-1 Anne/Baba, D1/E1, S8-4 Barnaby v2.2); 0–40 sn'nin 8 repliği ve S8-2…S9-2b'nin 15 repliği önceki onaylı TTS'ler. Ağız pencereleri Seedance'ın kendi konuşma zamanlarından (kelime zamanlı STT) alındı; her replik pencere başına oturtuldu, gerekirse en fazla ×1,22 (kısa ünlemlerde ×1,3) hız. 14 replik daha hızlı okunmuş ikinci take ile değiştirildi. Dört replik pencereyi 0,26–0,33 sn aşıyor (S3-5 "Promise", S4-4 "Run!", S5-3 "Then we stop and think", S6-5 "Not pie. Mama."): ağız kapanırken ses biter, anlaşılırlık için kabul edildi.
- **STT doğrulama (tüm diyalog izi):** 87 repliğin tamamı birebir okundu; yalnız üç kısa ünlemde STT farklı yazdı ("They're"→"Get", "Oh"→"Ho", "Run!"→"Rat"), kulakla anlaşılır.
- **Efekt geçişi v2.1:** film 24 kare/sn ile kare kare incelendi (252 kontak sayfası, 11 paralel inceleyici + 4 kare/sn ön tarama); 413 hareket olayı bulundu, tekilleştirme sonrası 219 yeni efekt yerleşimi eklendi (v2.2 düzeltmeleri sonrası toplam 260). Yeni çizgi film aksanları: yaprak üstünde kayarak durma (13,25 kazların önünde; 62,9 akçaağacın önünde; 109,0 ve 115,7 S5 duruşları), zıplama "sproing" ve inişler, yaprak yığınına dalış (22,4), yaprak uçuşmaları, dörtnala koşu döngüleri (10,0; 32,0; 104,0; 113,25; 184,0), kafa dönüşü whoosh'ları, göz açılma "ping"leri, tek tek toynak adımları (79), yün/kumaş hışırtıları, koklamalar, boynuz-dal sürtünmeleri.
- **v2.2 yönetmen düzeltmeleri:** (1) Fren/lastik kayması sesi filmin tonuna uymadığı için her yerden çıkarıldı; ani duruşlar için yeni, tonal olmayan "toynakların kuru yaprak üstünde kayması" efekti üretildi ve 13,25 / 62,9 / 109,0 / 115,7'ye kondu (3:06'daki duruşa efekt konmadı, adımlar yeter). Frenle gelen otomatik "doink"ler de gitti (1:03,3 / 1:49,4 / 1:56,1 / 3:07,2). (2) Gereksiz "çın" aksanları çıkarıldı: 1:03,0; 1:15,0; 1:15,4; 1:18,0; 3:09,6; 3:39,5. (3) 3:10'daki yakın kaz kornası çıkarıldı; 3:11,5'teki kaz sürüsü geçişi korundu. (4) S8-4'te eksik iki replik eklendi: Anne "Is that maple?" 3:41,50–3:42,45 (mevcut Anne TTS'inden kesit, ×1,15; kesmeden önce biter) ve Barnaby "Um… I followed Papa's pie." — "Um" 3:42,93–3:43,38 (kapalı ağızla mırıltı), "I followed Papa's pie" 3:43,44–3:44,75 (ağız 3:43,13–3:44,65); yeni Barnaby TTS STT ile birebir doğrulandı ("Um, I followed Papa's pie"). "It was a tree." 3:47,68'de aynı.
- **Önceki efektler (54 yerleşim):** açılış çanı 0,30; kazlar 17,0 ve 90,2 ve 191,5; iniş/adım 23,3 / 36,1; Papa'nın uzak adımı 30,15; koklamalar 40,55 / 50,7 / 67,9; koku şeridi 41,05 / 177,6 (kopuşu 186,3); şurup damlası 65,15; ağaca yapışma "thwup" 75,26, boğuk "mmf", kurtulma "pop" 77,16; rüzgâr 80,4 ("the wind turned"); ikinci çan "DONG DONG" 85,9; koşu adımları 104,2 ve 183,55; yün hışırtısı 110,3 / 173,95; yaprak düşüşü 120,0; S6-4 yumuşak çan 165,95 / 169,3; Baba'nın adımları 200,1; ding-dong 203,1; S8-2→S9-2b'deki önceki onaylı efektler (adımlar, koklama, burun burna, yapışkan tık, çan, fındık, tabure, tepikler) korundu.
- **Ortam:** gündüz orman döngüsü (0–2:17, gün batımında kısılır) → gece orman döngüsü (2:06'dan sona, 12 sn çapraz). Beyaz gürültü karakteri yok; sessiz pencerelerde 4–12 kHz enerjisi eski mikse göre ~35 dB düşük.
- **Müzik:** yeni açılış parçası M0 (0:00–2:14, 8 sn kuyruk), M1 (2:17–3:18) ve M2 (3:17–son) aynı; diyalog altında −8 dB ducking, sonda +4 dB kalkış.
- **Miks:** diyalog −15,5 LUFS'a sabitlendi; bus kompresör (−30 dB, 1,35), tepe sınırlayıcı (gecikme telafili). Ölçüm (v2.2): bütün −17,0 LUFS, TP −3,2 dBTP, LRA 3,9, kesimlerde sıçrama yok (en büyük < +6 dB), 1,5 sn'den uzun sessizlik yok. Not: bütün değeri −16'nın altında; diyalog seviyesi doğru, müzik/ortam bilinçli olarak diyaloğun altında tutuldu. İstenirse müzik +2 dB ile −16'ya çekilir.

## Kredi
v2 için harcanan: ~8.420 kredi (TTS 63+14 retake, 22 efekt, 1 müzik, 3 STT); v2.1 efekt turu 55; v2.2 düzeltmeleri 78 (1 TTS 56, 1 efekt 4,7, 1 STT 17,2). Proje toplamı: ~20.342 kredi (tavan 25.000). Kayıt: ses-log.csv.

## Bilinen sınırlar
- Görüntüdeki ağız hareketleri Seedance'ın orijinal konuşmasına göre; yeni TTS aynı pencereye oturtuldu, kare kare "dudak şekli" eşleşmesi yok (hiçbir dublajda olmaz).
- S1–S2 (0–26 sn) görsel içerik belgesi olmadığından efektler yalnız senaryoda geçen olaylara (çan, kazlar, iniş) kondu.
