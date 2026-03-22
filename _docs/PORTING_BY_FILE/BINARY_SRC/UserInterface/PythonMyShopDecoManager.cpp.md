# File: UserInterface/PythonMyShopDecoManager.cpp

## Amac
Tooltip preview akisini MyShopDeco'dan ayirip bagimsiz kanala tasimak.

## Adim
- ARAT:
```cpp
void CPythonMyShopDecoManager::SetShow(bool bShow)
```
- EKLE BENZER FONKSIYONLAR:
```cpp
void CPythonMyShopDecoManager::SetTooltipShow(bool bShow)
void CPythonMyShopDecoManager::SelectTooltipModel(DWORD dwVnum)
void CPythonMyShopDecoManager::ChangeTooltipEffect()
```

## Kural
- Tooltip fonksiyonlari, tooltip render target index'ine yazsin.
- MyShop fonksiyonlari mevcut davranisini korusun.
