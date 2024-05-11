from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import dotenv
import os
import json

dotenv.load_dotenv()
groq_api_key = os.environ.get('groq_api_key')

def UserInputProcessing(strInputText):
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    system = '''You need to perform this task with very high accuracy. Task : I am going to provide you a text, which is originally a Command from an human and it will be a raw input, you need to analyize the text and return ['True' or 'False'] weather the user wants to perfrom any operation on Todo list from [Create,Read,Update,Delete] if yes , return True along with Complete context of the action they wants to perfrom and if No , the return False and empty string and only return the output in json without any description fromat as 'OperationBool':'YourAnswerForUserOperationAsString', 'UserMessage':'YourAnswerForUserMessage' '''
    human = "{strInputText}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    strResponse = chain.invoke({strInputText}).content
    
    jsonResponse = json.loads(strResponse.replace("'",'"'))
    return jsonResponse


def TextProcessing(strInputText):
    chat = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama3-70b-8192")
    system = '''You need to perform this task with very high accuracy. Task : I am going to provide you a text, which is originally a Command from an human and it will be about doing some changes in a todo list, you need to analize it and based on it identiy the action they want to perfrom from [Create,Read,Update,Delete] and only return the output in json without any description fromat as 'Title':'YourAnswerForUserTitle', 'UserAction':'YourAnswerForUserAction' '''
    human = "{strInputText}"
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

    chain = prompt | chat
    strResponse = chain.invoke({strInputText}).content
    
    jsonResponse = json.loads(strResponse.replace("'",'"'))
    return jsonResponse


def HandleInputLLM(strUserText):
    jsonUserMessageDetails = UserInputProcessing(strUserText)

    if bool(jsonUserMessageDetails['OperationBool']):
        jsResponse = TextProcessing(jsonUserMessageDetails['UserMessage'])
        
    return jsResponse

if __name__ == '__main__':
    print(HandleInputLLM("Create a task to fill water bottles"))
