"""
Resim Sıkıştırma Programı
Bu program büyük JPEG ve PNG dosyalarını 1 MB'ın altına düşürür.
Giriş: input.jpg veya input.png
Çıkış: image_compressed.jpg (her zaman JPEG)
"""

import os
import sys
from io import BytesIO
from PIL import Image


def find_input_file():
    """
    Mevcut klasörde input.jpg, input.jpeg veya input.png dosyasını arar.

    Returns:
        str: Bulunan dosya yolu veya None
    """
    # Desteklenen dosya uzantıları
    extensions = ['.jpg', '.jpeg', '.png']

    for ext in extensions:
        filename = f'input{ext}'
        if os.path.exists(filename):
            return filename

    return None


def get_file_size_mb(filepath):
    """
    Dosya boyutunu MB cinsinden döndürür.

    Args:
        filepath (str): Dosya yolu

    Returns:
        float: Dosya boyutu (MB)
    """
    size_bytes = os.path.getsize(filepath)
    size_mb = size_bytes / (1024 * 1024)
    return size_mb


def compress_image(input_path, output_path):
    """
    Resmi 1 MB'ın altına düşürecek şekilde sıkıştırır.

    Args:
        input_path (str): Giriş dosyası yolu
        output_path (str): Çıkış dosyası yolu

    Returns:
        dict: Sonuç bilgileri (success, message, original_size, final_size, quality)
    """
    try:
        # Resmi yükle
        image = Image.open(input_path)

        # Orijinal dosya boyutunu kontrol et
        original_size_mb = get_file_size_mb(input_path)

        # Eğer dosya zaten 1 MB'ın altındaysa
        if original_size_mb < 1.0:
            # PNG ise JPEG'e dönüştür, değilse direkt kopyala
            if image.mode in ['RGBA', 'LA', 'P']:
                # RGBA veya LA modundaysa RGB'ye dönüştür
                if image.mode == 'P':
                    image = image.convert('RGBA')
                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[-1] if image.mode in ['RGBA', 'LA'] else None)
                rgb_image.save(output_path, 'JPEG', quality=95, optimize=True)
            elif image.mode != 'RGB':
                image.convert('RGB').save(output_path, 'JPEG', quality=95, optimize=True)
            else:
                image.save(output_path, 'JPEG', quality=95, optimize=True)

            final_size_mb = get_file_size_mb(output_path)
            return {
                'success': True,
                'skipped': True,
                'message': f'Dosya zaten 1 MB\'ın altında - işlem atlandı.',
                'original_size': original_size_mb,
                'final_size': final_size_mb,
                'quality': 95
            }

        # PNG veya RGBA modundaysa RGB'ye dönüştür
        if image.mode in ['RGBA', 'LA', 'P']:
            if image.mode == 'P':
                image = image.convert('RGBA')
            # Beyaz bir arka plan oluştur ve resmi üstüne yapıştır
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode in ['RGBA', 'LA']:
                rgb_image.paste(image, mask=image.split()[-1])
            else:
                rgb_image.paste(image)
            image = rgb_image
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # Kalite iterasyonu
        quality = 85
        min_quality = 20
        quality_step = 5
        max_iterations = 20
        target_size_mb = 1.0

        for iteration in range(max_iterations):
            # Resmi belleğe kaydet ve boyutunu kontrol et
            buffer = BytesIO()
            image.save(buffer, format='JPEG', quality=quality, optimize=True)
            size_mb = len(buffer.getvalue()) / (1024 * 1024)

            # Hedef boyuta ulaştık mı?
            if size_mb < target_size_mb:
                # Dosyaya kaydet
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())

                reduction_percent = ((original_size_mb - size_mb) / original_size_mb) * 100
                return {
                    'success': True,
                    'skipped': False,
                    'message': f'Sıkıştırıldı: {original_size_mb:.2f} MB -> {size_mb:.2f} MB (%{reduction_percent:.1f} azalma)',
                    'original_size': original_size_mb,
                    'final_size': size_mb,
                    'quality': quality
                }

            # Kaliteyi düşür
            quality -= quality_step

            # Minimum kaliteye ulaştık mı?
            if quality < min_quality:
                quality = min_quality
                buffer = BytesIO()
                image.save(buffer, format='JPEG', quality=quality, optimize=True)
                size_mb = len(buffer.getvalue()) / (1024 * 1024)

                # Dosyaya kaydet
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())

                reduction_percent = ((original_size_mb - size_mb) / original_size_mb) * 100
                return {
                    'success': True,
                    'skipped': False,
                    'message': f'Minimum kaliteye düşürüldü: {original_size_mb:.2f} MB -> {size_mb:.2f} MB (%{reduction_percent:.1f} azalma)',
                    'original_size': original_size_mb,
                    'final_size': size_mb,
                    'quality': quality
                }

        # Buraya normalde ulaşılmamalı
        return {
            'success': False,
            'message': 'Resim sıkıştırılamadı (maksimum iterasyon sayısına ulaşıldı)',
            'original_size': original_size_mb,
            'final_size': None,
            'quality': None
        }

    except Exception as e:
        return {
            'success': False,
            'message': f'Hata: {str(e)}',
            'original_size': None,
            'final_size': None,
            'quality': None
        }


def main():
    """
    Ana program akışı.
    """
    print("=" * 60)
    print("RESİM SIKIŞTIRMA PROGRAMI")
    print("=" * 60)
    print()

    # Giriş dosyasını bul
    input_file = find_input_file()

    if input_file is None:
        print("Hata: Giriş dosyası bulunamadı.")
        print("Lütfen program klasörüne 'input.jpg' veya 'input.png' yerleştirin.")
        print()
        return 1

    print(f"Giriş dosyası bulundu: {input_file}")

    # Orijinal dosya boyutunu göster
    try:
        original_size = get_file_size_mb(input_file)
        print(f"Orijinal boyut: {original_size:.2f} MB")
        print()
    except Exception as e:
        print(f"Hata: Dosya boyutu okunamadı: {e}")
        print()
        return 2

    # Çıkış dosya adı
    output_file = 'image_compressed.jpg'

    # Sıkıştırma işlemi
    print("İşleniyor...")
    print()

    result = compress_image(input_file, output_file)

    if result['success']:
        if result.get('skipped', False):
            print(f"{result['message']}")
        else:
            print(f"{result['message']}")
            print(f"Kalite ayarı: {result['quality']}")
        print(f"Çıkış kaydedildi: {output_file}")
        print()
        print("=" * 60)
        if result.get('skipped', False):
            print("DURUM: ATLANDI")
        else:
            print("DURUM: BAŞARILI")
        print("=" * 60)
        return 0
    else:
        print(f"{result['message']}")
        print()
        print("=" * 60)
        print("DURUM: BAŞARISIZ")
        print("=" * 60)
        return 2


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
