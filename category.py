from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+320+220")
        self.root.title("product category"  )
        self.root.config(bg="white")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ------------ Variables -------------
        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        # --------------- Title ---------------------
        lbl_title = Label(self.root, text="Manage Product Category", font=("goudy old style", 30),
                          bg="skyblue", fg="white", bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        # ------------ Input Fields -------------
        lbl_name = Label(self.root, text="Enter Category Name", font=("goudy old style", 20), bg="white")
        lbl_name.place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name, bg="lightyellow", font=("goudy old style", 18))
        txt_name.place(x=50, y=150, width=300)
        txt_name.focus()

        btn_add = Button(self.root, text="ADD", command=self.add, font=("goudy old style", 15),
                         bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=150, width=150, height=30)

        btn_delete = Button(self.root, text="Delete", command=self.delete, font=("goudy old style", 15),
                            bg="red", fg="white", cursor="hand2")
        btn_delete.place(x=520, y=150, width=150, height=30)

        # ------------ Category Details (at the bottom) -------------
        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=50, y=250, width=1000, height=230)  # Adjusted position and size

        title_cat_list = Label(cat_frame, text="Category List", font=("goudy old style", 15),
                               bg="skyblue", fg="white")
        title_cat_list.pack(side=TOP, fill=X)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)

        self.CategoryTable = ttk.Treeview(cat_frame, columns=("cid", "name"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CategoryTable.xview)
        scrolly.config(command=self.CategoryTable.yview)
        self.CategoryTable.heading("cid", text="C ID")
        self.CategoryTable.heading("name", text="Name")
        self.CategoryTable["show"] = "headings"
        self.CategoryTable.column("cid", width=100)
        self.CategoryTable.column("name", width=300)

        self.CategoryTable.pack(fill=BOTH, expand=1)
        self.CategoryTable.bind("<ButtonRelease-1>", self.get_data)
        self.show()

    # ----------------------------------------------------------------------------------
    def add(self):
        name = self.var_name.get().strip()
        if name == "":
            messagebox.showerror("Error", "Category Name must be required", parent=self.root)
            return

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category WHERE name=?", (name,))
            if cur.fetchone():
                messagebox.showerror("Error", "Category already exists", parent=self.root)
            else:
                cur.execute("INSERT INTO category(name) VALUES(?)", (name,))
                con.commit()
                messagebox.showinfo("Success", "Category Added Successfully", parent=self.root)
                self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.CategoryTable.delete(*self.CategoryTable.get_children())
            for row in rows:
                self.CategoryTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear(self):
        self.var_name.set("")
        self.show()

    def get_data(self, ev):
        f = self.CategoryTable.focus()
        content = self.CategoryTable.item(f)
        row = content['values']
        if row:
            self.var_cat_id.set(row[0])
            self.var_name.set(row[1])

    def delete(self):
        cat_id = self.var_cat_id.get()
        if cat_id == "":
            messagebox.showerror("Error", "Please select a category to delete", parent=self.root)
            return

        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category WHERE cid=?", (cat_id,))
            if not cur.fetchone():
                messagebox.showerror("Error", "Invalid Category ID", parent=self.root)
            else:
                if messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root):
                    cur.execute("DELETE FROM category WHERE cid=?", (cat_id,))
                    con.commit()
                    messagebox.showinfo("Delete", "Category Deleted Successfully", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
