import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk
import hash_search
import authorization_check as checks
import DBActions as act

index = ''
categories = ['Все',
              'Процессоры',
              'Графические карты',
              'Материнские платы',
              'Оперативная память',
              'Блоки питания',
              'Постоянная память',
              'Система охлаждения',
              'Корпусы']

nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

bucket_items = []
items = []
indices = []

user_id = 1
user_name = ''
user_surname = ''
status = ''


def IsDigit(text):
    try:
        int(text)
        return True
    except:
        return False


def RefreshTable(is_selected=False):
    global items, indices
    selected_indices = [0, 1, 3, 4, 5]
    items = []
    indices = []

    if is_selected:
        temp_items = act.products_selected
    else:
        temp_items = act.products

    for item in temp_items:
        elem = []
        for i in selected_indices:
            elem.append(item[i])
        indices.append(item[0])
        items.append(elem[1:])


def SelectedItems(text):
    global items, indices
    act.products_selected = []
    text.strip()
    text.rstrip()
    for item in act.products:
        if hash_search.find_all_elems(item[-1], text.lower()):
            act.products_selected.append(item)


def FirteredItems(tree, filter_entry, sort_option='Не сортировать', option_state='По возрастанию'):
    filter_entry = GetText(filter_entry)
    if sort_option != 'Не сортировать':
        sort_option = GetText(sort_option)
        option_state = option_state.get()

    act.GetTableData(filter_entry,
                     sort_option,
                     option_state)
    DrawTree(tree)


def DrawTree(tree, is_selected=False, text=''):
    global items, indices
    if is_selected:
        SelectedItems(text)
    tree.delete(*tree.get_children())
    RefreshTable(is_selected)
    iid = 1
    for item in items:
        tree.insert("", tk.END, iid=f'{iid}', values=item, tags='multiline')
        iid += 1


def ParseIndex(index):
    return int(index) - 1


def ReconType(text):
    flag = True
    text = text.strip()
    text = text.rstrip()
    for symb in text:
        if symb not in nums:
            flag = False
            break
    if flag:
        return text
    else:
        return f"''{text}''"


def FormatForDB(arr):
    st = "'("
    for i in arr:
        st += f"{i}, "
    st = st[:-2]
    st += ")'"
    return st


def GetText(entry_block):
    try:
        text = entry_block.get()
    except:
        text = entry_block.get("1.0", tk.END)
    return text


def get_all_items(tree):
    all_items = []
    for item_id in tree.get_children():
        item = tree.item(item_id)
        all_items.append(item['values'])
    return all_items


def SetText(entry_block, text):
    try:
        entry_block.insert(0, text)
    except:
        entry_block.insert(1.0, text)


def CheckData():
    # status = True
    status = False
    if status:
        MainWindow()
    else:
        UserWindow()


def on_entry_click(search_entry):
    if search_entry.get() == 'Поиск по каталогу:':
        search_entry.delete(0, tk.END)


def on_treeview_click(tree):
    global index
    index = tree.focus()
    print(index)


def EditDBWindow(tree, idx):
    element = tk.Tk()
    element.geometry(f'700x550+{screen_width // 2 - 350}+{screen_height // 2 - 300}')
    element.resizable(False, False)
    # element.resizable(True, True)
    element.title('Добавление позиции')

    element_frame = tk.Frame(element)
    element_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    title_label = tk.Label(element_frame, text='Название:')
    category_label = tk.Label(element_frame, text='Категория:')
    description_label = tk.Label(element_frame, text='Описание:')
    price_label = tk.Label(element_frame, text='Цена, руб.:')
    amount_label = tk.Label(element_frame, text='Количество, шт.:')

    title = tk.Entry(element_frame, width=60)
    category = ttk.Combobox(element_frame, values=categories, width=30)
    description = tk.Text(element_frame, width=70)
    price = tk.Entry(element_frame)
    amount = tk.Entry(element_frame)

    add_item_btn = ttk.Button(element_frame, text='Применить', width=20)

    title_label.grid(row=1, column=0, sticky='nw')
    title.grid(row=1, column=1, sticky='w', pady=5, padx=5)
    category_label.grid(row=2, column=0, sticky='nw')
    category.grid(row=2, column=1, sticky='w', pady=5, padx=5)
    description_label.grid(row=3, column=0, sticky='nw')
    description.grid(row=3, column=1, sticky='we', pady=5, padx=5)
    price_label.grid(row=4, column=0, sticky='nw')
    price.grid(row=4, column=1, sticky='w', pady=5, padx=5)
    amount_label.grid(row=5, column=0, sticky='nw')
    amount.grid(row=5, column=1, sticky='w', pady=5, padx=5)
    add_item_btn.grid(row=6, column=0, columnspan=2)

    return element, title, category, description, price, amount, add_item_btn, idx


