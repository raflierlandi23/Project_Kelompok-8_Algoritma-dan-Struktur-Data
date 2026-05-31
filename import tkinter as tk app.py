import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Book:
    def __init__(self, isbn, title, author, status="Tersedia"):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.status = status

class BookNode:
    def __init__(self, book):
        self.book = book
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0
    def append(self, book):
        new_node = BookNode(book)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def delete(self, isbn):
        if not self.head:
            return False
        if self.head.book.isbn == isbn:
            self.head = self.head.next
            self.size -= 1
            return True
        current = self.head
        while current.next:
            if current.next.book.isbn == isbn:
                current.next = current.next.next
                self.size -= 1
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.book)
            current = current.next
        return result

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def to_list_reversed(self):
        return list(reversed(self.items))

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def to_list(self):
        return self.items

class BSTNode:
    def __init__(self, book):
        self.isbn = book.isbn
        self.book = book
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, book):
        self.root = self._insert_recursive(self.root, book)

    def _insert_recursive(self, root, book):
        if root is None:
            return BSTNode(book)
        if book.isbn == root.isbn:
            root.book = book
            return root
        if book.isbn < root.isbn:
            root.left = self._insert_recursive(root.left, book)
        else:
            root.right = self._insert_recursive(root.right, book)
        return root

    def search(self, isbn):
        return self._search_recursive(self.root, isbn)

    def _search_recursive(self, root, isbn):
        if root is None or root.isbn == isbn:
            return root
        if isbn < root.isbn:
            return self._search_recursive(root.left, isbn)
        return self._search_recursive(root.right, isbn)

    def rebuild(self, book_list):
        self.root = None
        for book in book_list:
            self.insert(book)

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j].isbn < arr[min_idx].isbn:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def linear_search(arr, target_title):
    matched_results = []
    for book in arr:
        if target_title.lower() in book.title.lower():
            matched_results.append(book)
    return matched_results

class LibrarySystemGUI:
    def __init__(self, window):
        self.window = window
        self.window.title("Sistem Manajemen Perpustakaan - Kelompok Genap (Tema B)")
        self.window.geometry("1000x680")
        self.window.configure(bg="#F4F6F7")

        self.books_db = LinkedList()
        self.bst_index = BinarySearchTree()
        self.audit_stack = Stack()
        self.member_queue = Queue()

        self.colors = {'bg_primary': '#2C3E50', 'bg_card': '#FFFFFF', 'text_white': '#FFFFFF', 'accent': '#16A085'}
        self.fonts = {'title': ('Arial', 12, 'bold'), 'normal': ('Arial', 10)}

        self.load_initial_data()
        self.setup_user_interface()
        self.render_table_data()

    def load_initial_data(self):
        initial_books = [
            Book("101", "Algoritma dan Struktur Data", "Asisten Laboratorium"),
            Book("103", "Pengantar Sistem Informasi", "Dosen SI"),
            Book("102", "Manajemen Basis Data Relasional", "Teknik Informatika"),
        ]
        for book in initial_books:
            self.books_db.append(book)
        self.bst_index.rebuild(self.books_db.to_list())
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), "Sistem berhasil dimuat dengan data katalog awal."))
    
    def setup_user_interface(self):
        header = tk.Frame(self.window, bg=self.colors['bg_primary'], height=55)
        header.pack(fill="x", side="top")
        tk.Label(header, text="📚 MANAGEMENT LIBRARY INDUSTRIAL APP", font=("Arial", 14, "bold"), fg=self.colors['text_white'], bg=self.colors['bg_primary']).pack(pady=12)

        workspace = tk.Frame(self.window, bg="#F4F6F7")
        workspace.pack(fill="both", expand=True, padx=15, pady=10)

        left_side = tk.Frame(workspace, bg="#F4F6F7", width=360)
        left_side.pack(fill="both", side="left", padx=(0, 10))

        right_side = tk.Frame(workspace, bg="#F4F6F7")
        right_side.pack(fill="both", side="right", expand=True)

        crud_box = tk.LabelFrame(left_side, text=" Form Modifikasi Buku (CRUD) ", font=self.fonts['title'], bg=self.colors['bg_card'])
        crud_box.pack(fill="x", pady=(0, 10), ipady=5)

        tk.Label(crud_box, text="ISBN / Kode Buku:", bg=self.colors['bg_card']).grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.input_isbn = tk.Entry(crud_box, width=24)
        self.input_isbn.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(crud_box, text="Judul Buku:", bg=self.colors['bg_card']).grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.input_title = tk.Entry(crud_box, width=24)
        self.input_title.grid(row=1, column=1, padx=8, pady=6)

        tk.Label(crud_box, text="Nama Penulis:", bg=self.colors['bg_card']).grid(row=2, column=0, padx=8, pady=6, sticky="w")
        self.input_author = tk.Entry(crud_box, width=24)
        self.input_author.grid(row=2, column=1, padx=8, pady=6)

        crud_buttons = tk.Frame(crud_box, bg=self.colors['bg_card'])
        crud_buttons.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(crud_buttons, text="Tambah (Create)", bg="#27AE60", fg="white", width=12, font=("Arial", 9, "bold"), command=self.handle_create).grid(row=0, column=0, padx=3)
        tk.Button(crud_buttons, text="Ubah (Update)", bg="#2980B9", fg="white", width=12, font=("Arial", 9, "bold"), command=self.handle_update).grid(row=0, column=1, padx=3)
        tk.Button(crud_buttons, text="Hapus (Delete)", bg="#C0392B", fg="white", width=12, font=("Arial", 9, "bold"), command=self.handle_delete).grid(row=0, column=2, padx=3)

        queue_box = tk.LabelFrame(left_side, text=" Antrean Meja Layanan (Queue) ", font=self.fonts['title'], bg=self.colors['bg_card'])
        queue_box.pack(fill="x", pady=(0, 10), ipady=5)

        tk.Label(queue_box, text="Nama Pengunjung:", bg=self.colors['bg_card']).grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.input_member = tk.Entry(queue_box, width=24)
        self.input_member.grid(row=0, column=1, padx=8, pady=6)

        queue_buttons = tk.Frame(queue_box, bg=self.colors['bg_card'])
        queue_buttons.grid(row=1, column=0, columnspan=2, pady=5)

        tk.Button(queue_buttons, text="Masuk Antrean", bg="#D35400", fg="white", width=12, font=("Arial", 9, "bold"), command=self.handle_enqueue).grid(row=0, column=0, padx=5)
        tk.Button(queue_buttons, text="Panggil/Layani", bg="#8E44AD", fg="white", width=12, font=("Arial", 9, "bold"), command=self.handle_dequeue).grid(row=0, column=1, padx=5)

        self.label_queue_status = tk.Label(queue_box, text="Antrean Saat Ini: Kosong", bg=self.colors['bg_card'], font=("Arial", 9, "italic"), fg="#7F8C8D")
        self.label_queue_status.grid(row=2, column=0, columnspan=2, pady=5)