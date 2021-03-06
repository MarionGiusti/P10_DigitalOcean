"""
Define models to use in the database
"""
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Category model for the Category table in the database"""
    name = models.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        """Method to change the object name in QuerySet """
        return self.name

    class Meta:
        """Change model name in french"""
        verbose_name = "Catégorie"

class Product(models.Model):
    """Product model for the Product table in the database"""
    product_name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=300)
    categories = models.ManyToManyField(Category, related_name='products')
    code_prod = models.CharField(max_length=50, unique=True)
    brand_name = models.CharField(max_length=200)
    url = models.URLField()
    nova_gps = models.PositiveSmallIntegerField()
    nutri_grades = models.CharField(max_length=1)
    pnns_gps1 = models.CharField(max_length=200)
    pnns_gps2 = models.CharField(max_length=200)
    store_name = models.CharField(max_length=200)
    picture = models.URLField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    sugars_100g = models.FloatField()

    def __str__(self):
        """Method to change the object name in QuerySet """
        return self.product_name

    class Meta:
        """Change model name in french"""
        verbose_name = "Produit"

class FavoriteProduct(models.Model):
    """FavoriteProduct model for the FavoriteProduct table in the database"""
    product = models.ForeignKey(
        Product, related_name='chosen_product', on_delete=models.PROTECT
    )
    substitute = models.ForeignKey(
        Product, related_name='healthy_substitute', on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Change model name in french and define unique together constraint"""
        verbose_name = "Favoris"
        unique_together = [['product_id', 'substitute_id']]
