import requests
import pandas as pd
from pathlib import Path
import re

""" 
cd "Projects\\Mini Tools\\Shopfiy Product Scraper"
"""



def check_for_values(value):
    if value:
        return value
    else:
        return None




url = 'https://us.hismileteeth.com'


input_folder = Path("input")
input_folder.mkdir(exist_ok=True)

output_folder = Path("output")
output_folder.mkdir(exist_ok=True)


r = requests.get(url + "/products.json")
r.raise_for_status()


data = r.json()
# Debugging
print("-----------------")
print("URL: ", r.url)
print("Status Code: ", r.status_code)
print("Headers: ",r.headers["Content-Type"])
print("Text:\n", r.text[:100])
print()
print("Chat's request:")
print("Type:", type(data))
print("Keys: ", data.keys())
print("Type['products']: ", type(data['products']))
print(f"Number of items: {len(data['products'])}")
print("data['prodcuts'][0].keys():\n", data['products'][0].keys())
print()
print(data['products'][0])
print("-----------------")
###



# Getting the title and other attributes
print("-----------------")
print("Title: ", data['products'][0]['title'])
print("Vendor: ", data['products'][0]['vendor'])
print("Handle: ", data['products'][0]['handle'])
print("Price: ", data['products'][0]['variants'][0]['price'])
print("Src: ", data['products'][0]['images'][0]['src'])
print("SKU: ", data['products'][0]['variants'][0]['sku'])
print("-----------------")


# Loop it up
print("---- LOOP -----")
for product in data['products']:
    print(f"""
Title: \t{product['title']}
Vendor: {product['vendor']}
Handle: {product['handle']}
Price: \t{product['variants'][0]['price']}
Src: \t{product['images'][0]['src']}
SKU: \t{product['variants'][0]['sku']}
""")
print("-----------------")




attributes = [
    'title',
    'vendor',
    'handle',
    'variants',
    'images',
    'price',
    'src',
    'sku',
]



# Data to list
print("--------------")
products = []
for product in data['products']:
    product_data = {
        'title': {product[check_for_values('title')]},
        'vendor': {product[check_for_values('vendor')]},
        'handle': {product[check_for_values('handle')]},
        'price': {product[check_for_values('variants')][0][check_for_values('price')]},
        'src': {product[check_for_values('images')][0][check_for_values('src')]},
        'sku': {product[check_for_values('variants')][0][check_for_values('sku')]},
    }
    products.append(product_data)
print("------ Saved as List! --------")
print()
print(products[:3])



# Puting it into a pandas Dataframe
print("\n---------- DF Head ----------")
df = pd.DataFrame(products)
print(df.head())




# Preparing the filename to save
vendor = products[0]['vendor']
vendor = str(vendor)
safe_vendor = re.sub(r'[^\w\-]', '_', vendor)
filename = f"{safe_vendor}.csv"

# Save to CSV
df.to_csv(output_folder / filename)
print("---------- DF Saved to CSV! ----------")




###############
