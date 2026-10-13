# B090 Thanksgiving — Final kurgu raporu (B090-final-kurgu)

## Mobil özet (8 satır)
1. Film 251,4 sn (4:11), 1280x720 24p; B (efektli) ana sürüm, A (efektsiz) yedek. Ses −15 LUFS, TP ≤ −1, LRA ≈ 7.
2. S1–S4 bloğu dokunulmadı (ses 0 dB, görüntü CRF 17 tek re-encode). 6 siyah kare kaldırıldı, S4-4 → S5-1a sert kesme.
3. 23 Seedance repliği VC ile kilitli sese çevrildi; 3'ü (S7-1 Hazel ×2, S6-5 Barnaby) ters STT'yi geçemeyince kilitli sesle TTS'e alındı.
4. Sessiz 6 klip TTS ile dublajlandı; Barnaby/Hazel'in 4 repliği benzerlik ölçümüne göre TTS→VC ile düzeltildi. 'They kept the bell' VC sonrası 'I kept' çıktı, düz TTS kaldı.
5. Tüm replikler tek tek ve miks içinde STT ile doğrulandı (41 satır). Mikste tek sapma: S6-4 Hazel 'last bell' → 'west bell' (tek başına birebir); 'Mama's shawl' mikste doğru çıktı.
6. S7-2 üretilmediği için 'You were right / I always am' çıkarıldı (S7-1-B kuyruğunda ikisinin de ağzı kadrajda ve kapalı; S8-1 açılışı Anne/Baba).
7. Donuk kare taraması: S5-3a, D1 ve E2 kuyrukları kısaltıldı; bloktaki 2 donuk an ve D2 içindeki 0,4 sn (replik üstünde) olduğu gibi kaldı.
8. ElevenLabs toplam ≈ 7.631 kredi; en pahalı kalem tam miks STT (1.383) ve 6 TTS→VC düğümünün varsayılan 4 varyantla koşması (720). Seedance/Segmind çağrısı yapılmadı.

