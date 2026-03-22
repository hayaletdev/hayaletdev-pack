# File: UserInterface/PythonApplication.cpp

## Amac
Tooltip preview icin texture olusturmak.

## Adim
- ARAT:
```cpp
CreateA8R8G8B8Texture(m_dwWidth, m_dwHeight, CRenderTargetManager::RENDER_TARGET_INDEX_MYSHOPDECO)
```
- EKLE ALTINA:
```cpp
#if defined(ENABLE_MONSTER_CARD)
if (!CRenderTargetManager::Instance().CreateA8R8G8B8Texture(m_dwWidth, m_dwHeight, CRenderTargetManager::RENDER_TARGET_INDEX_TOOLTIP_PREVIEW))
    return false;
#endif
```

## Not
- YUTNORI vb texture bloklarinin yerini bozmayin, ayni pattern ile ekleyin.
