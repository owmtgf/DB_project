from sqlalchemy import create_engine, MetaData
from sqlalchemy import text


engine = create_engine('postgresql://app_user:prikolist@localhost:1488/Market', echo=False)
connection = engine.connect()
meta = MetaData()
meta.reflect(bind=engine)

tables = meta.tables.keys()
products = []
products_selected = []


def UpdateProductsList():
    global products
    products = connection.execute(text("SELECT * FROM table_out('products');")).fetchall()


def DeleteItem(index):
    global products
    connection.execute(text(f"SELECT delete_item({index});"))
    connection.commit()
    UpdateProductsList()


def AddItem(table_name, item_text):
    global products
    table_name = f"'{table_name}'"
    connection.execute(text("SELECT add_item({}, {})".format(table_name,
                                                             item_text)))
    connection.commit()
    UpdateProductsList()


def EditItem(index, elems):
    global products
    connection.execute(text("SELECT update_item({}, '{}', '{}', '{}', {}, {}, '{}')".format(index,
                                                                                            elems[0],
                                                                                            elems[1],
                                                                                            elems[2],
                                                                                            elems[3],
                                                                                            elems[4],
                                                                                            elems[5])))
    connection.commit()
    UpdateProductsList()


def GetTableData(category, sort_type, sort_order):
    global products
    products = connection.execute(text("SELECT * FROM get_table_data('{}', '{}', '{}')".format(category,
                                                                                        sort_type,
                                                                                        sort_order))).fetchall()


def DeleteCategory(category):
    global products
    connection.execute(text("SELECT delete_category('{}')".format(category)))
    connection.commit()
    UpdateProductsList()


def DeleteAll(table_name):
    global products
    connection.execute(text(f"SELECT delete_all('{table_name}')"))
    connection.commit()
    UpdateProductsList()


def AddOrder(item_text):
    order_id = connection.execute(text(f"SELECT add_order({item_text})")).fetchall()
    connection.commit()
    return order_id


def AddOrderDetails(item_text):
    connection.execute(text(f"SELECT add_order_detail({item_text})"))
    connection.commit()


def MyOrders(customer_id):
    orders_list = connection.execute(text(f"SELECT * FROM orders_out({customer_id})")).fetchall()
    return orders_list


def Specialists(category):
    spec_list = connection.execute(text(f"SELECT * FROM spec_out('{category}')")).fetchall()
    return spec_list


def UserInfo(email, password):
    user_info = connection.execute(text(f"SELECT * FROM check_login_password('{email}', '{password}')")).fetchall()
    return user_info


def AddUser(name, surname, login, password):
    connection.execute(text(f"SELECT add_customer('{name}', '{surname}', '{login}', '{password}')"))
    connection.commit()


def UpdateAmount(product_id, diff):
    connection.execute(text(f"SELECT update_product_amount({product_id}, {diff})"))
    connection.commit()
    UpdateProductsList()


UpdateProductsList()
