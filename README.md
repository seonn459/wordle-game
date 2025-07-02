# Wordle Oyunu - Pygame ile Geliştirildi

Bu proje, Wordle benzeri bir kelime tahmin oyunudur. Python ve Pygame kullanılarak geliştirilmiştir.
Amaç, 6 denemede 5 harfli bir kelimeyi doğru tahmin etmektir.

## Özellikler
- 5 harfli Türkçe kelimelerle oynanır.
- 6 tahmin hakkı.
- Renkli geri bildirim:
	- Yeşil: Harfin kendisi ve konumu doğru
	- Sarı: Harfin kendisi doğru ama konumu yanlış
	- Gri: Harf kelimede yok.
- Skor sistemi
- İpucu sistemi
- Klavye etkileşimi
- Pygame arayüzü

## Kurulum ve Çalıştırma

Python 3 ve pygame kütüphanesi gereklidir.

'''bash
pip install pygame

Oyunu başlatmak için:
python wordle.py