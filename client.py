
import requests


# data = {'new_balance':2420,
#         'user_email':'marinescu@gmail.com'}
# url = 'http://localhost:8000/api/learn'

# res = requests.put(url=url,data=data)
# print(res.status_code)
# print(res.text)


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
        'user_email':'teodorbriceanu@gmail.com',
        'products':[
                {'product_id':'10ddfa05-ba19-419a-94fe-94f9088f07a6','number_of_items':3},
                {'product_id':'09122b40-7757-452d-98bb-c767a82d45e6','number_of_items':2},
                # {'product_id':'5793488e-9c08-4204-8a8f-c658c5c5af50','number_of_items':1},
                # {'product_id':'0c0e9010-b5a9-4373-9800-3fe5173b9048','number_of_items':3}
                ],
        }

url='http://localhost:8000/api/place_orders'


res = requests.post(url=url,json=data)

print(res.status_code)
print(res.text)

 
 