def DeleteItem(tree, summary_entry=None, key=False):
    global index, offset
    print(index)
    if index != '':
        values = tree.item(index)['values']  # элемент для удаления
        tree.delete(index)  # удаление элемента из treeview
        if key:
            bucket_items.remove(values)
            order_price = 0
            for item in bucket_items:
                order_price += int(item[1]) * int(item[2])
            summary_entry.config(state=tk.NORMAL)
            summary_entry.delete(0, tk.END)
            summary_entry.insert(0, order_price)
            summary_entry.config(state=tk.DISABLED)
        else:
            print('Parsed index:', ParseIndex(index))
            index_from_db = indices[ParseIndex(index)]
            print('Index from db:', index_from_db)
            act.DeleteItem(index_from_db)
            RefreshTable()
            RefreshTable(True)
            if status:
                MainWindow()
            else:
                UserWindow()

        index = ''

    else:
        messagebox.showerror('Ошибка', 'Сначала выберите позицию.')


def AddItem(tree):
    element, title, category, description, price, amount, apply_btn, idx = EditDBWindow(tree, index)
    element.title('Добавление позиции')
    apply_btn.config(command=lambda: ApplyChanges('w', element, idx, tree, title, category, description, price, amount))


def EditItem(tree):
    global index
    print(index)
    if index != '':

        element, title, category, description, price, amount, apply_btn, idx = EditDBWindow(tree, index)
        apply_btn.config(
            command=lambda: ApplyChanges('e', element, idx, tree, title, category, description, price, amount))
        element.title('Редактирование позиции')

        initial_values = tree.item(index)['values']
        SetText(title, initial_values[0])
        SetText(category, 'Default')
        SetText(description, initial_values[1])
        SetText(price, initial_values[2])
        SetText(amount, initial_values[3])

        index = ''
    else:
        messagebox.showerror('Ошибка', 'Сначала выберите позицию.')


def ApplyChanges(key, edit_window, idx, tree, title, category, description, price, amount):
    new_values = [GetText(title), GetText(category), GetText(description), GetText(price), GetText(amount)]
    new_values[0] = new_values[0].replace("'", '"')
    new_values[2] = new_values[2].replace("'", '"').replace('\n', ' ')
    desc = new_values[2]
    while '  ' in desc:
        desc = desc.replace('  ', ' ')
    new_values[2] = desc
    if ' ' in new_values or '' in new_values or '\n' in new_values:
        messagebox.showerror('Ошибка редактирования', 'Заполните все поля.')
    else:
        if not IsDigit(new_values[3]) or not IsDigit(new_values[4]):
            messagebox.showerror('Ошибка', 'Введите корректные значения цены и количества.')
        else:
            if new_values[1] == 'default':
                messagebox.showerror('Ошибка редактирования', 'Вы не указали категорию товара.')
            else:
                to_db = new_values.copy()
                to_db.append(to_db[0].lower())
                for value in range(len(to_db)):
                    to_db[value] = ReconType(to_db[value])

                if key == 'w':
                    to_db = FormatForDB(to_db)
                    act.AddItem('products', to_db)
                    new_values = new_values[:1] + new_values[2:]
                    RefreshTable()
                    RefreshTable(True)
                    tree.insert('', tk.END, iid=f'{len(act.products)}', values=new_values)
                    if status:
                        MainWindow()
                    else:
                        UserWindow()

                elif key == 'e':
                    index_from_db = indices[ParseIndex(idx)]
                    for_func = new_values.copy()
                    for_func.append(new_values[0].lower())
                    act.EditItem(index_from_db, for_func)
                    new_values = new_values[:1] + new_values[2:]
                    tree.item(idx, values=new_values)
                RefreshTable()
                edit_window.destroy()


def DeleteCategory(tree, category='Full'):
    global indices, items
    if category == 'Full':
        act.DeleteAll('products')
        RefreshTable()
        DrawTree(tree)
    else:
        category = GetText(category)
        if category == 'Все':
            messagebox.showerror('Ошибка', 'Вы не выбрали категорию.')
        else:
            act.DeleteCategory(category)
            RefreshTable()
            DrawTree(tree)


