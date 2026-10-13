# RAPOR — TG-S8-2 (Klip 2/7)

## Üretim
- request_id: 7838fc33305d556295b4c39413c8ff1e
- Model: seedance-2.5, 720p, 16:9 (1280×720), 6 sn istendi → 6,04 sn geldi, 24 fps, ses yok (generate_audio false)
- 7 referans görsel, seed 20261010, prompt birebir
- Üretim süresi: 187 sn
- Bakiye önce / sonra: 30,2072 → 28,7760 → **maliyet $1,43**
- Dosyalar: `TG-S8-2_d01.mp4`, `TG-S8-2_lastframe.jpg`, `kareler/` (0–6 sn + son kare + `sheet.png`), `payload.json`, `result.json`, `meta.json`

## Kimlik kartı (kanon: Image1 Barnaby, Image2 Hazel)
Barnaby
1. Boynuz kürkten koyu çikolata — **SINIRDA/KALDI**: boynuz orta kahve, kürkle aynı ton (tüm süre)
2. Kalın hilal, ~3 kısa yuvarlak çatal — **KALDI**: çatallar 4–5 adet, uzun ve sivri-ince; gerçekçi geyik boynuzu (tüm süre)
3. Açıklık ~1,8×, simetrik, kadrajda tam — NOT (Owner kararı: kesik boynuz KALDI sayılmaz): boynuz uçları üst kenarda kesik, 0,0–6,04 sn boyunca (ilk kare dahil). Barnaby kadrajın ~%95'i; prompt %45–55 ve %25 boşluk istiyordu.
4. Burun dev, antrasit-siyah, mat — GEÇTİ (sınırda): büyük ve yüz genişliğinin ~%40'ı, ama koyu kahve-antrasit ve hafif parlak (highlight var)
5. Muzzle kısa kalın karamel — **KALDI**: muzzle uzun ve ince, gerçekçi geyik burnu; kanonun kısa tombul yüzü yok (tüm süre; en net 2–3 sn)
6. Gözler beyaz sklera, kehribar iris — GEÇTİ (3–6 sn net)
7. Kürk karamel, karın krem — GEÇTİ
8. Kazak parlak kırmızı, balıkçı yaka, desen yok — GEÇTİ (çok iyi; yaprak + amber şurup damlası resim-sol üst kolda)
9. Tombul armut gövde, dik — GEÇTİ (gövde kanona göre biraz ince-uzun)
10. Eller antrasit toynak — GEÇTİ (2–6 sn sağ el görünüyor; iki parmaklı)

Hazel
11. Çok büyük baş — GEÇTİ
12. Diz-uyluk boyu — GEÇTİ (omuzda, orantı iyi)
13. Büyük parlak siyah göz, kirpik yok — GEÇTİ (beyaz sklera yok)
14. Şişkin krem yanak — GEÇTİ
15. Açık ağızda 2 ön diş — GEÇTİ (3 sn ağız hafif açık, dişler seçiliyor)
16. Altın turuncu kürk, krem göğüs — GEÇTİ (çok iyi)
17. Tek koyu alın çizgisi — GEÇTİ (net)
18. Kabarık S kuyruk — GEÇTİ
19. Açık mint atkı, önde düğüm — GEÇTİ
20. Küçük kahve-pembe burun, yuvarlak kulak — GEÇTİ

Anne (Image4): antlersız, koyu kahve, krem karın, hardal şal — GEÇTİ; şal saçaksız ama panço gibi; burun dev antrasit — GEÇTİ.
Baba (Image3): yeşil düz kazak, altın yuvarlak gözlük, gri sakal, yarı kapalı göz, kalın koyu boynuz — GEÇTİ; toynak çan ipinde — GEÇTİ. Baba boynuzu ~2× baş, 4 çatal — GEÇTİ.
Çan direği (Image5): pirinç çan, braket, örgü ip — GEÇTİ.

**Kimlik sonucu: KALDI** (madde 2 ve 5 kaldı; 1 sınırda; madde 3 kesik boynuz Owner kararıyla sadece not). Barnaby kanon chibi tasarımdan "gerçekçi genç geyik"e kaymış ve kadrajı taşıyor. Hazel, Anne, Baba çok iyi.

## Süreklilik
- Barnaby resim-sol, Hazel resim-sol omuzda — GEÇTİ.
- Anne 0 sn'de sırtı dönük, çayıra bakıyor; ~1,5–2,5 sn'de Barnaby'ye dönüyor, 3 sn'de yüzü ona dönük, hafif öne eğik — GEÇTİ. Dönüş sırasında (2 sn) gözleri kapalı.
- Anne "Who's there?" dudak hareketi: 2–3 sn arasında ağız kapalı gülümseme, belirgin konuşma yok — ZAYIF (ElevenLabs dublajı için dudak eşleşmesi yok).
- Baba sağda çan direğinde, toynak ipte, gözü Barnaby'de (prompt: 5 sn'ye kadar çayıra bakmalı) — küçük sapma.
- Barnaby 0–1,5 sn iki küçük adım: belirgin adım yok, sadece hafif gövde dönüşü — ZAYIF.
- Hazel 3 sn'de yanağa yaslanıyor — GEÇTİ (3–4 sn). Hazel'in elinde FINDIK YOK (elleri boş, Barnaby'nin boynuna tutunuyor) — KALDI.
- Barnaby ~4,5–5 sn ağzı açık fısıltı ("They waited...") — GEÇTİ (5 sn net dudak hareketi), 5–6 sn küçük gülümseme, kulaklar öne, gözler parlak — GEÇTİ, duygusal olarak çok iyi.
- Push-in 1,5–5 sn: var, ama zaten büyük olan Barnaby daha da büyüdü.
- Sahne: fenerler (2–3 görünür), masa (turta 0–1 sn görünüyor, sonra Barnaby'nin arkasında), kızılcık, mısır, ekmek, çan, dolunay, lacivert gök, tabure yok — GEÇTİ.
- Kuyruk yok, beşinci karakter yok, ikinci Barnaby yok, insan parmağı yok — GEÇTİ.

## Hikâye eylemi
Yerinde: Anne'nin dönüşü, Hazel'in fısıltısı, Barnaby'nin "They waited..." anı ve duygulanması okunuyor. En güçlü an 4,5–6,0 sn.

## Kullanılabilir aralık
**0,0 – 6,04 sn** (uzun muzzle kabul edilirse; kesik boynuz Owner kararıyla kabul). Boynuz üst kenarda olduğu için kurguda yeniden kadrajlama (zoom-out) mümkün değil. Alternatif: 3,0–6,04 sn (Hazel fısıltısı + Barnaby tepkisi), yakın plan gibi kullanılırsa kesik boynuz daha az göze batar.

## Tuhaflıklar / blooper
- Anne 2 sn'de gözleri kapalı, "koklar gibi" dönüyor — tatlı ama planda yok.
- Hazel fındıksız.
- Barnaby yüzü "Bambi/gerçek geyik" tipinde; S6-5'teki Barnaby ile aynı karakter gibi durmuyor (yüz/boynuz uyumsuz).
