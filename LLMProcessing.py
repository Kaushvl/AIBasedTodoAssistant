from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import dotenv
import os
import json
from DBProcessing import fetch_all_data

dotenv.load_dotenv()
groq_api_key = os.environ.get('groq_api_key')

def UserInputProcessing(strInputText):
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    system = '''You are an obidient assistant which manages a todo list of a persion and you need to perform this task with very high accuracy. Task : 
    0. Act as a poliet assistant and reply to input text as a real human assistant in AssistantMessage.
    1. I am going to provide you a text, which is originally a Command from an human and it will be a raw input, you need to analyize the text and return 'True' or 'False' in string weather the user wants to perfrom any operation on Todo list from [Create,Read,Update,Delete] if yes , return True along with Actual task to add in todo list in UserTask and if No , the return False and empty string for UserTask and UserAction only.
    2. You need to analize it and based on it identiy the action they want to perfrom from [Create,Read,Update,Delete].
    3. Importantly notice that specifically dont use any symbol such as #'# or #"# in any of Values of json.
    4. Only return the output in json without any description fromat as "AssistantMessage":"YourActualAssistantMessageWithoutAnySymbol","OperationBool":"YourAnswerForUserOperationInString", "UserTask":"YourAnswerForUserMessage", "UserAction":"YourAnswerForUserAction"
    '''
    human = "{strInputText}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    strResponse = chain.invoke({strInputText}).content
    # strResponse = strResponse.replace('"'," ")
    print(strResponse,"18 strResponse")
    
    
    jsonResponse = json.loads(strResponse)
    return jsonResponse



def GetIdFromText(strInputText):
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    system = '''You need to perform this task with very high accuracy and 'only return the output in json without any description'. Task : I am going to provide you a text and a todolist from database, text is originally a Command from an human and it will be about doing some changes in a todo list, you need to analize it and based on it identify about which task user is talking about, and based on it 'only return the output in json without any description', fromat as 'Id':'ActualIdFromTasks' Output Example : 'Id' : '663f50599607c3ea3ac44806' '''
    
    all_tasks = fetch_all_data()
    strAllTasks = ''
    for task in all_tasks:
        strAllTasks += str(task) + '\n'
    strInputData = "text : "  + strInputText + ".    Database : " +  strAllTasks

    human = "{strInputData}"

    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    strResponse = chain.invoke({strInputData}).content
    print(strInputText, strResponse,"54 strResponse")
    jsonResponse = json.loads(strResponse.replace("'",'"'))
    
    return jsonResponse


# def HandleInputLLM(strUserText):
#     jsonUserMessageDetails = UserInputProcessing(strUserText)

#     if bool(jsonUserMessageDetails['OperationBool']):
#         jsResponse = TextProcessing(jsonUserMessageDetails['UserMessage'])
        
#     return jsResponse

if __name__ == '__main__':
    print(UserInputProcessing("Delete task which is about reaeding a book"))
