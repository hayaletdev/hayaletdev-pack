# File: root/modelpreviewcontroller.py

## Amac
Tum UI'lar icin ortak preview API + cache + index politikasi.

## Adim
- YENI DOSYA veya DEGISTIR:
  - `class ModelPreviewController`
  - `show_player(...)`, `show_monster(...)`, `close()`
  - Mount/Pet cozumleyici yardimcilar

- OPTIMIZASYON (zorunlu):
  - `_last_signature` cache alanini ekle.
  - `show_*` icinde ayni signature gelirse yeniden `SelectModel` atma.

- INDEX POLITIKASI:
  - `default_tooltip_index()` -> tooltip'e ozel
  - `default_shared_window_index()` -> shared UI icin tooltip index'inden kacinsin

## Not
- Bu dosya, yeni UI modullerinin tek giris noktasi olmalı.
