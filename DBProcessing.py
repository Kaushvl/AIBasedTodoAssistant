import pymongo
# from LLMProcessing import 

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["TodoProject"]
collection = db["TodoList"]

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
    
def fetch_all_data():
    """Fetches all call data from the database"""
    data = collection.find()
    return data


# def read_documents(natural_language_query):
#     """
#     Reads documents from the MongoDB collection based on a natural language query.

#     Args:
#         natural_language_query (str): A human-readable query for filtering documents.

#     Returns:
#         list: A list of matching documents in dictionary format.
#     """

#     try:
#         # Use the LLM to understand the query and potentially translate it to MongoDB syntax
#         llm_parsed_query = llm.parse_query(natural_language_query)

#         # Convert the parsed query to a MongoDB query object
#         mongo_query = process_llm_parsed_query(llm_parsed_query)

#         # Find matching documents in the collection
#         cursor = collection.find(mongo_query)

#         return list(cursor)

#     except Exception as e:
#         print(f"Error reading documents: {e}")
#         return []

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