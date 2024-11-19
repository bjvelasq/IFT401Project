from couchbase.exceptions import DocumentNotFoundException
from couchbase.collection import Collection

class User:
    def __init__(self, user_id: str, user_email: str, user_name: str, is_admin: bool, user_collection: Collection, portfolio_collection: Collection):
        """
        Initialize the User object with necessary attributes.
        
        :param user_id: Unique identifier for the user
        :param user_email: User's email address
        :param user_name: User's full name
        :param is_admin: Boolean value indicating if the user is an admin
        :param user_collection: The Couchbase collection for users
        :param portfolio_collection: The Couchbase collection for portfolios
        """
        self.user_id = user_id
        self.user_email = user_email
        self.user_name = user_name
        self.is_admin = is_admin
        self.user_collection = user_collection
        self.portfolio_collection = portfolio_collection

    def create_user(self):
        """
        Creates a new user in the Couchbase collection.
        If the user is not an admin, a portfolio is also created.
        """
        user_doc = {
            "userID": self.user_id,
            "email": self.user_email,
            "userName": self.user_name,
            "isAdmin": self.is_admin
        }
        try:
            # Create or update the user document
            self.user_collection.upsert(f"user_{self.user_id}", user_doc)
            print(f"User {self.user_id} created successfully.")
        except Exception as e:
            print(f"Error creating user: {e}")

    def create_portfolio(self):
        """
        Creates a new portfolio for a user in the portfolio collection.
        Portfolios are only created for non-admin users.
        """
        portfolio_doc = {
            "userID": self.user_id,
            "stocks": []  # Initialize with no stocks
        }
        try:
            # Create or update the portfolio document
            self.portfolio_collection.upsert(f"portfolio_{self.user_id}", portfolio_doc)
            print(f"Portfolio for user {self.user_id} created successfully.")
        except Exception as e:
            print(f"Error creating portfolio: {e}")

    def user_exists(self) -> bool:
        """
        Check if a user document exists in the user collection.
        
        :return: True if the user exists, False otherwise
        """
        try:
            # Try to get the user document from the collection
            self.user_collection.get(f"user_{self.user_id}")
            return True
        except DocumentNotFoundException:
            return False

# Function to create a user and their portfolio (if not an admin)
def create_user(user_id, user_email, user_name, is_admin, user_collection, portfolio_collection):
    """
    Function to handle the creation of a user and their portfolio.

    :param user_id: Unique identifier for the user
    :param user_email: Email of the user
    :param user_name: Full name of the user
    :param is_admin: Boolean indicating if the user is an admin
    :param user_collection: The Couchbase collection for user documents
    :param portfolio_collection: The Couchbase collection for portfolio documents
    """
    # Create the User object
    user = User(user_id, user_email, user_name, is_admin, user_collection, portfolio_collection)
    
    # Create the user document
    user.create_user()
    
    # If the user is not an admin, create a portfolio for them
    if not is_admin:
        user.create_portfolio()