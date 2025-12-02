import zipfile
import os
from pathlib import Path

def read_zip_files(zip_path, target_folder="extracted"):
    """
    ZIP faylini ochib, ichidagi barcha .in fayllarini o'qish
    
    Args:
        zip_path: ZIP fayl yo'li
        target_folder: ZIPdan chiqarilgan fayllar saqlanadigan papka
    
    Returns:
        dict: File nomi -> kontent
    """
    extracted_data = {}
    
    # Target folder'ni yaratish
    os.makedirs(target_folder, exist_ok=True)
    
    try:
        # ZIP faylini ochish
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Barcha fayllar ro'yxati
            file_list = zip_ref.namelist()
            print(f"ZIP ichida {len(file_list)} ta fayl topildi")
            
            # Faqat .in fayllarini olish
            in_files = [f for f in file_list if f.endswith('.in')]
            print(f"{len(in_files)} ta .in fayli topildi")
            
            # Har bir .in faylini o'qish
            for in_file in in_files:
                # Faylni extract qilish
                extracted_path = zip_ref.extract(in_file, target_folder)
                
                # Faylni o'qish
                with open(extracted_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    
                # Ma'lumotlarni dictionary'ga saqlash
                extracted_data[in_file] = content
                
                # Fayl nomi va kontentini chiqarish
                print(f"\n[file name]: {in_file}")
                print(f"[file content begin]")
                print(content)
                print(f"[file content end]")
                
                # Extract qilingan faylni o'chirish (agar kerak bo'lmasa)
                # os.remove(extracted_path)
                
        return extracted_data
        
    except zipfile.BadZipFile:
        print(f"Xatolik: {zip_path} - noto'g'ri ZIP fayl")
        return None
    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")
        return None

# Foydalanish misoli:
if __name__ == "__main__":
    # ZIP fayl yo'li
    zip_file_path = "~/Downloads/iMe Desktop/A.zip"  # O'zingizning ZIP faylingiz yo'li
    
    # Agar fayl mavjud bo'lsa
    if os.path.exists(zip_file_path):
        results = read_zip_files(zip_file_path)
        
        if results:
            print(f"\n\nJami {len(results)} ta .in fayli muvaffaqiyatli o'qildi")
            
            # Natijalarni saqlash
            for filename, content in results.items():
                print(f"\n{filename}: {content[:50]}...")  # Faqat 50 ta belgi
    else:
        print(f"Xatolik: {zip_file_path} fayli topilmadi")