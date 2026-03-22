# File: root/uitooltip.py

## Amac
Tooltip icinde armor/weapon/costume/mount/pet model onizleme.

## Adim 1 - State
- ARAT (`ItemToolTip.__init__` sonlari):
```python
self.ModelPreviewBoard = None
self.ModelPreview = None
self.ModelPreviewText = None
```
- EKLE ALTINA:
```python
self.ModelPreviewRenderIndex = 0
```

## Adim 2 - Index owner
- ARAT (`__ModelPreview`):
```python
RENDER_TARGET_INDEX = 0
```
- KURAL:
  - Mount/Pet (previewType == 5) icin once `app.RENDER_TARGET_INDEX_TOOLTIP_PREVIEW`
  - fallback `app.RENDER_TARGET_INDEX_MYSHOPDECO`
  - secilen index'i `self.ModelPreviewRenderIndex` icine yaz

## Adim 3 - Kapanis cleanup
- ARAT (`__ModelPreviewClose`):
```python
renderTarget.SetVisibility(0, False)
```
- DEGISTIR:
```python
renderTarget.SetVisibility(getattr(self, "ModelPreviewRenderIndex", 0), False)
```
- EKLE:
```python
self.ModelPreviewRenderIndex = 0
```

## Adim 4 - Mount/Pet model cozumleme
- `__GetMountModelVnum` kurali:
  1) APPLY_MOUNT
  2) mountpreviewmap
  3) value[] fallback
- `__GetPetModelVnum` kurali:
  - value[] icinden gecerli monster race

## Not
- Tooltip kendi index'ini kapatacak; baska pencerenin preview'ine dokunmayacak.
