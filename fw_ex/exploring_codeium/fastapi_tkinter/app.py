import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import json

class PythonProblemSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Problem Solver")
        self.root.geometry("800x600")

        # Problem List Frame
        self.problem_frame = tk.Frame(root)
        self.problem_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Problem List Label
        tk.Label(self.problem_frame, text="Python Problems", font=('Arial', 14, 'bold')).pack()

        # Problem Listbox
        self.problem_listbox = tk.Listbox(self.problem_frame, width=30)
        self.problem_listbox.pack(fill=tk.BOTH, expand=True)
        self.problem_listbox.bind('<<ListboxSelect>>', self.load_problem)

        # Code Editor Frame
        self.editor_frame = tk.Frame(root)
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Problem Description
        self.description_text = tk.Text(self.editor_frame, height=5, wrap=tk.WORD)
        self.description_text.pack(fill=tk.X)
        self.description_text.config(state=tk.DISABLED)

        # Code Editor
        tk.Label(self.editor_frame, text="Your Solution", font=('Arial', 12)).pack()
        self.code_editor = scrolledtext.ScrolledText(self.editor_frame, wrap=tk.WORD, height=20)
        self.code_editor.pack(fill=tk.BOTH, expand=True)

        # Save Button
        self.save_button = tk.Button(self.editor_frame, text="Save Solution", command=self.save_solution)
        self.save_button.pack(fill=tk.X, pady=10)

        # Load Problems
        self.load_problems()

    def load_problems(self):
        try:
            response = requests.get("http://localhost:8000/problems")
            problems = response.json()
            
            for problem in problems:
                self.problem_listbox.insert(tk.END, f"{problem['id']}. {problem['title']} ({problem['difficulty']})")
        except Exception as e:
            messagebox.showerror("Error", f"Could not load problems: {str(e)}")

    def load_problem(self, event):
        try:
            selection = self.problem_listbox.curselection()
            if selection:
                problem_id = int(self.problem_listbox.get(selection[0]).split('.')[0])
                
                response = requests.get(f"http://localhost:8000/problem/{problem_id}")
                problem = response.json()

                # Update Description
                self.description_text.config(state=tk.NORMAL)
                self.description_text.delete(1.0, tk.END)
                self.description_text.insert(tk.END, f"Problem: {problem['title']}\n\n{problem['description']}")
                self.description_text.config(state=tk.DISABLED)

                # Update Code Editor
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(tk.END, problem['starter_code'])
        except Exception as e:
            messagebox.showerror("Error", f"Could not load problem: {str(e)}")

    def save_solution(self):
        try:
            selection = self.problem_listbox.curselection()
            if selection:
                problem_id = int(self.problem_listbox.get(selection[0]).split('.')[0])
                code = self.code_editor.get(1.0, tk.END).strip()

                response = requests.post("http://localhost:8000/save_solution", 
                                         json={"problem_id": problem_id, "code": code})
                result = response.json()
                messagebox.showinfo("Success", result['message'])
            else:
                messagebox.showwarning("Warning", "Please select a problem first")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save solution: {str(e)}")

def main():
    root = tk.Tk()
    app = PythonProblemSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()
