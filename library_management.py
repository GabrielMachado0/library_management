# Instalar as bibliotecas PyQt5, psycopg2, bcrypt

from PyQt5 import uic, QtWidgets
from time import sleep
import psycopg2
import bcrypt

db = "host='localhost' dbname='library_management' user='postgres' password='password da tua DB'"
username = None

# Function to login in the app

def login_func():
    global username
    username = login.findChild(QtWidgets.QLineEdit, 'user_lb').text()
    password = login.findChild(QtWidgets.QLineEdit, 'password_lb').text()

    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM login WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            password_db = result[0]
            
            if isinstance(password_db, memoryview):
                password_db = password_db.tobytes()
            elif isinstance(password_db, str):
                password_db = password_db.encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), password_db):
                login.close()
                sleep(0.3)
                #login_ok.show()
                if username == 'admin':
                    admin_ops.show()
                else:
                    normal_ops.show()
            else:
                login.close()
                login.findChild(QtWidgets.QLineEdit, 'user_lb').clear()
                login.findChild(QtWidgets.QLineEdit, 'password_lb').clear()
                sleep(0.3)
                login_error.show()
        else:
            login.close()
            login.findChild(QtWidgets.QLineEdit, 'user_lb').clear()
            login.findChild(QtWidgets.QLineEdit, 'password_lb').clear()
            sleep(0.3)
            login_error.show()

    except Exception as e:
        print(f'Error: {e}')

# Function to create user in the app

def create_user():

    username = register.findChild(QtWidgets.QLineEdit, 'user_rg').text()
    password = register.findChild(QtWidgets.QLineEdit, 'pass_rg').text()

    try:
        gen_salt = bcrypt.gensalt()
        password_crypt = bcrypt.hashpw(password.encode('utf-8'), gen_salt)
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password_crypt.decode('utf-8')))
        conn.commit()
        cursor.close()
        conn.close()

        login.findChild(QtWidgets.QLineEdit, 'user_lb').clear()
        login.findChild(QtWidgets.QLineEdit, 'password_lb').clear()
        print('Sucessfull!')
        register.findChild(QtWidgets.QLineEdit, 'user_rg').clear()
        register.findChild(QtWidgets.QLineEdit, 'pass_rg').clear()
        #register.close()
        #sleep(0.3)
        created_user.show()

    except Exception as e:
        print(f'Error: {e}')     
        register.close()
        register.findChild(QtWidgets.QLineEdit, 'user_rg').clear()
        register.findChild(QtWidgets.QLineEdit, 'pass_rg').clear()
        sleep(0.3)
        error_rg.show()

def created_sucess():
    created_user.close()
    sleep(0.3)
    register.show()

def register_error():
    error_rg.close()
    sleep(0.3)
    register.show()

# Function to add books in the app

def add_books():
    global username
    title_book = add_book.findChild(QtWidgets.QLineEdit, 'title_lb').text()
    author_book = add_book.findChild(QtWidgets.QLineEdit, 'author_lb').text()
    genre_book = add_book.findChild(QtWidgets.QLineEdit, 'genre_lb').text()

    if username == 'admin':
        admin_ops.close()
        sleep(0.3)
        add_book.show()
    
    if not title_book or not author_book or not genre_book:
        print('All the labels must have be filled')
        return
    
    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM books WHERE title = %s', (title_book,))
        count = cursor.fetchone()[0]

        if count > 0:
            error_bk.show()
            add_book.findChild(QtWidgets.QLineEdit, 'title_lb').clear()
            add_book.findChild(QtWidgets.QLineEdit, 'author_lb').clear()
            add_book.findChild(QtWidgets.QLineEdit, 'genre_lb').clear()
            print('Already exist in our database')
        else:
            cursor.execute('INSERT INTO books (title, author, genre) VALUES (%s, %s, %s)', (title_book, author_book, genre_book,))
            conn.commit()
            print('Sucessful your book was add in our database!')
            add_book.findChild(QtWidgets.QLineEdit, 'title_lb').clear()
            add_book.findChild(QtWidgets.QLineEdit, 'author_lb').clear()
            add_book.findChild(QtWidgets.QLineEdit, 'genre_lb').clear()
            add_book.close()
            sleep(0.3)
            sucess_bk.show()
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f'Error: {e}')
    """
    add_book.close()
    sleep(0.3)
    admin_ops.show()
"""

def book_add_error():
    error_bk.close()
    sleep(0.3)
    add_book.show()

def book_add_sucess():
    sucess_bk.close()
    sleep(0.3)
    add_book.show()

# Function to list all books

