from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
# Libraries 


class Progress_Bar:
    def __init__(self,Script_name):
        self.root = tk.Tk()
        self.root.geometry('300x120')
        self.Script_name = Script_name
        self.root.title(f'{Script_name}')
        
        # progressbar
        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        # place the progressbar
        self.pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

        # label
        self.value_label = ttk.Label(self.root, text=self.update_progress_label())
        self.value_label.grid(column=0, row=1, columnspan=2)

        # start button
        
        self.progress()

        stop_button = ttk.Button(
            self.root,
            text='Cancel',
            command=self.stop
        )
        stop_button.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)


        self.root.mainloop()




    def update_progress_label(self):
        return f"Current Progress: {self.pb['value']}%"


    def progress(self):
        if self.pb['value'] < 100:
            self.pb['value'] += 20
            self.value_label['text'] = self.update_progress_label()
        else:
            showinfo(message='The progress completed!')
            self.root.destroy()


    def stop(self):
        self.pb.stop()
        self.value_label['text'] = self.update_progress_label()
        self.root.destroy()



init=Progress_Bar("LULU")