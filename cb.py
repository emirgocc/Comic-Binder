import os
import zipfile
import rarfile
from PIL import Image
from tkinter import Tk, filedialog
import shutil

def select_comic_archives():
    Tk().withdraw()
    return filedialog.askopenfilenames(
        title="Birleştirilecek .cbz/.cbr dosyalarını sırayla seçin",
        filetypes=[("Comic Archives", "*.cbz *.cbr")]
    )

def select_cover_image():
    Tk().withdraw()
    return filedialog.askopenfilename(
        title="Kapak olarak eklenecek resmi seçin",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )

def extract_cbz(cbz_path, extract_to):
    with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def extract_cbr(cbr_path, extract_to):
    try:
        with rarfile.RarFile(cbr_path, 'r') as rar_ref:
            for file_info in rar_ref.infolist():
                try:
                    rar_ref.extract(file_info, extract_to)
                except rarfile.BadRarFile as e:
                    print(f"Uyarı: {file_info.filename} dosyası bozuk - atlanıyor: {str(e)}")
                    continue
                except Exception as e:
                    print(f"Uyarı: {file_info.filename} dosyası işlenirken hata oluştu: {str(e)}")
                    continue
    except Exception as e:
        raise Exception(f"CBR dosyası açılırken hata oluştu: {str(e)}")

def extract_archive(path, extract_to):
    if path.lower().endswith('.cbz'):
        extract_cbz(path, extract_to)
    elif path.lower().endswith('.cbr'):
        extract_cbr(path, extract_to)
    else:
        raise ValueError("Sadece .cbz veya .cbr dosyaları destekleniyor.")

def create_cbz_from_images(image_paths, output_path):
    with zipfile.ZipFile(output_path, 'w') as cbz:
        for i, image_path in enumerate(image_paths):
            try:
                ext = os.path.splitext(image_path)[-1]
                arcname = f"{i:04}{ext}"
                cbz.write(image_path, arcname)
            except Exception as e:
                print(f"Uyarı: {image_path} dosyası işlenirken hata oluştu: {str(e)}")
                continue

def merge_comics(comic_files, cover_image_path, output_cbz):
    """
    Çizgi roman dosyalarını birleştirir ve yeni bir CBZ dosyası oluşturur.
    
    Args:
        comic_files (list): Birleştirilecek .cbz/.cbr dosyalarının yolları
        cover_image_path (str): Kapak resmi dosyasının yolu
        output_cbz (str): Çıktı CBZ dosyasının yolu
    
    Raises:
        Exception: Herhangi bir hata durumunda
    """
    temp_dir = "temp_comic_merge"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        all_images = []
        
        # Kapak resmini ekle
        try:
            all_images.append(cover_image_path)
        except Exception as e:
            print(f"Uyarı: Kapak resmi eklenirken hata oluştu: {str(e)}")

        # Dosyaları işle
        for idx, archive in enumerate(comic_files):
            try:
                extract_path = os.path.join(temp_dir, f"comic_{idx}")
                os.makedirs(extract_path, exist_ok=True)
                extract_archive(archive, extract_path)

                for root, _, files in os.walk(extract_path):
                    for file in sorted(files):
                        if file.lower().endswith((".jpg", ".jpeg", ".png")):
                            try:
                                file_path = os.path.join(root, file)
                                # Dosyanın geçerli bir resim olduğunu kontrol et
                                with Image.open(file_path) as img:
                                    img.verify()
                                all_images.append(file_path)
                            except Exception as e:
                                print(f"Uyarı: {file} dosyası işlenirken hata oluştu: {str(e)}")
                                continue
            except Exception as e:
                print(f"Uyarı: {archive} dosyası işlenirken hata oluştu: {str(e)}")
                continue

        if not all_images:
            raise ValueError("İşlenebilir resim dosyası bulunamadı!")

        create_cbz_from_images(all_images, output_cbz)

    finally:
        # Geçici dosyaları temizle
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    comic_files = select_comic_archives()
    cover_image = select_cover_image()
    output_file = filedialog.asksaveasfilename(
        title="Yeni CBZ dosyasının adı",
        defaultextension=".cbz",
        filetypes=[("CBZ files", "*.cbz")]
    )

    if comic_files and cover_image and output_file:
        merge_comics(comic_files, cover_image, output_file)
