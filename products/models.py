from django.db import models
import uuid
# Create your models here.


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    product_name = models.CharField(max_length=100,default='' ,verbose_name='name')
    description = models.TextField(max_length=1000,default='')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images',null=True)
    number_in_stock = models.PositiveSmallIntegerField(default=0, verbose_name='number of items')

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'
        ordering = ['product_name']