def list_book():

    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()

        cursor.execute('SELECT id, title, author, genre FROM books ORDER BY id ASC;')
        books = cursor.fetchall()

        table_list = list_db.findChild(QtWidgets.QTableWidget, 'table_db')

        if table_list:
            table_list.setRowCount(0)

            for row, book in enumerate(books):
                table_list.insertRow(row)
                for index, data in enumerate(book):
                    table_list.setItem(row, index, QtWidgets.QTableWidgetItem(str(data)))

        
        cursor.close()
        conn.close()
        normal_ops.close()
        admin_ops.close()
        sleep(0.3)
        list_db.show()

    except Exception as e:
        print(f'Error: {e}')

# Function to search books

def search_db():
    admin_ops.close()
    normal_ops.close()
    sleep(0.3)
    search_rt.show()

    title_search = search_rt.findChild(QtWidgets.QLineEdit, 'title_lb').text()
    author_search = search_rt.findChild(QtWidgets.QLineEdit, 'author_lb').text()
    genre_search = search_rt.findChild(QtWidgets.QLineEdit, 'genre_lb').text()

    if not title_search and not author_search and not genre_search:
        print('Unless one of the labels must have be filled')
        return
    
    search_info = []

    infos = 'SELECT id, title, author, genre FROM books WHERE '

    cond = []

    if title_search:
        cond.append('title ILIKE %s')
        search_info.append(f'%{title_search}%')
    if author_search:
        cond.append('author ILIKE %s')
        search_info.append(f'%{author_search}%')
    if genre_search:
        cond.append('genre ILIKE %s')
        search_info.append(f'%{genre_search}%')

    if cond:
        infos += ' AND '.join(cond)
    else:
        infos = 'SELECT id, title, author, genre FROM books'

    infos += 'ORDER BY id ASC;'

    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute(infos, tuple(search_info))

        books = cursor.fetchall()

        list_of_books = search_rt.findChild(QtWidgets.QTableWidget, 'table_db')
        if list_of_books:
            list_of_books.setRowCount(0)
            list_of_books.setHorizontalHeaderLabels(['ID', 'Title', 'Author', 'Genre'])

            for row, book in enumerate(books):
                list_of_books.insertRow(row)
                for col, data in enumerate(book):
                    list_of_books.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))
        
        cursor.close()
        conn.close()
        search_rt.findChild(QtWidgets.QLineEdit, 'title_lb').clear()
        search_rt.findChild(QtWidgets.QLineEdit, 'author_lb').clear()
        search_rt.findChild(QtWidgets.QLineEdit, 'genre_lb').clear()

    except Exception as e:
        print(f'Error: {e}')
                    
# Function to delete books

