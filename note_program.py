# insert your complete, modified code here. Use additional cells if needed.
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import datetime

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")  # Larger window size (1)
        self.title('Notebook')
        self.items = []  # Combined notes and snippets list (2)
        self.create_widgets()

    def create_widgets(self): # creating new function for buttons 
        tk.Button(self, text='New Note', command=lambda: ItemForm(self, item_type='note')).pack()
        tk.Button(self, text='New Snippet', command=lambda: ItemForm(self, item_type='snippet')).pack()
        tk.Button(self, text='Open Notebook', command=self.open_notebook).pack()
        tk.Button(self, text='Save Notebook', command=self.save_notebook).pack()
        tk.Button(self, text = 'Print Notes', command =self.print_notes).pack() # print notes out
        self.load_notebook()

    def display_items(self):
        for widget in self.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text").startswith("View"):
                widget.destroy()
        for item in self.items:
            display_text = f"{item['title']} - {item['type'].capitalize()} - Last edited: {item['metadata']}"
            tk.Button(self, text=display_text, command=lambda item=item: ItemForm(self, item, item['type'])).pack()

    def open_notebook(self):
        # opens a filedialog
        filepath = filedialog.askopenfilename(filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if filepath: # reads files and displays snippets or notes
            with open(filepath, 'r') as file: 
                self.items = eval(file.read())
                self.display_items()

    def save_notebook(self):
         #open a file dialog to choose where to save the notebook
        filepath = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
        if filepath:
            with open(filepath, 'w') as file:
                file.write(str(self.items))
                messagebox.showinfo("Save", "Notebook has been saved")

    def load_notebook(self):
        try:
            with open('default_notes.txt', 'r') as file:
                self.items = eval(file.read())
                self.display_items()
        except FileNotFoundError:
            self.items = []
    
    def print_notes(self):
        for item in self.items:
            if item['type']== 'note':
                print(f"Title: {item['title']}\nText: {item['text']}\nLast Editied: {item['metadata']}\n")

class ItemForm(tk.Toplevel): # new class, instead of NoteForm, both notes and snippets (2) 
    def __init__(self, master, item=None, item_type='note'):
        super().__init__(master)
        self.item = item
        self.item_type = item_type
        self.create_widgets()

    def create_widgets(self):
        self.title_entry = tk.Entry(self)
        self.title_entry.pack()
        self.text_entry = ScrolledText(self, height = 10) # utilization of scrolledtext
        self.text_entry.pack()
        tk.Button(self, text='Submit', command=self.submit).pack()

        if self.item:
            self.title_entry.insert(0, self.item['title'])
            self.text_entry.insert('1.0', self.item['text'])

    def submit(self):
        # add lines to the submit method
        title = self.title_entry.get() # gathers info and updates
        text = self.text_entry.get('1.0', 'end').strip()
        metadata = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_item = {'title': title, 'text': text, 'metadata': metadata, 'type': self.item_type}
        if self.item:
            self.item.update(new_item)
        else:
            self.master.items.append(new_item)
        self.master.display_items() # displays 
        self.destroy() # closes window

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()