def Bucket():
    global bucket_items
    bucket_window = tk.Tk()
    bucket_window.geometry(f'700x500+{screen_width // 2 - 350}+{screen_height // 2 - 250}')
    bucket_window.resizable(False, False)
    bucket_window.title('Корзина')

    frame_bucket = tk.Frame(bucket_window)
    frame_bucket.place(relx=0, rely=0, relwidth=1, relheight=1)

    columns = ('item_id', 'title', 'price', 'amount')
    purchases = ttk.Treeview(frame_bucket, columns=columns, show='headings')
    purchases.heading("item_id", text="Артикул", anchor=tk.W)
    purchases.heading("title", text="Название", anchor=tk.W)
    purchases.heading("price", text="Цена", anchor=tk.W)
    purchases.heading("amount", text="Кол-во", anchor=tk.W)

    purchases.column("item_id", stretch=tk.NO, width=70)
    purchases.column("title", stretch=tk.NO, width=430)
    purchases.column("price", stretch=tk.NO, width=100)
    purchases.column("amount", stretch=tk.NO, width=70)

    purchases.bind("<ButtonRelease-1>", lambda event: on_treeview_click(purchases))

    order_price = 0
    for item in bucket_items:
        print(item)
        purchases.insert("", tk.END, values=item)
        order_price += item[2] * item[3]

    delete_item_btn = ttk.Button(frame_bucket, text='Удалить товар', width=15,
                                 command=lambda: DeleteItem(purchases, summary_entry, True))
    order_btn = ttk.Button(frame_bucket, text='Оформить заказ', width=20,
                           command=lambda: RegisterOrder(bucket_window, purchases))

    summary_label = tk.Label(frame_bucket, text='Сумма заказа:')
    summary_entry = tk.Entry(frame_bucket)
    summary_entry.insert(0, order_price)
    summary_entry.config(state=tk.DISABLED)

    scrollbar = ttk.Scrollbar(frame_bucket, orient=tk.VERTICAL, command=purchases.yview)
    purchases.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=5, sticky="nsw")

    orders = ttk.Button(frame_bucket, text='Мои заказы', command=MyOrders)
    orders.grid(row=1, column=4, rowspan=2, pady=5, sticky='ensw')

    purchases.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky='ensw')
    delete_item_btn.grid(row=1, column=0, rowspan=2, padx=5, pady=5, sticky='nsw')
    order_btn.grid(row=1, column=2, rowspan=2, columnspan=2, padx=5, pady=5, sticky='ens')

    summary_label.grid(row=1, column=1, sticky='e')
    summary_entry.grid(row=2, column=1, sticky='e')

    frame_bucket.rowconfigure(0, weight=10)
    frame_bucket.rowconfigure(1, weight=1)
    frame_bucket.rowconfigure(2, weight=1)

    frame_bucket.columnconfigure(0, weight=1)
    frame_bucket.columnconfigure(1, weight=1)
    frame_bucket.columnconfigure(2, weight=1)
    frame_bucket.columnconfigure(3, weight=1)


def CreateOrder(window, tree, item_amount, city_entry, street_entry, building_entry, apartment_entry):
    global bucket_items
    city_entry = GetText(city_entry)
    street_entry = GetText(street_entry)
    building_entry = GetText(building_entry)
    apartment_entry = GetText(apartment_entry)

    count = 0
    if city_entry == '':
        messagebox.showerror('Ошибка', 'Сначала введите название города.')
    else:
        count += 1

    if street_entry == '' and count == 1:
        messagebox.showerror('Ошибка', 'Сначала введите название улицы.')
    else:
        count += 1

    if building_entry == '' and count == 2:
        messagebox.showerror('Ошибка', 'Сначала введите номер дома.')
    else:
        count += 1

    if apartment_entry == '':
        apartment_entry = 'NULL'
    else:
        apartment_entry = f"''{apartment_entry}''"

    if count == 3:
        to_db = f"'({user_id}, {item_amount}, ''{city_entry}'', ''{street_entry}'', ''{building_entry}'', {apartment_entry}, CURRENT_DATE)'"

        id = act.AddOrder(to_db)

        for item in get_all_items(tree):
            to_db = f"'({id[0][0]}, {item[0]}, {item[3]}, {item[2]})'"
            act.AddOrderDetails(to_db)
            act.UpdateAmount(item[0], item[3])

        if status:
            MainWindow()
        else:
            UserWindow()

        bucket_items = []
        tree.delete(*tree.get_children())

        messagebox.showinfo('Заказ оформлен',
                            f'Товары доставят по адресу {city_entry}, {street_entry}, {building_entry}')

        window.destroy()
        Bucket()


