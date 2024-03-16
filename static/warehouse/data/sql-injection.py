import csv
import mysql.connector

connection = mysql.connector.connect(
    host="132.145.18.222",
    user="sb2050",
    password="wnd4VKSANY3",
    database="sb2050",
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

total_count = 37606
count = 0

prod_id = 0

with open('flipkart-prod.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    cursor = connection.cursor()

    for row in reader:
        prod_id += 1
        name = row['product_name']
        description = row['description']
        category_tree = row['product_category_tree']
        image = row['image']
        retail_price = row['retail_price']
        brand = row['brand']

        try:
            query = "INSERT INTO sales_item (id, name, category_tree, retail_price, image, description, brand) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (prod_id, name, category_tree, retail_price, image, description, brand))

        except mysql.connector.Error as err:
            print("Error:", err)
            continue
        
        if count % 500 == 0:
            print("\nCOMMIT MADE.\n")
            connection.commit()

        count += 1
        total_count -= 1

        print(f"Inserted {count} of 37606. Remaining: {total_count}\n\n")

    connection.commit()
    cursor.close()

connection.close()
