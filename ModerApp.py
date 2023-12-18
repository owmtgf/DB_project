import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from sqlalchemy import create_engine, MetaData
from sqlalchemy import text
from DBActions import DeleteAll


def GetText(entry_block):
    try:
        text = entry_block.get()
    except:
        text = entry_block.get("1.0", tk.END)
    return text


def UpdateLists():
    global dbs, tables, pg_connection, meta
    dbs = pg_connection.execute(text("SELECT * FROM get_all_dbs();")).fetchall()
    dbs = [i[0] for i in dbs]
    meta = MetaData()
    meta.reflect(bind=tab_engine)
    tables = list(meta.tables.keys())


def CreateTable(name, params, create_window):
    global dbs, tables
    name = GetText(name)
    params = GetText(params).rstrip('\n').replace('\n', ', ')
    if params == '':
        messagebox.showerror('Ошибка', 'Введите параметры.')
    else:
        params = f"({params})"
        tab_connection.execute(text(f"SELECT create_table('{name}', '{params}')"))
        tab_connection.commit()
        UpdateLists()
        messagebox.showinfo('Успех', f'Таблица "{name}" успешно создана.')
        create_window.destroy()
        Window()


def DropTable(combobox):
    global dbs, tables
    name = GetText(combobox)
    if name == '':
        messagebox.showerror('Ошибка', 'Вы не ввели имя таблицы.')
    else:
        tab_connection.execute(text(f"SELECT drop_table('{name}')"))
        tab_connection.commit()
        UpdateLists()
        messagebox.showinfo('Успех', f'Таблица "{name}" успешно удалена.')
        Window()


def CreateDB(name):
    global dbs, tables
    name = GetText(name)
    if name == '':
        messagebox.showerror('Ошибка', 'Вы не ввели имя базы данных.')
    elif name in dbs:
        messagebox.showerror('Ошибка', f'База данных с именем "{name}" уже существует.')
    else:
        pg_connection.execute(text(f"CREATE DATABASE {name}"))
        UpdateLists()
        messagebox.showinfo('Успех', f'База данных "{name}" успешно создана.')
        Window()


def DropDB(combobox):
    global dbs, tables
    name = GetText(combobox)
    if name == '':
        messagebox.showerror('Ошибка', 'Вы не ввели имя базы данных.')
    elif name == 'postgres':
        messagebox.showerror('Ошибка', 'Базу данных невозможно удалить, ввиду ее использования в целях модерации.')
    else:
        pg_connection.execute((text(f"DROP DATABASE {name}")))
        pg_connection.commit()
        UpdateLists()
        messagebox.showinfo('Успех', f'База данных "{name}" успешно удалена.')
        Window()


def DeleteAllTablesFill():
    global dbs, tables
    for table in tables:
        DeleteAll(table)
    messagebox.showinfo('Успех', 'Все таблицы очищены.')


def CreateTableWindow(name):
    global dbs, tables
    print(GetText(name))
    if GetText(name) == '':
        messagebox.showerror('Ошибка', 'Вы не ввели имя таблицы.')
    elif GetText(name) in tables:
        messagebox.showerror('Ошибка', f'Таблица с именем "{GetText(name)}" уже существует.')
    else:
        create_window = tk.Tk()
        create_window.geometry(f'575x450+100+50')
        create_window.resizable(False, False)

        create_window.title('Ввод')
        create_frame = tk.Frame(create_window)
        create_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        title = tk.Label(create_frame, text='Введите столбцы и типы:')
        params = tk.Text(create_frame, width=70)
        button = ttk.Button(create_frame, text='Создать', width=20, command=lambda: CreateTable(name, params, create_window))

        title.grid(row=0, column=0, sticky='w', padx=5)
        params.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        button.grid(row=2, column=0, padx=5, pady=5)

        create_frame.rowconfigure(0, weight=1)
        create_frame.rowconfigure(1, weight=10)
        create_frame.rowconfigure(2, weight=1)


def Window():
    global dbs, tables

    frame = tk.Frame(window)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    db_title = tk.Label(frame, text='Работа с базой данных')
    db_choose = ttk.Combobox(frame, values=dbs)

    create_db_button = ttk.Button(frame, text='Создать базу данных', command=lambda: CreateDB(db_name_entry))
    db_name = tk.Label(frame, text='Имя:')
    db_name_entry = tk.Entry(frame)

    delete_db_button = ttk.Button(frame, text='Удалить базу данных', command=lambda: DropDB(db_choose))

    table_title = tk.Label(frame, text='Работа с таблицами')
    table_choose = ttk.Combobox(frame, values=tables)
    create_table_button = ttk.Button(frame, text='Создать таблицу', command=lambda: CreateTableWindow(table_name_entry))
    table_name = tk.Label(frame, text='Имя:')
    table_name_entry = tk.Entry(frame)

    delete_table_button = ttk.Button(frame, text='Удалить таблицу', command=lambda: DropTable(table_choose))

    delete_fill_button = ttk.Button(frame, text='Удалить содержимое всех таблиц', command=DeleteAllTablesFill)
    delete_fill_button.grid(row=5, column=2, columnspan=2, sticky='ew', padx=5)

    db_title.grid(row=0, column=0, columnspan=2, sticky='ew')
    db_choose.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)
    create_db_button.grid(row=2, column=0, columnspan=2, sticky='sew', padx=5, pady=5)
    db_name.grid(row=3, column=0, sticky='nw', padx=5)
    db_name_entry.grid(row=3, column=1, sticky='new', padx=10)
    delete_db_button.grid(row=4, column=0, columnspan=2, sticky='ew', padx=5)

    table_title.grid(row=0, column=2, columnspan=2, sticky='ew')
    table_choose.grid(row=1, column=2, columnspan=2, sticky='ew', padx=5)
    create_table_button.grid(row=2, column=2, columnspan=2, sticky='sew', padx=5, pady=5)
    table_name.grid(row=3, column=2, sticky='nw', padx=5)
    table_name_entry.grid(row=3, column=3, sticky='new', padx=10)
    delete_table_button.grid(row=4, column=2, columnspan=2, sticky='ew', padx=5)

    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=2)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=2)
    frame.rowconfigure(5, weight=2)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=10)
    frame.columnconfigure(2, weight=1)
    frame.columnconfigure(3, weight=10)


pg_engine = create_engine('postgresql://app_user:prikolist@localhost:1488/postgres', echo=False, isolation_level="AUTOCOMMIT")
pg_connection = pg_engine.connect()


dbs = pg_connection.execute(text("SELECT get_all_dbs();")).fetchall()

dbs = [i[0] for i in dbs]
print(dbs)

tab_engine = create_engine('postgresql://app_user:prikolist@localhost:1488/Market', echo=False)
tab_connection = tab_engine.connect()
meta = MetaData()
meta.reflect(bind=tab_engine)
tables = list(meta.tables.keys())
print(tables)

window = tk.Tk()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.geometry(f'500x200+{screen_width//2-250}+{screen_height//2-100}')
window.resizable(False, False)
window.title('Модерация')


Window()

window.mainloop()


