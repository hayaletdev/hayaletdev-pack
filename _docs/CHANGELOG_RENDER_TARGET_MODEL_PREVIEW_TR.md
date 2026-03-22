# Render Target Model Preview - Changelog (TR)

- Izole Render Target yapisi aktif edildi: Binek ve pet onizlemeleri, MyShopDeco kanalindan ayrilip RENDER_TARGET_INDEX_TOOLTIP_PREVIEW index'ine tasindi.
- CPythonMyShopDecoManager genisletildi: Arac ipucu (tooltip) icin bagimsiz onizleme durumu, model yonetimi ve render akis eklendi.
- Yeni Python API'leri entegre edildi: Tooltip onizleme kontrolu icin TooltipPreviewShow, TooltipPreviewSelectModel ve TooltipPreviewChangeEffect komutlari tanimlandi.
- Python Yonlendirme Protokolu guncellendi: Binek ve pet onizleme talepleri otomatik olarak ilgili ozel index'e yonlendiriliyor.
- Geriye donuk uyumluluk korundu: Mevcut kostum, zirh ve sac onizleme akisi bozulmadan eski yapiyla calismaya devam ediyor.
- Cakisma Onleyici (Owner) mantigi eklendi: Ayni render index'inin birden fazla pencere tarafindan ayni anda kullanilmasi engellenerek goruntu hatalari giderildi.
- Veri Esleme Standartlari belirlendi: APPLY_MOUNT ve Value[] uzerinden pet/binek mob race kodlari icin otomatik fallback mekanizmasi kuruldu.
- Optimizasyon ve Temizlik: Harita degisimi veya pencere kapanisinda cleanup cagrisi zorunlu hale getirilerek bellek sizintilari onlendi.
- Ortak Controller katmani guclendirildi: ModelPreviewController icine model-signature cache eklendi; ayni model tekrar secilmedigi icin animasyon reseti ve gereksiz render maliyeti azaltildi.
- Paylasimli UI index politikasi merkezilestirildi: default_shared_window_index ile tooltip disi pencereler icin guvenli index secimi standart hale getirildi.

Not: ModelPreviewController entegrasyonu ile tum UI modulleri ortak API uzerinden calisacak.
