class User:
    def __init__(self, user_id: str, user_email: str, user_name: str, is_admin: bool):
        self.user_id = user_id        # Changed to user_id
        self.user_email = user_email  # Changed to user_email
        self.user_name = user_name    # Changed to user_name
        self.is_admin = is_admin      # Changed to is_admin

    # Display user information
    def display_user_info(self):
        role = "Admin" if self.is_admin else "Customer"
        print(f"User ID: {self.user_id}")          # Updated
        print(f"User Name: {self.user_name}")      # Updated
        print(f"User Email: {self.user_email}")    # Updated
        print(f"Role: {role}")