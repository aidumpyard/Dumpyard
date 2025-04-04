import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess  # To run another Python script (if needed)
import os

def browse_file1():
    file_path = filedialog.askopenfilename(title="Select First File")
    if file_path:
        entry_file1.delete(0, tk.END)
        entry_file1.insert(0, file_path)

def browse_file2():
    file_path = filedialog.askopenfilename(title="Select Second File")
    if file_path:
        entry_file2.delete(0, tk.END)
        entry_file2.insert(0, file_path)

def browse_directory():
    dir_path = filedialog.askdirectory(title="Select Input Directory")
    if dir_path:
        entry_dir.delete(0, tk.END)
        entry_dir.insert(0, dir_path)

def run_script():
    file1 = entry_file1.get()
    file2 = entry_file2.get()
    directory = entry_dir.get()

    if not (file1 and file2 and directory):
        messagebox.showerror("Error", "Please select all inputs before running.")
        return

    try:
        # Example: calling another script
        # subprocess.run(["python", "your_script.py", file1, file2, directory])
        
        # Or call a function directly if importing the script
        import your_script  # Replace with your actual script name
        your_script.main(file1, file2, directory)  # assuming `main()` takes 3 arguments

        messagebox.showinfo("Success", "Script ran successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# GUI setup
root = tk.Tk()
root.title("Input File and Directory Selector")

tk.Label(root, text="Input File 1:").grid(row=0, column=0, sticky="e")
entry_file1 = tk.Entry(root, width=50)
entry_file1.grid(row=0, column=1)
tk.Button(root, text="Browse", command=browse_file1).grid(row=0, column=2)

tk.Label(root, text="Input File 2:").grid(row=1, column=0, sticky="e")
entry_file2 = tk.Entry(root, width=50)
entry_file2.grid(row=1, column=1)
tk.Button(root, text="Browse", command=browse_file2).grid(row=1, column=2)

tk.Label(root, text="Input Directory:").grid(row=2, column=0, sticky="e")
entry_dir = tk.Entry(root, width=50)
entry_dir.grid(row=2, column=1)
tk.Button(root, text="Browse", command=browse_directory).grid(row=2, column=2)

tk.Button(root, text="Run", command=run_script, bg="green", fg="white").grid(row=3, column=1, pady=10)

root.mainloop()