def RegisterOrder(bucket_window, purchases):
    purchases_list = get_all_items(purchases)
    if len(purchases_list) != 0:
        bucket_window.title('Оформление заказа')
        reg_frame = tk.Frame(bucket_window)
        reg_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        name = tk.Label(reg_frame, text='Имя: Еблан')
        surname = tk.Label(reg_frame, text='Фамилия: Ебланов')

        city_label = tk.Label(reg_frame, text='Город:')
        street_label = tk.Label(reg_frame, text='Улица:')
        building_label = tk.Label(reg_frame, text='Дом:')
        apartment_label = tk.Label(reg_frame, text='Квартира:')

        city_entry = tk.Entry(reg_frame, width=80)
        street_entry = tk.Entry(reg_frame, width=80)
        building_entry = tk.Entry(reg_frame, width=80)
        apartment_entry = tk.Entry(reg_frame, width=80)

        name.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        surname.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        city_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        city_entry.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        street_label.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        street_entry.grid(row=2, column=1, sticky='w', padx=5, pady=5)
        building_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)
        building_entry.grid(row=4, column=0, sticky='w', padx=5, pady=5)
        apartment_label.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        apartment_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        apply_btn = ttk.Button(reg_frame, text='Оформить заказ', width=40, command=lambda: CreateOrder(bucket_window,
                                                                                                       purchases,
                                                                                                       item_amount,
                                                                                                       city_entry,
                                                                                                       street_entry,
                                                                                                       building_entry,
                                                                                                       apartment_entry))
        apply_btn.grid(row=5, column=0, columnspan=2, pady=20)

        reg_frame.columnconfigure(0, weight=1)
        reg_frame.columnconfigure(1, weight=1)

        item_amount = 0
        for i in purchases_list:
            item_amount += i[-1]

    else:
        messagebox.showerror('Ошибка', 'Корзина пуста, перед заказом добавьте в нее товары.')


def MyOrders():
    orders_window = tk.Tk()
    orders_window.title('Мои заказы')
    orders_window.geometry(f'450x300+{screen_width // 2 - 225}+{screen_height // 2 - 150}')
    orders_window.resizable(False, False)

    orders_frame = tk.Frame(orders_window)
    orders_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    columns = ('id', 'count', 'price', 'date')
    orders = ttk.Treeview(orders_frame, columns=columns, show='headings')
    orders.heading("id", text="Номер заказа", anchor=tk.W)
    orders.heading("count", text="Товаров в заказе", anchor=tk.W)
    orders.heading("price", text="Общая стоимость", anchor=tk.W)
    orders.heading("date", text="Дата покупки", anchor=tk.W)

    orders.column("id", stretch=tk.NO, width=100)
    orders.column("count", stretch=tk.NO, width=100)
    orders.column("price", stretch=tk.NO, width=120)
    orders.column("date", stretch=tk.NO, width=100)

    orders.grid(row=0, column=0, sticky='ensw', padx=5, pady=5)

    orders_list = act.MyOrders(user_id)
    for item in orders_list:
        orders.insert("", tk.END, values=list(item))

    scrollbar = ttk.Scrollbar(orders_frame, orient=tk.VERTICAL, command=orders.yview)
    orders.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky="nsw")

    orders_frame.rowconfigure(0, weight=1)

    orders_frame.columnconfigure(0, weight=10)
    orders_frame.columnconfigure(1, weight=1)


def AddToBucket(number, tree):
    global index, bucket_items
    print(index)
    if index != '':
        count = GetText(number)
        if count != '':
            values = items[int(index) - 1]
            idx = indices[int(index) - 1]
            print(values)
            values_cart = [idx, values[0], values[2], int(count)]

            if int(values[3]) >= int(values_cart[-1]):
                bucket_items.append(values_cart)
                messagebox.showinfo('Успех', 'Товар добавлен в корзину.')
            else:
                messagebox.showerror('Ошибка', 'Товаров на складе недостаточно.')
        else:
            messagebox.showerror('Ошибка', 'Сначала введите количество.')



    else:
        messagebox.showerror('Ошибка', 'Сначала выберите товар, который хотите добавить в корзину.')
    index = ''


def Specialists(category):
    category = GetText(category)
    if category != 'Все':
        spec_window = tk.Tk()
        spec_window.title(f'Специалисты в категории "{category}"')
        spec_window.geometry(f'400x300+{screen_width // 2 - 200}+{screen_height // 2 - 150}')
        spec_window.resizable(False, False)

        spec_frame = tk.Frame(spec_window)
        spec_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        columns = ('name', 'surname', 'email')
        empl = ttk.Treeview(spec_frame, columns=columns, show='headings')
        empl.heading("name", text="Имя", anchor=tk.W)
        empl.heading("surname", text="Фамилия", anchor=tk.W)
        empl.heading("email", text="Почтовый адрес", anchor=tk.W)

        empl.column("name", stretch=tk.NO, width=100)
        empl.column("surname", stretch=tk.NO, width=100)
        empl.column("email", stretch=tk.NO, width=200)

        empl.grid(row=0, column=0, sticky='ensw', padx=5, pady=5)

        spec_list = act.Specialists(category)
        for item in spec_list:
            empl.insert("", tk.END, values=list(item))

        scrollbar = ttk.Scrollbar(spec_frame, orient=tk.VERTICAL, command=empl.yview)
        empl.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="nsw")

        spec_frame.rowconfigure(0, weight=1)

        spec_frame.columnconfigure(0, weight=10)
        spec_frame.columnconfigure(1, weight=1)
    else:
        messagebox.showerror('Ошибка', 'Сначала выберите категорию.')