def del_select_book():
    list_of_books = del_book.findChild(QtWidgets.QTableWidget, 'table_db')
    sel_row = list_of_books.currentRow()
    
    if sel_row == -1:
        select_bk.show()
        print('Select a book.')
        return

    id_book_item = list_of_books.item(sel_row, 0)
    if not id_book_item or not id_book_item.text():
        print('No valid book ID selected.')
        return
    
    name_book_item = list_of_books.item(sel_row, 1)
    if not name_book_item or not name_book_item.text():
        print('No valid book selected')
        return

    id_book = id_book_item.text()
    name_book = name_book_item.text()

    msg_box = QtWidgets.QMessageBox(del_book)
    msg_box.setWindowTitle('Confirm you exclusion.')
    msg_box.setText(f'Are you sure do you want to delete you selected book. ID {id_book}, Title {name_book}?')
    msg_box.setIcon(QtWidgets.QMessageBox.Question)

    yes_bt = msg_box.addButton('Yes', QtWidgets.QMessageBox.YesRole)
    no_bt = msg_box.addButton('No', QtWidgets.QMessageBox.NoRole)

    yes_bt.setStyleSheet('background-color: green; color: white; font-size: 12px; font-weight: bold; padding: 5px;')
    no_bt.setStyleSheet('background-color: red; color: white; font-size: 12px; font-weight: bold; padding: 5px;')

    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: rgb(54, 54, 54);
            color: white;
            font-size: 12px;
        }
        QLabel {
            color: white;
        }
    """)
    
    msg_box.exec_()
    """
    confirm_del = QtWidgets.QMessageBox.question(
        del_book, 'Confirm exclusion', f'Are you sure you want to delete book ID {id_book}?',
        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
    )"""

    if msg_box.clickedButton() == yes_bt:
        try:
            conn = psycopg2.connect(db)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM books WHERE id = %s', (id_book,))
            conn.commit()
            print(f'Book with ID {id_book} was deleted.')
            load_books()
            cursor.close()
            conn.close()
            del_book_ok.show()

        except Exception as e:
            print(f'Error: {e}')
    elif msg_box.clickedButton() == no_bt:
        del_book.show()

def select_del_book():
    select_bk.close()
    sleep(0.3)
    del_book.show()

def del_sucess():
    del_book_ok.close()
    sleep(0.3)
    del_book.show()

def load_books():
    list_of_books = del_book.findChild(QtWidgets.QTableWidget, 'table_db')
    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, author, genre FROM books')
        books = cursor.fetchall()

        list_of_books.setRowCount(0)

        for row, book in enumerate(books):
            list_of_books.insertRow(row)
            for col, data in enumerate(book):
                list_of_books.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

        cursor.close()
        conn.close()
    except Exception as e:
        print(f'Error: {e}')

# Function to update books

def up_books():
    admin_ops.close()
    sleep(0.3)
    up_book.show()

    load_up_book()

    list_of_books = up_book.findChild(QtWidgets.QTableWidget, 'table_db')

    list_of_books.setEditTriggers(QtWidgets.QTableWidget.AllEditTriggers)

def load_up_book():
    list_of_books = up_book.findChild(QtWidgets.QTableWidget, 'table_db')

    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()

        cursor.execute('SELECT id, title, author, genre FROM books')
        books = cursor.fetchall()

        if not books:
            print('Books not found.')
            return
        
        list_of_books.setRowCount(0)

        for row, book in enumerate(books):
            list_of_books.insertRow(row)
            for col, data in enumerate(book):
                list_of_books.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))
        
        cursor.close()
        conn.close()
    
    except Exception as e:
        print(f'Error: {e}')

def save_up():

    list_of_books = up_book.findChild(QtWidgets.QTableWidget, 'table_db')

    row = list_of_books.currentRow()

    id_book_item = list_of_books.item(row, 0)

    if not id_book_item or not id_book_item.text():
        print('ID not found.')
        return
    
    id_book = id_book_item.text()

    print(f'Cell changed at row {row}')
    
    title_up = list_of_books.item(row, 1).text() if list_of_books.item(row, 1) else None
    author_up = list_of_books.item(row, 2).text() if list_of_books.item(row, 2) else None
    genre_up = list_of_books.item(row, 3).text() if list_of_books.item(row, 3) else None

    print(f'Update data: title: {title_up}, author: {author_up}, genre: {genre_up}')

    try:
        conn = psycopg2.connect(db)
        cursor = conn.cursor()

        if title_up:
            cursor.execute('UPDATE books SET title = %s WHERE id = %s', (title_up, id_book))
        if author_up:
            cursor.execute('UPDATE books SET author = %s WHERE id = %s', (author_up, id_book))
        if genre_up:
            cursor.execute('UPDATE books SET genre = %s WHERE id = %s', (genre_up, id_book))
        
        conn.commit()

        cursor.close()
        conn.close()
        up_book_ok.show()
        print(f'Book with ID {id_book} was updated.')
    except Exception as e:
        print(f'Error: {e}')

def up_book_sucess():
    up_book_ok.close()
    sleep(0.3)
    up_book.show()


"""
def on_cell(row, col):
    print(f'Cell changed at row {row}, column {col}.')
