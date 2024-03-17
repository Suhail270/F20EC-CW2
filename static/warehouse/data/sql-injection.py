import csv
import mysql.connector
import requests

connection = mysql.connector.connect(
    host="132.145.18.222",
    user="vjv2000",
    password="wnd4VKSANY3",
    database="vjv2000",
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

prod_id = 0


with open('flipkart-prod.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    cursor = connection.cursor()

    for row in reader:
        prod_id += 1
        name = row['product_name']
        description = row['description']
        category_name = row['product_category_tree']
        image = row['image']
        retail_price = row['retail_price']
        brand = row['brand']

        response = requests.get(image)

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
            except Exception as e:
                print(f"Error inserting item with name: {name}. Error: {e}")

    cursor.close()

connection.close()