# ОКНО РАБОТНИКА -------------------------------------------------------------------------------------------------------


def MainWindow():
    global index, indices, items, user_name, user_surname
    window.geometry('1200x700+100+50')
    window.resizable(False, False)

    window.title('Goods Manager')
    frame_main = tk.Frame(window)
    frame_main.place(relx=0, rely=0, relwidth=1, relheight=1)

    style = ttk.Style()
    style.configure("TEntry", foreground="gray")

    log_out_btn = ttk.Button(frame_main, text='Log Out', width=8, command=LogIn)
    add_btn = ttk.Button(frame_main, text='Добавить позицию', width=20, command=lambda: AddItem(tree))
    edit_btn = ttk.Button(frame_main, text='Редактировать позицию', width=25, command=lambda: EditItem(tree))
    delete_btn = ttk.Button(frame_main, text='Удалить позицию', width=20, command=lambda: DeleteItem(tree))
    search_btn = ttk.Button(frame_main, text='Найти', width=15,
                            command=lambda: DrawTree(tree, True, GetText(search_entry)))
    search_out_btn = ttk.Button(frame_main, text='Показать все', width=15, command=lambda: DrawTree(tree, True))

    search_entry = ttk.Entry(frame_main, style='TEntry')
    search_entry.insert(0, 'Поиск по каталогу:')  # установка текста заполнителя
    search_entry.bind('<FocusIn>', lambda event: on_entry_click(search_entry))  # прикрепление обработчика события
    columns = ('title', 'description', 'price', 'amount')
    tree = ttk.Treeview(frame_main, columns=columns, show="headings")
    tree.heading("title", text="Название", anchor=tk.W)
    tree.heading("description", text="Описание", anchor=tk.W)
    tree.heading("price", text="Цена", anchor=tk.W)
    tree.heading("amount", text="Кол-во", anchor=tk.W)

    tree.column("title", stretch=tk.NO, width=320)
    tree.column("description", stretch=tk.NO, width=560)
    tree.column("price", stretch=tk.NO, width=50)
    tree.column("amount", stretch=tk.NO, width=50)

    tree.bind("<ButtonRelease-1>", lambda event: on_treeview_click(tree))

    DrawTree(tree)

    scrollbar = ttk.Scrollbar(frame_main, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=2, column=3, sticky="nsw")

    log_out_btn.grid(row=0, column=4, sticky='e', padx=5)
    add_btn.grid(row=3, column=0)
    edit_btn.grid(row=3, column=1)
    delete_btn.grid(row=3, column=2)

    search_entry.grid(row=0, column=0, columnspan=2, sticky='we', padx=10)
    search_btn.grid(row=0, column=2, sticky='w')
    search_out_btn.grid(row=1, column=2, sticky='nw')

    tree.grid(row=2, column=0, columnspan=3, sticky='ensw', padx=5, pady=5)

    account = tk.Label(frame_main, text=f'{user_name} {user_surname}')
    account.grid(row=0, column=3)

    bruh_label = tk.Label(frame_main, width=20)
    bruh_label.grid(row=3, column=3)
    filter_frame = tk.Frame(window)
    filter_frame.place(relx=0.86, rely=0.1, relwidth=0.2, relheight=0.9)
    filter_label = tk.Label(filter_frame, text="Категория:")
    filter_label.grid(row=0, column=0, sticky='w', pady=5)

    filter_entry = ttk.Combobox(filter_frame, values=['Все',
                                                      'Процессоры',
                                                      'Графические карты',
                                                      'Материнские платы',
                                                      'Оперативная память',
                                                      'Блоки питания',
                                                      'Постоянная память',
                                                      'Система охлаждения',
                                                      'Корпусы'])
    filter_entry.set('Все')
    filter_entry.grid(row=1, column=0)

    show_button = ttk.Button(filter_frame, text='Показать', command=lambda: FirteredItems(tree, filter_entry))
    show_button.grid(row=2, column=0, sticky='ew')

    delete_cat_button = ttk.Button(filter_frame, text='      Удалить все\nобъекты категории',
                                   command=lambda: DeleteCategory(tree, filter_entry))
    delete_cat_button.grid(row=3, rowspan=2, column=0, sticky='ew', pady=20)

    delete_all_button = ttk.Button(filter_frame, text='Удалить все\n  элементы', command=lambda: DeleteCategory(tree))
    delete_all_button.grid(row=5, rowspan=2, column=0, sticky='ew')

    frame_main.rowconfigure(0, weight=1)
    frame_main.rowconfigure(1, weight=1)
    frame_main.rowconfigure(2, weight=30)
    frame_main.rowconfigure(3, weight=1)

    frame_main.columnconfigure(0, weight=10)
    frame_main.columnconfigure(1, weight=10)
    frame_main.columnconfigure(2, weight=10)
    frame_main.columnconfigure(3, weight=30)
    frame_main.columnconfigure(4, weight=5)


