import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
from sqlalchemy import text
from models.engine.storage import Storage
from models.customers import Customer
from models.products import Product
from models.staff import Staff
from models.sales import Sales
from models.dashboard import Dashboard



def driver():
    my_obj= My_gui()
    my_obj.mainloop()


class My_gui(tk.Tk):
    #TODO: Error Handling
    #TODO: Data validation

    
    """My gui application for MySQL database.
    Pages- Dashboard, Sales, Customers, Products, Sales reps"""

    my_bg="white"
    colour1= "#e28743"
    colour2= "#334350"
    colour3= "#7E7B7B"
    storage = Storage()


    def __init__(self):
        """"Initialization"""


        super().__init__()
        self.title("Sales management system")
        self.create_sidebar()
        self.create_container()
        self.load_dashboard()
        

    def create_sidebar(self):
        """" Loads the sidebar with pages buttons"""


        #Dashboard button
        side_bar = tk.Frame(self, bg=self.colour1, width=70).grid(row=0, column=0, rowspan=15, sticky='ns')
        d_image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_ib69b.png")
        d_img=d_image.resize((40, 40))
        dash_image=ImageTk.PhotoImage(d_img)
        butn_wdgt1 = tk.Button(side_bar, image=dash_image, background=self.colour1, borderwidth=0, cursor="hand2", command=lambda:self.load_dashboard())
        butn_wdgt1.image = dash_image
        butn_wdgt1.place(x=15, y=100)

        #Sales orders button
        s_image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_kddca.png")
        s_img=s_image.resize((50, 50))
        sales_image=ImageTk.PhotoImage(s_img)
        butn_wdgt2 = tk.Button(side_bar, image=sales_image, background=self.colour1, borderwidth=0, cursor="hand2", command=lambda:self.load_sales_orders_page())
        butn_wdgt2.image = sales_image
        butn_wdgt2.place(x=10, y=200)

        #Customer Button
        c_image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_a3abp.png")
        cust_img=c_image.resize((40, 40))
        cust_image=ImageTk.PhotoImage(cust_img)
        butn_wdgt1 = tk.Button(side_bar, image=cust_image, background=self.colour1, borderwidth=0, cursor="hand2", command=lambda:self.load_customers_page())
        butn_wdgt1.image = cust_image
        butn_wdgt1.place(x=15, y=300)

        #Product button
        p_image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_f8e1m.png")
        p_img=p_image.resize((40, 40))
        pr_image=ImageTk.PhotoImage(p_img)
        butn_wdgt3 = tk.Button(side_bar, image=pr_image, background=self.colour1, borderwidth=0, cursor="hand2", command=lambda:self.load_products_page())
        butn_wdgt3.image = pr_image
        butn_wdgt3.place(x=15, y=400)

        #Sales reps Button
        r_image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\png_uuoij.png")
        r_img=r_image.resize((40, 40))
        reps_image=ImageTk.PhotoImage(r_img)
        butn_wdgt4 = tk.Button(side_bar, image=reps_image, background=self.colour1, borderwidth=0, cursor="hand2", command=lambda:self.load_reps_page())
        butn_wdgt4.image = reps_image
        butn_wdgt4.place(x=15, y=500)


    def create_container(self):
        """"Creates the pages and scrollbar"""


        container = ttk.Frame(self)
        canvas = tk.Canvas(container, width=980, height=700, bg=self.my_bg)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        container.grid(row=0, column=1, rowspan=15, columnspan=10, sticky='nsew')
        canvas.grid(row=0, column=1, rowspan=15, sticky='nsew')
        scrollbar.grid(row=0, column=11, rowspan=15, sticky='ns')
        self.dashboard_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.customer_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.sales_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.product_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.reps_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.new_order_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.sales_order_frame = tk.Frame(self.scrollable_frame, bg=self.my_bg)
        self.my_frames = [self.dashboard_frame, self.customer_frame, self.sales_frame, self.product_frame, self.reps_frame, self.new_order_frame, self.sales_order_frame]
        for frame in self.my_frames:
            frame.bind_all("<Button-1>", lambda event: self.set_focus(event))
            frame.grid(row=0, column=1, rowspan=15, sticky='nsew')
    

    def load_dashboard(self):
        """"Loads the dashboard page"""


        self.dashboard_frame.tkraise()
        Dashboard(self.dashboard_frame)


    def load_customers_page(self):
        """"Loads the customers page"""


        
        self.customer_frame.tkraise()
        Customer(self.customer_frame)


    def load_sales_orders_page(self):
        """"Loads the sales orders page"""


        self.sales_frame.tkraise()
        Sales(self.sales_frame, self.new_order_frame, self.sales_order_frame)


    def load_products_page(self):
        """"Loads the products page"""


        self.product_frame.tkraise()
        Product(self.product_frame)


    def load_reps_page(self):
        """"Loads the sales reps page"""


        self.reps_frame.tkraise()
        Staff(self.reps_frame)


    def set_focus(self, event):
        """Sets the focus on the widget being clicked on"""


        if (isinstance(event.widget, str)==False):
                event.widget.focus_set()
        

if __name__ == "__main__":
    driver()






