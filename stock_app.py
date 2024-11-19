# file name: stock_app.py

from couchbase.cluster import Cluster
from couchbase.auth import PasswordAuthenticator
from couchbase.options import ClusterOptions
from couchbase.exceptions import CouchbaseException, DocumentNotFoundException
from datetime import timedelta
from stock_user import User # Import User class
from stock import Stock  # Import Stock Class
import traceback
from customer_functions import deposit_funds, withdraw_funds, buy_stock, sell_stock, view_portfolio

# Connection configuration
endpoint = "couchbases://cb.nnq3yiry4lf6y7e2.cloud.couchbase.com"  # Replace with your endpoint
username = "Admin"  # Username
password = "Password123!"  # Password
bucket_name = "Stocks"  # Stock bucket name
user_bucket_name = "User"  # User bucket name
portfolio_bucket_name = "Portfolios" # Portfolio bucket name
scope_name = "_default"  
collection_name = "_default" 

# Connect options - authentication
auth = PasswordAuthenticator(username, password)
options = ClusterOptions(auth)
options.apply_profile("wan_development")

try:
    # Get a reference to the Couchbase cluster
    cluster = Cluster(endpoint, options)
    # Wait until the cluster is ready for use
    cluster.wait_until_ready(timedelta(seconds=5))
    print("Connected to Couchbase cluster successfully!")
except Exception as e:
    traceback.print_exc()

# Bucket connection
bucket = cluster.bucket(bucket_name)
user_bucket = cluster.bucket(user_bucket_name)  # Connect to the User bucket
portfolio_bucket = cluster.bucket(portfolio_bucket_name)  # Connect to the Portfolio bucket
stock_bucket = cluster.bucket(bucket_name)  # Connect to the Stock bucket (same bucket as `bucket_name`)

# Scope and collection setup for stocks
stock_scope = stock_bucket.scope(scope_name) if scope_name else stock_bucket.default_scope()
stock_collection = stock_scope.collection(collection_name) if collection_name else stock_bucket.default_collection()

# Scope and collection setup for users
user_scope = user_bucket.scope(scope_name) if scope_name else user_bucket.default_scope()
user_collection = user_scope.collection(collection_name) if collection_name else user_bucket.default_collection()

# Scope and collection setup for portfolios
portfolio_scope = portfolio_bucket.scope(scope_name) if scope_name else portfolio_bucket.default_scope()
portfolio_collection = portfolio_scope.collection(collection_name) if collection_name else portfolio_bucket.default_collection()

# Use user_collection and portfolio_collection for operations on User and Portfolio data.
print("Collection setup completed.")

# Function to retrieve stock info based on stock code and return a Stock object
def get_stock_info(stock_code):
    try:
        # Fetch the document based on the stock code
        result = stock_collection.get(f"stock_{stock_code}")
        stock_data = result.content_as[dict]

        # Create a Stock object from the retrieved data
        stock = Stock(
            stock_code=stock_data['stock_code'],
            stock_name=stock_data['stock_name'],
            price=stock_data['price'],
            high_price=stock_data['high_price'],
            low_price=stock_data['low_price'],
            quantity_available=stock_data['quantity_available']
        )
        
        return stock
    
    except DocumentNotFoundException:
        print(f"Stock with code '{stock_code}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving stock information: {e}")
        return None

# Admin function to update stock information
def update_stock():
    stock_code = input("Enter the stock code you want to update: ").strip()
    stock = get_stock_info(stock_code)
    
    if stock:
        print("Current stock information:")
        stock.display_stock_info()

        # Prompt admin for new price and quantity
        try:
            new_price = float(input(f"Enter the new price for {stock.stock_name} (current price: {stock.price}): ").strip())
            new_quantity = int(input(f"Enter the new quantity available for {stock.stock_name} (current quantity: {stock.quantity_available}): ").strip())

            # Update stock object with new values
            stock.price = new_price
            stock.quantity_available = new_quantity

            # Prepare the updated data
            updated_data = {
                'stock_code': stock.stock_code,
                'stock_name': stock.stock_name,
                'price': stock.price,
                'high_price': stock.high_price,
                'low_price': stock.low_price,
                'quantity_available': stock.quantity_available
            }

            # Update the document in Couchbase
            stock_collection.upsert(f"stock_{stock.stock_code}", updated_data)
            print("Stock information updated successfully!")
        except ValueError as e:
            print(f"Error with the input: {e}")
    else:
        print(f"Stock with code '{stock_code}' not found.")

# Function to add a new stock
def add_stock():
    try:
        stock_code = input("Enter new stock code: ").strip()
        stock_name = input("Enter stock name: ").strip()
        price = float(input("Enter stock price: ").strip())
        high_price = float(input("Enter high price: ").strip())
        low_price = float(input("Enter low price: ").strip())
        quantity_available = int(input("Enter quantity available: ").strip())

        # Create a Stock object
        stock = Stock(stock_code, stock_name, price, high_price, low_price, quantity_available)

        # Prepare the data to insert into Couchbase
        stock_data = {
            'stock_code': stock.stock_code,
            'stock_name': stock.stock_name,
            'price': stock.price,
            'high_price': stock.high_price,
            'low_price': stock.low_price,
            'quantity_available': stock.quantity_available
        }

        # Insert the stock into Couchbase
        stock_collection.upsert(f"stock_{stock_code}", stock_data)
        print(f"Stock '{stock_code}' added successfully!")
    
    except Exception as e:
        print(f"Error adding stock: {e}")