## 1. Önce sorunlar ve riskler
- **Tam sessizlik yok, ama S8-2/S8-3 fısıltıları** (Hazel 'They kept the bell for you.', Barnaby 'They waited...') −20 LUFS'ta; telefonda hoparlörde zayıf duyulabilir. İsterseniz −18'e çekilir (tek sayı, yeniden render 2 dk).
- **Dudak eşlemesi yaklaşık.** Sessiz kliplerde replikler ağzın açıldığı pencerelere kare bakılarak yerleştirildi (4 kare/sn kontak sayfaları: `is/agiz/`). S8-2 Anne ve S9-2b dudak hareketi zaten zayıf (Bulut raporu); burada fısıltı/kısa replik kullanıldı. S6-2-D2 Hazel repliği üstünde 0,4 sn donuk kare var (Seedance).
- **Kimliği zayıf klipler** (S8-2, S8-3, S8-4, S9-1, S9-2a) Owner kararıyla kullanıldı; kesim yapılmadı, yalnız S8-1'de Anne'ye punch-in ile Baba'daki renk kaymasının temiz aralığı kullanıldı. Yaprak sürekliliği (S6-5 göğüs / S8-S9 kol) düzeltilmedi, kabul.
- **Ortam hatası yakalandı ve düzeltildi:** ilk miksin tam STT'si S6-5'te replikleri çift gösterdi; Seedance ortam dosyalarında orijinal konuşma pencereleri oda tonuyla değiştirilmemişti (7 klip). `bin/ortam.py` ile yeniden üretildi (pencere ±0,1 sn, en sessiz 0,6 sn oda tonu döngüsü, 15 ms çapraz), S6–S8-1 bölgesi yeniden STT ile doğrulandı: tüm replikler tek ve birebir. Tam STT 1.383 kredi tuttuğu için ikinci kontrol yalnız 69 sn'lik bölgeye (380 kredi) yapıldı; S8-2–S9 bölümünde ortam yok, ilk STT geçerli.
- **S6-4 Hazel 'That's not the last bell.'** tek başına STT'de birebir, mikste 'west bell' duyuldu (çan SFX ile üst üste). Çan −16 dB'de; isterseniz −19'a çekilir.
- **Parlaklık sıçraması > 15/255 olan 3 kesim** (S5-1a→S5-1b +23,6; S7-1-B→S8-1 −27; S8-3→S8-4 −20) gelen klibin ilk 0,5 sn'sinde ±0,06 parlaklık rampasıyla yumuşatıldı (sendcmd+eq). Mekân değiştiği için tamamen giderilmez; sert kesme kasıtlı.
- **Flaş güvenliği:** ΔY≥12 olayı saniyede >3 olan iki saniye var: 11. sn (S1–S4 bloğu, dokunulmadı) ve S8-4 içinde 8,0–9,0 sn (Baba'ya kesme + kamera hareketi; kırmızı parlama yok, strob değil). Raporlandı, müdahale edilmedi.
- **Kredi defteri:** 11labs connector işlem başına bakiye döndürmüyor; `ses-log.csv`'de her çağrının `price.credits` değeri var, bakiye öncesi/sonrası yok. 14 TTS ters STT'sinde fiyat alanı boş döndü (0 yazıldı).
- **STT'de köşeli etiketler:** TTS çıktılarının ters STT'si eleven_v3 stil etiketlerini ('[warmly]' gibi) 0 süreli kelime olarak yazdı; seste etiket okunmuyor (kelime zamanları bunu doğruluyor).
- **E2 kuyruğu** 100 kareye (4,17 sn) kısaltıldı; 'It's Barnaby!' 3,22'de bitiyor, 0,45 sn dinleme tutuşu kalıyor; cevap çanı S6-4 açılışında EL SFX olarak geliyor.

## 2. EDL (24 kare/sn; kare numaraları kaynak klibe göre)
| # | Parça | Kaynak | Giriş–Çıkış (kare) | Zaman çizelgesi t0 | Süre | Geçiş | Ses kaynağı |
|---|---|---|---|---|---|---|---|
| 1 | S1-S4 blok | TG-ARA-KURGU-S1-S4-mobil-v2.mp4 | 0–2497 | 0,00 | 104,04 sn | kes | blok miks (0 dB) |
| 2 | S5-1a | TG-S5-1a_d01.mp4 | 24–142 | 104,04 | 4,92 sn | kes | 03 B-efektli r3 / A-efektsiz |
| 3 | S5-1b | TG-S5-1b_d01.mp4 | 9–97 | 108,96 | 3,67 sn | kes | 03 B r2 / A |
| 4 | S5-2a | TG-S5-2a_d01.mp4 | 0–96 | 112,62 | 4,00 sn | kes | 03 B/A |
| 5 | S5-2b | TG-S5-2b_d02.mp4 | 0–96 | 116,62 | 4,00 sn | kes | 03 B/A |
| 6 | S5-2c | TG-S5-2c_d01.mp4 | 0–96 | 120,62 | 4,00 sn | kes | 03 B/A |
| 7 | S5-3a | TG-S5-3a_d01.mp4 | 0–87 | 124,62 | 3,62 sn | kes | 03 B/A (+2,5 dB) |
| 8 | S5-3b | TG-S5-3b_d01.mp4 | 0–264 | 128,25 | 11,00 sn | kes | 03 B/A (ilk 2,5 sn −5→0 dB) |
| 9 | S6-1 | TG-S6-1_d01.mp4 | 0–139 | 138,75 | 5,79 sn | ['xfade', 12] | ortam + VC |
| 10 | S6-2-D1 | B090-TG-S6-2-D1_d01.mp4 | 0–126 | 144,54 | 5,25 sn | kes | 03 D1-B v3 / A |
| 11 | S6-2-D2 | B090-TG-S6-2-D2_d01.mp4 | 0–145 | 149,79 | 6,04 sn | kes | ortam + VC |
| 12 | S6-3-E1 | B090-TG-S6-3-E1_d01.mp4 | 0–142 | 155,83 | 5,92 sn | kes | 03 E1-B v2 / A |
| 13 | S6-3-E2 | B090-TG-S6-3-E2_d01.mp4 | 0–100 | 161,75 | 4,17 sn | kes | ortam + VC |
| 14 | S6-4 | B090-TG-S6-4_d01.mp4 | 0–188 | 165,92 | 7,83 sn | kes | ortam + VC + ham Hmm + EL çan |
| 15 | S6-5 | B090-TG-S6-5_d01.mp4 | 0–289 | 173,75 | 12,04 sn | kes | ortam + VC + TTS(B2) |
| 16 | S7-1-B | B090-TG-S7-1-B_d01.mp4 | 0–289 | 185,79 | 12,04 sn | kes | ortam + VC + TTS(H2,H3) + kaz SFX |
| 17 | S8-1-B2 genis | B090-TG-S8-1-B2_d01.mp4 | 17–70 | 197,83 | 2,21 sn | kes | ortam + VC (Anne/Baba) |
| 18 | S8-1-B2 Anne punch-in | B090-TG-S8-1-B2_d01.mp4 | 70–193 | 200,04 | 5,12 sn | punch | ortam + VC |
| 19 | S8-2 | B090-TG-S8-2_d01.mp4 | 0–145 | 205,17 | 6,04 sn | kes | rüzgâr + TTS + SFX |
| 20 | S8-3 | B090-TG-S8-3_d01.mp4 | 0–193 | 211,21 | 8,04 sn | kes | rüzgâr + TTS/TTS→VC + SFX |
| 21 | S8-4 | B090-TG-S8-4_d01.mp4 | 0–265 | 219,25 | 11,04 sn | kes | rüzgâr + TTS/TTS→VC + SFX |
| 22 | S9-1 | B090-TG-S9-1_d01.mp4 | 0–193 | 230,29 | 8,04 sn | kes | rüzgâr + TTS + çan + SFX |
| 23 | S9-2a | B090-TG-S9-2a_d01.mp4 | 0–97 | 238,33 | 4,04 sn | kes | rüzgâr + TTS + fındık |
| 24 | S9-2b | B090-TG-S9-2b_d01.mp4 | 0–145 | 242,38 | 6,04 sn | kes | rüzgâr + TTS→VC + tabure |
| 25 | Son kart | KART | 0–84 | 247,92 | 3,50 sn | ['xfade', 12] | müzik kuyruğu |

Son kart: koyu lacivert (0x0a1428) üstüne logo 420 px, 0,3–1,2 sn alfa girişi, 3,5 sn; S9-2b'den 12 kare çapraz. S6-1 girişi 12 kare çapraz (aynı mekân/zaman atlaması), diğer tüm geçişler sert kesme.

## 3. Plan seçimleri
- **S5 geçişi:** Bloğun sonundaki 6 siyah kare kaldırıldı; S4-4 son karesinden S5-1a'nın 24. karesine sert kesme (S5-1a-B miksi zaten bu kesimle hazırlanmış). Siyah perde yerine akış tercih edildi; blok sesi kuyruğu 0,05 sn fade.
- **S6-2:** D1 (geniş, 03'te sesi hazır) + D2 (yakın, Seedance sesi VC'li). S6-2-B kimlik sorunu (boynuz/ölçek) nedeniyle kullanılmadı; 'şartlı yakın plan aralığı' D2 ile karşılandığı için B'ye gerek kalmadı. Her replik bir kez duyuluyor ('It found a tree.' D2'de, 'itiraf' D1'de).
- **S6-3:** E1 (hazır ses) + E2 (seslenme 'Mama... It's Barnaby!'). B ve C varyantları aynı eylemi tekrarladığı için dışarıda. E2 100 kareye kısaltıldı (donuk kuyruk).
- **S6-4 → S6-5:** S6-4 188 karede (7,83 sn) kesildi, S6-5 0. kareden sert; poz ve ışık sürekliliği H-23 sayfasında 14. çift.
- **S7-2 (üretilmedi):** 'You were right.' / 'I always am.' çıkarıldı. S7-1-B'nin son 1,5 sn'sinde Barnaby ve Hazel kadrajda, ağızlar kapalı (V.O. kuralına takılıyor); S8-1 açılışı Anne/Baba geniş planı, Hazel kadraj dışı ama sahne atlıyor. Kaz kornaları (6,2/6,7/7,1) 'Then don't smell. Look. The geese.' motivasyonunu taşıyor.
- **S8-1-B2:** 17. kareden giriş (1,0 sn kuralına yakın, temiz), 70. karede Anne'ye %18 punch-in (zoompan, 6 karede), 193. kareye kadar; Baba'nın renk kayması kadraj dışına atıldı. Anne/Baba replikleri VC (kendi ID'leri).
- **S8-4:** Kesme 3,25 sn'de (78. kare); Anne'nin 'Look how big you are! Is that maple?' repliği iç duraklar 0,22 sn'ye kısaltılıp %5 hızlandırıldı, 0,45–3,7 arasına oturdu; Barnaby 3,45'ten, Anne 6,8'den, Baba 9,45'ten (kesme 8,25).
- **S9-1:** Çan 2,8 sn'de EL SFX; Anne 0,3, Baba 'Hm.' 2,45. S9-2a: yalnız Anne 'Thank you, Hazel.' 2,0'da, fındık tik 0,9'da. S9-2b: 'So... ten?' 1,4 / 'Ten out of ten.' 3,5, tabure 5,45 (geniş plana kesme).

## 4. Ses tasarımı
- **Stemler:** `diyalog` (VC+TTS+ham Hmm), `muzik` (M1 S6–S7 64 sn, M2 S8–S9+kart 58 sn; ElevenLabs Music instrumental), `sfx` (yalnız B'de), `ortam` (Seedance konuşmasız ortamları + rüzgâr yatağı), ayrıca `hazir-miks-S5-D1-E1-B/A` (03'teki hazır miksler, +1,5 dB) ve `S1-S4-blok`. A = B − sfx, hazır A miksleriyle.
- **Müzik:** M1 S5-3b bitiminden 1,5 sn önce (137,25) girer, S7-1-B sonunda 1,2 sn söner; M2 S8-1'den 1,0 sn önce (196,8) girer, son replikten sonra +5 dB yükselir, kartta 2,5 sn'de çözülür. Diyalog altında otomatik ducking: M1 −9 dB, M2 −8 dB (0,3 sn rampa), D1/E1 hazır miksleri altında ek −5 dB. Sonuç: müzik diyalog altında ≈ −35 LUFS, diyalog ≈ −17 → 18 dB fark.
- **Seviye hedefleri:** replikler −17 LUFS (fısıltılar −20, 'Not pie?'/'Go.' −18,5, Anne S8-4 −18,5), Seedance ortamları 0 dB (≈ −26), rüzgâr −27, çanlar −8…−16, foley −12…−18. Miks: hafif bus kompresörü (−26 dB, 1,8:1) → −15 LUFS → limiter −1,7 dB.
- **Duygu sesleri:** S6-4 kapalı ağız 'Hmm' (1,78–2,10, ham Seedance, −4 dB) korundu; başka efor sesi eklenmedi (fısıltı planları zaten sessiz).

## 5. Ölçüm tablosu
| Ölçüm | Hedef | B (efektli) | A (efektsiz) |
|---|---|---|---|
| Integrated loudness | −16…−14 LUFS | -15,00 | -15,10 |
| True peak | ≤ −1 dBTP | -0,80 | -0,90 |
| LRA | ≤ 8 LU | 6,80 | 7,00 |
| Tam sessizlik > 1,5 sn | yok | 0 | 0 |
| Kesimde M−3s sıçraması > +6 dB | yok | 0 | 0 |
| Donuk kare (freezedetect −60 dB, 0,4 sn) | elle bak | 8,4–9,1 ve 36,6–38,4 (blok, dokunulmadı); 155,4–155,8 (D2, Hazel repliği üstünde, kaynak); 164,9–165,3 (E2 dinleme tutuşu); 249,1→son (kart) | aynı |
| Flaş (ΔY≥12, sn başına >3) | yok | 11. sn (blok) ve 229–230 (S8-4 Baba kesmesi) — ikisi de strob değil | aynı |
| Kesimde ortalama Y sıçraması > 15 | yumuşat | 3 kesim, 0,5 sn pozlama rampası uygulandı | aynı |

**Kesim parlaklık farkları (son kare → ilk kare, Y/255):** S1-S4 blok→S5-1a +0,7; S5-1a→S5-1b +23,6; S5-1b→S5-2a -0,9; S5-2a→S5-2b -2,3; S5-2b→S5-2c -2,3; S5-2c→S5-3a -2,2; S5-3a→S5-3b +6,2; S5-3b→S6-1 -0,3; S6-1→S6-2-D1 +0,3; S6-2-D1→S6-2-D2 +0,4; S6-2-D2→S6-3-E1 -1,7; S6-3-E1→S6-3-E2 -1,9; S6-3-E2→S6-4 +0,5; S6-4→S6-5 -2,2; S6-5→S7-1-B +0,8; S7-1-B→S8-1-B2 genis -27,0; S8-1-B2 genis→S8-1-B2 Anne punch-in +1,1; S8-1-B2 Anne punch-in→S8-2 +0,3; S8-2→S8-3 -3,4; S8-3→S8-4 -19,9; S8-4→S9-1 +0,4; S9-1→S9-2a +1,3; S9-2a→S9-2b +6,2; S9-2b→Son kart -3,3

**Parça bazlı RMS (B, dBFS):** S1-S4 blok -18,2; S5-1a -18,2; S5-1b -24,9; S5-2a -24,1; S5-2b -23,7; S5-2c -22,8; S5-3a -26,7; S5-3b -19,7; S6-1 -19,4; S6-2-D1 -18,9; S6-2-D2 -19,5; S6-3-E1 -18,4; S6-3-E2 -20,6; S6-4 -18,7; S6-5 -18,7; S7-1-B -18,4; S8-1-B2 genis -17,3; S8-1-B2 Anne punch-in -20,3; S8-2 -20,2; S8-3 -22,0; S8-4 -17,8; S9-1 -19,1; S9-2a -19,9; S9-2b -20,3; Son kart -30,1

## 6. STT ters test (replik bazlı)
| Replik | Kaynak | Beklenen | STT sonucu | Durum |
|---|---|---|---|---|
| S6-1_H1 | VC | We stop here until morning. | We stop here until morning | ✓ |
| S6-1_B1 | VC | But Mama's table... | But Mama's table | ✓ |
| S6-1_H2 | VC | Morning, Barnaby. | Morning, Barnaby | ✓ |
| S6-2-D2_B1 | VC | It found a tree. | It found a tree | ✓ |
| S6-2-D2_H1 | VC | Barnaby. You are very hard to not know. | (ilk tur, 17'lik STT) birebir | ✓ |
| S6-3-E2_B1 | VC | Mama... It's Barnaby! | Mama, it's Barnaby | ✓ |
| S6-4_H1 | VC | That's not the last bell. | (ilk tur) birebir | ✓ |
| S6-4_B1 | VC | A soft bell... like a lamp left on. | (ilk tur) birebir | ✓ |
| S6-4_H2 | VC | Somebody's still waiting. | (ilk tur) birebir | ✓ |
| S6-4_B2 | VC | For... me? | (ilk tur) birebir | ✓ |
| S6-5_B1 | VC | Nose, I know you love pie. But today, please... find Mama. | (ilk tur) birebir | ✓ |
| S6-5_B2 | TTS v2 (VC ve retake elendi) | Warm wool. Mama's shawl! This way! | Warm wool. Mama shawl. This way | ≈ ('s yok; VC'de de aynı) |
| S6-5_H1 | VC | Not pie? | (ilk tur) birebir | ✓ |
| S6-5_B3 | VC | Not pie. Mama. | (ilk tur) birebir | ✓ |
| S6-5_H2 | VC | Go. | 0,42 sn; tek başına boş döndü, tam miks STT'ye bak | ? |
| S7-1_B1 | VC | The fog ate Mama's smell. I can't smell anything! | (ilk tur) birebir | ✓ |
| S7-1_H1 | VC | Then don't smell. Look. The geese. | (ilk tur) birebir | ✓ |
| S7-1_H2 | TTS v2 (VC 2 kez 'lice') | They eat Mama's corn at the lights. They know the way. | They eat mama's corn at the lights. They know the way | ✓ |
| S7-1_B2 | VC | Dinner before me?! | Dinner before me? | ✓ |
| S7-1_H3 | TTS v1 (VC 'Geyser', TTS v2 'These') | Geese are punctual. | Geese are punctual | ✓ |
| S8-1_A1 | VC | Papa, the sun went down a long time ago. | (ilk tur) birebir | ✓ |
| S8-1_P1 | VC | The table isn't full yet. | The table isn't full yet | ✓ |
| S8-1_A2 | VC | No. It isn't. | (ilk tur) birebir | ✓ |
| S8-2_A68 | TTS | Who's there? | Who's there? | ✓ |
| S8-2_H69 | TTS (TTS→VC 'I kept' elendi) | They kept the bell for you. | They kept the bell for you. | ✓ |
| S8-2_B70 | TTS | They waited... | They waited... | ✓ |
| S8-3_A71 | TTS | ...Barnaby? | ...Barnaby? | ✓ |
| S8-3_B72 | TTS→VC | Mama. | Mama | ✓ |
| S8-4_A73 | TTS (duraklar kısaltıldı, ×1,05) | Look how big you are! Is that maple? | Look how big you are! Is that maple? | ✓ |
| S8-4_B74 | TTS→VC (×1,05) | I followed Papa's pie. It was a tree. | I followed Papa's pie. It was a tree | ✓ |
| S8-4_A75 | TTS (×1,05) | Papa's pie has a tree in it. | Papa's pie has a tree in it. | ✓ |
| S8-4_P76 | TTS | ...Hm. Maple. | ...Hm. Maple. | ✓ |
| S9-1_A77 | TTS | Now we can ring it, Papa. | Now we can ring it, Papa. | ✓ |
| S9-1_P78 | TTS | Hm. | Hm. | ✓ |
| S9-2a_A79 | TTS | Thank you, Hazel. | Thank you, Hazel. | ✓ |
| S9-2b_B81 | TTS→VC | So... ten? | So, 10? | ✓ (rakam) |
| S9-2b_H82 | TTS→VC | Ten out of ten. | 10 out of 10 | ✓ (rakam) |

'(ilk tur) birebir' = 17 VC çıktısının ilk ters testi (ses-log #28) bu oturumdan önce raporlanmıştı; metin birebir çıktı.

### Tam miks STT (final B, kelime zamanlı)
| Zaman çizelgesi | Replik | Beklenen | Tam miks STT | Durum |
|---|---|---|---|---|
| 138,8 | S6-1_H1 | We stop here until morning. | We stop here until morning | ✓ |
| 142,0 | S6-1_B1 | But Mama's table... | But Mama's table. | ✓ |
| 143,0 | S6-1_H2 | Morning, Barnaby. | Morning, Barnaby. | ✓ |
| 145,5 | S6-2-D1 (hazır miks) | My antlers grew. Mama won't know me. / Your nose found a pie three valleys away. | My antlers grew. Mama won't know me. Your nose found a pie three valleys away. | ✓ |
| 151,4 | S6-2-D2_B1 | It found a tree. | It found a tree. | ✓ |
| 153,4 | S6-2-D2_H1 | Barnaby. You are very hard to not know. | Barnaby, you are very hard to not know. | ✓ |
| 156,2 | S6-3-E1 (hazır miks) | Sound travels at night. Call. / Mama. Papa. | Sound travels at night. Call. Mama, Papa. | ✓ |
| 163,0 | S6-3-E2_B1 | Mama... It's Barnaby! | Mama, it's Barnaby. | ✓ |
| 166,2 | S6-4_H1 | That's not the last bell. | That's not the west bell. | ≈ (tek başına STT birebir; mikste 'last'→'west') |
| 167,8 | S6-4_Hmm | (kapalı ağız Hmm) | — (ilk tam STT'de 'Hmm.') | ✓ |
| 168,5 | S6-4_B1 | A soft bell... like a lamp left on. | A soft bell, like a lamp left on. | ✓ |
| 170,9 | S6-4_H2 | Somebody's still waiting. | Somebody's still waiting. | ✓ |
| 172,8 | S6-4_B2 | For... me? | For me? | ✓ |
| 175,3 | S6-5_B1 | Nose, I know you love pie. But today, please... find Mama. | Nose, I know you love pie, but today please find Mama. | ✓ |
| 180,0 | S6-5_B2 | Warm wool. Mama's shawl! This way! | Warm wool, Mama's shawl. This way. | ✓ |
| 182,6 | S6-5_H1 | Not pie? | Not pie. | ✓ |
| 183,5 | S6-5_B3 | Not pie. Mama. | Not pie, Mama. | ✓ |
| 184,9 | S6-5_H2 | Go. | Go. | ✓ |
| 188,0 | S7-1_B1 | The fog ate Mama's smell. I can't smell anything! | The fog ate Mama's smell. I can't smell anything. | ✓ |
| 190,4 | S7-1_H1 | Then don't smell. Look. The geese. | Then don't smell. Look, the geese. | ✓ |
| 192,7 | S7-1_H2 | They eat Mama's corn at the lights. They know the way. | They eat Mama's corn at the lights. They know the way. | ✓ |
| 195,6 | S7-1_B2 | Dinner before me?! | Dinner before me? | ✓ |
| 196,6 | S7-1_H3 | Geese are punctual. | Geese are punctual. | ✓ |
| 197,6 | S8-1_A1 | Papa, the sun went down a long time ago. | Papa, the sun went down a long time ago. | ✓ |
| 200,4 | S8-1_P1 | The table isn't full yet. | The table isn't full yet. | ✓ |
| 202,6 | S8-1_A2 | No. It isn't. | No, it isn't. | ✓ |
| 206,7 | S8-2_A68 | Who's there? | Who's there? | ✓ |
| 208,0 | S8-2_H69 | They kept the bell for you. | They kept the bell for you. | ✓ |
| 209,8 | S8-2_B70 | They waited... | They waited. | ✓ |
| 213,0 | S8-3_A71 | ...Barnaby? | Barnaby? | ✓ |
| 216,0 | S8-3_B72 | Mama. | Mama. | ✓ |
| 219,8 | S8-4_A73 | Look how big you are! Is that maple? | Look how big you are. Is that maple? | ✓ |
| 222,8 | S8-4_B74 | I followed Papa's pie. It was a tree. | I followed Papa's pie. It was a tree. | ✓ |
| 226,1 | S8-4_A75 | Papa's pie has a tree in it. | Papa's pie has a tree in it. | ✓ |
| 228,7 | S8-4_P76 | ...Hm. Maple. | Hmm, maple. | ✓ |
| 230,7 | S9-1_A77 | Now we can ring it, Papa. | Now we can ring it, Papa. | ✓ |
| 232,8 | S9-1_P78 | Hm. | Hmm. | ✓ |
| 240,4 | S9-2a_A79 | Thank you, Hazel. | Thank you, Hazel. | ✓ |
| 243,9 | S9-2b_B81 | So... ten? | So, 10? | ✓ (rakam) |
| 245,9 | S9-2b_H82 | Ten out of ten. | 10 out of 10. | ✓ (rakam) |

## 7. Ses benzerliği (MFCC-13 kosinüs mesafesi + simetrik KL; referans: `04/TG-S3-4r2+S3-5_A-ham-rotuslu.mp4` Barnaby 3 / Hazel 3 kesit)
Ölçek: diğer karakterin referansına uzaklık cos 0,354 / KL 0,533 (bu değerlerin altı 'aynı karakter' bölgesi; kısa ve fısıltılı kesitlerde ölçüm gürültülü),
| Dosya | Karakter | cos ↓ | KL ↓ | Spektral merkez (Hz) |
|---|---|---|---|---|
| S6-1_B1_vc,mp3 | barnaby | 1,058 | 0,497 | 1164 |
| S6-1_H1_vc,mp3 | hazel | 0,583 | 0,603 | 1235 |
| S6-1_H2_vc,mp3 | hazel | 0,364 | 0,680 | 1138 |
| S6-2-D2_B1_vc,mp3 | barnaby | 0,763 | 0,559 | 2060 |
| S6-2-D2_H1_vc,mp3 | hazel | 0,106 | 0,539 | 1862 |
| S6-3-E2_B1_vc,mp3 | barnaby | 0,322 | 0,282 | 1891 |
| S6-4_B1_vc,mp3 | barnaby | 0,403 | 0,400 | 2178 |
| S6-4_B2_vc,mp3 | barnaby | 1,321 | 1,081 | 1041 |
| S6-4_H1_vc,mp3 | hazel | 0,101 | 0,452 | 2422 |
| S6-4_H2_vc,mp3 | hazel | 0,445 | 0,609 | 1355 |
| S6-5_B1_vc,mp3 | barnaby | 0,611 | 0,355 | 2239 |
| S6-5_B2_tts,mp3 | barnaby | 0,072 | 0,278 | 1618 |
| S6-5_B3_vc,mp3 | barnaby | 0,575 | 0,646 | 1888 |
| S6-5_H1_vc,mp3 | hazel | 0,129 | 0,669 | 2058 |
| S6-5_H2_vc,mp3 | hazel | 0,229 | 0,653 | 906 |
| S7-1_B1_vc,mp3 | barnaby | 0,147 | 0,147 | 2022 |
| S7-1_B2_vc,mp3 | barnaby | 0,405 | 0,372 | 1896 |
| S7-1_H1_vc,mp3 | hazel | 0,043 | 0,169 | 2240 |
| S7-1_H2_tts,mp3 | hazel | 0,055 | 0,273 | 2003 |
| S7-1_H3_tts,mp3 | hazel | 0,056 | 0,386 | 1860 |
| S8-2_B70_tts,mp3 | barnaby | 0,383 | 0,774 | 4386 |
| S8-2_H69_tts,mp3 | hazel | 0,232 | 0,377 | 2480 |
| S8-3_B72_ttsvc,mp3 | barnaby | 0,623 | 0,706 | 1698 |
| S8-4_B74_ttsvc,mp3 | barnaby | 0,190 | 0,225 | 2503 |
| S9-2b_B81_ttsvc,mp3 | barnaby | 0,033 | 0,257 | 2402 |
| S9-2b_H82_ttsvc,mp3 | hazel | 0,062 | 0,699 | 2105 |

TTS→VC kararı: 'Mama.' (0,839→0,623), 'I followed...' (0,299→0,190), 'So... ten?' (0,185→0,033), 'Ten out of ten.' (0,171→0,062) VC ile yaklaştı ve STT'yi geçti; 'They waited...' (0,383→0,625) ve 'They kept the bell' (STT 'I kept') düz TTS'te kaldı. Yüksek cos çıkan VC satırları (S6-1_B1 1,06; S6-4_B2 1,32; S6-2-D2_B1 0,76) 1 sn'den kısa, ünlem/nefesli kesitler; dinlemede Barnaby tınısında.

## 8. Krediler
- Toplam ElevenLabs harcaması (ses-log.csv, `price.credits` toplamı): **≈ 7.631 kredi**. Üst sınırlar: 25.000 ve kalan bakiyenin %35'i — connector bakiye döndürmediği için %35 kontrolü yapılamadı; toplam 25.000'in çok altında.
- Kalemler: STT 7 klip 320; TTS 14 replik 1.563; SFX 233+86; VC 23 replik 612 (+3 retake 93); müzik 960+870; 6 TTS→VC × 4 varyant 720; 3 yeniden TTS × 2 varyant 280; ters STT'ler ≈ 350; tam miks STT 1.383.
- Yeni video üretimi yok; Seedance/Segmind çağrısı yok; ElevenLabs dışında ücretli servis yok; yeni ses (voice) oluşturulmadı.

## 9. Kullanılmayan iyi anlar
- S6-2-B (11 sn): kimlik dışı ama 4,0–6,5 arası ağaç kovuğuna bakış güzel; ileride yakın plan yerine kullanılabilir.
- S6-3-B / S6-3-C: 'seslen' tekrarları; C'nin 7–9 sn arası Hazel'in kulak hareketi en iyisi.
- S6-2-D1 son 12 kare, S5-3a son 10 kare, E2 3,2–6,0: donuk/statik olduğu için kesildi.
- S7-1-B 12,04 sn'nin tamamı kullanıldı; S8-1-B2 0–17 ve 193–194 kareleri (renk kayması / giriş) dışarıda.
- Yeniden TTS'in v1 varyantları (S7-1_H2 3,76 sn, S6-5_B2 3,76 sn) daha oyunculu ama pencereye sığmadı; `is/el/tts2/` içinde.
- TTS→VC'nin kullanılmayan varyantları (24 üretim) `is/el/vc_tts/`; 'theywaited' VC varyantları fısıltıyı kaybediyor.

## 10. Teslim içeriği
`teslim/B090-TG-FINAL-B-efektli.mp4` (ana), `teslim/B090-TG-FINAL-A-efektsiz.mp4`, `teslim/stems/` (48 kHz stereo 24-bit; zip içinde FLAC olarak sıkıştırıldı, `ffmpeg -i x.flac x.wav` ile birebir wav), `teslim/RAPOR.md`, `teslim/kontakt.jpg` (1 sn), `teslim/h23-sinir-sayfasi.jpg` (24 kesim, son/ilk kare + ΔY), `teslim/ses-log.csv`. Çalışma dosyaları (`is/out/cues.json`, `timeline.json`, `bin/*.py`) ayrıca `kurgu-is/` altında.