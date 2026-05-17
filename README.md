# Basit Optik Karakter Tanıma (OCR) Uygulaması

Bu proje, görüntülerden metin çıkarmak için Python ile geliştirilmiş basit bir OCR (Optik Karakter Tanıma) uygulamasıdır. Uygulama, Tesseract OCR motorunu kullanarak görüntülerdeki metinleri tanır ve çıkarır.

## Özellikler

- Görüntü dosyalarından metin çıkarma
- Görüntü ön işleme (gri tonlama, bulanıklaştırma, eşikleme)
- Çoklu dil desteği (İngilizce, Almanca, Fransızca, İspanyolca)
- Kullanıcı dostu grafik arayüzü
- Komut satırı arayüzü

## Gereksinimler

- Python 3.6 veya üzeri
- Tesseract OCR (https://github.com/tesseract-ocr/tesseract)
- Python kütüphaneleri (requirements.txt dosyasında listelenmiştir)

## Kurulum

1. Tesseract OCR'ı sisteminize kurun:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - Linux: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

2. İhtiyaç duyarsanız ek dil paketlerini kurun:
   - Windows: Kurulum sırasında dil paketlerini seçin
   - Linux: `sudo apt install tesseract-ocr-[dil kodu]`
   - macOS: `brew install tesseract-lang`

3. Python bağımlılıklarını yükleyin:
   ```
   pip install -r requirements.txt
   ```

4. `ocr_app.py` dosyasında Tesseract yolunu kontrol edin:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Users\guvnr\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
   ```
   Eğer Tesseract farklı bir konuma kurulduysa, bu yolu değiştirin.

## Kullanım

### Grafik Arayüz (GUI)

GUI uygulamasını başlatmak için:

```
python ocr_gui.py
```

1. "Görüntü Seç" düğmesine tıklayarak bir görüntü dosyası seçin
2. İsterseniz dil seçimini değiştirin (varsayılan: İngilizce)
3. "Metni Tanı" düğmesine tıklayarak OCR işlemini başlatın
4. Tanınan metin sağ panelde görüntülenecektir

### Komut Satırı Arayüzü

Komut satırından bir görüntü dosyasından metin çıkarmak için:

```
python ocr_app.py <görüntü_dosyası>
```

Örnek:
```
python ocr_app.py ornek.jpg
```

### Test Görüntüsü Oluşturma

Test için bir görüntü oluşturmak isterseniz:

```
python test_goruntu_olustur.py
```

Bu komut, OCR testleri için iki görüntü oluşturacaktır: temiz bir görüntü ve gürültü eklenmiş bir görüntü.

## Proje Yapısı

- `ocr_app.py`: OCR işlevselliğini içeren ana modül
- `ocr_gui.py`: Grafik kullanıcı arayüzü
- `test_goruntu_olustur.py`: Test görüntüleri oluşturan betik
- `requirements.txt`: Gerekli Python kütüphaneleri

## Notlar

- Tesseract OCR'ın doğruluğu, görüntü kalitesine ve metin formatına bağlıdır
- En iyi sonuçlar için yüksek kontrastlı, temiz görüntüler kullanın
- Ön işleme seçeneği, düşük kaliteli görüntülerde tanıma doğruluğunu artırabilir