# Function to remove a stock
def remove_stock():
    try:
        stock_code = input("Enter the stock code you want to remove: ").strip()

        # Try to retrieve the stock to ensure it exists
        stock = get_stock_info(stock_code)
        
        if stock:
            # Remove the stock document from Couchbase
            stock_collection.remove(f"stock_{stock_code}")
            print(f"Stock '{stock_code}' removed successfully!")
        else:
            print(f"Stock with code '{stock_code}' not found.")
    
    except DocumentNotFoundException:
        print(f"Stock with code '{stock_code}' not found.")
    except Exception as e:
        print(f"Error removing stock: {e}")

# Admin menu for managing stock data
def admin_functions():
    while True:
        print("\nAdmin Menu:")
        print("1. Update Stock Information")
        print("2. Add New Stock")
        print("3. Remove Stock")
        print("4. Exit Admin Menu")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            update_stock()
        elif choice == '2':
            add_stock()  # Add new stock
        elif choice == '3':
            remove_stock()  # Remove existing stock
        elif choice == '4':
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

def customer_functions():
    print("Customer functions started.")
    while True:
        print("\nCustomer Menu:")
        print("1. View Stock Information")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Buy Stock")
        print("5. Sell Stock")
        print("6. View Portfolio")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            stock_code = input("Enter the stock code you want to search for: ").strip()
            stock = get_stock_info(stock_code)
            if stock:
                stock.display_stock_info()
            else:
                print(f"Stock with code '{stock_code}' not found.")

        elif choice == '2':
            user_id = input("Enter your user ID for deposit: ").strip()
            amount = float(input("Enter amount to deposit: ").strip())
            deposit_funds(user_id, amount, user_collection, portfolio_collection)

        elif choice == '3':
            user_id = input("Enter your user ID for withdrawal: ").strip()
            amount = float(input("Enter amount to withdraw: ").strip())
            withdraw_funds(user_id, amount, user_collection)

        elif choice == '4':
            user_id = input("Enter your user ID for buying stock: ").strip()
            stock_code = input("Enter stock code: ").strip()
            quantity = int(input("Enter quantity to buy: ").strip())
            buy_stock(user_id, stock_code, quantity, user_collection, stock_collection, portfolio_collection)

        elif choice == '5':
            user_id = input("Enter your user ID for selling stock: ").strip()
            stock_code = input("Enter stock code: ").strip()
            quantity = int(input("Enter quantity to sell: ").strip())
            sell_stock(user_id, stock_code, quantity, user_collection, stock_collection, portfolio_collection)

        elif choice == '6':
            user_id = input("Enter your user ID to view your portfolio: ").strip()
            view_portfolio(user_id, portfolio_collection)

        elif choice == '7':
            print("Exiting Customer Menu.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

def user_role(user):
    print(f"User role detected: {'Admin' if user.is_admin else 'Customer'}")
    user.display_user_info()  # Display user information
    if user.is_admin:
        print("Welcome, Admin!")
        admin_functions()  # Admin can update stock information
    else:
        print("Welcome, Customer!")
        customer_functions()

# Function to search for a user in the Couchbase User bucket
def find_user(user_id):
    try:
        # Retrieve the user data from Couchbase using user_collection
        result = user_collection.get(f"user_{user_id}")  # Get user document by user_id
        user_data = result.content_as[dict]  # Convert the result to a dictionary
        
        # Instantiate the User object with the necessary collections
        user = User(
            user_id=user_data['user_id'],
            user_email=user_data['user_email'],
            user_name=user_data['user_name'],
            is_admin=user_data['is_admin'],
            user_collection=user_collection,  # Pass the user collection
            portfolio_collection=portfolio_collection  # Pass the portfolio collection
        )
        
        return user

    except DocumentNotFoundException:
        print(f"User with ID '{user_id}' not found.")
        return None
    except Exception as e:
        print(f"Error retrieving user information: {e}")
        return None

# Function to create a new user and save to the User bucket
def create_user():
    # Collect user information
    user_id = input("Enter user ID: ")
    user_email = input("Enter user email: ")
    user_name = input("Enter user name: ")
    is_admin = input("Is the user an admin? (yes/no): ").lower() == "yes"

    try:
        # Create the User object
        user = User(
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
            is_admin=is_admin,
            user_collection=user_collection,  # Assume `user_collection` is defined
            portfolio_collection=portfolio_collection  # Assume `portfolio_collection` is defined
        )

        # Create the user document in the user collection
        user.create_user()

        # If the user is not an admin, create a portfolio for them
        if not is_admin:
            user.create_portfolio()

        print(f"User {user_name} with ID {user_id} created successfully.")

        return user  # Optionally return the user object

    except Exception as e:
        print(f"Error creating user: {e}")

# Function to display the main menu
def main_menu():
    while True:
        print("\nWelcome to the Stock Management Application!")
        print("1. Create a new user.")
        print("2. Login as an existing user.")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            create_user()  # Create a new user
        elif choice == '2':
            user_id = input("Enter your user ID: ")  # Ask for user ID
            user = find_user(user_id)  # Search for user in the User bucket

            if user is None:
                print("User not found. Please try again.")
            else:
                print("User found. Proceeding...")
                user_role(user)  # Use the same user object in both admin and customer functions
        elif choice == '3':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Main function to start the application
if __name__ == "__main__":
    print("Starting application...")
    main_menu()  # Start the application