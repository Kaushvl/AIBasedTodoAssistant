from DBProcessing import create_task,fetch_all_data,delete_task,update_task
from LLMProcessing import UserInputProcessing,GetIdFromText
import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3 

class AudioInputApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo Assistant")

        self.label = tk.Label(master, text="Press 'Record' to start recording")
        self.label.pack()

        self.record_button = tk.Button(master, text="Record", command=self.record_audio)
        self.record_button.pack()

        # Configure the style for the Treeview
        style = ttk.Style()
        style.configure("Treeview", rowheight=30)  # Adjust row height if needed
        style.configure("Treeview.Heading", font=("Arial", 12))  # Customize heading font if needed

        # Create a Treeview with centered alignment
        self.tree = ttk.Treeview(master, columns=("TaskName", "TaskPriority", "TaskStatus"), style="Treeview")
        self.tree.heading("#0", text="Index")
        self.tree.heading("TaskName", text="TaskName")
        self.tree.heading("TaskPriority", text="TaskPriority")
        self.tree.heading("TaskStatus", text="TaskStatus")
        self.tree.pack()

        # Fetch all tasks and display in the table
        self.display_tasks()

    def record_audio(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.label.config(text="Recording... Say something!")
            audio_data = recognizer.listen(source,timeout=4)
            self.label.config(text="Processing...")

        try:
            recognized_text = recognizer.recognize_google(audio_data)
            print(recognized_text,"recognized_text")
            dbStatus = self.ProcessInput(recognized_text)
            self.label.config(text=f"Speech Recognition Result: {recognized_text}")
        except sr.UnknownValueError:
            self.label.config(text="Sorry, I could not understand what you said")
        except sr.RequestError:
            self.label.config(text="Sorry, could not request results. Please check your internet connection.")

    def display_tasks(self):
        # Clear existing table data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all tasks from MongoDB
        all_tasks = fetch_all_data()

        # Insert tasks into the table
        for idx, task in enumerate(all_tasks):
            self.tree.insert("", "end", text=str(idx + 1), values=(task["MessageTitle"],task["TaskPriority"],task["TaskStatus"]))

        # Set the alignment for each column to center
        self.tree.column("#0", anchor=tk.CENTER)  # Anchor for the index column
        self.tree.column("TaskName", anchor=tk.CENTER)  # Anchor for the TaskName column
        self.tree.column("TaskPriority", anchor=tk.CENTER)  # Anchor for the TaskPriority column
        self.tree.column("TaskStatus", anchor=tk.CENTER)

    def read_out_message(self, message):
        engine = pyttsx3.init()
        engine.say(message)
        engine.runAndWait()



    def ProcessInput(self,strUserText):
        DBResponse = ''
        if strUserText:
            response = UserInputProcessing(strUserText)
            if bool(response['OperationBool']):
                if response["UserAction"] == "Create":
                    DBResponse = create_task(response['UserTask'])

                if response["UserAction"] == "Delete":
                    if response["UserTask"]["MessageTitle"]:
                        strId = GetIdFromText(response["UserTask"]['MessageTitle'])
                        DBResponse = delete_task(strId['Id'])
                    print(DBResponse)

                if response["UserAction"] == "Update":
                    if response["UserTask"]["MessageTitle"]:
                        strId = GetIdFromText(response["UserTask"]['MessageTitle'])
                        del response["UserTask"]['MessageTitle']
                        DBResponse = update_task(strId['Id'],response["UserTask"])
                    print(DBResponse)
            if response['AssistantMessage']:
                self.read_out_message(response['AssistantMessage'])

            self.display_tasks()
        return DBResponse
            
    
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioInputApp(root)
    root.mainloop()
