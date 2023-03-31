import random
import tkinter as tk
from tkinter import ttk
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_rec()


    def init_main(self):

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)


        btn_best = tk.Button(toolbar, text="Хорошие дни", command=self.open_best, bg='light green', bd=3,compound=tk.TOP)
        btn_best.pack(side=tk.RIGHT)
        btn_worse = tk.Button(toolbar, text="Дни похуже", command=self.open_worse, bg='light blue', bd=3,compound=tk.TOP)
        btn_worse.pack(side=tk.RIGHT)

        btn_winter = tk.Button(toolbar, text="Зима", command=self.open_winter, bd=2, compound=tk.TOP)
        btn_winter.pack(side=tk.TOP)
        btn_winter.place(x=350, y=3)
        btn_spring = tk.Button(toolbar, text="Весна", command=self.open_spring, bd=2, compound=tk.TOP)
        btn_spring.pack(side=tk.TOP)
        btn_spring.place(x=348, y=33)
        btn_summer = tk.Button(toolbar, text="Лето", command=self.open_summer, bd=2, compound=tk.TOP)
        btn_summer.pack(side=tk.TOP)
        btn_summer.place(x=350, y=63)
        btn_fall = tk.Button(toolbar,  text="Осень", command=self.open_fall, bd=2, compound=tk.TOP)
        btn_fall.pack(side=tk.TOP)
        btn_fall.place(x=347, y=93)

        btn_stat = tk.Button(toolbar, text="Статистика по месяцам", command=self.open_stat, compound=tk.TOP)
        btn_stat.pack()
        btn_stat.place(x = 450, y=10)

        btn_stat_w = tk.Button(toolbar, text="Статистика за неделю", command=self.show_stat_week,
                             compound=tk.TOP)
        btn_stat_w.pack()
        btn_stat_w.place(x=450, y=85)

        self.add_img = tk.PhotoImage(file="cup.gif")
        btn_open_dialog = tk.Button(toolbar, text="Вода", command=self.open_dialog_water, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.add_img2 = tk.PhotoImage(file="sleep.gif")
        btn_open_dialog2 = tk.Button(toolbar, text="Сон", command=self.open_dialog_sleep, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img2 )
        btn_open_dialog2.pack(side=tk.LEFT)

        self.add_img3 = tk.PhotoImage(file="sport.gif")
        btn_open_dialog3 = tk.Button(toolbar, text="Активность", command=self.open_dialog_sport, bg='#d7d8e0', bd=0,
                                     compound=tk.TOP, image=self.add_img3 )
        btn_open_dialog3.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('Date', 'Water', 'Sleep', 'Sport'), height=15, show='headings')

        self.tree.column('Date', width=145, anchor=tk.CENTER)
        self.tree.column('Water', width=145, anchor=tk.CENTER)
        self.tree.column('Sleep', width=145, anchor=tk.CENTER)
        self.tree.column('Sport', width=145, anchor=tk.CENTER)

        self.tree.heading('Date', text='Дата, ММДДГГГ')
        self.tree.heading('Water', text='Вода, стаканы')
        self.tree.heading('Sleep', text='Сон, часы')
        self.tree.heading('Sport', text='Активность, минуты')

        self.tree.pack(side='bottom')

        btn_moto = tk.Button(self, text="Получить поддержку", command=self.lab)
        btn_moto.pack(side='top')

    def lab(self):
        m=tk.Toplevel()
        m.view=app
        m.title("Ты не один")
        m.geometry("450x50+300+400")
        ch = random.randint(0,4)
        self.db.c.execute('''SELECT moto FROM moto''')
        t = self.db.c.fetchall()[ch][0]
        lab = tk.Label(m, text=str(t))
        lab.place(x=30, y=15)

    def update_water(self, date, water):
        self.db.c.execute('''UPDATE water SET water=? WHERE date=?''',
                          (water, date))
        self.db.conn.commit()


    def update_sleep(self, date, sleep):
        self.db.c.execute('''UPDATE sleep SET sleep=? WHERE date=?''',
                          (sleep, date))
        self.db.conn.commit()
        self.open_dialog_sleep()

    def update_sport(self, date, sport):
        self.db.c.execute('''UPDATE sport SET sport=? WHERE date=?''',
                          (sport, date))
        self.db.conn.commit()
        self.open_dialog_sport()

    def record_water(self, date, water):
        self.db.insert_water(date, water)
        self.view_rec()

    def record_sleep(self, date, sleep):
        self.db.insert_sleep(date, sleep)
        self.view_rec()

    def record_sport(self, date, sport):
        self.db.insert_sport(date, sport)
        self.view_rec()

    def view_rec(self):
        self.db.c.execute('''SELECT water.date, water.water, sleep.sleep, sport.sport 
        FROM water JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date
         ORDER BY water.date DESC''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_stat(self):
        stat = tk.Toplevel()
        stat.view=app
        stat.title("Статистика по месяцам")
        stat.geometry('320x80+400+300')
        stat.resizable(False, False)
        label_stat = tk.Label(stat, text="Выберите показатель")
        label_stat.place(x=100, y=10)

        combo = ttk.Combobox(stat, values=['Вода', 'Сон', 'Активность'])


        btn_wat = tk.Button(stat, text="Вода", command=self.show_water_month, bd=2)
        btn_wat.pack()
        btn_wat.place(x=50, y=40)

        btn_sleep = tk.Button(stat, text="Сон", command=self.show_sleep_month, bd=2)
        btn_sleep.pack()
        btn_sleep.place(x=130, y=40)

        btn_sport = tk.Button(stat, text="Активность", command=self.show_sport_month, bd=2)
        btn_sport.pack()
        btn_sport.place(x=200, y=40)

    def show_water_month(self):
        znach = []
        self.db.c.execute('''SELECT SUM(water) FROM water WHERE date LIKE '01%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water) FROM water WHERE date LIKE '02%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '03%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '04%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '05%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '06%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '07%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '08%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '09%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '10%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '11%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(water.water) FROM water WHERE date LIKE '12%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)


        months=["Янв","Фев","Март","Апр","Май","Июн","Июл","Авг","Сент","Окт","Нояб","Дек"]

        fig, ax = plt.subplots()
        color_rec = [[0.45471839, 0.92970341, 0.43199191, 0.75123214]]
        ax.bar(months, znach, color=color_rec, width=0.6)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        plt.show()

    def show_sleep_month(self):
        znach = []
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '01%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '02%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '03%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '04%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '05%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '06%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '07%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '08%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '09%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '10%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '11%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sleep) FROM sleep WHERE date LIKE '12%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)


        months=["Янв","Фев","Март","Апр","Май","Июн","Июл","Авг","Сент","Окт","Нояб","Дек"]

        fig, ax = plt.subplots()
        color_rec = [[0.2184069,  0.07235148, 0.87257637, 0.42588282]]
        ax.bar(months, znach, color=color_rec, width=0.6)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        plt.show()

    def show_sport_month(self):
        znach = []
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '01%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '02%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '03%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '04%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '05%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '06%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '07%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '08%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '09%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '10%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '11%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)
        self.db.c.execute('''SELECT SUM(sport) FROM sport WHERE date LIKE '12%' ''')
        znach.append(self.db.c.fetchall()[0][0] or 0)


        months=["Янв","Фев","Март","Апр","Май","Июн","Июл","Авг","Сент","Окт","Нояб","Дек"]

        fig, ax = plt.subplots()
        color_rec = [[0.77782451, 0.84204563, 0.34805547, 1]]
        ax.bar(months, znach, color=color_rec, width=0.6)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        plt.show()

    def show_stat_week(self):
        self.db.c.execute('''SELECT water.date, water.water, sleep.sleep, sport.sport 
        FROM water JOIN sleep on sleep.date=water.date JOIN sport on sport.date=water.date GROUP BY water.date ORDER BY water.date LIMIT 7''')
        x_w, y_w, y_sl, y_sp = [], [], [], []
        for row in self.db.c.fetchall():
            x_w.append(row[0][2:4]+'.'+row[0][:2])
            y_w.append(int(row[1])*100/8)
            y_sl.append(int(row[2])*100/7)
            y_sp.append(int(row[3])*100/40)
        fig, ax = plt.subplots()

        color_rectangle_w = [[0.19587479, 0.33520324, 0.67584163]]
        #color_rectangle_w[:, 3] = 0.7
        ax.bar(x_w, y_w, color=color_rectangle_w, width=0.3, label="Вода, %", alpha=1)

        color_rectangle_sl = [[0.83911514, 0.24102614, 0.54884459]]
        #color_rectangle_sl[0][3] = 0.7
        ax.bar(x_w, y_sl, color=color_rectangle_sl, width=0.5, label="Сон, %", alpha=0.7)

        color_rectangle_sp = [[0.46048208, 0.91164316, 0.05277555, 0.70178657]]
        # color_rectangle_sl[0][3] = 0.7
        ax.bar(x_w, y_sp, color=color_rectangle_sp, width=0.7, label="Активность, %", alpha=0.5)
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        ax.legend()
        plt.show()


    def open_winter(self):
        wnt = tk.Toplevel()
        wnt.view = app
        wnt.title("Твоя зима")
        wnt.geometry('460x50+400+300')
        wnt.resizable(False, False)
        wnt.tree = ttk.Treeview(wnt, yscrollcommand=True, columns=('Water', 'Sleep', 'Sport'), height=15, show='headings')
        wnt.tree.column('Water', width=160, anchor=tk.CENTER)
        wnt.tree.column('Sleep', width=160, anchor=tk.CENTER)
        wnt.tree.column('Sport', width=160, anchor=tk.CENTER)
        wnt.tree.heading('Water', text='Вода, стаканы')
        wnt.tree.heading('Sleep', text='Сон, часы')
        wnt.tree.heading('Sport', text='Спорт, минуты')
        wnt.tree.pack()
        self.db.c.execute(
            '''SELECT SUM(water.water), SUM(sleep.sleep), SUM(sport.sport) FROM water 
            JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date 
            WHERE water.date BETWEEN '01012023' AND '02282023' ''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        [wnt.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_spring(self):
        spr = tk.Toplevel()
        spr.view = app
        spr.title("Твоя весна")
        spr.geometry('460x50+400+300')
        spr.resizable(False, False)
        spr.tree = ttk.Treeview(spr, yscrollcommand=True, columns=('Water', 'Sleep', 'Sport'), height=15, show='headings')
        spr.tree.column('Water', width=160, anchor=tk.CENTER)
        spr.tree.column('Sleep', width=160, anchor=tk.CENTER)
        spr.tree.column('Sport', width=160, anchor=tk.CENTER)
        spr.tree.heading('Water', text='Вода, стаканы')
        spr.tree.heading('Sleep', text='Сон, часы')
        spr.tree.heading('Sport', text='Спорт, минуты')
        spr.tree.pack()
        self.db.c.execute(
            '''SELECT SUM(water.water), SUM(sleep.sleep), SUM(sport.sport) FROM water 
            JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date 
            WHERE water.date BETWEEN '03012023' AND '05012023' ''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        [spr.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_summer(self):
        smr = tk.Toplevel()
        smr.view = app
        smr.title("Твое лето")
        smr.geometry('460x100+400+300')
        smr.resizable(False, False)
        smr.tree = ttk.Treeview(smr, yscrollcommand=True, columns=('Water', 'Sleep', 'Sport'), height=15, show='headings')
        smr.tree.column('Water', width=160, anchor=tk.CENTER)
        smr.tree.column('Sleep', width=160, anchor=tk.CENTER)
        smr.tree.column('Sport', width=160, anchor=tk.CENTER)
        smr.tree.heading('Water', text='Вода, стаканы')
        smr.tree.heading('Sleep', text='Сон, часы')
        smr.tree.heading('Sport', text='Спорт, минуты')
        smr.tree.pack()
        self.db.c.execute(
            '''SELECT SUM(water.water), SUM(sleep.sleep), SUM(sport.sport) FROM water 
            JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date 
            WHERE water.date BETWEEN '06012023' AND '08012023' ''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        [smr.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_fall(self):
        fall = tk.Toplevel()
        fall.view = app
        fall.title("Твоя осень")
        fall.geometry('460x100+400+300')
        fall.resizable(False, False)
        fall.tree = ttk.Treeview(fall, yscrollcommand=True, columns=('Water', 'Sleep', 'Sport'), height=15,
                                show='headings')
        fall.tree.column('Water', width=160, anchor=tk.CENTER)
        fall.tree.column('Sleep', width=160, anchor=tk.CENTER)
        fall.tree.column('Sport', width=160, anchor=tk.CENTER)
        fall.tree.heading('Water', text='Вода, стаканы')
        fall.tree.heading('Sleep', text='Сон, часы')
        fall.tree.heading('Sport', text='Спорт, минуты')
        fall.tree.pack()
        self.db.c.execute(
            '''SELECT SUM(water.water), SUM(sleep.sleep), SUM(sport.sport) FROM water 
            JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date 
            WHERE water.date BETWEEN '09012023' AND '11012023' ''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        [fall.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_best(self):
        best = tk.Toplevel()
        best.view = app
        best.title("Отличная работа")
        best.geometry('300x400+400+300')
        best.resizable(False, False)
        best.tree = ttk.Treeview(best, yscrollcommand=True, columns=('Date'), height=15, show='headings')
        best.tree.column('Date', width=260, anchor=tk.CENTER)
        best.tree.heading('Date', text='Дата')
        best.tree.pack()
        self.db.c.execute(
            '''SELECT water.date FROM water JOIN sleep ON sleep.date = water.date 
            JOIN sport ON sport.date = water.date WHERE water.water > 7 AND sleep.sleep > 6 AND sport.sport>=40 ORDER BY water.date''')
        #[self.tree.delete(i) for i in self.tree.get_children()]
        [best.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_worse(self):
        worse = tk.Toplevel()
        worse.view = app
        worse.title("Ты можешь лучше")
        worse.geometry('300x400+400+300')
        worse.resizable(False, False)
        worse.tree = ttk.Treeview(worse, yscrollcommand=True, columns=('Date'), height=15, show='headings')
        worse.tree.column('Date', width=260, anchor=tk.CENTER)
        worse.tree.heading('Date', text='Дата')
        worse.tree.pack()
        self.db.c.execute(
            '''SELECT water.date FROM water JOIN sleep ON sleep.date = water.date JOIN sport ON sport.date = water.date
            WHERE water.water <= 7 AND sleep.sleep <= 6 AND sport.sport<40 ORDER BY water.date''')
        # [self.tree.delete(i) for i in self.tree.get_children()]
        [worse.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog_water(self):
        wat = tk.Toplevel()
        #wat.wat_db = self.db
        wat.view = app
        #wat.view.view_wat_rec()
        wat.title("Добавить воду")
        wat.geometry('600x400+400+300')
        wat.resizable(False, False)

        #toolbar_wat = tk.Frame(bg='#d7d8e0', bd=2)
        #toolbar_wat.pack(side=tk.TOP, fill=tk.X)

        label_date = tk.Label(wat, text="Дата, ММДДГГГ")
        label_date.place(x=10, y=10)

        label_water = tk.Label(wat, text="Количество стаканов")
        label_water.place(x=10, y=40)

        wat.entry_date = ttk.Entry(wat)
        wat.entry_date.place(x=200, y=10)

        wat.entry_water = ttk.Entry(wat)
        wat.entry_water.place(x=200, y=40)

        btn_cancel = ttk.Button(wat, text="Закрыть", command=wat.destroy)
        btn_cancel.place(x=500, y=40)

        btn_ok = ttk.Button(wat, text="Добавить")
        btn_ok.place(x=420, y=40)
        btn_ok.bind('<Button-1>', lambda event: wat.view.record_water(wat.entry_date.get(), wat.entry_water.get()))

        btn_upd = ttk.Button(wat, text='Изменить')
        btn_upd.place(x=460, y=10)
        btn_upd.bind('<Button-1>', lambda event: wat.view.update_water(wat.entry_date.get(), wat.entry_water.get()))

        wat.grab_set()
        wat.focus_set()

        wat.tree = ttk.Treeview(wat, yscrollcommand=True, columns=('Date', 'Water'), height=15, show='headings')

        wat.tree.column('Date', width=260, anchor=tk.CENTER)
        wat.tree.column('Water', width=260, anchor=tk.CENTER)

        wat.tree.heading('Date', text='Дата, ММДДГГГ')
        wat.tree.heading('Water', text='Вода, стаканы')

        wat.tree.pack(padx=30, pady=70)

        self.db.c.execute('''SELECT date, SUM(water) FROM water GROUP BY date ORDER BY date''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [wat.tree.insert('', 0 , values=row) for row in self.db.c.fetchall()]

    def open_dialog_sleep(self):
        slp = tk.Toplevel()
        #wat.wat_db = self.db
        slp.view = app
        #wat.view.view_wat_rec()
        slp.title("Добавить сон")
        slp.geometry('600x400+400+300')
        slp.resizable(False, False)

        #toolbar_wat = tk.Frame(bg='#d7d8e0', bd=2)
        #toolbar_wat.pack(side=tk.TOP, fill=tk.X)

        label_date = tk.Label(slp, text="Дата, ММДДГГГ")
        label_date.place(x=10, y=10)

        label_sleep = tk.Label(slp, text="Количество часов")
        label_sleep.place(x=10, y=40)

        slp.entry_date = ttk.Entry(slp)
        slp.entry_date.place(x=200, y=10)

        slp.entry_sleep = ttk.Entry(slp)
        slp.entry_sleep.place(x=200, y=40)

        btn_cancel = ttk.Button(slp, text="Закрыть", command=slp.destroy)
        btn_cancel.place(x=500, y=40)

        btn_ok = ttk.Button(slp, text="Добавить")
        btn_ok.place(x=420, y=40)
        btn_ok.bind('<Button-1>', lambda event: slp.view.record_sleep(slp.entry_date.get(), slp.entry_sleep.get()))

        btn_upd = ttk.Button(slp, text='Изменить')
        btn_upd.place(x=460, y=10)
        btn_upd.bind('<Button-1>', lambda event: slp.view.update_sleep(slp.entry_date.get(), slp.entry_sleep.get()))

        slp.grab_set()
        slp.focus_set()

        slp.tree = ttk.Treeview(slp, yscrollcommand=True, columns=('Date', 'Sleep'), height=15, show='headings')

        slp.tree.column('Date', width=260, anchor=tk.CENTER)
        slp.tree.column('Sleep', width=260, anchor=tk.CENTER)

        slp.tree.heading('Date', text='Дата, ММДДГГГ')
        slp.tree.heading('Sleep', text='Сон, часы')

        slp.tree.pack(padx=30, pady=70)

        self.db.c.execute('''SELECT * FROM sleep ORDER BY date''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [slp.tree.insert('', 0 , values=row) for row in self.db.c.fetchall()]

    def open_dialog_sport(self):
        spt = tk.Toplevel()
        #wat.wat_db = self.db
        spt.view = app
        #wat.view.view_wat_rec()
        spt.title("Добавить активность")
        spt.geometry('600x400+400+300')
        spt.resizable(False, False)

        #toolbar_wat = tk.Frame(bg='#d7d8e0', bd=2)
        #toolbar_wat.pack(side=tk.TOP, fill=tk.X)

        label_date = tk.Label(spt, text="Дата, ММДДГГГ")
        label_date.place(x=10, y=10)

        label_sport = tk.Label(spt, text="Количество минут")
        label_sport.place(x=10, y=40)

        spt.entry_date = ttk.Entry(spt)
        spt.entry_date.place(x=200, y=10)

        spt.entry_sport = ttk.Entry(spt)
        spt.entry_sport.place(x=200, y=40)

        btn_cancel = ttk.Button(spt, text="Закрыть", command=spt.destroy)
        btn_cancel.place(x=500, y=40)

        btn_ok = ttk.Button(spt, text="Добавить")
        btn_ok.place(x=420, y=40)
        btn_ok.bind('<Button-1>', lambda event: spt.view.record_sport(spt.entry_date.get(), spt.entry_sport.get()))

        btn_upd = ttk.Button(spt, text='Изменить')
        btn_upd.place(x=460, y=10)
        btn_upd.bind('<Button-1>', lambda event: spt.view.update_sleep(spt.entry_date.get(), spt.entry_sport.get()))

        spt.grab_set()
        spt.focus_set()

        spt.tree = ttk.Treeview(spt, yscrollcommand=True, columns=('Date', 'Sport'), height=15, show='headings')

        spt.tree.column('Date', width=260, anchor=tk.CENTER)
        spt.tree.column('Sport', width=260, anchor=tk.CENTER)

        spt.tree.heading('Date', text='Дата, ММДДГГГ')
        spt.tree.heading('Sport', text='Спорт, минуты')

        spt.tree.pack(padx=30, pady=70)

        self.db.c.execute('''SELECT * FROM sport ORDER BY date''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [spt.tree.insert('', 0 , values=row) for row in self.db.c.fetchall()]



# class Child(tk.Toplevel):
#     def __int__(self):
#         super().__init__(root)
#         self.init_child()
#
#     def init_child(self):
#         self.title("Добавить данные сегодняшнего дня")
#         self.geometry('400x220+400+300')
#         self.resizable(False, False)
#
#         label_date = tk.Label(self, text="Дата")
#         label_date.place(x=50, y=50)
#
#         label_water = tk.Label(self, text="Количество стаканов")
#         label_water.place(x=50, y=80)
#
#         self.entry_date = ttk.Entry(self)
#         self.entry_date.place(x=200, y=50)
#
#         self.entry_water = ttk.Entry(self)
#         self.entry_water.place(x=200, y=110)
#
#         btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
#         btn_cancel.place(x=300,y=80)
#
#         btn_ok = ttk.Button(self, text="Добавить")
#         btn_ok.place(x=220, y=170)
#         btn_ok.bind('<Button-1>')
#
#         self.grab_set()
#         self.focus_set()

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('habits.db')
        self.c = self.conn.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS water(date text primary key, water integer)'''
        )
        self.conn.commit()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS sleep(date text primary key, sleep integer)'''
        )
        self.conn.commit()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS sport(date text primary key, sport integer)'''
        )
        self.conn.commit()

    def insert_water(self, date, water):
        self.c.execute('''INSERT INTO water(date, water) VALUES (?, ?)''', (date, water))
        self.conn.commit()

    def insert_sleep(self, date, sleep):
        self.c.execute('''INSERT INTO sleep(date, sleep) VALUES (?, ?)''', (date, sleep))
        self.conn.commit()

    def insert_sport(self, date, sport):
        self.c.execute('''INSERT INTO sport(date, sport) VALUES (?, ?)''', (date, sport))
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Habits Tracker")
    root.geometry("610x500+300+200")
    root.resizable(False, False)
    root.mainloop()

