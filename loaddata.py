import os
import django
import json

# Django settings ni ulash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from app_name.models import Masala, Test  # o'zingizning app nomi bilan almashtiring

# JSON faylni ochib o'qish
with open('masalalar.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ma'lumotlarni qo'shish
for item in data:
    model = item['model'].split('.')[-1]
    pk = item['pk']
    fields = item['fields']
    
    if model == "Masala":
        Masala.objects.create(defaults=fields)
    elif model == "Test":
        # Test uchun Masala foreign key ni alohida olish kerak
        masala_id = fields.pop('masala')
        test_fields = fields
        test_fields['masala_id'] = masala_id
        Test.objects.create(defaults=test_fields)

print("Ma'lumotlar qo'shildi!")
