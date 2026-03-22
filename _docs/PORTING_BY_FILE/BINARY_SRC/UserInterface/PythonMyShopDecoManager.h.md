# File: UserInterface/PythonMyShopDecoManager.h

## Amac
Tooltip preview icin manager API eklemek.

## Adim
- ARAT (public methodlar):
```cpp
void ChangeEffect();
```
- EKLE ALTINA:
```cpp
void SetTooltipShow(bool bShow);
void SelectTooltipModel(DWORD dwVnum);
void ChangeTooltipEffect();
```

## Not
- Internal owner/state degiskenleri varsa tooltip icin ayri instance state tutun.
