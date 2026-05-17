#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basit Optik Karakter Tanıma (OCR) Uygulaması
Bu uygulama, görüntülerden metin çıkarmak için Tesseract OCR kullanır.
"""

import os
import sys
import cv2
import numpy as np
import pytesseract
from PIL import Image

# Windows için Tesseract yolunu ayarlayın
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\guvnr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class OCRUygulamasi:
    """OCR işlemlerini gerçekleştiren sınıf."""
    
    def __init__(self, dil='eng'):
        """
        OCR Uygulaması sınıfını başlatır.
        
        Args:
            dil (str): OCR için kullanılacak dil. Varsayılan: 'eng' (İngilizce)
        """
        self.dil = dil
        
    def goruntu_oku(self, goruntu_yolu):
        """
        Belirtilen yoldaki görüntüyü okur.
        
        Args:
            goruntu_yolu (str): Görüntü dosyasının yolu
            
        Returns:
            numpy.ndarray: Okunan görüntü
        """
        if not os.path.exists(goruntu_yolu):
            raise FileNotFoundError(f"Görüntü dosyası bulunamadı: {goruntu_yolu}")
        
        return cv2.imread(goruntu_yolu)
    
    def on_isleme(self, goruntu):
        """
        OCR öncesi görüntüye ön işleme uygular.
        
        Args:
            goruntu (numpy.ndarray): İşlenecek görüntü
            
        Returns:
            numpy.ndarray: Ön işleme uygulanmış görüntü
        """
        # Gri tonlamaya dönüştür
        gri = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
        
        # Gürültüyü azaltmak için Gaussian bulanıklaştırma
        gri = cv2.GaussianBlur(gri, (5, 5), 0)
        
        # Eşikleme ile ikili görüntüye dönüştür
        _, ikili = cv2.threshold(gri, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        return ikili
    
    def metin_cikart(self, goruntu, on_isleme_uygula=True):
        """
        Görüntüden metin çıkarır.
        
        Args:
            goruntu (numpy.ndarray): Metin çıkarılacak görüntü
            on_isleme_uygula (bool): Ön işleme uygulanıp uygulanmayacağı
            
        Returns:
            str: Çıkarılan metin
        """
        if on_isleme_uygula:
            goruntu = self.on_isleme(goruntu)
        
        # Tesseract OCR ile metin çıkarma
        metin = pytesseract.image_to_string(goruntu, lang=self.dil)
        
        return metin
    
    def dosyadan_metin_cikart(self, goruntu_yolu, on_isleme_uygula=True):
        """
        Dosyadan görüntü okuyarak metin çıkarır.
        
        Args:
            goruntu_yolu (str): Görüntü dosyasının yolu
            on_isleme_uygula (bool): Ön işleme uygulanıp uygulanmayacağı
            
        Returns:
            str: Çıkarılan metin
        """
        goruntu = self.goruntu_oku(goruntu_yolu)
        return self.metin_cikart(goruntu, on_isleme_uygula)


def main():
    """Ana program fonksiyonu."""
    if len(sys.argv) < 2:
        print("Kullanım: python ocr_app.py <görüntü_dosyası>")
        sys.exit(1)
    
    goruntu_yolu = sys.argv[1]
    
    try:
        ocr = OCRUygulamasi()
        metin = ocr.dosyadan_metin_cikart(goruntu_yolu)
        
        print("\nÇıkarılan Metin:")
        print("-" * 50)
        print(metin)
        print("-" * 50)
        
    except Exception as e:
        print(f"Hata: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 