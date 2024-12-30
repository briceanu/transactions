from .models import Order
from .serializers import OrderSerializer
from rest_framework import generics
from products.models import Product
from user.models import User
from django.db import transaction
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework import mixins
from decimal import Decimal
import httpx
from adrf.views import APIView as adrfView
import requests
from django.core.mail import send_mail
from django.conf import settings
from transactions.tasks import send_client_email
from products.serializers import ProductSerializer
from products.models import Product

 
# from adrf.views import APIView
class PlaceOrderAPI(generics.CreateAPIView, mixins.CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# buying only one product
    def post(self,request,*args,**kwargs):
        # we are extracting the data from the request body
        number_of_items = request.data.get('number_of_items')
        user_email = request.data.get('user_email')
        product_id = request.data.get('product_id')
        # we are checking to see if all the data is provided in the request body
        if number_of_items is None or user_email is None or product_id is None:
            return Response({'error':'must provide number_of_items, user_email and product_id'},status=status.HTTP_400_BAD_REQUEST)
        # we are validating the number of items to be an integer
        try:
            number_of_items = int(number_of_items)
        except ValueError:
            return Response({'error':'number or items must be a valid number'},status=status.HTTP_400_BAD_REQUEST)

        # we are starting the operations in the transaction
        with transaction.atomic():
            # we check to see if the products exists in the database
            try:
                product_queryset = Product.objects.get(product_id=product_id)
            except Product.DoesNotExist:
                # we can use raise a NotFound error from rest_framework or we return a 400 Response
                # return Response({'error':f'no product with the id {product_id}'},status=status.HTTP_400_BAD_REQUEST)
                raise NotFound(detail=f'no product with the id {product_id} found.')
            # if there are no more products we throw an error
            if product_queryset.number_in_stock == 0:
                return Response(
            {'error':f'product {product_queryset.product_name} is not avaliable in the stock anymore.'},
            status=status.HTTP_400_BAD_REQUEST
            )
            # we calculate the total amount of the bought products
            total_purchase = number_of_items * product_queryset.price
            # if the number of products in the dbis less than the number of products we throw an error
            if product_queryset.number_in_stock < number_of_items:
                return Response(
            {'error': f'only {product_queryset.number_in_stock} item{"s" if product_queryset.number_in_stock > 1 else ""} left'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # remove the sold items form the stock
            product_queryset.number_in_stock -= number_of_items
            # save change in the db
            product_queryset.save()
            # we get the user who made the purchase
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                # if user does not exist throw an NotFound error
                raise NotFound(detail=f'No user with the email {user_email} found')
            #  throw an error if the balance is to small   
            if user.balance < total_purchase:
                return Response(
            {'error':'not sufficient funds to make the purchase'}
            ,status=status.HTTP_400_BAD_REQUEST) 
            # we are updating the user balance
            user.balance -=  total_purchase
            # we save in the db the new value
            user.save()
            # return a dictionary with the new data
            data  = {
                'success':'your purchase has been confirmed',
                'product':product_queryset.product_name,
                     'items purchased': number_of_items,
                     'total payment':total_purchase,
                'nice':f'thank you for the purchase mr {user.username}'
                     }

        return Response(data,status=status.HTTP_200_OK)



# client orders many products
class PlaceOrderProductsAPI(generics.CreateAPIView, mixins.CreateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Buying many products
    def post(self, request, *args, **kwargs):
        # Extract the data from the request body
        products = request.data.get('products')
        user_email = request.data.get('user_email')
        # Extract product_id from the request
        products_id = [product['product_id'] for product in products]
        # get all the number of items
        bought_items = [product['number_of_items'] for product in products]
        
        # we validate the number_of_items to be an integer
        for item in bought_items:
            if not isinstance(item,int):
                try:
                    int(item)
                except (ValueError,TypeError):
                    return Response({'error':'number_of_items must be a valid integer'},status=status.HTTP_400_BAD_REQUEST)
        # if the client does not provide products we throw an 400 bad request
        if not products:
            return Response({'error': 'No products provided'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            # we filter for the products the client provided
            existing_products = Product.objects.filter(product_id__in=products_id).values_list('product_id', flat=True).order_by()
            existing_product_ids = {str(product_id) for product_id in existing_products}  
            not_found_products = [product_id for product_id in products_id if product_id not in existing_product_ids]
            # If the client provides product_ids that aren't in the db we throw an 404  
            if not_found_products:
                return Response(
                    {'error': f"Product(s) with the ID(s) {', '.join(not_found_products)} not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            selected_products = Product.objects.filter(product_id__in=existing_product_ids)
            #  total amount the client has to pay
            total_sum = Decimal('0.00')
            purchased_items=[]
            # using the zip() function the queryset we check to see how many items are in the stock 
            for item, number_of_items in zip(selected_products, bought_items):
                if item.number_in_stock == 0:
                    return Response({'error':f"Sorry, the {item.product_name} product is not in the stock at the moment."}
                        ,status=status.HTTP_404_NOT_FOUND)
                if item.number_in_stock < number_of_items:
                    return Response(
                        {'error': f"Sorry, the product {item.product_name} has only {item.number_in_stock} item{'s' if item.number_in_stock > 1 else ''} left in stock."}
                    )

                # calculating the total amount the client has to pay
                price = Decimal(item.price)  * number_of_items
                total_sum+= price
                # append the purchased items to the purchased_itmes
                purchased_items.append( {'item':item.product_name, 'number_of_items':number_of_items, 'price':item.price})
                # remove the bought items from the db
                item.number_in_stock -= number_of_items
                item.save()
            # we find the user in the db 
            try:
                user = User.objects.get(email=user_email)
            except User.DoesNotExist:
                raise NotFound(detail=f'no user with the email {user_email} found.')
            # if the user does not have enough money we throw a 400 bad request error
            if user.balance < total_sum:
                return Response({'error':'insufficient funds to make the purchase'},status=status.HTTP_400_BAD_REQUEST)
            # withdraw the amount from the account
            user.balance -= Decimal(total_sum)
            user.save()
            # we are creating a new order   
            Order.objects.create(
                user=user,
                number_of_items=number_of_items
                )

            subject = 'Details of your order'
            message = f"Items purchased: {purchased_items}, Total Amount: {total_sum}"
   
            data = (
                "Your order has been placed successfully."
                "You will receive an email with the details of your purchase."
                "On behalf of our team, we wish you a nice day."
            )
            try:
            # we are importing the shared task from tasks.py to send the confirmation email
                send_client_email(subject,message,user.email)
            except Exception as e:
                return Response({'error':f'Error sending email: {e}'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # If all products are valid, proceed with the request
            return Response(data, status=status.HTTP_200_OK)

# subject message address
# testing 
# we create two views for sending emails
# one asynchronous and one synchronous




 
class LearnAPI(generics.ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

 