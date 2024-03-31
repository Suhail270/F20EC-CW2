import csv
import mysql.connector
import requests
import pandas as pd
connection = mysql.connector.connect(
    host="132.145.18.222",
    user="mm2107",
    password="wnd4VKSANY3",
    database="mm2107",
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

prod_id = 0
add_count = 0
unique_cat_dict = dict()
with open(r'static\warehouse\data\flipkart-prod.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    cursor = connection.cursor()

    for row in reader:
        prod_id += 1
        name = row['product_name']
        description = row['description']
        category_name = row['product_category_tree']
        image = row['image']
        retail_price = (int(row['retail_price']) * 0.0095) + 2
        brand = row['brand']
        
        if not connection.is_connected():
            connection.disconnect()
            connection = mysql.connector.connect(
                host="132.145.18.222",
                user="mm2107",
                password="wnd4VKSANY3",
                database="mm2107",
                charset='utf8mb4',
                collation='utf8mb4_unicode_ci'
            )
        response = requests.get(image)
        if unique_cat_dict.keys().__contains__(category_name):
            cnt = unique_cat_dict.get(category_name)
            if cnt == 20:
                print("continuing")
                continue
            else:
                unique_cat_dict.update({str(category_name): cnt+1})
        else:
            print("added new cat!")
            unique_cat_dict[str(category_name)] = 1

        if response.status_code != 404:
            try:
                cursor.execute("SELECT id FROM sales_category WHERE name = %s", (category_name,))
                category_row = cursor.fetchone()
                if category_row:
                    category_id = category_row[0]
                else:
                    cursor.execute("INSERT INTO sales_category (name) VALUES (%s)", (category_name,))
                    category_id = cursor.lastrowid

                cursor.execute("INSERT INTO sales_item (id, name, category_id, retail_price, image, description, brand) VALUES (%s, %s, %s, %s, %s, %s, %s)", (prod_id, name, category_id, retail_price, image, description, brand))
                connection.commit()
                
                if prod_id % 100 == 0:
                    print(f"Inserted item with name: {name}")
                    print(unique_cat_dict)
                # if len(unique_cat_dict.keys()) == 166:
                #     break
                print("num prods:",prod_id)
            except Exception as e:
                print(f"Error inserting item with name: {name}. Error: {e}")

    cursor.close()
# print(len(unique_cat))
connection.close()
