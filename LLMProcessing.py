from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import dotenv
import os
import json
from DBProcessing import DatabaseAct
dotenv.load_dotenv()
groq_api_key = os.environ.get('groq_api_key')

class LLMProcessing:
    @staticmethod
    def UserInputProcessing(strInputText):
        chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
        system = '''You are an obidient assistant which manages a todo list of a persion and you need to perform this task with very high accuracy. Task : 
        0. Act as a poliet assistant and reply to input text as a real human assistant in AssistantMessage.
        1. I am going to provide you a text, which is originally a Command from an human and it will be a raw input, you need to analyize the text and return 'True' or 'False' in string weather the user wants to perfrom any operation on Todo list from [Create,Read,Update,Delete] if yes , return True along with Actual task to add in todo list in UserTask and if No , the return False and empty string for UserTask and UserAction only.
        2. You need to analize it and based on it identiy the action they want to perfrom from [Create,Read,Update,Delete] and Give the MessageTitle.
        3. Task Status will be only from [NotStarted(Give this as Default),InProgress,Completed] and Task Priority will be only from [Low,Medium(Give this as Default),High] 
        3. Importantly notice that specifically dont use any symbol such as #'# or #"# in any of Values of json.
        4. Only return the output in json without any description fromat as "AssistantMessage":"YourActualAssistantMessageWithoutAnySymbol","OperationBool":"YourAnswerForUserOperationInString","UserAction":"YourAnswerForUserAction", "UserTask": Dict("MessageTitle" : "YourAnswerForMessageTitleForCRUDOperation", "TaskPriority": "YourAnswerForUserTaskPriority", "TaskStatus": "YourAnswerForTaskStatus")
        '''
        human = "{strInputText}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

        chain = prompt | chat
        strResponse = chain.invoke({strInputText}).content
        # strResponse = strResponse.replace('"'," ")
        print(strResponse,"18 strResponse")
        
        
        jsonResponse = json.loads(strResponse)
        return jsonResponse


    @staticmethod
    def GetIdFromText(strInputText):
        chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
        system = '''You need to perform this task with very high accuracy and 'only return the output in json without any description'. Task : I am going to provide you a text and a todolist from database, text is originally a Command from an human and it will be about doing some changes in a todo list, you need to analize it and based on it identify about which task user is talking about, and based on it 'only return the output in json without any description', fromat as "Id":"ActualIdFromTasks" Output Example : 'Id' : '663f50599607c3ea3ac44806' '''
        
        all_tasks = DatabaseAct.fetch_all_data()
        strAllTasks = ''
        i = 1
        for task in all_tasks:
            strAllTasks += 'TaskNumber : '+ str(-i) + "    " + str(task) + '\n'
            i += 1
        strInputData = "text : "  + strInputText + ".    Database : " +  strAllTasks

        human = "{strInputData}"

        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

        chain = prompt | chat
        strResponse = chain.invoke({strInputData}).content
        print(strInputText, strResponse,"54 strResponse")
        jsonResponse = json.loads(strResponse)
        
        return jsonResponse

    @staticmethod
    def PerfromDBTask(strInputText):
        # Assuming ChatGroq and other necessary imports are defined elsewhere in your code
        chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
        system = '''You need to perform this task with very high accuracy and 'only return the output in json without any description'. Task : I am going to provide you a text and a todolist from database, text is originally a Command from an human and it will ask to read some info from the database, please analyze the input and based on that return the clear and concise data from database in such format that a assistant is giving answer to a boss, and based on it 'only return the output in json without any description', fromat as "message" : "YourMessageForInputQuery"  '''
        
        
        all_tasks = DatabaseAct.fetch_all_data()  # Ensure this function returns a list of tasks
        strAllTasks = ''
        for task in all_tasks:
            strAllTasks += str(task) + '\n'
        
        # Constructing the input data for the chatbot
        strInputData = "text : "  + strInputText + ".    Database : " +  strAllTasks
        
        # Creating the prompt for the chatbot
        human = "{strInputData}"
        prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])
        
        # Generating the response from the chatbot
        chain = prompt | chat
        strResponse = chain.invoke({strInputData}).content
        print(strInputText, strResponse,"54 strResponse")
        
        # Parsing the JSON response to extract the task ID
        jsonResponse = json.loads(strResponse.replace("'",'"'))
        strMessage = jsonResponse.get('message')  # Assuming the JSON structure has an 'Id' key
        
        return strMessage  # Return the extracted task ID



if __name__ == '__main__':
    print(LLMProcessing.UserInputProcessing("Add a task about cleaning labtop with low priority and status as inprogress"))
