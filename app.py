import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import time
from DBProcessing import DatabaseAct
from LLMProcessing import LLMProcessing
import threading

class AudioInputApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo Assistant")

        self.label = tk.Label(master, text="Listening for trigger word...")
        self.label.pack()

        self.ButtonText = 'Activate'

        style = ttk.Style()
        style.configure("Treeview", rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 12))

        self.tree = ttk.Treeview(master, columns=("TaskName", "TaskPriority", "TaskStatus"), style="Treeview")
        self.tree.heading("#0", text="Index")
        self.tree.heading("TaskName", text="TaskName")
        self.tree.heading("TaskPriority", text="TaskPriority")
        self.tree.heading("TaskStatus", text="TaskStatus")

        self.tree.pack()

        self.comment_box_label = tk.Label(master, text="Comment Box:")
        self.comment_box_label.pack()

        self.comment_box = tk.Text(master, height=5, width=50)
        self.comment_box.pack()

        self.recognizer = sr.Recognizer()
        self.ttsEngine = pyttsx3.init()

        self.trigger_word = "assistant"
        self.ProcessCondition = True

        self.display_tasks()

            # Start the command processing thread
        self.command_thread = threading.Thread(target=self.record_audio)
        self.command_thread.start()

    def record_audio(self):
        with sr.Microphone() as source:
            print("Listening...")
            audio_data = self.recognizer.listen(source,timeout=2)

        try:
            recognized_text = self.recognizer.recognize_google(audio_data)
            print("Recognized:", recognized_text)
            if self.trigger_word in recognized_text.lower():
                print("Trigger word detected. Activating assistant...")
                self.label.config(text="Assistant activated. Listening...")
                self.ProcessCondition = True
                self.process_commands()
            else:
                print("Trigger word not detected. Listening for trigger word...")
                self.label.config(text="Listening for trigger word...")
                self.record_audio()
        except sr.UnknownValueError:
            print("Sorry, I could not understand what you said")
            self.record_audio()
        except sr.RequestError:
            print("Sorry, could not request results. Please check your internet connection.")
            self.record_audio()

    def process_commands(self):
        while self.ProcessCondition:
            with sr.Microphone() as source:
                print("Listening for commands...")
                audio_data = self.recognizer.listen(source)

            try:
                recognized_text = self.recognizer.recognize_google(audio_data)
                print("Recognized command:", recognized_text)
                if "exit" in recognized_text.lower():
                    print("Exiting assistant...")
                    self.label.config(text="Assistant deactivated.")
                    self.ProcessCondition = False
                    self.record_audio()
                else:
                    self.ProcessInput(recognized_text)
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said")
            except sr.RequestError:
                print("Sorry, could not request results. Please check your internet connection.")
    def check_for_commands(self):
        # Update the UI after each command is processed
        self.display_tasks()

        # Check for new commands after a delay
        if self.ProcessCondition:
            self.master.after(100, self.process_commands)

    def display_tasks(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        all_tasks = DatabaseAct.fetch_all_data()

        for idx, task in enumerate(all_tasks):
            print(task['MessageTitle'])
            self.tree.insert("", "end", text=str(idx + 1), values=(task["MessageTitle"], task["TaskPriority"], task["TaskStatus"]))

        self.tree.column("#0", anchor=tk.CENTER)
        self.tree.column("TaskName", anchor=tk.CENTER)
        self.tree.column("TaskPriority", anchor=tk.CENTER)
        self.tree.column("TaskStatus", anchor=tk.CENTER)

    def read_out_message(self, message):
        message = "you and " + message
        self.ttsEngine.say(message)
        self.ttsEngine.runAndWait()

    def ProcessInput(self, strUserText):
        DBResponse = ''
        if strUserText:
            response = LLMProcessing.UserInputProcessing(strUserText)
            if bool(response['OperationBool']):
                if response["UserAction"] == "Create":
                    DBResponse = DatabaseAct.create_task(response['UserTask'])
                elif response["UserAction"] == "Delete":
                    if response["UserTask"]["MessageTitle"]:
                        strId = LLMProcessing.GetIdFromText(response["UserTask"]['MessageTitle'])
                        DBResponse = DatabaseAct.delete_task(strId['Id'])
                elif response["UserAction"] == "Update":
                    if response["UserTask"]["MessageTitle"]:
                        strId = LLMProcessing.GetIdFromText(response["UserTask"]['MessageTitle'])
                        del response["UserTask"]['MessageTitle']
                        DBResponse = DatabaseAct.update_task(strId['Id'], response["UserTask"])
                elif response["UserAction"] == "Read":
                    if response["UserTask"]["MessageTitle"]:
                        self.BoxMessage = LLMProcessing.PerfromDBTask(response["UserTask"]['MessageTitle'])
                        self.comment_box.delete("1.0", tk.END)
                        self.comment_box.insert(tk.END, self.BoxMessage)
                        response['AssistantMessage'] = self.BoxMessage

            self.display_tasks()

            if response['AssistantMessage']:
                self.read_out_message(response['AssistantMessage'])

        return DBResponse
def run_app():
    root = tk.Tk()
    app = AudioInputApp(root)
    # root.after(100, app.record_audio)
    root.mainloop()

if __name__ == "__main__":
    # Run the GUI in a separate thread
    gui_thread = threading.Thread(target=run_app)
    gui_thread.start()
