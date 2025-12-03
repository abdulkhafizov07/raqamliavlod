import zipfile
import os
from pathlib import Path

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from kontest.models import Test, Masala  # <-- to‘g‘ri app nomini yozing


def load_tests_from_zip(zip_path, masala_id, target_folder="extracted"):
    os.makedirs(target_folder, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()

        in_files = sorted([f for f in file_list if f.endswith('.in')])
        out_files = sorted([f for f in file_list if f.endswith('.out')])

        print(f"Topildi: {len(in_files)} ta .in fayl, {len(out_files)} ta .out fayl")

        masala = Masala.objects.get(id=masala_id)

        created_count = 0

        for in_file in in_files:
            base = in_file.replace('.in', '')     # 010.in → 010
            out_file = f"{base}.out"

            if out_file not in out_files:
                print(f"⚠️ Juft topilmadi: {in_file} -> {out_file}")
                continue

            # ichidan content o‘qish
            in_path = zip_ref.extract(in_file, target_folder)
            out_path = zip_ref.extract(out_file, target_folder)

            with open(in_path, 'r', encoding='utf-8') as f:
                input_data = f.read().strip()

            with open(out_path, 'r', encoding='utf-8') as f:
                output_data = f.read().strip()

            # Django'ga saqlash
            Test.objects.create(
                masala=masala,
                kirish=input_data,
                output=output_data,
                hidden=True
            )

            created_count += 1
            print(f"✓ Yaratildi: {base} -> Test object")

        print(f"\nJAMI {created_count} TA TEST QO‘SHILDI.")