# ОКНО ПОЛЬЗОВАТЕЛСЯ ---------------------------------------------------------------------------------------------------


def UserWindow():
    global indices, items, user_name, user_surname
    window.geometry('1400x700+50+50')
    window.resizable(False, False)
    window.title('Каталог')

    frame_user = tk.Frame(window)
    frame_user.place(relx=0, rely=0, relwidth=1, relheight=1)

    log_out_btn = ttk.Button(frame_user, text='Log Out', width=8, command=LogIn)
    add_to_bucket_btn = ttk.Button(frame_user, text='Добавить в корзину',
                                   command=lambda: AddToBucket(count_entry, tree))

    bucket_btn = ttk.Button(frame_user, image=bucket_image, command=Bucket)

    count_label = tk.Label(frame_user, text='Количество:')
    count_entry = tk.Entry(frame_user, width=5)

    style = ttk.Style()
    style.configure("TEntry", foreground="gray")
    search_entry = ttk.Entry(frame_user, style='TEntry', width=155)
    search_entry.insert(0, 'Поиск по каталогу:')  # установка текста заполнителя
    search_entry.bind('<FocusIn>', lambda event: on_entry_click(search_entry))  # прикрепление обработчика события

    search_btn = ttk.Button(frame_user, text='Найти', command=lambda: DrawTree(tree, True, GetText(search_entry)))

    columns = ('title', 'description', 'price', 'amount')
    tree = ttk.Treeview(frame_user, columns=columns, show="headings")
    tree.heading("title", text="Название", anchor=tk.W)
    tree.heading("description", text="Описание", anchor=tk.W)
    tree.heading("price", text="Цена", anchor=tk.W)
    tree.heading("amount", text="Кол-во", anchor=tk.W)

    tree.column("title", stretch=tk.NO, width=340)
    tree.column("description", stretch=tk.NO, width=650)
    tree.column("price", stretch=tk.NO, width=50)
    tree.column("amount", stretch=tk.NO, width=50)

    tree.bind("<ButtonRelease-1>", lambda event: on_treeview_click(tree))

    DrawTree(tree)

    scrollbar = ttk.Scrollbar(frame_user, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    account = tk.Label(frame_user, text=f'{user_name} {user_surname}')
    account.grid(row=0, column=4)

    log_out_btn.grid(row=0, column=5)
    search_entry.grid(row=0, column=0, columnspan=4, sticky='w', padx=10)
    search_btn.grid(row=0, column=3, sticky='w')
    tree.grid(row=1, column=1, columnspan=4, sticky='ens', padx=5, pady=5)
    scrollbar.grid(row=1, column=5, sticky="nsw")
    add_to_bucket_btn.grid(row=2, column=4, sticky='e', padx=10)
    bucket_btn.grid(row=2, column=5, sticky='w')
    count_label.grid(row=2, column=2, sticky='e', padx=5)
    count_entry.grid(row=2, column=3, sticky='w', padx=5)

    frame_user.rowconfigure(0, weight=1)
    frame_user.rowconfigure(1, weight=10)
    frame_user.rowconfigure(2, weight=1)

    frame_user.columnconfigure(0, weight=20)
    frame_user.columnconfigure(1, weight=10)
    frame_user.columnconfigure(2, weight=1)
    frame_user.columnconfigure(3, weight=1)
    frame_user.columnconfigure(4, weight=10)
    frame_user.columnconfigure(5, weight=1)

    filter_frame = tk.Frame(window)
    filter_frame.place(relx=0.005, rely=0.1, relwidth=.16, relheight=1)

    option_state = tk.StringVar(value='По возрастанию')
    sort_option1 = tk.Radiobutton(filter_frame, text='По возрастанию', value='По возрастанию', variable=option_state)
    sort_option2 = tk.Radiobutton(filter_frame, text='По убыванию', value='По убыванию', variable=option_state)
    sort_option1.grid(row=1, column=1, sticky='w')
    sort_option2.grid(row=2, column=1, sticky='w')

    sort_label = tk.Label(filter_frame, text="Сортировка:")
    sort_label.grid(row=0, column=0, sticky='w')

    sort_option = ttk.Combobox(filter_frame, values=['Не сортировать', 'По цене', 'По количеству'])
    sort_option.set('Не сортировать')
    sort_option.grid(row=0, column=1, sticky='w')

    filter_label = tk.Label(filter_frame, text="Категория:")
    filter_label.grid(row=3, column=0, sticky='w', pady=10)

    filter_entry = ttk.Combobox(filter_frame, values=['Все',
                                                      'Процессоры',
                                                      'Графические карты',
                                                      'Материнские платы',
                                                      'Оперативная память',
                                                      'Блоки питания',
                                                      'Постоянная память',
                                                      'Система охлаждения',
                                                      'Корпусы'])
    filter_entry.set('Все')
    filter_entry.grid(row=3, column=1, sticky='w', pady=10)

    apply_button = ttk.Button(filter_frame, text="Применить", width=30, command=lambda: FirteredItems(tree,
                                                                                                      filter_entry,
                                                                                                      sort_option,
                                                                                                      option_state))
    apply_button.grid(row=4, column=0, columnspan=3, sticky='ew', pady=10)

    spec_list_button = ttk.Button(filter_frame, text='Список специалистов', command=lambda: Specialists(filter_entry))
    spec_list_button.grid(row=5, column=0, columnspan=3, pady=10, sticky='ew')


# ОКНО АВТОРИЗАЦИ ------------------------------------------------------------------------------------------------------


def AuthorizationBlocks(frame):
    empty_label = tk.Label(frame, text=' ')

    login_title = tk.Label(frame, text='E-Mail address:', font=8)
    login = tk.Entry(frame)

    passwd_title = tk.Label(frame, text='Password:', font=8)
    passwd = tk.Entry(frame, show='*')

    submit_button = ttk.Button(frame, text='Continue', width=20)

    login_button = ttk.Button(frame, text='Log In', width=7, command=LogIn)
    signup_button = ttk.Button(frame, text='Sign Up', width=7, command=SignUp)

    return empty_label, login_title, login, passwd_title, passwd, submit_button, login_button, signup_button


def LogIn():
    global bucket_items, user_id, user_name, user_surname, status

    def GetLogInData():
        global user_id, user_name, user_surname, status
        email = GetText(login)
        password = GetText(passwd)

        if len(email) == 0:
            messagebox.showerror('Пустое поле', 'Введите почтовый адрес.')
        elif len(password) == 0:
            messagebox.showerror('Пустое поле', 'Введите пароль.')
        else:
            check_mail = checks.CheckMail(email)
            if not check_mail[0]:
                messagebox.showerror('Ошибка авторизации', 'Почта указана неверно.')
            else:
                password = hash_search.encode_password(password)
                user_info = act.UserInfo(email.lower(), password)
                print(user_info)
                if len(user_info) != 0:
                    if user_info[0][0] != 0:
                        user_id = user_info[0][0]
                        user_name = user_info[0][1]
                        user_surname = user_info[0][2]

                        status = check_mail[1]
                        if status:
                            MainWindow()
                        else:
                            UserWindow()
                    else:
                        messagebox.showerror('Ошибка авторизации', 'Пароль введен неверно.')
                else:
                    messagebox.showerror('Ошибка авторизации', 'Такого пользователя не существует.')

    bucket_items = []

    window.title('Log In')
    window.geometry(f'400x200+{screen_width // 2 - 200}+{screen_height // 2 - 200}')
    frame = tk.Frame(window)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    empty_label, login_title, login, passwd_title, passwd, submit_button, login_button, signup_button = \
        AuthorizationBlocks(frame)
    submit_button.config(command=GetLogInData)
    # submit_button.config(command=UserWindow)
    # submit_button.config(command=MainWindow)

    empty_label.grid(row=0, column=1)

    login_title.grid(row=1, column=1, padx=5, sticky='w')
    login.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

    passwd_title.grid(row=3, column=1, padx=5, sticky='w')
    passwd.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

    submit_button.grid(row=5, column=1, padx=5, pady=5)
    login_button.grid(row=0, column=2)
    signup_button.grid(row=1, column=2)

    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=7)
    frame.columnconfigure(2, weight=1)

    return window


