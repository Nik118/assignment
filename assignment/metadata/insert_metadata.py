import os
import sys
import csv

DJANGO_PATH = '/Users/nikhil/Documents/repos/test/assignment'
sys.path.append(DJANGO_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')
import django
django.setup()

from metadata.models import Location, Department, Category, SubCategory


file_path = os.getcwd() + '/metadata.csv'
with open(file_path) as f:
    reader = csv.DictReader(f)

    for item in reader:
        location_obj, success = Location.objects.get_or_create(name=item['Location'].strip())
        department_obj, success = Department.objects.get_or_create(name=item['Department'].strip(),
                                                                location=location_obj
                                                                )
        category_obj, success = Category.objects.get_or_create(name=item['Category'].strip(),
                                                              department=department_obj
                                                              )
        subcategory_obj, success = SubCategory.objects.get_or_create(name=item['SubCategory'].strip(),
                                                                    category=category_obj
                                                                    )

print('Metadata insertion is completed')
