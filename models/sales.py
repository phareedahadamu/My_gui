import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from PIL import ImageTk, Image
from models.engine.storage import Storage
from .orders import Orders
from .sales_order import Sales_Order


class Sales:

    my_bg="white"
    colour1="light grey"
    colour2= "#063970"
    colour3= "#1e81b0"
    colour4= "#e28743"
    storage = Storage()


    def __init__(self, frame, frame2, frame3):
        self.frame=frame
        self.frame2 =frame2
        self.frame3 =frame3
        image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\2-removebg-preview.png")
        img=image.resize((100, 39))
        self.logo_img = ImageTk.PhotoImage(img)
        image2=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_1596r.png")
        img2=image2.resize((20, 20))
        self.search = ImageTk.PhotoImage(img2)
        image3=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_ubl0p.png")
        img3=image3.resize((20, 20))
        self.trash = ImageTk.PhotoImage(img3)
        image4=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_mix61.png")
        img4=image4.resize((12,12))
        self.edit_img = ImageTk.PhotoImage(img4)
        self.add_page_header()
        self.add_header()
        self.table_content = self.storage.read_table(self.__class__.__name__)
        self.create_table(self.table_content)
        self.my_list= tk.Listbox(self.frame, width=50, selectmode='browse', cursor='hand2', selectbackground=self.colour2)
        self.my_list.bind('<<ListboxSelect>>', lambda e: self.assign(e))


    def add_page_header(self):
        
        logo_widget= tk.Label(self.frame, image=self.logo_img, bg=self.my_bg)
        logo_widget.image = self.logo_img
        logo_widget.grid(row=0, column=2, columnspan=8, pady=20)
        txt_wdgt = tk.Label(self.frame, text="Sales Orders", bg=self.my_bg, fg=self.colour2, font=("lucida", 20, "bold")).grid(row=1, column=2, columnspan=8)
        blank= tk.Label(self.frame, text="                     ", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=1, pady=25)
        name_wdgt = tk.Label(self.frame, text="Name", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=2, pady=25, sticky='w')
        namevar = tk.StringVar()
        self.name_entry = tk.Entry(self.frame, relief="ridge", textvariable=namevar, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=50)
        self.name_entry.bind("<KeyRelease>", lambda e, key=namevar: self.search_check(e, namevar))
        self.name_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
        self.name_entry.grid(row=2, column=3, pady=25, columnspan=2, sticky='w')
        search_btn = tk.Button(self.frame, image=self.search, bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=lambda: self.search_table(namevar))
        search_btn.image = self.search
        search_btn.grid(row=2, column=5, pady=25, stick='w')
        add_new_btn = tk.Button(self.frame, text="Add new", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=self.add_new).grid(row=2, column=6, pady=25, sticky='e')


    def add_header(self):
        header = ["ID", "Customer", "Amount", "Sales Rep", "Order date"]
        for item in range(len(header)):
            if (item==0):
                my_label= tk.Label(self.frame, text=header[item], relief='ridge', wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.colour4, height=1, width=7, borderwidth=1).grid(row=3, column=item+2)
            else:
                my_label= tk.Label(self.frame, text=header[item], relief='ridge', wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.colour4, height=1, width=22, borderwidth=1).grid(row=3, column=item+2)
            

    def create_table(self, content):
        if (len(content)==0):
            return
        row_len = len(content)
        column_len = len(content[0])
        for rows in range(row_len):
            for cols in range(column_len):
                if (cols == 0):
                    my_label= tk.Label(self.frame, text=content[rows][cols], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, height=2, width=7).grid(row=rows+4, column=cols+2)
                else:
                    my_label= tk.Label(self.frame, text=content[rows][cols], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, height=2, width=22).grid(row=rows+4, column=cols+2)
        for r in range(row_len):
            edit_btn=tk.Button(self.frame, image=self.edit_img, borderwidth=0, cursor='hand2', bg=self.my_bg)
            edit_btn.image = self.edit_img
            edit_btn.grid(row=r+4, column=column_len+2, padx=5)
            edit_btn.bind('<Button-1>', lambda event: self.update(event))
            del_btn=tk.Button(self.frame, image=self.trash, borderwidth=0, cursor='hand2', bg=self.my_bg)
            del_btn.image = self.trash
            del_btn.grid(row=r+4, column=column_len+3, padx=5)
            del_btn.bind('<Button-1>', lambda event: self.delete_row(event))


    def search_table(self, my_var):
        keyword = my_var.get()
        my_var.set("")
        if (keyword == ""):
            messagebox.showerror('Error', 'Enter search keyword')
        else:
            result = self.storage.search(self.__class__.__name__, keyword)
            for w in self.frame.winfo_children():
                if (len(w.grid_info()) > 0):
                    if(w.grid_info()['row'] >=4):
                        w.destroy()
            self.create_table(result)

    
    def add_new(self):
        for w in self.frame2.winfo_children():
            w.destroy()
        self.frame2.tkraise()
        Orders(self.frame2, self.frame3)


    def delete_row(self, event):
        widget = event.widget
        grid_info = widget.grid_info()
        row=grid_info['row']
        response = messagebox.askyesno('Confirm delete', 'Are you sure?')
        if (response == True):
            for w in self.frame.winfo_children():
                if (len(w.grid_info())>0):
                    if (w.grid_info()['row'] == row and w.grid_info()['column'] == 2):
                        r_id = int(w.cget("text"))
            self.storage.delete(self.__class__.__name__, r_id)
            messagebox.showinfo('Successful', 'Sales Rep deleted')
            result = self.storage.read_table(self.__class__.__name__)
            for w in self.frame.winfo_children():
                if (len(w.grid_info()) > 0):
                    if(w.grid_info()['row'] >=4):
                        w.destroy()
            self.create_table(result)


    def update(self, event):
        row_num = event.widget.grid_info()['row']
        for w in self.frame.winfo_children():
            if (len(w.grid_info())>0):
                if (w.grid_info()['row'] == row_num and w.grid_info()['column'] == 2):
                    id = int(w.cget("text"))
        for w in self.frame3.winfo_children():
            w.destroy()
        self.frame3.tkraise()
        Sales_Order(self.frame3, id)
         

    def search_check(self, e, key):
        typed = key.get()
        data = []
        self.my_list.place_forget()
        if (typed != "" and len(self.storage.search(self.__class__.__name__, typed)) !=0):
            self.my_list.place(in_=self.name_entry, rely=1.0)
            result = self.storage.search(self.__class__.__name__, typed)
            for row in result:
                if (row[1] not in data):
                    data.append(row[1])
            self.update_list(data)

            
    def update_list(self, data):
        self.my_list.delete(0, 'end')
        for item in data:
            self.my_list.insert('end', item)
    

    def assign(self, e):
        result = self.storage.search(self.__class__.__name__, self.my_list.get('anchor'))
        for w in self.frame.winfo_children():
            if (len(w.grid_info()) > 0):
                if(w.grid_info()['row'] >=4):
                    w.destroy()
        self.create_table(result)
    

    def close_listbox(self, e):
        self.my_list.place_forget()