# File: EterLib/RenderTargetManager.h

## Amac
Tooltip icin ayri render target index tanimi.

## Adim
- ARAT (enum ERENDERTARGETINDEX bolumu):
```cpp
RENDER_TARGET_INDEX_MYSHOPDECO,
```
- EKLE ALTINA:
```cpp
#if defined(ENABLE_MONSTER_CARD)
RENDER_TARGET_INDEX_TOOLTIP_PREVIEW,
#endif
```

## Not
- Index sirasi bozulmasin.
- `RENDER_TARGET_INDEX_MAX` enum sonu olarak kalmali.
