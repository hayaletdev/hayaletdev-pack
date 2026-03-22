# File: UserInterface/PythonPlayerModule.cpp

## Amac
Python tarafinda tooltip preview komutlarini acmak.

## Adim 1 - Yeni C API fonksiyonlari
- ARAT:
```cpp
PyObject* playerMyShopDecoChangeEffect(PyObject* poSelf, PyObject* poArgs)
```
- EKLE ALTINA:
```cpp
PyObject* playerTooltipPreviewShow(PyObject* poSelf, PyObject* poArgs)
PyObject* playerTooltipPreviewSelectModel(PyObject* poSelf, PyObject* poArgs)
PyObject* playerTooltipPreviewChangeEffect(PyObject* poSelf, PyObject* poArgs)
```

## Adim 2 - Python method table
- ARAT (method table):
```cpp
{ "MyShopDecoChangeEffect", playerMyShopDecoChangeEffect, METH_VARARGS },
```
- EKLE ALTINA:
```cpp
#if defined(ENABLE_MONSTER_CARD)
{ "TooltipPreviewShow", playerTooltipPreviewShow, METH_VARARGS },
{ "TooltipPreviewSelectModel", playerTooltipPreviewSelectModel, METH_VARARGS },
{ "TooltipPreviewChangeEffect", playerTooltipPreviewChangeEffect, METH_VARARGS },
#endif
```

## Not
- Duplicate kayit olmamali; method table'da tek set olsun.
