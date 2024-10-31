import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from PIL import ImageTk, Image
from models.engine.storage import Storage
import matplotlib
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from matplotlib.ticker import ScalarFormatter, FuncFormatter


class Dashboard:
    my_bg="white"
    colour1="light grey"
    colour2= "#063970"
    colour3= "#1e81b0"
    colour4= "#e28743"
    storage = Storage()

    def __init__(self, frame):
        self.frame = frame
        image=Image.open(r"D:\Training\Data Analysis\Python\crm_db_gui\assets\2-removebg-preview.png")
        img=image.resize((100, 39))
        self.logo_img = ImageTk.PhotoImage(img)
        logo_widget= tk.Label(self.frame, image=self.logo_img, bg=self.my_bg)
        logo_widget.image = self.logo_img
        logo_widget.grid(row=0, column=2, columnspan=8, pady=10)
        blank= tk.Label(self.frame, text="     ", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=1)
        blank= tk.Label(self.frame, text="     ", bg=self.my_bg, fg=self.colour2, font=("lucida", 10, "bold"), justify="left").grid(row=2, column=4)
        self.sales_per_month()
        self.plot_gauge()
        self.highest_product()
        self.highest_rep()
        #self.months_total()


    def sales_per_month(self):
        orders = self.storage.read_table('Sales')
        months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        total_sales = {}
        for key in months:
            total = 0
            total_sales[key] = 0
            for row in orders:
                if (months[key]==row[4].month):
                    if (row[4].year == date.today().year):
                        total_sales[key]=total_sales[key]+row[2]
        x = total_sales.keys()
        y = total_sales.values()
        fig = Figure(figsize=(6,3))
        figure_canvas = FigureCanvasTkAgg(fig, self.frame)
        axes = fig.add_subplot()
        axes.plot(x, y)
        axes.set_title('Sales per month', fontsize=8, color=self.colour2)
        axes.set_ylabel('Total Sales', fontsize=8, color=self.colour2)
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.ticklabel_format(style="plain", axis="y")
        axes.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'₦{int(x):,}'))
        axes.tick_params(axis='y', labelsize=8)
        axes.tick_params(axis='x', labelsize=8)
        for label in axes.get_xticklabels():
            label.set_color("grey")
        for label in axes.get_yticklabels():
            label.set_color("grey")
        for spine in axes.spines.values():
            spine.set_edgecolor("grey")
        fig.tight_layout()
        figure_canvas.get_tk_widget().grid(row=1, column=2, columnspan=2)


    def highest_product(self):
        products = self.storage.read_table('Sales_Order')
        my_dict = {}

        for p in products:
            if (p[2] not in my_dict):
                my_dict[p[2]]=0
        for key in my_dict:
            for p in products:
                if (p[2]==key):
                    my_dict[key]=my_dict[key]+p[4]

        
        top3= {}
        for i in range(3):
            max=0
            max_product=""
            for key in my_dict:
                if (my_dict[key] > max):
                    max = my_dict[key]
                    max_product=key
            top3[max_product]=max
            my_dict.pop(max_product)

        x = top3.keys()
        y = top3.values()
        x_labels = [labels.replace(' ', '\n') for labels in x]
        fig = Figure(figsize=(3, 3))
        figure_canvas = FigureCanvasTkAgg(fig, self.frame)
        axes = fig.add_subplot()
        axes.bar(x_labels, y, width=0.4)
        axes.set_title('Best selling products', fontsize=8, color=self.colour2)
        axes.set_ylabel('Number sold', fontsize=8, color=self.colour2)
        axes.tick_params(axis='y', labelsize=8)
        axes.tick_params(axis='x', labelsize=8)
        for label in axes.get_xticklabels():
            label.set_color("grey")
        for label in axes.get_yticklabels():
            label.set_color("grey")
        for spine in axes.spines.values():
            spine.set_edgecolor("grey")
        fig.tight_layout()
        figure_canvas.get_tk_widget().grid(row=2, column=3)

    
    def highest_rep(self):
        rep = self.storage.read_table('Sales')
        my_dict = {}

        for r in rep:
            if (r[3] not in my_dict):
                my_dict[r[3]]=0
        for key in my_dict:
            for r in rep:
                if (r[3]==key):
                    my_dict[key]=my_dict[key]+r[2]

        
        top3= {}
        for i in range(3):
            max=0
            max_product=""
            for key in my_dict:
                if (my_dict[key] > max):
                    max = my_dict[key]
                    max_product=key
            top3[max_product]=max
            my_dict.pop(max_product)
        x = top3.keys()
        y = top3.values()
        x_labels = [labels.replace(' ', '\n') for labels in x]
        fig = Figure(figsize=(3, 3))
        figure_canvas = FigureCanvasTkAgg(fig, self.frame)
        axes = fig.add_subplot()
        axes.bar(x_labels, y, width=0.4)
        axes.set_title('Best selling Reps', fontsize=8, color=self.colour2)
        axes.set_ylabel('Total Sales', fontsize=8, color=self.colour2)
        axes.yaxis.set_major_formatter(ScalarFormatter())
        axes.ticklabel_format(style="plain", axis="y")
        axes.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'₦{int(x):,}'))
        axes.tick_params(axis='y', labelsize=8)
        axes.tick_params(axis='x', labelsize=8)
        for label in axes.get_xticklabels():
            label.set_color("grey")
        for label in axes.get_yticklabels():
            label.set_color("grey")
        for spine in axes.spines.values():
            spine.set_edgecolor("grey")
        fig.tight_layout()
        figure_canvas.get_tk_widget().grid(row=2, column=2)

    
    def plot_gauge(self):
        fr= tk.Frame(self.frame, background=self.my_bg, highlightbackground="grey", highlightthickness=1, width=320, height=530).grid(row=1, column=5, rowspan=3)
        info = self.storage.read_table('Sales')
        amount_sold = 0
        for row in info:
            if (row[4].year==date.today().year):
                amount_sold = amount_sold + row[2]
        amount_sold = float(amount_sold)
        target = 40000000
        target = float(target)
        fig, ax = plt.subplots(figsize=(3, 0.3))
        ax.barh(0, target, color='lightgrey', height=0.1)
        ax.barh(0, amount_sold, color='orange', height=0.1)
        ax.set_yticks([])
        ax.set_xticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.get_tk_widget().grid(row=1, column=5)
        mylabel= tk.Label(self.frame, text='{}%'.format(round((amount_sold*100)/target)), font=("lucida", 8), fg=self.colour2, bg=self.my_bg).place(x=685, y=180)
        mylabel= tk.Label(self.frame, text='₦{}m'.format(str(target)[:2]), font=("lucida", 8), fg=self.colour2, bg=self.my_bg).place(x=890, y=180)
        mylabel= tk.Label(self.frame, text='{} sales'.format(date.today().year), font=("lucida", 10), fg=self.colour2, bg=self.my_bg).place(x=685, y=110)
        mylabel= tk.Label(self.frame, text='₦{:,}'.format(int(amount_sold)), font=("lucida", 15, "bold"), fg=self.colour2, bg=self.my_bg).place(x=685, y=130)
        month_sales=0
        for row in info:
            if (row[4].month==date.today().month and row[4].year==date.today().year):
                month_sales+=row[2]
        month_sales = float(month_sales)
        mylabel= tk.Label(self.frame, text='{} {} sales'.format(date.today().strftime("%B"), date.today().year), font=("lucida", 10), fg=self.colour2, bg=self.my_bg).place(x=685, y=300)
        mylabel= tk.Label(self.frame, text='₦{:,}'.format(int(month_sales)), font=("lucida", 15, "bold"), fg=self.colour2, bg=self.my_bg).place(x=685, y=320)
        avg=amount_sold/date.today().month
        mylabel= tk.Label(self.frame, text='{} Avg. monthly sales'.format(date.today().year), font=("lucida", 10), fg=self.colour2, bg=self.my_bg).place(x=685, y=420)
        mylabel= tk.Label(self.frame, text='₦{:,}'.format(round(avg)), font=("lucida", 15, "bold"), fg=self.colour2, bg=self.my_bg).place(x=685, y=440)
        count=0
        for row in info:
            if (row[4].year==date.today().year):
                count+=1

        mylabel= tk.Label(self.frame, text='{} Avg. number of jobs per month'.format(date.today().year), font=("lucida", 10), fg=self.colour2, bg=self.my_bg).place(x=685, y=530)
        mylabel= tk.Label(self.frame, text='{}'.format(round(count/date.today().month)), font=("lucida", 15, "bold"), fg=self.colour2, bg=self.my_bg).place(x=685, y=550)