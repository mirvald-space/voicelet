from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB_NAME, logger

class Database:
    """Database utility for MongoDB operations"""
    
    def __init__(self):
        """Initialize the database connection"""
        try:
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[MONGODB_DB_NAME]
            self.users = self.db.users
            logger.info(f"Connected to MongoDB database: {MONGODB_DB_NAME}")
        except Exception as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise
    
    def add_user(self, user_id, username, first_name, last_name=None, language_code=None):
        """
        Add a new user to the database or update if already exists
        
        Args:
            user_id: Telegram user ID
            username: Telegram username
            first_name: User's first name
            last_name: User's last name
            language_code: User's language code
            
        Returns:
            The inserted or updated user document ID
        """
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "language_code": language_code,
                "last_activity": None
            }
            
            result = self.users.update_one(
                {"user_id": user_id},
                {"$set": user_data},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"New user added to database: {username} (ID: {user_id})")
                return result.upserted_id
            else:
                logger.info(f"User updated in database: {username} (ID: {user_id})")
                return user_id
                
        except Exception as e:
            logger.error(f"Error adding user to database: {e}")
            return None
    
    def get_user(self, user_id):
        """
        Get user by Telegram ID
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            User document or None
        """
        try:
            return self.users.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"Error retrieving user from database: {e}")
            return None
    
    def get_all_users(self):
        """
        Get all users from database
        
        Returns:
            List of user documents
        """
        try:
            return list(self.users.find())
        except Exception as e:
            logger.error(f"Error retrieving users from database: {e}")
            return [] 