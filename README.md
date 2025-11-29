# Fotoğraf Boyutu Küçültücü

Büyük JPEG ve PNG resim dosyalarını otomatik olarak 1 MB'ın altına düşüren Python programı.

## Neden Oluşturuldu?

Bu proje GitHub profil fotoğrafları gibi 1 MB boyut sınırı olan platformlar için resim dosyalarını hızlıca sıkıştırmak üzere geliştirilmiştir. Nano Banana ile oluşturulan 6-7 MB boyutundaki profil resimlerini GitHub'ın kabul ettiği boyuta düşürmek için ideal bir çözümdür.

## Özellikler

- **Desteklenen Formatlar:** JPEG (.jpg, .jpeg) ve PNG (.png)
- **Hedef Boyut:** Maksimum 1 MB
- **Kalite Koruması:** Kaliteyi olabildiğince koruyarak sıkıştırır
- **Akıllı Algoritma:** Kalite-tabanlı iteratif sıkıştırma

## Gereksinimler

- Python 3.7 veya üzeri
- Pillow kütüphanesi

## Kurulum

1. Bu klasöre gidin:
```bash
cd fotograf-boyutu-kucultucu
```

2. Gerekli kütüphaneyi yükleyin (eğer yüklü değilse):
```bash
pip install -r requirements.txt
```

## Kullanım

1. Sıkıştırmak istediğiniz resmi `input.jpg` veya `input.png` olarak kaydedin
2. Programı çalıştırın:
```bash
python compress_image.py
```

3. Sıkıştırılmış resim `image_compressed.jpg` olarak kaydedilecektir

## Çalışma Mantığı

1. Program `input.jpg`, `input.jpeg` veya `input.png` dosyasını arar
2. Dosya boyutunu kontrol eder:
   - **1 MB'dan küçükse:** Dosyayı olduğu gibi JPEG formatında kaydeder (işlem atlanır)
   - **1 MB'dan büyükse:** Kalite-tabanlı sıkıştırma yapar
3. PNG dosyaları otomatik olarak JPEG'e dönüştürülür
4. Çıktı her zaman `image_compressed.jpg` olarak kaydedilir

## Sıkıştırma Algoritması

- **Başlangıç Kalitesi:** 85 (iyi denge noktası)
- **Kalite Adımı:** 5 puan düşüş
- **Minimum Kalite:** 20 (kabul edilebilir minimum)
- **JPEG Optimizasyonu:** Ek boyut azaltma için optimize=True

Program, dosya boyutu 1 MB'ın altına düşene kadar kaliteyi kademeli olarak düşürür.

## Örnek Çıktı

### Başarılı Sıkıştırma
```
============================================================
RESİM SIKIŞTIRMA PROGRAMI
============================================================

Giriş dosyası bulundu: input.jpg
Orijinal boyut: 5.45 MB

İşleniyor...

Sıkıştırıldı: 5.45 MB -> 0.98 MB (%82.0 azalma)
Kalite ayarı: 75
Çıkış kaydedildi: image_compressed.jpg

============================================================
DURUM: BAŞARILI
============================================================
```

### Zaten Küçük Dosya
```
============================================================
RESİM SIKIŞTIRMA PROGRAMI
============================================================

Giriş dosyası bulundu: input.png
Orijinal boyut: 0.65 MB

İşleniyor...

Dosya zaten 1 MB'ın altında - işlem atlandı.
Çıkış kaydedildi: image_compressed.jpg

============================================================
DURUM: ATLANDI
============================================================
```

### Dosya Bulunamadı
```
============================================================
RESİM SIKIŞTIRMA PROGRAMI
============================================================

Hata: Giriş dosyası bulunamadı.
Lütfen program klasörüne 'input.jpg' veya 'input.png' yerleştirin.
```

## Notlar

- PNG dosyaları her zaman JPEG formatına dönüştürülür (daha iyi sıkıştırma)
- Şeffaf arka planlı PNG'ler beyaz arka plan ile kaydedilir
- Çok büyük dosyalar için bile minimum kalite (20) ile 1 MB'a yakın sonuçlar elde edilir
- Dosya isimleri sabit: `input.*` ve `image_compressed.jpg`

## Lisans

Bu proje açık kaynak yazılımdır, serbestçe kullanılabilir.
