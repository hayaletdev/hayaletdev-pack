# File: UserInterface/PythonIllustratedManager.cpp

## Amac
Python wrapper'dan gelen layer degisimlerini uygulamak.

## Adim
- ARAT:
```cpp
bool CPythonIllustratedManager::SelectModel(DWORD dwVnum)
```
- KONTROL:
  - Race 0 hard fail olmasin (gerekiyorsa fallback).
  - Model seciminden sonra `ChangeEffect()` cagrilabilsin.

- YENI FONKSIYONLAR EKLE:
```cpp
void CPythonIllustratedManager::ChangeHair(DWORD dwHair)
void CPythonIllustratedManager::ChangeArmor(DWORD dwArmor)
void CPythonIllustratedManager::ChangeWeapon(DWORD dwWeapon)
void CPythonIllustratedManager::ChangeAcce(DWORD dwAcce)
void CPythonIllustratedManager::ChangeEffect()
```

## Not
- Cagrilar `CInstanceBase` katmanina inmeli.
