#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basit Optik Karakter Tanıma (OCR) Uygulaması - GUI Arayüzü
Bu uygulama, görüntülerden metin çıkarmak için kullanıcı dostu bir arayüz sağlar.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# Kendi OCR modülümüzü içe aktarıyoruz
from ocr_app import OCRUygulamasi

class OCRGUIUygulamasi:
    """OCR için grafik kullanıcı arayüzü sınıfı."""
    
    def __init__(self, root):
        """
        GUI uygulamasını başlatır.
        
        Args:
            root (tk.Tk): Ana Tkinter penceresi
        """
        self.root = root
        self.root.title("OCR Uygulaması")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        self.ocr = OCRUygulamasi()
        
        self.goruntu_yolu = None
        
        self.goruntu = None
        self.islenmis_goruntu = None
        
        self.arayuz_olustur()
    
    def arayuz_olustur(self):
        """GUI bileşenlerini oluşturur ve yerleştirir."""
        
        ana_cerceve = ttk.Frame(self.root, padding="10")
        ana_cerceve.pack(fill=tk.BOTH, expand=True)
        
        ust_panel = ttk.Frame(ana_cerceve)
        ust_panel.pack(fill=tk.X, pady=5)
    
        ttk.Button(ust_panel, text="Görüntü Seç", command=self.goruntu_sec).pack(side=tk.LEFT, padx=5)
        
        
        ttk.Label(ust_panel, text="Dil:").pack(side=tk.LEFT, padx=5)
        self.dil_secimi = ttk.Combobox(ust_panel, values=["eng", "deu", "fra", "spa"], width=5)
        self.dil_secimi.current(0)  # Varsayılan olarak İngilizce
        self.dil_secimi.pack(side=tk.LEFT, padx=5)
        

        ttk.Button(ust_panel, text="Metni Tanı", command=self.ocr_uygula).pack(side=tk.LEFT, padx=5)
        
        
        self.on_isleme_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ust_panel, text="Ön İşleme Uygula", variable=self.on_isleme_var).pack(side=tk.LEFT, padx=5)
        
    
        ttk.Button(ust_panel, text="Temizle", command=self.temizle).pack(side=tk.RIGHT, padx=5)
        
        
        orta_panel = ttk.PanedWindow(ana_cerceve, orient=tk.HORIZONTAL)
        orta_panel.pack(fill=tk.BOTH, expand=True, pady=5)
        
        
        self.goruntu_cercevesi = ttk.LabelFrame(orta_panel, text="Görüntü")
        orta_panel.add(self.goruntu_cercevesi, weight=1)
        
        self.goruntu_etiketi = ttk.Label(self.goruntu_cercevesi)
        self.goruntu_etiketi.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        metin_cercevesi = ttk.LabelFrame(orta_panel, text="Tanınan Metin")
        orta_panel.add(metin_cercevesi, weight=1)
        
        self.metin_alani = scrolledtext.ScrolledText(metin_cercevesi, wrap=tk.WORD, width=40, height=20)
        self.metin_alani.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        
        self.durum_cubugu = ttk.Label(ana_cerceve, text="Hazır", relief=tk.SUNKEN, anchor=tk.W)
        self.durum_cubugu.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
    
    def goruntu_sec(self):
        """Kullanıcının görüntü dosyası seçmesini sağlar."""
        dosya_tipleri = [
            ("Görüntü Dosyaları", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
            ("Tüm Dosyalar", "*.*")
        ]
        
        dosya_yolu = filedialog.askopenfilename(
            title="Görüntü Dosyası Seç",
            filetypes=dosya_tipleri
        )
        
        if dosya_yolu:
            self.goruntu_yolu = dosya_yolu
            self.durum_cubugu.config(text=f"Seçilen dosya: {os.path.basename(dosya_yolu)}")
            
            try:
            
                self.goruntu = cv2.imread(dosya_yolu)
                self.goruntu_goster(self.goruntu)
                
                
                self.metin_alani.delete(1.0, tk.END)
            except Exception as e:
                messagebox.showerror("Hata", f"Görüntü yüklenirken hata oluştu: {e}")
    
    def goruntu_goster(self, goruntu):
        """
        Görüntüyü GUI'de gösterir.
        
        Args:
            goruntu (numpy.ndarray): Gösterilecek görüntü
        """
        if goruntu is None:
            return
        
    
        goruntu_rgb = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
        
    
        h, w = goruntu_rgb.shape[:2]
        max_h = 400  # Maksimum yükseklik
        max_w = 500  # Maksimum genişlik
        
    
        if h > max_h or w > max_w:
            oran = min(max_h / h, max_w / w)
            yeni_h, yeni_w = int(h * oran), int(w * oran)
            goruntu_rgb = cv2.resize(goruntu_rgb, (yeni_w, yeni_h))
        
    
        pil_goruntu = Image.fromarray(goruntu_rgb)
        
        
        tk_goruntu = ImageTk.PhotoImage(pil_goruntu)
        
        
        self.goruntu_etiketi.config(image=tk_goruntu)
        self.goruntu_etiketi.image = tk_goruntu  # Referansı koru
    
    def ocr_uygula(self):
        """Seçilen görüntüye OCR uygular ve sonuçları gösterir."""
        if self.goruntu is None:
            messagebox.showwarning("Uyarı", "Lütfen önce bir görüntü seçin.")
            return
        
        try:

            self.ocr.dil = self.dil_secimi.get()
            
        
            on_isleme_uygula = self.on_isleme_var.get()
            
            
            self.durum_cubugu.config(text="OCR uygulanıyor...")
            self.root.update()
            
            
            if on_isleme_uygula:
                self.islenmis_goruntu = self.ocr.on_isleme(self.goruntu)
                self.goruntu_goster(self.islenmis_goruntu)
                metin = self.ocr.metin_cikart(self.goruntu, on_isleme_uygula=True)
            else:
                metin = self.ocr.metin_cikart(self.goruntu, on_isleme_uygula=False)
            
        
            self.metin_alani.delete(1.0, tk.END)
            self.metin_alani.insert(tk.END, metin)
            
            
            self.durum_cubugu.config(text="OCR tamamlandı.")
            
        except Exception as e:
            messagebox.showerror("Hata", f"OCR uygulanırken hata oluştu: {e}")
            self.durum_cubugu.config(text="Hata oluştu.")
    
    def temizle(self):
        """Uygulamayı sıfırlar."""
        self.goruntu = None
        self.islenmis_goruntu = None
        self.goruntu_yolu = None
        
        
        self.goruntu_etiketi.config(image="")
        
        
        self.metin_alani.delete(1.0, tk.END)
        
    
        self.durum_cubugu.config(text="Hazır")


def main():
    """Ana program fonksiyonu."""
    root = tk.Tk()
    app = OCRGUIUygulamasi(root)
    root.mainloop()


if __name__ == "__main__":
    main() 