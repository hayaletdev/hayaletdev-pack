# File: root/uihuntingmission.py

## Amac
Custom UI penceresinde model preview kullanimi (ornek entegrasyon).

## Adim 1 - Controller import
- ARAT:
```python
import app
```
- EKLE ALTINA:
```python
try:
    import modelpreviewcontroller
except:
    modelpreviewcontroller = None
```

## Adim 2 - Render target widget
- `__CreateModelPreview` icinde:
  - `self.modelPreviewIndex = modelpreviewcontroller.default_shared_window_index()`
  - `self.modelPreviewController = modelpreviewcontroller.ModelPreviewController(self.modelPreviewIndex)`
  - `ui.RenderTarget()` olusturup ayni index'i bagla

## Adim 3 - Refresh
- ARAT:
```python
self.modelPreviewController.show_monster(self.targetMobVnum)
```
- KURAL:
  - `show_monster` sonucu false ise close
  - ayni model tekrarinda reset olmamasi controller cache ile saglanacak

## Adim 4 - Kapanis
- Window Close/Destroy akisinda `self.modelPreviewController.close()` zorunlu.

## Not
- Bu dosya sadece ornek. Gunluk gorev, battlepass vb UI'lar ayni pattern ile baglanabilir.
