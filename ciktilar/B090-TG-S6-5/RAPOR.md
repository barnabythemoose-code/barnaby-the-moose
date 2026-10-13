# RAPOR — B090-TG-S6-5 (Klip 1/7)

## Üretim
- request_id: 42ac4d07-bbd6-4ac1-9eef-8d8cf970a29e
- Model: seedance-2.5, 720p, adaptive (çıktı 1286×716, ilk kareyle aynı), 12 sn istendi → 12,06 sn geldi, 24 fps, ses AAC stereo (generate_audio true)
- İstek: first_frame_url ile, reference_images YOK, seed 20261010, prompt birebir
- Üretim süresi: 192 sn
- Bakiye önce / sonra: 33,0573 → 30,2072 → **maliyet $2,85**
- Dosyalar: `B090-TG-S6-5_d01.mp4`, `B090-TG-S6-5_lastframe.jpg` (API son karesi), `kareler/` (0–12 sn + son kare + `sheet.png` kontak), `payload.json`, `result.json`, `meta.json`

## Kimlik kartı (kanon: Image1 Barnaby baş, Image2 Hazel)
Barnaby
1. Boynuz koyu çikolata-kahve, kürkten koyu — **SINIRDA/KALDI**: boynuzlar açık tarçın-bej, yüz kürküyle aynı ton, koyu değil (0–12 sn, en net 8 ve 11 sn). Bu ton zaten ilk karede (S6-4 son karesi) vardı; model ilk kareyi korudu.
2. Boynuz kalın hilal, ~3 yuvarlak çatal — GEÇTİ (3 sn, 8 sn)
3. Açıklık ~1,7–1,8× baş, simetrik, kadrajda tam — GEÇTİ (tüm süre, üstte bol boşluk)
4. Burun dev, antrasit-siyah, mat, ~%45–50 — GEÇTİ (2, 6, 8, 11 sn: büyük ve koyu antrasit; ilk karede hafif kahve, 1 sn'den sonra koyulaşıyor)
5. Muzzle kısa kalın karamel, bant yok — GEÇTİ
6. Gözler beyaz sklera, kehribar iris — GEÇTİ (7–11 sn açıkken net)
7. Kürk karamel, karın krem — GEÇTİ (11 sn karın krem)
8. Kazak parlak kırmızı, balıkçı yaka, desen yok — GEÇTİ (hafif soluk/tuğla kırmızı; ilk kareden geliyor). Göğüste yapışık akçaağaç yaprağı var, desen değil (bkz. süreklilik).
9. Tombul armut gövde, iki ayak üstü dik — GEÇTİ (1,9 sn'den sonra hep dik; 0,5–1,5 sn arası kalkış çömelmesi)
10. Eller antrasit, iki parmaklı toynak — GEÇTİ (8–9 sn işaret toynağı net)

Hazel
11. Çok büyük baş — GEÇTİ
12. Diz-uyluk boyu — GEÇTİ (omuzda, Barnaby başı kadar)
13. Büyük parlak siyah göz, kirpik yok — GEÇTİ (11 sn)
14. Şişkin krem yanak — GEÇTİ
15. Açık ağızda 2 ön diş — GÖRÜNMÜYOR (11 sn ağız açık ama 720p'de diş seçilemiyor; KALDI demiyorum)
16. Altın turuncu kürk, krem göğüs — **SINIRDA**: kürk kanona göre daha kahve-tarçın, turuncu değil (ilk kareden geliyor)
17. Tek koyu alın çizgisi — GEÇTİ (11 sn'de seçiliyor, küçük ölçek)
18. Kabarık S kuyruk — GEÇTİ
19. Açık mint atkı, önde düğüm — GEÇTİ
20. Küçük kahve-pembe burun, yuvarlak kulak — GEÇTİ

**Kimlik sonucu: KALDI (madde 1 sınırda-kaldı; madde 16 sınırda).** Her ikisi ilk kareden miras; S6-4 ile uyumlu, kanon Image1/2 ile değil.

## Süreklilik (Kontrol notu)
- Kadraj kilitli, kamera hiç oynamıyor — GEÇTİ.
- 0 sn karesi ilk kareyle birebir — GEÇTİ.
- 0–1,9 sn kalkış — GEÇTİ (1,1 sn'de ayakta değil, ~1,6 sn'de dik; 1 sn'de çömelmiş geçiş pozu, biraz dört ayak hissi var).
- Ay: 0 sn'de yok, 1 sn'de bulut perdesi, 2 sn'de açılmış — GEÇTİ.
- **Yaprak sürekliliği KALDI:** yaprak sağ kol yenine geçmiyor. ~0,5 sn'de göğsün sol tarafına (resim-sol, Hazel'in altına) ayrı bir yaprak beliriyor ve klip boyunca orada kalıyor; duvardaki sap damlası yaprağıyla birlikte duvarda duruyor (son karede hâlâ orada). 2 sn'de sağ kol üstünde de ikinci küçük yaprak var. S8/S9 promptları "near arm sleeve"de yaprak bekliyor → kurguda yaprak yeri uyuşmayacak.
- Koku şeridi: sağdan ~4,3 sn'de giriyor (prompt 4,9), 5–11 sn arası burnuna bağlı — GEÇTİ.
- Göz açma ~6,5 sn, işaret 8–9 sn, yürüyüş 10,5 sn'den itibaren sağa — GEÇTİ.
- Çıkış: 11,8 sn'de tamamen çıkmış olması gerekiyordu; 12,06 sn'de arka/kuyruk ve Hazel'in kuyruğu hâlâ sağ kenarda.
- Hazel konumu hep resim-sol omuz — GEÇTİ.

## Hikâye eylemi
Yerinde: kalkış → burun silme → gözler kapalı buruna konuşma (2–4 sn) → sessizlik + şerit (4,3–6,5) → gözler açılır, "Warm wool" işaret (6,5–9) → "Not pie?"/"Not pie. Mama." (9–10,5) → "Go." (Hazel ağzı açık 11 sn) → sağa çıkış.
Ses: AAC var (ort. −29,9 dB, tepe −10,3 dB), replikler model tarafından üretilmiş; içerik kulakla doğrulanamadı (bulutta dinleme yok). ElevenLabs dublaj planı aynen geçerli.

## Kullanılabilir aralık
**0,0 – 12,06 sn (tamamı)** eylem olarak kullanılabilir. Yaprak-göğüs sorunu tüm süreyi kapsıyor; kurguda kabul ya da 0,0–0,5 sn kesimi + S8'de "göğüste yaprak" kabulü gerekir. Çıkış için 11,5 sn'den sonrası kesilebilir (kuyruk sarkıyor).

## Tuhaflıklar / blooper adayı
- Barnaby'de kabarık KUYRUK görünüyor (11–12 sn, sağ kenardan çıkarken; S8 promptlarında yasak).
- 10 sn: ağız abartılı kocaman açık ("Not pie. Mama." için fazla geniş) — blooper adayı.
- 1 sn: kalkış pozu dört ayak/çömelme arası, biraz tuhaf.
- Boynuzlar kanondan açık renkte.
