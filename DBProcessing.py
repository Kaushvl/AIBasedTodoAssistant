import pymongo

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


# def update_document(natural_language_update):
#     """
#     Updates a document in the MongoDB collection based on a natural language update instruction.

#     Args:
#         natural_language_update (str): A human-readable instruction for updating a document.

#     Returns:
#         bool: True if the update was successful, False otherwise.
#     """

#     try:
#         # Use the LLM to comprehend the update instruction and extract relevant details
#         llm_update_info = llm.parse_update(natural_language_update)

#         # Process the LLM interpretation to construct a MongoDB update query
#         update_query, update_document = process_llm_update_info(llm_update_info)

#         # Update the document in the collection
#         result = collection.update_one(update_query, update_document)

#         return result.matched_count > 0

#     except Exception as e:
#         print(f"Error updating document: {e}")
#         return False


# def delete_documents(natural_language_filter):
#     """
#     Deletes documents from the MongoDB collection based on a natural language filter.

#     Args:
#         natural_language_filter (str): A human-readable filter for selecting documents to delete.

#     Returns:
#         int: The number of documents deleted.
#     """

#     try:
#         # Use the LLM to interpret the filter and convert it to a MongoDB filter expression
#         llm_filter_expression = llm.parse_filter(natural_language_filter)

#         # Convert the parsed filter to a MongoDB filter object
#         mongo_filter = process_llm_filter_expression(llm_filter_expression)

#         # Delete matching documents from the collection
#         result = collection.delete_many(mongo_filter)

#         return result.deleted_count

    # except Exception as e:
    #     print(f"Error deleting documents: {e}")
    #     return 0