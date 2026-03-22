# File: UserInterface/InstanceBase.cpp

## Amac
Preview model effectlerini tazelemek.

## Adim
- YENI FONKSIYON EKLE:
```cpp
void CInstanceBase::SetEffect()
{
    ShowAllAttachingEffect();
    Refresh(NAME_WAIT, true);
}
```

## Not
- Fonksiyon imzasi header ile birebir ayni olmali.
