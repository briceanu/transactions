from django.db import models
import uuid


class Order(models.Model):
    # product user data_purchased  number_of_items

    order_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='orders')
    date_of_purchase = models.DateTimeField(auto_now_add=True)
    number_of_items = models.PositiveSmallIntegerField(default=1)


    def __str__(self):
        return self.user.username


