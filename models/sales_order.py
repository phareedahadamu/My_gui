import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from PIL import ImageTk, Image
from models.engine.storage import Storage


class Sales_Order:

    my_bg="white"
    colour1="light grey"
    colour2= "#063970"
    colour3= "#1e81b0"
    colour4= "#e28743"
    storage = Storage()

    def __init__(self, frame, id):
        self.frame=frame
        self.id = id
        image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\2-removebg-preview.png")
        img=image.resize((100, 39))
        self.logo_img = ImageTk.PhotoImage(img)
        image2=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_ubl0p.png")
        img2=image2.resize((20, 20))
        self.trash = ImageTk.PhotoImage(img2)
        self.my_amountvars = []
        self.vars_bank = []
        self.add_page_header()
        self.add_header()
        order_info = self.storage.read_table(self.__class__.__name__)
        content = []
        for i in order_info:
            if (i[1]==self.id):
                content.append(i)
        self.create_table(content)
        self.add_product()
        self.cust_list= tk.Listbox(self.frame, width=50, selectmode='browse', cursor='hand2', selectbackground=self.colour2)
        self.cust_list.bind('<<ListboxSelect>>', lambda e: self.customer_assign(e))
        self.rep_list= tk.Listbox(self.frame, width=50, selectmode='browse', cursor='hand2', selectbackground=self.colour2)
        self.rep_list.bind('<<ListboxSelect>>', lambda e: self.rep_assign(e))
        self.prod_list= tk.Listbox(self.frame, width=22, selectmode='browse', cursor='hand2', selectbackground=self.colour2)
        self.prod_list.bind('<<ListboxSelect>>', lambda e: self.product_assign(e))


    def add_page_header(self):
        order_details = self.storage.search(self.__class__.__name__, self.id)
        logo_widget= tk.Label(self.frame, image=self.logo_img, bg=self.my_bg)
        logo_widget.image = self.logo_img
        logo_widget.grid(row=0, column=2, columnspan=8, pady=10)
        txt_wdgt = tk.Label(self.frame, text="Sales Order", bg=self.my_bg, fg=self.colour2, font=("lucida", 20, "bold")).grid(row=1, column=2, columnspan=8, pady=5)
        save_btn = tk.Button(self.frame, text="Save", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2", command=lambda:self.save_order()).grid(row=1, column=7, columnspan=2, sticky='e')
        blank= tk.Label(self.frame, text="           ", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=1)
        name_wdgt = tk.Label(self.frame, text="Name", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=2, sticky='w')
        self.namevar = tk.StringVar()
        self.namevar.set(order_details[0][1])
        name_entry = tk.Entry(self.frame, relief="ridge", textvariable=self.namevar, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=50)
        name_entry.bind("<KeyRelease>", lambda e, key=self.namevar: self.cust_search_check(e, self.namevar))
        name_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
        name_entry.grid(row=2, column=3, columnspan=2, sticky='w')
        date_wdgt = tk.Label(self.frame, text="Date", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=5, sticky='e')
        self.datevar= tk.StringVar()
        self.datevar.set(order_details[0][4])
        date_entry = tk.Entry(self.frame, relief="ridge", textvariable=self.datevar, bg=self.colour1, fg=self.colour2, borderwidth=2, width=20).grid(row=2, column=6, sticky='w', padx=15, pady=5)
        rep_wdgt = tk.Label(self.frame, text="Sales rep", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=3, column=2, pady=10, sticky='w')
        self.repvar = tk.StringVar()
        self.repvar.set(order_details[0][3])
        rep_entry = tk.Entry(self.frame, relief="ridge", textvariable=self.repvar, bg=self.colour1, fg=self.colour2, borderwidth=2, cursor="tcross", width=50)
        rep_entry.bind("<KeyRelease>", lambda e, key=self.namevar: self.rep_search_check(e, self.repvar))
        rep_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
        rep_entry.grid(row=3, column=3, columnspan=2, sticky='w')
        id_wdgt = tk.Label(self.frame, text="Order ID", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=3, column=5, sticky='e')
        self.idvar = tk.StringVar()
        self.idvar.set(self.id)
        id_entry = tk.Label(self.frame, relief="ridge", textvariable=self.idvar, bg=self.colour1, fg=self.colour2, borderwidth=2, width=17).grid(row=3, column=6, sticky='w', padx=15)
         

    def add_header(self):
        self.row_pos = 5
        header = ["Product", "Description", "Price", "Quantity", "Amount"]
        for item in range(len(header)):
            if (item==3):
                my_label= tk.Label(self.frame, text=header[item], relief='ridge', wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.colour4, height=1, width=7, borderwidth=1).grid(row=4, column=item+2)
            else:
                my_label= tk.Label(self.frame, text=header[item], relief='ridge', wraplength=150, justify="center", font=("lucida", 10, "bold"), fg=self.colour2, bg=self.colour4, height=1, width=22, borderwidth=1).grid(row=4, column=item+2)
        
        
    def create_table(self, content):
        row_len = len(content)
        column_len = 6
        for rows in range(row_len):
            my_vars = ['prodvar{}'.format(str(self.row_pos)), 'descvar{}'.format(str(self.row_pos)), 'pricevar{}'.format(str(self.row_pos)), 'qtyvar{}'.format(str(self.row_pos)), 'amountvar{}'.format(str(self.row_pos))]
            vars=[]
            for v in my_vars:
                v= tk.StringVar()
                vars.append(v)
            vars.append(self.row_pos)
            vars.append('old')
            vars.append(content[rows][0])
            self.vars_bank.append(vars)
            for cols in range(column_len):
                if (cols==0):
                    self.vars_bank[self.row_pos-5][0].set(content[rows][2])
                    prod_entry= tk.Entry(self.frame, relief="ridge", textvariable=self.vars_bank[self.row_pos-5][0], borderwidth=0, font=("lucida", 10), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, width=25)
                    prod_entry.bind("<KeyRelease>", lambda e: self.product_search_check(e))
                    prod_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
                    prod_entry.grid(row=self.row_pos, column=2)
                if (cols==1):
                    self.vars_bank[self.row_pos-5][1].set(self.storage.search('Order_product', content[rows][2])[0][1])
                    desc_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][1], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
                    desc_label.grid(row=self.row_pos, column=3)
                if (cols==2):
                    self.vars_bank[self.row_pos-5][2].set(content[rows][3])
                    price_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][2], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
                    price_label.grid(row=self.row_pos, column=4)
                if (cols==3):
                    self.vars_bank[self.row_pos-5][3].set(content[rows][4])
                    qty_entry= tk.Entry(self.frame, relief="ridge", textvariable=self.vars_bank[self.row_pos-5][3], borderwidth=0, font=("lucida", 10), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, width=8)
                    qty_entry.bind("<KeyRelease>", lambda e: self.assign_amount(e))
                    qty_entry.grid(row=self.row_pos, column=5)   
                if (cols==4):
                    amount = float(self.vars_bank[self.row_pos-5][2].get()) * int(self.vars_bank[self.row_pos-5][3].get())
                    self.vars_bank[self.row_pos-5][4].set(amount)
                    amount_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][4], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
                    amount_label.grid(row=self.row_pos, column=6)
                if (cols==5):
                    del_btn=tk.Button(self.frame, image=self.trash, borderwidth=0, cursor='hand2', bg=self.my_bg)
                    del_btn.image = self.trash
                    del_btn.grid(row=self.row_pos, column=7, padx=5)
                    del_btn.bind('<Button-1>', lambda e: self.delete_row(e))
            self.row_pos = self.row_pos+1
    
    
    def add_product(self):
        self.btn_pos = self.row_pos
        self.row_btn = tk.Button(self.frame, text="Add", bg=self.colour2, font=('lucida', 10), fg=self.my_bg, activebackground=self.my_bg, activeforeground=self.colour2, cursor="hand2")
        self.row_btn.bind("<Button-1>", lambda e: self.add_row(e))
        self.row_btn.grid(row=self.btn_pos, column=2, columnspan=6, pady=10)
        self.total_wdgt = tk.Label(self.frame, text="Total", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=self.btn_pos+1, column=5, sticky='e')
        self.totalvar = tk.StringVar()
        self.totalvar.set(self.storage.search(self.__class__.__name__, self.id)[0][2])
        self.total_entry = tk.Label(self.frame, textvariable=self.totalvar, borderwidth=0, font=("lucida", 12, 'bold'), fg=self.colour2, bg=self.my_bg).grid(row=self.btn_pos+1, column=6)
    

    def add_row(self,e):
        for w in self.frame.winfo_children():
            if (len(w.grid_info()) > 0):
                if (w.grid_info()['row'] == self.btn_pos+1):
                    w.destroy()
        
        self.btn_pos = self.btn_pos+1
        e.widget.forget()
        e.widget.grid(row=self.btn_pos, column=2, columnspan=6, pady=10)
        self.total_wdgt = tk.Label(self.frame, text="Total", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=self.btn_pos+1, column=5, sticky='e')
        self.total_entry = tk.Label(self.frame, relief="ridge", textvariable=self.totalvar, borderwidth=0, font=("lucida", 12, 'bold'), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1).grid(row=self.btn_pos+1, column=6)
        
        
        my_vars = ['prodvar{}'.format(str(self.row_pos)), 'descvar{}'.format(str(self.row_pos)), 'pricevar{}'.format(str(self.row_pos)), 'qtyvar{}'.format(str(self.row_pos)), 'amountvar{}'.format(str(self.row_pos))]
        vars=[]
        for v in my_vars:
            v= tk.StringVar()
            vars.append(v)
        vars.append(self.row_pos)
        vars.append('new')
        self.vars_bank.append(vars)
        prod_entry= tk.Entry(self.frame, relief="ridge", textvariable=self.vars_bank[self.row_pos-5][0], borderwidth=0, font=("lucida", 10), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, width=25)
        prod_entry.bind("<KeyRelease>", lambda e: self.product_search_check(e))
        prod_entry.bind("<FocusOut>", lambda e: self.close_listbox(e), add='+')
        prod_entry.grid(row=self.row_pos, column=2)
        desc_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][1], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
        desc_label.grid(row=self.row_pos, column=3)
        price_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][2], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
        price_label.grid(row=self.row_pos, column=4)
        qty_entry= tk.Entry(self.frame, relief="ridge", textvariable=self.vars_bank[self.row_pos-5][3], borderwidth=0, font=("lucida", 10), fg=self.colour2, bg=self.my_bg, highlightbackground=self.colour1, highlightthickness=1, width=8)
        qty_entry.bind("<KeyRelease>", lambda e: self.assign_amount(e))
        qty_entry.grid(row=self.row_pos, column=5)
        amount_label= tk.Label(self.frame, textvariable=self.vars_bank[self.row_pos-5][4], relief='ridge', borderwidth=0, wraplength=150, justify="center", font=("lucida", 10), fg=self.colour2, bg=self.my_bg, height=2, width=22)
        amount_label.grid(row=self.row_pos, column=6)
        del_btn=tk.Button(self.frame, image=self.trash, borderwidth=0, cursor='hand2', bg=self.my_bg)
        del_btn.image = self.trash
        del_btn.grid(row=self.row_pos, column=7, padx=5)
        del_btn.bind('<Button-1>', lambda e: self.delete_row(e))
        self.row_pos = self.row_pos+1


    def delete_row(self, event):
        row = event.widget.grid_info()['row']
        for v in self.vars_bank:
            if (v[5]==row):
                if (v[6] =='old'):
                    self.storage.delete(self.__class__.__name__, int(v[7]))
                    print(v[7], type(v[7]))
                if (v[4].get() != ""):
                    t = float(self.totalvar.get())
                    self.totalvar.set(t-float(v[4].get()))
                self.vars_bank.remove(v)
                for w in self.frame.winfo_children():
                    info=w.grid_info()
                    if (len(info)>0):
                        if (info['row'] == row):
                            w.destroy()

                #elif (v[6] =='old'):
            #         if (v[4].get() != ""):
            #             t = float(self.totalvar.get())
            #             self.totalvar.set(t-float(v[4].get()))
            #         id = self.storage.read_table(self.__class__.__name__)[v[5]-5][0]
            #         self.storage.delete(self.__class__.__name__, id)
            #         self.vars_bank.remove(v)
            # for w in self.frame.winfo_children():
            #             info=w.grid_info()
            #             if (len(info)>0):
            #                 if (info['row'] == row):
            #                     w.destroy()


    def cust_search_check(self, e, key):
        typed = key.get()
        data = []
        self.cust_list.place_forget()
        if (typed != "" and len(self.storage.search('Order_customer', typed)) !=0):
            self.cust_list.place(in_=e.widget, rely=1.0)
            result = self.storage.search('Order_customer', typed)
            for row in result:
                data.append(row[0])
            self.update_list(self.cust_list, data)
    

    def rep_search_check(self, e, key):
        typed = key.get()
        data = []
        self.rep_list.place_forget()
        if (typed != "" and len(self.storage.search('Order_rep', typed)) !=0):
            self.rep_list.place(in_=e.widget, rely=1.0)
            result = self.storage.search('Order_rep', typed)
            for row in result:
                data.append(row[0])
            self.update_list(self.rep_list, data)


    def product_search_check(self, e):
        widget = e.widget
        grid_info = widget.grid_info()
        rows=grid_info['row']
        for v in self.vars_bank:
            if (v[5]==rows):
                typed = v[0].get()
        data = []
        self.prod_list.place_forget()
        if (typed != "" and len(self.storage.search('Order_product', typed)) !=0):
            self.prod_list.place(in_=e.widget, rely=1.0)
            result = self.storage.search('Order_product', typed)
            for row in result:
                data.append(row[0])
            self.update_list(self.prod_list, data)

            
    def update_list(self, my_list, data):
        my_list.delete(0, 'end')
        for item in data:
            my_list.insert('end', item)
    

    def customer_assign(self, e):
        self.namevar.set(self.cust_list.get('anchor'))


    def rep_assign(self, e):
        self.repvar.set(self.rep_list.get('anchor'))


    def product_assign(self, e):
        widget = e.widget
        place_info = widget.place_info()
        parent=place_info['in']
        rows = parent.grid_info()['row']
        for v in self.vars_bank:
            if (rows==v[5]):
                v[0].set(self.prod_list.get('anchor'))
                row = self.storage.search('Order_product', self.prod_list.get('anchor'))[0]
                v[2].set(row[2])
                v[1].set(row[1])


    def assign_amount(self, e):
        widget = e.widget
        grid_info = widget.grid_info()
        rows=grid_info['row']
        for v in self.vars_bank:
            if (rows==v[5]):
                if (v[3].get()=="") :
                    v[4].set('0')
                elif(v[3].get().isdigit()==True):
                    amount = float(v[2].get()) * int(v[3].get())
                    v[4].set(str(amount))
                else:
                    messagebox.showerror('Error', 'Please enter a whole number')
        total = 0
        for v in self.vars_bank:
            if (v[4].get()!=""):
                total = total+float(v[4].get())
        self.totalvar.set(total)
            

    def close_listbox(self, e):
        self.cust_list.place_forget()
        self.rep_list.place_forget()
        self.prod_list.place_forget()


    def clear_page(self):
        for w in self.frame.winfo_children():
            w.destroy()
    

    def save_order(self):
        log_args = [self.namevar.get(), self.totalvar.get(), self.repvar.get(), self.datevar.get()]
        self.storage.update('Order_log', log_args, self.idvar.get())
        for v in self.vars_bank:
            if (v[6]=='old'):
                self.storage.update('Order_info', [v[0].get(), v[2].get(), v[3].get()], v[7])
            elif (v[6]=='new'):
                self.storage.create('Orders', [self.idvar.get(), v[0].get(), v[2].get(), v[3].get()])
        messagebox.showinfo('Order update', 'Successful')
        