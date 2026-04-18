import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB = dict(host='localhost', user='root', password='root', database='lab_db')

def db():
    return mysql.connector.connect(**DB)

def login():
    c = db()
    cur = c.cursor()
    cur.execute("SELECT id, full_name FROM users WHERE login=%s AND password=%s",
                (e_login.get(), e_pwd.get()))
    r = cur.fetchone()
    c.close()
    if r:
        root.destroy()
        main(r[0], r[1])
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

def main(uid, uname):
    w = tk.Tk()
    w.title(f"Лаборатория — {uname}")
    w.geometry("750x500")

    tk.Label(w, text="Пациенты").pack()
    tp = ttk.Treeview(w, columns=('id','fio','dob','phone'), show='headings', height=5)
    for c, t in zip(('id','fio','dob','phone'), ('ID','ФИО','Дата рожд.','Телефон')):
        tp.heading(c, text=t)
    tp.pack(fill='x')

    tk.Label(w, text="Анализы (справочник)").pack()
    tt = ttk.Treeview(w, columns=('id','name','unit','norm'), show='headings', height=4)
    for c, t in zip(('id','name','unit','norm'), ('ID','Анализ','Ед.','Норма')):
        tt.heading(c, text=t)
    tt.pack(fill='x')

    tk.Label(w, text="Проведённые исследования").pack()
    ts = ttk.Treeview(w, columns=('id','pat','test','date','res'), show='headings', height=5)
    for c, t in zip(('id','pat','test','date','res'), ('ID','Пациент','Анализ','Дата','Результат')):
        ts.heading(c, text=t)
    ts.pack(fill='x')

    def reload():
        for tv in (tp, tt, ts):
            for i in tv.get_children(): tv.delete(i)
        c = db(); cur = c.cursor()
        cur.execute("SELECT id, full_name, birth_date, phone FROM patients")
        for r in cur.fetchall(): tp.insert('', 'end', values=r)
        cur.execute("SELECT id, name, unit, norm FROM tests")
        for r in cur.fetchall(): tt.insert('', 'end', values=r)
        cur.execute("""SELECT s.id, p.full_name, t.name, s.study_date,
                       CONCAT(s.result,' ',IFNULL(t.unit,''))
                       FROM studies s
                       JOIN patients p ON s.patient_id=p.id
                       JOIN tests t ON s.test_id=t.id
                       ORDER BY s.id""")
        for r in cur.fetchall(): ts.insert('', 'end', values=r)
        c.close()

    f = tk.Frame(w); f.pack(pady=8)
    tk.Label(f, text="Пациент ID:").grid(row=0, column=0)
    e_pid = tk.Entry(f, width=5); e_pid.grid(row=0, column=1)
    tk.Label(f, text="Анализ ID:").grid(row=0, column=2)
    e_tid = tk.Entry(f, width=5); e_tid.grid(row=0, column=3)
    tk.Label(f, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=4)
    e_dt = tk.Entry(f, width=12); e_dt.grid(row=0, column=5)
    tk.Label(f, text="Результат:").grid(row=0, column=6)
    e_res = tk.Entry(f, width=10); e_res.grid(row=0, column=7)

    def add():
        try:
            c = db(); cur = c.cursor()
            cur.execute("""INSERT INTO studies
                           (patient_id, test_id, user_id, study_date, result)
                           VALUES (%s,%s,%s,%s,%s)""",
                        (e_pid.get(), e_tid.get(), uid, e_dt.get(), e_res.get()))
            c.commit(); c.close()
            for e in (e_pid, e_tid, e_dt, e_res): e.delete(0, 'end')
            reload()
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))

    tk.Button(f, text="Добавить", command=add).grid(row=0, column=8, padx=5)
    tk.Button(w, text="Обновить", command=reload).pack()
    reload()
    w.mainloop()

root = tk.Tk()
root.title("Авторизация")
root.geometry("260x160")
tk.Label(root, text="Логин:").pack()
e_login = tk.Entry(root); e_login.pack()
tk.Label(root, text="Пароль:").pack()
e_pwd = tk.Entry(root, show='*'); e_pwd.pack()
tk.Button(root, text="Войти", command=login).pack(pady=10)
root.mainloop()
