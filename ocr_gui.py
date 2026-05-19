#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Basit Optik Karakter Tanıma (OCR) Uygulaması - GUI Arayüzü
Bu uygulama, görüntülerden metin çıkarmak için modern ve şık bir arayüz sağlar.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

# Gelişmiş OCR modülümüzü içe aktarıyoruz
from ocr_app import OCRUygulamasi


class OCRGUIUygulamasi:
    """OCR için modern, premium grafik kullanıcı arayüzü sınıfı."""
    
    def __init__(self, root):
        """
        GUI uygulamasını başlatır.
        
        Args:
            root (tk.Tk): Ana Tkinter penceresi
        """
        self.root = root
        self.root.title("Basit Optik Karakter Tanıma (OCR) Sistemi")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        
        self.ocr = OCRUygulamasi(dil='eng+tur')
        
        self.goruntu_yolu = None
        self.goruntu = None
        self.islenmis_goruntu = None
        
        self.stil_ayarla()
        self.arayuz_olustur()
        
    def stil_ayarla(self):
        """Uygulamanın modern dark stilini yapılandırır."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.bg_color = "#1e1e2e"       # Ana arka plan
        self.card_color = "#252538"     # Panel arka planı
        self.fg_color = "#cdd6f4"       # Yazı rengi
        self.accent_color = "#89b4fa"   # Belirgin mavi/cyan
        self.accent_green = "#a6e3a1"   # Başarı yeşili
        self.border_color = "#45475a"   # İnce kenarlıklar
        
        self.root.configure(bg=self.bg_color)
        
        self.style.configure(".", background=self.bg_color, foreground=self.fg_color, font=("Segoe UI", 10))
        self.style.configure("TFrame", background=self.bg_color)
        
        self.style.configure("TLabelframe", background=self.bg_color, bordercolor=self.border_color, borderwidth=1)
        self.style.configure("TLabelframe.Label", background=self.bg_color, foreground=self.accent_color, font=("Segoe UI", 10, "bold"))
        
        self.style.configure("TButton", background=self.card_color, foreground=self.fg_color, bordercolor=self.border_color, borderwidth=1, focuscolor=self.accent_color, padding=6)
        self.style.map("TButton",
            background=[("active", self.accent_color), ("pressed", "#74c7ec")],
            foreground=[("active", "#1e1e2e")]
        )
        
        self.style.configure("Accent.TButton", background=self.accent_color, foreground="#1e1e2e", bordercolor=self.border_color, font=("Segoe UI", 10, "bold"), padding=6)
        self.style.map("Accent.TButton",
            background=[("active", self.accent_green), ("pressed", "#94e2d5")],
            foreground=[("active", "#1e1e2e")]
        )
        

        self.style.configure("TCombobox", fieldbackground=self.card_color, background=self.card_color, foreground=self.fg_color, bordercolor=self.border_color, arrowcolor=self.fg_color)
        
        self.style.configure("TCheckbutton", background=self.bg_color, foreground=self.fg_color, focuscolor="")
        self.style.map("TCheckbutton",
            indicatorcolor=[("selected", self.accent_green), ("!selected", self.card_color)],
            background=[("active", self.bg_color)]
        )
        
        self.style.configure("TLabel", background=self.bg_color, foreground=self.fg_color)
        self.style.configure("Title.TLabel", foreground=self.accent_color, font=("Segoe UI", 14, "bold"))
        self.style.configure("Status.TLabel", background=self.card_color, foreground=self.accent_green, font=("Segoe UI", 9, "italic"))
        
    def arayuz_olustur(self):
        """GUI bileşenlerini oluşturur ve yerleştirir."""
        
        ana_cerceve = ttk.Frame(self.root, padding="15")
        ana_cerceve.pack(fill=tk.BOTH, expand=True)
        
        ust_panel = ttk.Frame(ana_cerceve)
        ust_panel.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(ust_panel, text="🎛️ BASİT OPTİK KARAKTER TANIMA (OCR) UYGULAMASI", style="Title.TLabel")
        title_label.pack(side=tk.LEFT)
        
        kontrol_cercevesi = ttk.LabelFrame(ana_cerceve, text=" OCR Kontrol ve Yapılandırma Paneli ", padding="10")
        kontrol_cercevesi.pack(fill=tk.X, pady=(0, 10))
        
        kontrol_satir1 = ttk.Frame(kontrol_cercevesi)
        kontrol_satir1.pack(fill=tk.X, pady=5)
        
        ttk.Button(kontrol_satir1, text="📂 Görüntü Dosyası Seç", command=self.goruntu_sec, style="TButton").pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(kontrol_satir1, text="Dil Tanıma Paketi:").pack(side=tk.LEFT, padx=5)
        self.dil_secimi = ttk.Combobox(kontrol_satir1, values=["eng+tur", "tur", "eng", "deu", "fra", "spa"], width=10, state="readonly")
        self.dil_secimi.current(0)  # Varsayılan: eng+tur
        self.dil_secimi.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(kontrol_satir1, text="Ön İşleme Modu:").pack(side=tk.LEFT, padx=5)
        self.yontem_secimi = ttk.Combobox(kontrol_satir1, values=[
            "El Yazısı / Düşük Kalite",
            "Lokal Aydınlatma Düzeltmesi (Gölge Giderme)",
            "Akıllı Adaptif Eşikleme",
            "Sadece Gri Tonlama",
            "Klasik Otsu Binarizasyon",
            "Gelişmiş Kontrast İyileştirme (CLAHE)",
            "Renkleri Ters Çevir (Koyu Tema)",
            "Orijinal"
        ], width=38, state="readonly")
        self.yontem_secimi.current(0)  
        self.yontem_secimi.pack(side=tk.LEFT, padx=(0, 15))
        
        kontrol_satir2 = ttk.Frame(kontrol_cercevesi)
        kontrol_satir2.pack(fill=tk.X, pady=5)
        
        self.otomatik_duzelt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(kontrol_satir2, text="Metin Hatalarını Akıllı Otomatik Düzelt", variable=self.otomatik_duzelt_var).pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Button(kontrol_satir2, text="🔍 METNİ TANI VE ANALİZ ET", command=self.ocr_uygula, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(kontrol_satir2, text="🧹 Arayüzü Temizle", command=self.temizle, style="TButton").pack(side=tk.RIGHT, padx=5)
        
        orta_panel = ttk.PanedWindow(ana_cerceve, orient=tk.HORIZONTAL)
        orta_panel.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Sol Panel
        self.goruntu_cercevesi = ttk.LabelFrame(orta_panel, text=" Ön İşlenmiş / Orijinal Görüntü Önizleme ")
        orta_panel.add(self.goruntu_cercevesi, weight=1)
        
        self.resim_kapsayici = ttk.Frame(self.goruntu_cercevesi)
        self.resim_kapsayici.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.goruntu_etiketi = ttk.Label(self.resim_kapsayici, anchor=tk.CENTER)
        self.goruntu_etiketi.pack(fill=tk.BOTH, expand=True)
        
        # Sağ Panel
        metin_cercevesi = ttk.LabelFrame(orta_panel, text=" OCR Tarafından Tanınan ve Düzeltilen Metin ")
        orta_panel.add(metin_cercevesi, weight=1)
        
        self.metin_alani = scrolledtext.ScrolledText(
            metin_cercevesi, wrap=tk.WORD, width=40, height=20,
            bg="#11111b", fg="#a6e3a1", insertbackground="#cdd6f4",
            selectbackground="#313244", selectforeground="#a6e3a1",
            font=("Consolas", 11), bd=0, highlightthickness=1, highlightcolor=self.accent_color
        )
        self.metin_alani.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        
        durum_cercevesi = ttk.Frame(ana_cerceve, padding=(5, 2))
        durum_cercevesi.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        durum_cercevesi.configure(style="TFrame")
        
        self.durum_cubugu = ttk.Label(durum_cercevesi, text="🔋 Hazır. Lütfen OCR işlemi için bir görüntü yükleyin.", style="Status.TLabel", relief=tk.FLAT, padding=4)
        self.durum_cubugu.pack(fill=tk.X)
        self.durum_cubugu.configure(background="#11111b")
        
    def goruntu_sec(self):
        """Kullanıcının dosya sisteminden güvenli bir şekilde görüntü seçmesini sağlar."""
        dosya_tipleri = [
            ("Görüntü Dosyaları", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff"),
            ("Tüm Dosyalar", "*.*")
        ]
        
        dosya_yolu = filedialog.askopenfilename(
            title="OCR Görüntü Dosyası Seç",
            filetypes=dosya_tipleri
        )
        
        if dosya_yolu:
            self.goruntu_yolu = dosya_yolu
            dosya_adi = os.path.basename(dosya_yolu)
            self.durum_cubugu.config(text=f"📂 Görüntü yüklendi: {dosya_adi} | Şimdi tanıma dillerini seçip 'Metni Tanı' butonuna tıklayabilirsiniz.")
            
            try:
                self.goruntu = self.ocr.goruntu_oku(dosya_yolu)
                
                self.goruntu_goster(self.goruntu)
                self.metin_alani.delete(1.0, tk.END)
                
                h, w = self.goruntu.shape[:2]
                öneri = ""
                if "thumbnail" in dosya_adi.lower() or h < 600 or w < 600:
                    öneri = " [Öneri: Bu görüntü düşük çözünürlüklü görünüyor, 'El Yazısı / Düşük Kalite' modu en iyi sonucu verecektir.]"
                elif "röportaj" in dosya_adi.lower() or "uzmanı" in dosya_adi.lower():
                    öneri = " [Öneri: Bu görsel Türkçe isimler barındıran bir mektup/mülakat, 'eng+tur' dil paketini seçmeniz önerilir.]"
                elif "AFMNKDOC" in dosya_adi:
                    öneri = " [Öneri: Bu bir teknik şema/katalog. Düşük kaliteli veya silik yazılar için 'Akıllı Adaptif Eşikleme' veya 'CLAHE' modunu deneyebilirsiniz.]"
                
                self.durum_cubugu.config(text=f"📂 Görüntü yüklendi: {dosya_adi}.{öneri}")
                
            except Exception as e:
                messagebox.showerror("Görüntü Yükleme Hatası", f"Görüntü yüklenirken kritik bir hata oluştu:\n{e}")
                self.durum_cubugu.config(text="⚠️ Dosya yüklenemedi.")
                
    def goruntu_goster(self, goruntu):
        """
        Görüntüyü GUI ekran boyutlarına göre orantılı küçülterek güvenli bir şekilde gösterir.
        Grayscale tek kanallı görüntüleri de güvenle işler.
        
        Args:
            goruntu (numpy.ndarray): Gösterilecek görüntü dizisi
        """
        if goruntu is None:
            return
        
        if len(goruntu.shape) == 2:
            goruntu_rgb = cv2.cvtColor(goruntu, cv2.COLOR_GRAY2RGB)
        else:
            goruntu_rgb = cv2.cvtColor(goruntu, cv2.COLOR_BGR2RGB)
            
        h, w = goruntu_rgb.shape[:2]
        
        max_h = 420
        max_w = 480
        
        if h > max_h or w > max_w:
            oran = min(max_h / h, max_w / w)
            yeni_h, yeni_w = int(h * oran), int(w * oran)
            goruntu_rgb = cv2.resize(goruntu_rgb, (yeni_w, yeni_h), interpolation=cv2.INTER_AREA)
            
        pil_goruntu = Image.fromarray(goruntu_rgb)
        tk_goruntu = ImageTk.PhotoImage(pil_goruntu)
        
        self.goruntu_etiketi.config(image=tk_goruntu)
        self.goruntu_etiketi.image = tk_goruntu  
        
    def ocr_uygula(self):
        """Seçilen ön işleme yöntemlerini ve OCR algoritmasını görsel üzerinde çalıştırır."""
        if self.goruntu is None:
            messagebox.showwarning("Görüntü Eksik", "Lütfen öncelikle 'Görüntü Dosyası Seç' butonu ile bir resim yükleyin.")
            return
            
        try:
            dil = self.dil_secimi.get()
            self.ocr.dil = dil
            
            yontem = self.yontem_secimi.get()
            oto_duzelt = self.otomatik_duzelt_var.get()
            
            self.durum_cubugu.config(text=f"⚡ OCR Tanıma İşlemi Yapılıyor... Dil: {dil} | Mod: {yontem} | Lütfen bekleyin...")
            self.root.update()
            
            # Görüntüye ön işlemeyi uygulayıp arayüzde gösteriyoruz
            self.islenmis_goruntu = self.ocr.on_isleme_uygula(self.goruntu, yontem)
            self.goruntu_goster(self.islenmis_goruntu)
            
            # OCR işlemi
            metin = self.ocr.metin_cikart(
                self.goruntu,
                on_isleme_yontemi=yontem,
                otomatik_duzeltme_uygula=oto_duzelt
            )
            
            self.metin_alani.delete(1.0, tk.END)
            self.metin_alani.insert(tk.END, metin)
            
            karakter_sayisi = len(metin)
            kelime_sayisi = len(metin.split())
            self.durum_cubugu.config(
                text=f"✅ Başarılı! OCR tamamlandı. {kelime_sayisi} kelime, {karakter_sayisi} karakter başarıyla okundu."
            )
            
        except Exception as e:
            messagebox.showerror("OCR İşlem Hatası", f"Optik karakter tanıma sırasında bir sorunla karşılaşıldı:\n{e}")
            self.durum_cubugu.config(text="⚠️ OCR işlemi hata nedeniyle durduruldu.")
            
    def temizle(self):
        """Uygulama arayüzünü ve yüklenen verileri sıfırlar."""
        self.goruntu = None
        self.islenmis_goruntu = None
        self.goruntu_yolu = None
        
        self.goruntu_etiketi.config(image="")
        self.metin_alani.delete(1.0, tk.END)
        self.durum_cubugu.config(text="🔋 Hazır. Lütfen OCR işlemi için bir görüntü yükleyin.")


def main():
    """Grafik arayüzü başlatan ana fonksiyon."""
    root = tk.Tk()
    app = OCRGUIUygulamasi(root)
    root.mainloop()


if __name__ == "__main__":
    main()