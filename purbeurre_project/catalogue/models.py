from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=200, unique=True, null=False)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Catégorie"

class Product(models.Model):
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
		return self.product_name

	class Meta:
		verbose_name = "Produit"

class FavoriteProduct(models.Model):
	product_id = models.ForeignKey(Product, related_name='chosen_product', on_delete=models.PROTECT)
	substitute_id = models.ForeignKey(Product, related_name='healthy_substitute', on_delete=models.PROTECT)
	custumer_id = models.ForeignKey(User, on_delete=models.CASCADE)


	class Meta:
		verbose_name = "Favoris"
		unique_together = [['product_id', 'substitute_id']]