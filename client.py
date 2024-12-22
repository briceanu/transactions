
import requests


# placing one order



# data = {
#         'user_email':'marinescu@gmail.com',
#         'product_id':'7ed251dd-5fb2-4c12-98e8-1ff891a9eeb1',
#         'number_of_items':2
#         }
   

# url='http://localhost:8000/api/order_products'


# res = requests.post(url=url,data=data)

# print(res.status_code)
# print(res.text)











data = {
        'user_email':'dumitrescu@gmail.com',
        'products':[
                # {'product_id':'bb12e082-a7fb-49c9-a9c4-1796f38cfaf3','number_of_items':2},
                {'product_id':'afa9d14e-2b73-4e20-942d-58e3993f8fdd','number_of_items':2},
                # {'product_id':'6162b522-caa7-4ce1-ab06-92729d00c393','number_of_items':1},
                # {'product_id':'3fdb51f7-1f46-4d44-9fd9-e50115c38ece','number_of_items':3}
                ],
        }

url='http://localhost:8000/api/place_orders'


res = requests.post(url=url,json=data)

print(res.status_code)
print(res.text)

 
# my_list=[2,5,8,34,78]
# my_secon_list= [12,34,65,87,23]


# new_list = [item *2 for item in zip(my_list,my_secon_list) ]

# print(new_list)