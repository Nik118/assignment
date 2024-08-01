import os
import sys
import csv

DJANGO_PATH = '/Users/nikhil/Documents/repos/test/assignment'
sys.path.append(DJANGO_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')
import django
django.setup()

from metadata.models import Location, Department, Category, SubCategory, SKU


file_path = os.getcwd() + '/sku.csv'
with open(file_path) as f:
    reader = csv.DictReader(f)

    for item in reader:
        print(item)
        location_obj = Location.objects.get(name=item['LOCATION'].strip())
        department_obj = Department.objects.get(name=item['DEPARTMENT'].strip(),
                                                location=location_obj
                                                )
        category_obj = Category.objects.get(name=item['CATEGORY'].strip(),
                                            department=department_obj
                                            )
        sub_category_obj = SubCategory.objects.get(name=item['SUBCATEGORY'].strip(),
                                                  category=category_obj
                                                  )
        sku_obj, success = SKU.objects.get_or_create(name=item['NAME'].strip(),
                                    location=location_obj,
                                    department=department_obj,
                                    category=category_obj,
                                    sub_category=sub_category_obj
                                    )

print('SKU insertion is completed')
