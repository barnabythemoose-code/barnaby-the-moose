# RAPOR — TG-S9-1 (Klip 5/7)

## Üretim
- request_id: abec4e4c0e376b2f3febf5ef929180c2
- Model: seedance-2.5, 720p, 16:9 (1280×720), 8 sn istendi → 8,04 sn geldi, 24 fps, ses yok
- 7 referans görsel, seed 20261010, prompt birebir
- Üretim süresi: 203 sn
- Bakiye önce / sonra: 24,2552 → 22,3501 → **maliyet $1,91**
- Dosyalar: `TG-S9-1_d01.mp4`, `TG-S9-1_lastframe.jpg`, `kareler/` (0–8 sn + son kare + `sheet.png`), `payload.json`, `result.json`, `meta.json`

## Kimlik kartı (kanon: Image1 Barnaby, Image2 Hazel)
Barnaby
1. Boynuz kürkten koyu çikolata — **SINIRDA**: açık tarçın (tüm süre)
2. Kalın hilal, ~3 kısa yuvarlak çatal — GEÇTİ
3. Açıklık ~1,8×, simetrik, kadrajda tam — GEÇTİ (tüm süre tam kadrajda; üstte az boşluk). Toynaklar da kadrajda, altta çim var — GEÇTİ
4. Burun dev, antrasit, mat — GEÇTİ (koyu kahve-antrasit, büyük)
5. Muzzle kısa kalın karamel — **KALDI**: uzun geyik muzzle (tüm süre)
6. Gözler beyaz sklera, kehribar iris — GEÇTİ
7. Kürk karamel, karın krem — GEÇTİ
8. Kazak parlak kırmızı, balıkçı yaka, desen yok — GEÇTİ (yaprak + şurup resim-sol göğüs/kolda)
9. Tombul armut gövde, dik — GEÇTİ (bacaklar kanona göre uzun-ince)
10. Eller antrasit iki parmaklı toynak — GEÇTİ (3–5 sn)

Hazel
11–20: GEÇTİ (büyük baş, siyah göz, krem yanak, turuncu kürk, alın çizgisi, S kuyruk, mint atkı). Fındık: elinde küçük bir şey var ama 720p'de belirsiz (3 sn). Resim-sol omuzda — GEÇTİ.

Anne (Image4): antlersız, hardal şal, dev burun — GEÇTİ; renk açık karamel (S8-3/S8-4 Shot 2 ile uyumlu, S8-2 ile değil).
Baba (Image3): yeşil kazak, gözlük, gri sakal, kalın boynuz, toynak çan ipinde — GEÇTİ.
Çan direği (Image5): GEÇTİ.

**Kimlik sonucu: KALDI** (madde 5; madde 1 sınırda).

## Süreklilik
- **Konum sapması:** prompt üçünü masanın ÖNÜNDE istiyordu. Barnaby masanın önünde (sol), ama Anne ve Baba masanın ARKASINDA (uzak tarafında) duruyor. Hikâye için sorun değil (S9-2b'de zaten masanın arkasına oturacaklar), ama S9-2a ile eşleşme kontrol edilmeli.
- 0–1,4 sn üçü gülümsüyor, Barnaby'nin gözü masada — GEÇTİ (0 sn gözü turtada).
- 1,4 sn Anne yüzünü Baba'ya çevirip başını sallıyor — GEÇTİ (1–2 sn Baba'ya bakıyor).
- 2,2 "Hm." + 2,8 ip çekme — 3 sn Baba'nın toynağı ipte, çan hafif eğik — GEÇTİ (sallanma karelerden kesin değil); üçünün gözü çana — 3 sn Barnaby sağa/yukarı bakıyor — GEÇTİ. Fenerler sabit — GEÇTİ.
- 4,4 sn Baba üç küçük adım — Baba masanın arkasında, bacaklar masa ve taburelerle kısmen örtülü; 5–6 sn gövde hareketi var, adımlar net okunmuyor — ZAYIF.
- 5,6/6,0/6,4 Barnaby üç toynak vuruşu — 6–8 sn ağırlık değiştiriyor, 7 sn'de arka bacak kalkık — GEÇTİ (kabaca).
- 7–8 sn üçü gülümseyip duruyor — GEÇTİ (son kare çok iyi: üçü de gülümsüyor).
- Push-in 0–4,4 sn — var, hafif — GEÇTİ.
- Sahne: tabureli masa, turta, kızılcık, mısır, ekmek, fenerler, çan, dolunay — GEÇTİ. Kimse oturmuyor — GEÇTİ.

## Hikâye eylemi
Yerinde: nod → çan → Baba'nın adımları (zayıf) → Barnaby'nin taklidi → ortak gülümseme. Çan vuruşu ve adım ritmi ElevenLabs/ses efektiyle güçlendirilmeli.

## Kullanılabilir aralık
**0,0 – 8,04 sn (tamamı).**

## Tuhaflıklar / blooper
- Anne ve Baba masanın arkasında (plan: önünde).
- Baba'nın adım ritmi görünmüyor; Barnaby'nin taklidi tek başına "yerinde kıpırdanma" gibi okunabilir.
- Barnaby'nin bacakları ince/uzun, kanon tombulluğu az.
