import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import threading
from DBProcessing import DatabaseAct
from LLMProcessing import LLMProcessing

class AudioInputApp:
    def __init__(self, master):
        self.master = master
        master.title("Todo Assistant")
        master.geometry("800x600")
        master.configure(bg="#2C3E50")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#2C3E50", foreground="#ECF0F1", font=("Arial", 12))
        style.configure("TButton", background="#2980B9", foreground="#ECF0F1", font=("Arial", 12))
        style.configure("Treeview", background="#ECF0F1", foreground="#2C3E50", fieldbackground="#ECF0F1", rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#2980B9", foreground="#ECF0F1")
        style.map("Treeview.Heading", background=[("active", "#3498DB")])

        self.label = ttk.Label(master, text="Listening for trigger word...")
        self.label.pack(pady=10)

        self.tree_frame = ttk.Frame(master)
        self.tree_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.tree_frame, columns=("TaskName", "TaskPriority", "TaskStatus"), yscrollcommand=self.tree_scroll.set, style="Treeview")
        self.tree.heading("#0", text="Index", anchor=tk.CENTER)
        self.tree.heading("TaskName", text="Task Name", anchor=tk.CENTER)
        self.tree.heading("TaskPriority", text="Task Priority", anchor=tk.CENTER)
        self.tree.heading("TaskStatus", text="Task Status", anchor=tk.CENTER)
        self.tree.column("#0", width=50, anchor=tk.CENTER)
        self.tree.column("TaskName", width=200, anchor=tk.CENTER)
        self.tree.column("TaskPriority", width=150, anchor=tk.CENTER)
        self.tree.column("TaskStatus", width=150, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        self.comment_box_label = ttk.Label(master, text="Comment Box:")
        self.comment_box_label.pack(pady=10)

        self.comment_box_frame = ttk.Frame(master)
        self.comment_box_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.comment_box_scroll = ttk.Scrollbar(self.comment_box_frame)
        self.comment_box_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.comment_box = tk.Text(self.comment_box_frame, height=5, width=50, bg="#ECF0F1", fg="#2C3E50", font=("Arial", 12), yscrollcommand=self.comment_box_scroll.set)
        self.comment_box.pack(fill=tk.BOTH, expand=True)
        self.comment_box_scroll.config(command=self.comment_box.yview)

        self.recognizer = sr.Recognizer()
        self.ttsEngine = pyttsx3.init()

        self.trigger_word = "assistant"
        self.ProcessCondition = True

        self.display_tasks()

        # Start the command processing thread
        self.command_thread = threading.Thread(target=self.record_audio)
        self.command_thread.start()

    def record_audio(self):
        '''
        Purpose : Acitvily listens for audio until trigger word is received
        '''
        with sr.Microphone() as source:
            print("Listening...")
            try:
                audio_data = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                print("Listening timed out, retrying...")
                self.record_audio()
                return

        try:
            recognized_text = self.recognizer.recognize_google(audio_data)
            print("Recognized:", recognized_text)
            if self.trigger_word in recognized_text.lower():
                self.read_out_message("Hey! I am your Task Assistant, How can I help you?")
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
        '''
        Purpose : Becomes active trigger words is detected and perfrom the command given
        '''
        while self.ProcessCondition:
            with sr.Microphone() as source:
                print("Listening for commands...")
                audio_data = self.recognizer.listen(source)

            try:
                recognized_text = self.recognizer.recognize_google(audio_data)
                print("Recognized command:", recognized_text)
                if "exit" in recognized_text.lower():
                    self.read_out_message("Bye! Have a great day!")
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


    def display_tasks(self):
        '''
        Purpose : Fetcha all the task from database and display in tree table
        '''
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
        '''
        Purpose : takes text as an input and read the messgae init
        '''
        message = " " + message
        self.ttsEngine.say(message)
        self.ttsEngine.runAndWait()

    def ProcessInput(self, strUserText):
        '''
        Purpose : takes text as an input and Process it using llm and then perfrom the db task as needed
        '''
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
    root.mainloop()

if __name__ == "__main__":
    # Run the GUI in a separate thread
    gui_thread = threading.Thread(target=run_app)
    gui_thread.start()
