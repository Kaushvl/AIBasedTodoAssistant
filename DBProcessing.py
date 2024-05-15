import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TodoProject"]
collection = db["TodoList"]

class DatabaseAct:
    @staticmethod
    def create_task(document):
        """
        Creates a new document in the MongoDB collection based on a natural language description.

        Args:
            natural_language_description (str): A human-readable description of the document to be created.

        Returns:
            dict: The newly created document in dictionary format.
        """

        try:
            # Insert the document into the collection
            result = collection.insert_one(document)

            return document

        except Exception as e:
            print(f"Error creating document: {e}")
            return None
        
    @staticmethod 
    def fetch_all_data():
        """Fetches all call data from the database"""
        data = collection.find()
        return data

    @staticmethod 
    def update_task(strId, new_fields):
        """
        Updates fields of a document in the MongoDB collection based on the _id provided.

        Args:
            strId (str): The _id of the document to update.
            new_fields (dict): A dictionary containing the fields to update and their new values.

        Returns:
            int: 1 if the document was updated successfully, 0 otherwise.
        """

        try:
            # Convert strId to ObjectId if needed
            from bson import ObjectId
            object_id = ObjectId(strId)

            result = collection.update_one({"_id": object_id}, {"$set": new_fields})

            if result.modified_count == 1:
                return 1
            else:
                return 0

        except Exception as e:
            print(f"Error updating document: {e}")
            return 0
    @staticmethod 
    def delete_task(strId):
        """
        Deletes a document from the MongoDB collection based on the _id provided.

        Args:
            strId (str): The _id of the document to delete.

        Returns:
            int: 1 if the document was deleted successfully, 0 otherwise.
        """

        try:
            # Convert strId to ObjectId if needed
            from bson import ObjectId
            object_id = ObjectId(strId)

            result = collection.delete_one({"_id": object_id})

            if result.deleted_count == 1:
                return 1
            else:
                return 0

        except Exception as e:
            print(f"Error deleting document: {e}")
            return 0