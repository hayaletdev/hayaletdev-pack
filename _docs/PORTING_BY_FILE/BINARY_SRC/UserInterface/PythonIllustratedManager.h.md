# File: UserInterface/PythonIllustratedManager.h

## Amac
Render wrapper'in kullandigi modern layer API'lerini acmak.

## Adim
- ARAT (public):
```cpp
bool SelectModel(DWORD dwVnum);
```
- EKLE ALTINA:
```cpp
void ChangeHair(DWORD dwHair);
void ChangeArmor(DWORD dwArmor);
void ChangeWeapon(DWORD dwWeapon);
void ChangeAcce(DWORD dwAcce);
void ChangeEffect();
```

## Not
- `ChangeAcce` sadece acce sistemi aktifse derlensin.
