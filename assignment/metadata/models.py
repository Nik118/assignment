from django.db import models

# Create your models here.


class Location(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Category(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'SubCategories'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class SKU(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name