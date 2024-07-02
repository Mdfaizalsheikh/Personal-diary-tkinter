import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import sqlite3
from datetime import datetime


conn = sqlite3.connect('diary.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS diary
             (id INTEGER PRIMARY KEY, date TEXT, entry TEXT)''')
conn.commit()


class PersonalDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Diary")
        self.root.geometry("500x400")

        self.entry_text = tk.Text(root, height=10, width=50)
        self.entry_text.pack(pady=10)

        self.save_button = tk.Button(root, text="Save Entry", command=self.save_entry)
        self.save_button.pack(pady=5)

        self.view_button = tk.Button(root, text="View Entries", command=self.view_entries)
        self.view_button.pack(pady=5)

        self.entries_listbox = tk.Listbox(root, width=70)
        self.entries_listbox.pack(pady=10)
        self.entries_listbox.bind('<Double-1>', self.edit_entry)
        self.entries_listbox.bind('<Delete>', self.delete_entry)

        self.load_entries()

    def save_entry(self):
        entry = self.entry_text.get("1.0", tk.END).strip()
        if entry:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute("INSERT INTO diary (date, entry) VALUES (?, ?)", (date, entry))
            conn.commit()
            self.entry_text.delete("1.0", tk.END)
            self.load_entries()
            messagebox.showinfo("Success", "Entry saved successfully!")
        else:
            messagebox.showwarning("Warning", "Please write something in the diary entry.")

    def load_entries(self):
        self.entries_listbox.delete(0, tk.END)
        c.execute("SELECT * FROM diary ORDER BY date DESC")
        for row in c.fetchall():
            self.entries_listbox.insert(tk.END, f"Date: {row[1]} - Entry: {row[2][:30]}...")

    def view_entries(self):
        self.load_entries()

    def edit_entry(self, event):
        selected_item = self.entries_listbox.curselection()
        if selected_item:
            index = selected_item[0]
            item = self.entries_listbox.get(index)
            date = item.split(' - ')[0][6:]
            c.execute("SELECT * FROM diary WHERE date = ?", (date,))
            entry = c.fetchone()
            if entry:
                new_entry = simpledialog.askstring("Edit Entry", "Edit your diary entry:", initialvalue=entry[2])
                if new_entry is not None:
                    c.execute("UPDATE diary SET entry = ? WHERE id = ?", (new_entry, entry[0]))
                    conn.commit()
                    self.load_entries()
                    messagebox.showinfo("Success", "Entry updated successfully!")

    def delete_entry(self, event):
        selected_item = self.entries_listbox.curselection()
        if selected_item:
            index = selected_item[0]
            item = self.entries_listbox.get(index)
            date = item.split(' - ')[0][6:]
            c.execute("DELETE FROM diary WHERE date = ?", (date,))
            conn.commit()
            self.load_entries()
            messagebox.showinfo("Success", "Entry deleted successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalDiary(root)
    root.mainloop()
