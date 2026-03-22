# Render Target 2.0 Porting Tutorial (Musteri Kurulumu)

Bu dokuman, sistemi kendi files'iniz disindaki bir musteri altyapisina guvenli sekilde tasimak icin hazirlandi.

## 1) Branch ve yedek stratejisi
- Her repo icin ayri branch acin:
  - Client Source: feature/render-target-integration
  - Pack: feature/render-target-integration
  - (Gerekirse Server Source/Binary Source icin de ayni isim)
- Entegrasyon oncesi calisan binary + pack yedegi alin.

## 2) On kosullar
- Client tarafinda RenderTarget altyapisi mevcut olmali.
- Python root tarafi custom moduller yukleyebilmeli.
- Sistem tanimlari derleme aninda aktif olmali:
  - Locale_inc.h: ENABLE_MONSTER_CARD (ve sizin yapinizdaki ilgili makrolar)
  - service.h: sunucunuzda ihtiyac duyulan sistem bayraklari

## 3) Client Source (Binary) entegrasyonu
- Render target indexleri:
  - EterLib/RenderTargetManager.h -> RENDER_TARGET_INDEX_TOOLTIP_PREVIEW
- Python'a index export:
  - UserInterface/PythonApplicationModule.cpp
- Texture olusturma:
  - UserInterface/PythonApplication.cpp -> tooltip preview index texture olusturma
- Player API baglantilari:
  - UserInterface/PythonPlayerModule.cpp
  - TooltipPreviewShow / TooltipPreviewSelectModel / TooltipPreviewChangeEffect

## 4) Pack (Root) entegrasyonu
- Zorunlu dosyalar:
  - root/rendertarget.py
  - root/modelpreviewcontroller.py
  - root/mountpreviewmap.py (mount item -> model map)
- Tooltip entegrasyonu:
  - root/uitooltip.py
  - Ownership mantigi: tooltip sadece kendi render index'ini kapatir.
- Ozellik kullanan UI'lar (ornek):
  - root/uihuntingmission.py
  - Index secimi ortak API'den alin: default_shared_window_index()

## 5) Veri cozumleme kurallari
- Pet preview:
  - once item value[] icinde gecerli monster race ara
- Mount preview:
  - once APPLY_MOUNT affect degeri
  - sonra static map (mountpreviewmap)
  - sonra value[] fallback
- Armor/weapon/hair/acce preview:
  - oyuncu race + ilgili layer setter (SetArmor/SetWeapon/SetHair/SetAcce)

## 6) Cakisma ve performans kurallari
- Ayrik index prensibi:
  - Tooltip penceresi: default_tooltip_index()
  - Paylasimli UI pencereleri: default_shared_window_index()
- Yeniden secim optimizasyonu:
  - ModelPreviewController signature cache kullanir.
  - Ayni model tekrar secilmez; animasyon reset ve render spike azalir.

## 7) Test matrisi (minimum)
- Tooltip:
  - armor / weapon / hair / acce / mount / pet
- UI cakisma:
  - Av gorevleri acikken envanter tooltip ac-kapa
- Durum degisimi:
  - map degisimi, pencere kapatma/acma, character relog
- Beklenen:
  - syserr yok
  - preview kaybolma / baska UI preview'ini oldurme yok
  - mount/pet bos ekran yok

## 8) Saha devreye alma (go-live)
- Once test client + test pack ile staging'de dogrulayın.
- Canary: sinirli oyuncu grubunda 24 saat izleme.
- Sorun yoksa genel dagitima alin.

## 9) Sik gorulen hatalar
- Bos mount preview:
  - APPLY_MOUNT yerine sure/deger okunuyor olabilir -> map fallback kontrol edin.
- UI cakisma:
  - farkli pencere ayni render index'i kullaniyor olabilir.
- Tooltip kapaninca diger preview'in gitmesi:
  - owner kapanis mantigi yoksa gorulur.

## 10) Hizli port checklist
- [ ] Client index + texture + python export tamam
- [ ] Tooltip python API baglandi
- [ ] rendertarget wrapper aktif
- [ ] modelpreviewcontroller aktif
- [ ] mountpreviewmap guncel
- [ ] uitooltip owner mantigi aktif
- [ ] hedef UI'lar default_shared_window_index kullaniyor
- [ ] test matrisi gecti
