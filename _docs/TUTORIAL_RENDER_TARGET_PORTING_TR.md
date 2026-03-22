# Render Target 2.0 Porting - File by File (TR)

Bu rehber, dosya kopyalamadan (bizden full file vermeden) musteri source'una patch uygulamak icin hazirlandi.

Kurallar:
- Her dosyada sadece gerekli satiri degistirin.
- Adim formati: ARAT -> EKLE / DEGISTIR / YENI DOSYA
- Her adimdan sonra derleme veya client acilis testi alin.

## 1) Binary Source adimlari
Klasor: `_docs/PORTING_BY_FILE/BINARY_SRC`

Sirali uygulama:
1. `UserInterface/Locale_inc.h.md`
2. `EterLib/RenderTargetManager.h.md`
3. `UserInterface/PythonApplication.cpp.md`
4. `UserInterface/PythonApplicationModule.cpp.md`
5. `UserInterface/PythonMyShopDecoManager.h.md`
6. `UserInterface/PythonMyShopDecoManager.cpp.md`
7. `UserInterface/PythonPlayerModule.cpp.md`
8. `UserInterface/InstanceBase.h.md`
9. `UserInterface/InstanceBase.cpp.md`
10. `UserInterface/PythonIllustratedManager.h.md`
11. `UserInterface/PythonIllustratedManager.cpp.md`

## 2) Pack (root) adimlari
Klasor: `_docs/PORTING_BY_FILE/PACK`

Sirali uygulama:
1. `root/constinfo.py.md`
2. `root/rendertarget.py.md`
3. `root/modelpreviewcontroller.py.md`
4. `root/mountpreviewmap.py.md`
5. `root/uitooltip.py.md`
6. `root/uimyshopdecoration.py.md`
7. `root/uihuntingmission.py.md` (ornek custom UI)

## 3) Test check
- Tooltip: armor/weapon/hair/acce/mount/pet model geliyor mu?
- Cakisma: Av gorevi acikken tooltip ac-kapa yaptiginda preview kayiyor mu?
- Performans: kill update gelirken model her pakette resetleniyor mu?
- Syserr: `GetRaceDataPointer` veya `TooltipPreview* missing` hatasi var mi?
