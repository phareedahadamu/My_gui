import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import ImageTk, Image
from models.engine.storage import Storage


class Customer:

    my_bg="white"
    colour1="light grey"
    colour2= "#063970"
    colour3= "#1e81b0"
    colour4= "#e28743"


    def __init__(self, frame):
        self.frame=frame
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
        self.storage = Storage()
        self.table_content = self.storage.read_table(self.__class__.__name__)
        self.create_table(self.table_content)
        self.my_list= tk.Listbox(self.frame, width=50, selectmode='browse', cursor='hand2', selectbackground=self.colour2)
        self.my_list.bind('<<ListboxSelect>>', lambda e: self.assign(e))
        

    def add_page_header(self):
        logo_widget= tk.Label(self.frame, image=self.logo_img, bg=self.my_bg)
        logo_widget.image = self.logo_img
        logo_widget.grid(row=0, column=2, columnspan=7, pady=20)
        txt_wdgt = tk.Label(self.frame, text="Customers", bg=self.my_bg, fg=self.colour2, font=("lucida", 20, "bold")).grid(row=1, column=2, columnspan=7)
        blank= tk.Label(self.frame, text="                         ", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=1, pady=25)
        name_wdgt = tk.Label(self.frame, text="Name", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=2, pady=25, sticky='w')
        namevar = tk.StringVar()
        self.name_entry = tk.Entry(self.frame, relief="ridge", textvariable=namevar, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=50)
        self.name_entry.bind("<KeyRelease>", lambda e, key=namevar: self.search_check(e, namevar))
        self.name_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
        self.name_entry.grid(row=2, column=2, pady=25, columnspan=2, sticky='e')
        search_btn = tk.Button(self.frame, image=self.search, bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=lambda: self.search_table(namevar))
        search_btn.image = self.search
        search_btn.grid(row=2, column=4, pady=25, stick='w', padx=15)
        add_new_btn = tk.Button(self.frame, text="Add new", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=self.add_new_form).grid(row=2, column=5, pady=25, sticky='e')


    def add_header(self):
        header = ["Name", "Email", "Phone number", "Address"]
        for item in range(len(header)):
            my_label= tk.Label(self.frame, text=header[item], relief='ridge', wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.colour4, height=1, width=22, borderwidth=1).grid(row=3, column=item+2)
            

    def create_table(self, content):
        if (len(content)==0):
            return
        row_len = len(content)
        column_len = len(content[0])-1
        for rows in range(row_len):
            for cols in range(column_len):
                my_label= tk.Label(self.frame, text=content[rows][cols], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, height=2, width=22).grid(row=rows+4, column=cols+2)
        
        
        for r in range(row_len):
            edit_btn=tk.Button(self.frame, image=self.edit_img, borderwidth=0, cursor='hand2', bg=self.my_bg)
            edit_btn.image = self.edit_img
            edit_btn.grid(row=r+4, column=column_len+2, padx=5)
            edit_btn.bind('<Button-1>', lambda event: self.update_form(event))
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
            

    def add_new_form(self):
         add_form = Toplevel(self.frame, bg=self.my_bg, width=400, height=400)
         add_form.title('New Customer form')
         c_name = tk.StringVar()
         c_email = tk.StringVar()
         c_phone = tk.StringVar()
         c_address = tk.StringVar()
         my_vars = [c_name, c_email, c_phone, c_address]
         name_wdgt = tk.Label(add_form, text="Name", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=0, column=0, pady=25, sticky='w', padx=10)
         name_entry = tk.Entry(add_form, relief="ridge", textvariable=c_name, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=0, column=1, pady=25, columnspan=2, sticky='w', padx=10)
         email_wdgt = tk.Label(add_form, text="Email", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=1, column=0, pady=25, sticky='w', padx=10)
         email_entry = tk.Entry(add_form, relief="ridge", textvariable=c_email, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=1, column=1, pady=25, columnspan=2, sticky='w', padx=10)
         phone_wdgt = tk.Label(add_form, text="Phone number", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=0, pady=25, sticky='w', padx=10)
         phone_entry = tk.Entry(add_form, relief="ridge", textvariable=c_phone, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=2, column=1, pady=25, columnspan=2, sticky='w', padx=10)
         address_wdgt = tk.Label(add_form, text="Address", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=3, column=0, pady=25, sticky='w', padx=10)
         address_entry = tk.Entry(add_form, relief="ridge", textvariable=c_address, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=3, column=1, pady=25, columnspan=2, sticky='w', padx=10)
         done_btn = tk.Button(add_form, text="Done", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=lambda:self.add_new(add_form, my_vars)).grid(row=4, column=0, columnspan= 3, pady=25)
         add_form.mainloop()

    
    def add_new(self, top, my_vars):
        vars = [i.get() for i in my_vars]
        my_vars = [x.set("") for x in my_vars]
        if ("" in my_vars):
            messagebox.showerror("Error", "Fields cannot be blank")
        else:
            self.storage.create(self.__class__.__name__, vars)
            messagebox.showinfo('Customer Creation', 'Successful!')
            top.destroy()
            for w in self.frame.winfo_children():
                if (len(w.grid_info()) > 0):
                    if(w.grid_info()['row'] >=4):
                        w.destroy()
            result = self.storage.read_table(self.__class__.__name__)
            self.create_table(result)
            

    def delete_row(self, event):
        widget = event.widget
        grid_info = widget.grid_info()
        row=grid_info['row']
        response = messagebox.askyesno('Confirm delete', 'Are you sure?')
        if (response == True):
            for w in self.frame.winfo_children():
                if (len(w.grid_info())>0):
                    if (w.grid_info()['row'] == row and w.grid_info()['column'] == 2):
                        cust = w.cget("text")
                        
            for r in self.storage.read_table(self.__class__.__name__):
                if (r[0]==cust):
                    cust_id=r[4]
            
            self.storage.delete(self.__class__.__name__, cust_id)
            messagebox.showinfo('Successful', 'Customer deleted')
            result = self.storage.read_table(self.__class__.__name__)
            for w in self.frame.winfo_children():
                if (len(w.grid_info()) > 0):
                    if(w.grid_info()['row'] >=4):
                        w.destroy()
            self.create_table(result)


    def update_form(self, event):
        widget = event.widget
        grid_info = widget.grid_info()
        row=grid_info['row']
        cust_details = []
        for w in self.frame.winfo_children():
            if (len(w.grid_info())>0):
                if (w.grid_info()['row'] == row and w.grid_info()['column'] >= 2 and w.grid_info()['column'] < 6):
                        cust_details.append(w.cget("text"))
                        
        up_form=Toplevel(self.frame, background=self.my_bg, width=400, height=400)
        up_form.title('Customer Update form')
        up_name = tk.StringVar()
        up_email = tk.StringVar()
        up_phone = tk.StringVar()
        up_address = tk.StringVar()
        my_vars = [up_name, up_email, up_phone, up_address]
        for i in range(len(cust_details)):
            my_vars[i].set(cust_details[i])
        name_wdgt = tk.Label(up_form, text="Name", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=0, column=0, pady=25, sticky='w', padx=10)
        name_entry = tk.Entry(up_form, relief="ridge", textvariable=up_name, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=0, column=1, pady=25, columnspan=2, sticky='w', padx=10)
        email_wdgt = tk.Label(up_form, text="Email", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=1, column=0, pady=25, sticky='w', padx=10)
        email_entry = tk.Entry(up_form, relief="ridge", textvariable=up_email, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=1, column=1, pady=25, columnspan=2, sticky='w', padx=10)
        phone_wdgt = tk.Label(up_form, text="Phone number", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=0, pady=25, sticky='w', padx=10)
        phone_entry = tk.Entry(up_form, relief="ridge", textvariable=up_phone, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=2, column=1, pady=25, columnspan=2, sticky='w', padx=10)
        address_wdgt = tk.Label(up_form, text="Address", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=3, column=0, pady=25, sticky='w', padx=10)
        address_entry = tk.Entry(up_form, relief="ridge", textvariable=up_address, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=56).grid(row=3, column=1, pady=25, columnspan=2, sticky='w', padx=10)
        update_btn = tk.Button(up_form, text="Update", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=lambda: self.update(up_form, my_vars, cust_details[4])).grid(row=4, column=0, columnspan= 3, pady=25)
        up_form.mainloop()


    def update(self, top, my_vars, id):
        vars = [i.get() for i in my_vars]
        my_vars = [x.set("") for x in my_vars]
        if ("" in vars):
            messagebox.showerror('Error', 'Field cannot be blank')
        else:
            self.storage.update(self.__class__.__name__, vars, id)
            messagebox.showinfo('Customer Update', 'Successful!')
            top.destroy()
            for w in self.frame.winfo_children():
                if (len(w.grid_info()) > 0):
                    if(w.grid_info()['row'] >=4):
                        w.destroy()
            result = self.storage.read_table(self.__class__.__name__)
            self.create_table(result)


    def search_check(self, e, key):
        typed = key.get()
        data = []
        self.my_list.place_forget()
        if (typed != "" and len(self.storage.search(self.__class__.__name__, typed)) !=0):
            self.my_list.place(in_= self.name_entry, rely=1.0)
            result = self.storage.search(self.__class__.__name__, typed)
            for row in result:
                data.append(row[0])
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
