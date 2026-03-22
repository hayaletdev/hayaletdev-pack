# File: UserInterface/PythonApplicationModule.cpp

## Amac
Tooltip render index'ini Python `app` moduline export etmek.

## Adim
- ARAT:
```cpp
PyModule_AddIntConstant(poModule, "RENDER_TARGET_INDEX_MYSHOPDECO", CRenderTargetManager::RENDER_TARGET_INDEX_MYSHOPDECO);
```
- EKLE USTUNE:
```cpp
#if defined(ENABLE_MONSTER_CARD)
PyModule_AddIntConstant(poModule, "RENDER_TARGET_INDEX_TOOLTIP_PREVIEW", CRenderTargetManager::RENDER_TARGET_INDEX_TOOLTIP_PREVIEW);
#endif
```

## Not
- `#if defined(ENABLE_MYSHOP_DECO)` bloklari ile uyumlu kalin.