def SignUp():
    global user_id, user_name, user_surname

    def GetLogInData():
        global user_id, user_name, user_surname
        entry_access = 0

        name, surname, email, password, password_verification, check_mail = [''] * 6

        # name check
        name = GetText(first_name)
        if len(name) == 0:
            messagebox.showerror('Ошибка регистрации',
                                 'Введите имя.')
        else:
            access, name = checks.ChangeReg(name)
            if not access:
                messagebox.showerror('Ошибка регистрации',
                                     'Имя не может содержать посторонние символы.')
            else:
                print(name)
                entry_access += 1

        # surname check
        if entry_access == 1:
            surname = GetText(second_name)
            if len(surname) == 0:
                messagebox.showerror('Ошибка регистрации',
                                     'Введите фамилию.')
            else:
                access, surname = checks.ChangeReg(surname)
                if not access:
                    messagebox.showerror('Ошибка',
                                         'Фамилия не может содержать посторонние символы.')
                else:
                    print(surname)
                    entry_access += 1

        # email check
        if entry_access == 2:
            email = GetText(login)
            user_info = act.UserInfo(email, '')
            if len(email) == 0:
                messagebox.showerror('Ошибка регистрации',
                                     'Введите почтовый адрес.')
            else:
                check_mail = checks.CheckMail(email)
                if not check_mail[0]:
                    messagebox.showerror('Ошибка регистрации',
                                         'Почта указана неверно.')
                elif len(user_info) != 0 and user_info[0][0] == 0:
                    messagebox.showerror('Ошибка регистрации',
                                         'Такой пользователь уже существует.')
                elif check_mail[1]:
                    messagebox.showerror('Ошибка регистрации',
                                         'Вы регистрируетесь, используя корпоративную почту сотрудника.\n'
                                         'Регистрация такого типа возможна только в офисе компании.')
                else:
                    entry_access += 1

        # password check
        if entry_access == 3:
            password = GetText(passwd)
            if len(password) == 0:
                messagebox.showerror('Ошибка регистрации',
                                     'Введите пароль.')
            elif not checks.CheckPasswdLength(password):
                messagebox.showerror('Ошибка регистрации',
                                     'Ваш пароль слишком короткий. Пароль должен содержать не менее 8 символов.')
            else:
                entry_access += 1

        # password verification check
        if entry_access == 4:
            password_verification = GetText(passwd_subm)
            if password_verification != password:
                messagebox.showerror('Ошибка регистрации',
                                     'Пароль не совпадает.')
            else:
                print('Passwd verified')
                entry_access += 1

        if entry_access == 5:
            password = hash_search.encode_password(password)
            act.AddUser(name, surname, email, password)
            user_name = name
            user_surname = surname
            user_id = act.UserInfo(email, password)[0][0]
            messagebox.showinfo('Регистрация', 'Ваш аккаунт успешно зарегистрирован!')

            if check_mail[1]:
                MainWindow()
            else:
                UserWindow()

    window.title('Sign Up')
    window.geometry(f'400x400+{screen_width // 2 - 200}+{screen_height // 2 - 200}')
    frame = tk.Frame(window)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    empty_label, login_title, login, passwd_title, passwd, submit_button, login_button, signup_button = \
        AuthorizationBlocks(frame)
    submit_button.config(command=GetLogInData)

    first_name_title = tk.Label(frame, text='First name:', font=8)
    first_name = tk.Entry(frame)

    second_name_title = tk.Label(frame, text='Last name:', font=8)
    second_name = tk.Entry(frame)

    passwd_subm_title = tk.Label(frame, text='Submit password:', font=8)
    passwd_subm = tk.Entry(frame, show='*')

    # /////////////////////////////////////////////////////
    empty_label.grid(row=0, column=1)

    first_name_title.grid(row=1, column=1, padx=5, sticky='w')
    first_name.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

    second_name_title.grid(row=3, column=1, padx=5, sticky='w')
    second_name.grid(row=4, column=1, padx=5, pady=10, sticky='ew')

    login_title.grid(row=5, column=1, padx=5, sticky='w')
    login.grid(row=6, column=1, padx=5, pady=10, sticky='ew')

    passwd_title.grid(row=7, column=1, padx=5, sticky='w')
    passwd.grid(row=8, column=1, padx=5, pady=10, sticky='ew')

    passwd_subm_title.grid(row=9, column=1, padx=5, sticky='w')
    passwd_subm.grid(row=10, column=1, padx=5, pady=10, sticky='ew')

    submit_button.grid(row=11, column=1, padx=5, pady=5)

    login_button.grid(row=0, column=2)
    signup_button.grid(row=1, column=2)

    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)
    frame.rowconfigure(3, weight=1)
    frame.rowconfigure(4, weight=1)
    frame.rowconfigure(5, weight=1)
    frame.rowconfigure(6, weight=1)
    frame.rowconfigure(7, weight=1)
    frame.rowconfigure(8, weight=1)
    frame.rowconfigure(9, weight=1)
    frame.rowconfigure(10, weight=1)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=7)
    frame.columnconfigure(2, weight=1)


window = tk.Tk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window.resizable(False, False)
window.iconbitmap('logo.ico')

bucket_image = ImageTk.PhotoImage(file="cart.png")

LogIn()

window.mainloop()
