import csv
import stripe
import mysql.connector


stripe.api_key = 'sk_test_51Os180JDw3WYrLo5uSYV1Wgv6UfqWv1wiEoKMyVnYjOFjF3UcyaxMQE5Xya0qfmyGkhfx4GafZITxtP1VVw9G5Xt00C0OEUdxM'


connection = mysql.connector.connect(
    host='132.145.18.222',
    user='sb2050',
    password='wnd4VKSANY3',
    database='sb2050'
)

count  = 0


csv_file = open('product_price_details.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product ID', 'Product Name', 'Description', 'Price ID', 'Retail Price'])

try:
    with connection.cursor() as cursor:

        sql = "SELECT * FROM sales_item"
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            product_name = row[1]
            description = row[5]

            if len(description) > 200:
                description = description[:200]

            retail_price = float(row[3])


            product = stripe.Product.create(
                name=product_name,
                description=description,
            )


            price = stripe.Price.create(
                unit_amount=int((retail_price * 0.009) + 2),
                currency='gbp',
                product=product.id,
            )


            csv_writer.writerow([product.id, product_name, description, price.id, int((retail_price * 0.009) + 2)])

            count += 1

            print("\nProduct and price registered successfully for", count, "products.\n")

    print("All products and prices registered successfully.")

except Exception as e:
    print("An error occurred:", str(e))

finally:
    connection.close()
    csv_file.close()
