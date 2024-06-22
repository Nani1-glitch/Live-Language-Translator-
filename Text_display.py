import tkinter as tk

def display_text(text):
    root = tk.Tk()
    root.title("Translated Text")
    text_widget = tk.Text(root, height=10, width=50)
    text_widget.pack()
    text_widget.insert(tk.END, text)
    root.mainloop()

translated_text = "Hello, how are you?"
display_text(translated_text)
