#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test için İngilizce metin içeren bir görüntü oluşturan betik.
Bu betik, OCR uygulamasını test etmek için kullanılabilecek basit bir görüntü oluşturur.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

def test_goruntu_olustur(dosya_adi="test_goruntu.png", metin=None):
    """
    Test için İngilizce metin içeren bir görüntü oluşturur.
    
    Args:
        dosya_adi (str): Oluşturulacak görüntü dosyasının adı
        metin (str): Görüntüye yazılacak metin. None ise varsayılan metin kullanılır.
    
    Returns:
        str: Oluşturulan görüntü dosyasının yolu
    """
    # Varsayılan metin
    if metin is None:
        metin = """Hello World!
This is an OCR test image.
English characters: abcdefghijklmnopqrstuvwxyz
Numbers: 0123456789
Special characters: !@#$%^&*()_+-="""
    
    # Görüntü boyutları
    genislik = 800
    yukseklik = 400
    
    # Beyaz arka planlı görüntü oluştur
    goruntu = Image.new('RGB', (genislik, yukseklik), color=(255, 255, 255))
    cizim = ImageDraw.Draw(goruntu)
    
    # Font seçimi (varsayılan font kullan)
    try:
        # Windows'ta yaygın bir font
        font = ImageFont.truetype("arial.ttf", 32)
    except IOError:
        try:
            # Linux/macOS'ta yaygın bir font
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except IOError:
            # Font bulunamazsa varsayılan font kullan
            font = ImageFont.load_default()
    
    # Metni görüntüye ekle
    cizim.text((50, 50), metin, fill=(0, 0, 0), font=font)
    
    # Görüntüyü kaydet
    goruntu.save(dosya_adi)
    
    print(f"Test görüntüsü oluşturuldu: {dosya_adi}")
    return os.path.abspath(dosya_adi)

def goruntu_bozma(kaynak_dosya, hedef_dosya="test_goruntu_bozuk.png", gurultu_seviyesi=20):
    """
    Var olan bir görüntüye gürültü ekleyerek bozar.
    
    Args:
        kaynak_dosya (str): Kaynak görüntü dosyasının yolu
        hedef_dosya (str): Bozulmuş görüntünün kaydedileceği dosya yolu
        gurultu_seviyesi (int): Gürültü seviyesi (0-100 arası)
    
    Returns:
        str: Bozulmuş görüntü dosyasının yolu
    """
    # Görüntüyü oku
    goruntu = cv2.imread(kaynak_dosya)
    
    if goruntu is None:
        print(f"Hata: {kaynak_dosya} dosyası okunamadı.")
        return None
    
    # Gürültü ekle
    satir, sutun, kanal = goruntu.shape
    gauss_gurultu = np.random.normal(0, gurultu_seviyesi, (satir, sutun, kanal))
    gauss_gurultu = gauss_gurultu.astype(np.uint8)
    bozuk_goruntu = cv2.add(goruntu, gauss_gurultu)
    
    # Hafif bulanıklaştırma
    bozuk_goruntu = cv2.GaussianBlur(bozuk_goruntu, (3, 3), 0)
    
    # Görüntüyü kaydet
    cv2.imwrite(hedef_dosya, bozuk_goruntu)
    
    print(f"Bozulmuş test görüntüsü oluşturuldu: {hedef_dosya}")
    return os.path.abspath(hedef_dosya)

if __name__ == "__main__":
    # Temiz test görüntüsü oluştur
    temiz_goruntu = test_goruntu_olustur()
    
    # Bozulmuş test görüntüsü oluştur
    bozuk_goruntu = goruntu_bozma(temiz_goruntu)
    
    print("\nTest görüntüleri oluşturuldu. OCR uygulamasını test etmek için şu komutları kullanabilirsiniz:")
    print(f"python ocr_app.py {temiz_goruntu}")
    print(f"python ocr_app.py {bozuk_goruntu}")
    print("\nVeya GUI uygulamasını başlatın ve görüntüleri seçin:")
    print("python ocr_gui.py") 