"""

# Extra functions to open and close windows

def del_books():
    admin_ops.close()
    sleep(0.3)
    del_book.show()

    load_books()

def criation_user():
    admin_ops.close()
    sleep(0.3)
    register.show()

def admin_log():
    login_ok.close()
    error_rg.close()
    sucess_bk.close()
    add_book.close()
    register.close()
    sleep(0.3)
    admin_ops.show()

def normal_log():
    login.close()
    sleep(0.3)
    normal_ops.show()

def tryagain_func():
    login_error.close()
    sleep(0.3)
    login.show()

def back_to():
    global username
    if username == 'admin':
        list_db.close()
        sleep(0.3)
        admin_ops.show()
    else:
        list_db.close()
        sleep(0.3)
        normal_ops.show()

def back_to_back():
    global username
    if username == 'admin':
        up_book.close()
        search_rt.close()
        del_book.close()
        search = search_rt.findChild(QtWidgets.QTableView, 'table_db')
        if search and search.model():
            search.model().removeRows(0, search.model().rowCount())
        sleep(0.3)
        admin_ops.show()
    else:
        up_book.close()
        del_book.close()
        search_rt.close()
        search = search_rt.findChild(QtWidgets.QTableView, 'table_db')
        if search and search.model():
            search.model().removeRows(0, search.model().rowCount())
        sleep(0.3)
        normal_ops.show()

# Function to close aplication Exit_bt

def close_func():
    login.close()
    login_error.close()
    admin_ops.close()
    normal_ops.close()
    #register.close()
    #add_book.close()
    list_db.close()
    search_rt.close()
    del_book.close()
    up_book.close()
    error_rg.close()
    error_bk.close()

# Start aplication

app = QtWidgets.QApplication([])

# Load the Screen

login = uic.loadUi(r"UI\login_sys.ui")
login_ok = uic.loadUi(r"UI\login_ok.ui")
login_error = uic.loadUi(r"UI\login_error.ui")
admin_ops = uic.loadUi(r"UI\admin_ops.ui")
normal_ops = uic.loadUi(r"UI\normal_ops.ui")
register = uic.loadUi(r"UI\register.ui")
add_book = uic.loadUi(r"UI\add_book.ui")
list_db = uic.loadUi(r"UI\list_db.ui")
search_rt = uic.loadUi(r"UI\search_rt.ui")
del_book = uic.loadUi(r"UI\del_book.ui")
up_book = uic.loadUi(r"UI\up_book.ui")
error_rg = uic.loadUi(r"UI\register_error.ui")
error_bk = uic.loadUi(r"UI\book_rg_error.ui")
sucess_bk = uic.loadUi(r"UI\book_rg_sucess.ui")
select_bk = uic.loadUi(r"UI\select_book.ui")
del_book_ok = uic.loadUi(r"UI\deleted_book.ui")
up_book_ok = uic.loadUi(r"UI\uptaded_book.ui")
created_user = uic.loadUi(r"UI\created_user.ui")

# Sensitive content

password_lbs = login.findChild(QtWidgets.QLineEdit, 'password_lb')
password_lbs.setEchoMode(QtWidgets.QLineEdit.Password)

password_register = register.findChild(QtWidgets.QLineEdit, 'pass_rg')
password_register.setEchoMode(QtWidgets.QLineEdit.Password)

#list_of_book = up_book.findChild(QtWidgets.QTableWidget, 'table_db')
#list_of_book.cellChanged.connect(on_cell)

# Butons login_sys

login.login_bt.clicked.connect(login_func)
login.exit_bt.clicked.connect(close_func)

# Butons login_ok

login_ok.okbt.clicked.connect(admin_log)

# Butons login_error

login_error.trbt.clicked.connect(tryagain_func)
login_error.exit_bt.clicked.connect(close_func)

# Butons register

register.rg_bt.clicked.connect(create_user)
register.exit_bt.clicked.connect(admin_log)

# Butons register error

error_rg.trbt.clicked.connect(register_error)
error_rg.exit_bt.clicked.connect(close_func)

# Butons created user

created_user.ok_bt.clicked.connect(created_sucess)

# Butons admin_ops

admin_ops.sh_bk.clicked.connect(search_db)
admin_ops.bk_ls.clicked.connect(list_book)
admin_ops.add_bk.clicked.connect(add_books)
admin_ops.up_bk.clicked.connect(up_books)
admin_ops.del_bk.clicked.connect(del_books)
admin_ops.rg_user.clicked.connect(criation_user)
admin_ops.exit_bt.clicked.connect(close_func)

# Butons normal_ops

normal_ops.sh_bk.clicked.connect(search_db)
normal_ops.bk_ls.clicked.connect(list_book)
normal_ops.exit_bt.clicked.connect(close_func)

# Butons add_book

add_book.add_bt.clicked.connect(add_books)
add_book.exit_bt.clicked.connect(admin_log)

# Butons error_add_book

error_bk.trbt.clicked.connect(book_add_error)
error_bk.exit_bt.clicked.connect(close_func)

# Butons sucess_add_book

sucess_bk.trbt.clicked.connect(book_add_sucess)
sucess_bk.exit_bt.clicked.connect(admin_log)

# Butons list_db

list_db.back_bt.clicked.connect(back_to)
list_db.exit_bt.clicked.connect(close_func)


# Butons search

search_rt.search_bt.clicked.connect(search_db)
search_rt.back_bt.clicked.connect(back_to_back)
search_rt.exit_bt.clicked.connect(close_func)

# Butons delete

del_book.back_bt.clicked.connect(back_to_back)
del_book.exit_bt.clicked.connect(close_func)
del_book.del_bt.clicked.connect(del_select_book)

# Butons deleted sucessful

del_book_ok.ok_bt.clicked.connect(del_sucess)

# Select book to delete

select_bk.ok_bt.clicked.connect(select_del_book)

# Butons update

up_book.up_bt.clicked.connect(save_up)
up_book.back_bt.clicked.connect(back_to_back)
up_book.exit_bt.clicked.connect(close_func)

# Buttons updated book

up_book_ok.ok_bt.clicked.connect(up_book_sucess)

# Open login screen

login.show()

# Open Program

app.exec_()

# Codigo produzido por Gabriel H. B. Machado
