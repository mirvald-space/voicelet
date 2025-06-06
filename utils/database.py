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
            
            # Check if this is a new user to initialize the transcription count
            existing_user = self.get_user(user_id)
            if not existing_user:
                user_data["transcriptions_count"] = 0
            
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
            
    def increment_transcription_count(self, user_id):
        """
        Increment the transcription count for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            New transcription count or None if error
        """
        try:
            # If user doesn't exist, create with count 1
            result = self.users.update_one(
                {"user_id": user_id},
                {"$inc": {"transcriptions_count": 1}},
                upsert=True
            )
            
            # Get the updated user to return the new count
            updated_user = self.get_user(user_id)
            if updated_user and "transcriptions_count" in updated_user:
                new_count = updated_user["transcriptions_count"]
                logger.info(f"Transcription count incremented for user {user_id}: {new_count}")
                return new_count
            return None
                
        except Exception as e:
            logger.error(f"Error incrementing transcription count: {e}")
            return None
    
    def get_transcription_count(self, user_id):
        """
        Get the transcription count for a user
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Transcription count or 0 if not found
        """
        try:
            user = self.get_user(user_id)
            if user and "transcriptions_count" in user:
                return user["transcriptions_count"]
            return 0
        except Exception as e:
            logger.error(f"Error getting transcription count: {e}")
            return 0 