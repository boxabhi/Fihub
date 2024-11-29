import csv
from django.core.management.base import BaseCommand
from sales.models import Product, Customer, Order, Delivery, Platform, Category


class Command(BaseCommand):
    help = "Import data from a specified CSV file with platform-specific columns"

    def add_arguments(self, parser):
        # Add an argument for the file path
        parser.add_argument(
            "file_path",
            type=str,
            help="Path to the CSV file containing the data to be imported",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            # Open the file
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                

                platform_name = reader.fieldnames[-3]  # The last column name should be 'Platform'
                
                platform_column = "Platform"
                if platform_column not in reader.fieldnames:
                    self.stdout.write(self.style.ERROR(f"Missing 'Platform' column in the file."))
                    return
                
                platform_name = None
                for row in reader:
                    platform_name = row[platform_column]
                    break  # Just need to check the first row for platform info

                if not platform_name:
                    self.stdout.write(self.style.ERROR(f"Could not determine platform from the data."))
                    return
                

                # Define platform-specific expected columns
                platform_columns = {
                    "Amazon": [
                        "OrderID", "ProductID", "ProductName", "Category", "QuantitySold", "SellingPrice",
                        "DateOfSale", "CustomerID", "CustomerName", "ContactEmail", "PhoneNumber",
                        "DeliveryAddress", "DeliveryDate", "DeliveryStatus", "Platform", "PrimeDelivery", 
                        "WarehouseLocation",
                    ],
                    "Meesho": [
                        "OrderID", "ProductID", "ProductName", "Category", "QuantitySold", "SellingPrice",
                        "DateOfSale", "CustomerID", "CustomerName", "ContactEmail", "PhoneNumber",
                        "DeliveryAddress", "DeliveryDate", "DeliveryStatus", "Platform", "ResellerName", 
                        "CommissionPercentage",
                    ],
                    "Flipkart": [
                        "OrderID", "ProductID", "ProductName", "Category", "QuantitySold", "SellingPrice",
                        "DateOfSale", "CustomerID", "CustomerName", "ContactEmail", "PhoneNumber",
                        "DeliveryAddress", "DeliveryDate", "DeliveryStatus", "Platform",
                          "CouponUsed", 
                        "ReturnWindow",
                    ],
                }

                # Check if the columns in the CSV file match the expected columns for the given platform

                if platform_name in platform_columns:
                    expected_headers = platform_columns[platform_name]
                else:
                    self.stdout.write(self.style.ERROR("Unsupported platform in the CSV file"))
                    return

                # Check if the CSV headers match the expected headers for the platform
                if reader.fieldnames != expected_headers:
                    self.stdout.write(
                        self.style.ERROR(
                            f"Incorrect headers in the file for platform {platform_name}! Expected headers are: {', '.join(expected_headers)}"
                        )
                    )
                    return

                # Process the file if headers are correct
                for row in reader:
                    try:
                        # Create or get the category
                        category, _ = Category.objects.get_or_create(name=row["Category"])

                        # Create or get the product
                        product, _ = Product.objects.get_or_create(
                            product_id=row["ProductID"],
                            defaults={"product_name": row["ProductName"], "category": category},
                        )

                        platform, _ = Platform.objects.get_or_create(
                            platform_name=row["Platform"],
                        )

                        # Create or get the customer
                        customer, _ = Customer.objects.get_or_create(
                            customer_id=row["CustomerID"],
                            defaults={
                                "customer_name": row["CustomerName"],
                                "contact_email": row["ContactEmail"],
                                "phone_number": row["PhoneNumber"],
                            },
                        )

                        # Create the order
                        order_data = {
                            "order_id": row["OrderID"],
                            "product": product,
                            "customer": customer,
                            "quantity_sold": int(row["QuantitySold"]),
                            "selling_price": float(row["SellingPrice"]),
                            "total_sale_value": float(row["QuantitySold"]) * float(row["SellingPrice"]),
                            "date_of_sale": row["DateOfSale"],
                            "platform" : platform
                        }

                        # Add platform-specific fields to order
                        if platform_name == "Meesho":
                            order_data["reseller_name"] = row["ResellerName"]
                            order_data["commission_percentage"] = float(row["CommissionPercentage"])
                        elif platform_name == "Amazon":
                            order_data["prime_delivery"] = row["PrimeDelivery"]
                            order_data["warehouse_location"] = row["WarehouseLocation"]
                        elif platform_name == "Flipkart":
                            order_data["coupon_used"] = row["CouponUsed"]
                            order_data["return_window"] = row["ReturnWindow"]

                        # Create the order

                        order,_ = Order.objects.get_or_create(**order_data)

                        # Create the delivery
                        Delivery.objects.get_or_create(
                            order=order,
                            delivery_address=row["DeliveryAddress"],
                            delivery_date=row["DeliveryDate"],
                            delivery_status=row["DeliveryStatus"],
                        )

                        # Create or get the platform

                    except Exception as e:
                        print(e)
                        continue

                self.stdout.write(self.style.SUCCESS("Data imported successfully!"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"The file '{file_path}' was not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
