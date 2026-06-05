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

        queue_box = tk.LabelFrame(left_side, text=" Antrean Pengunjung (Queue) ", font=self.fonts['title'], bg=self.colors['bg_card'])
        queue_box.pack(fill="x", pady=5, ipady=5)

        tk.Label(queue_box, text="Nama Member:", bg=self.colors['bg_card']).grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.input_member = tk.Entry(queue_box, width=16)
        self.input_member.grid(row=0, column=1, padx=8, pady=8)

        tk.Button(queue_box, text="Masuk Antrean", bg="#8E44AD", fg="white", font=("Arial", 8, "bold"), command=self.handle_enqueue).grid(row=0, column=2, padx=5)

        self.label_queue_state = tk.Label(queue_box, text="Antrean Saat Ini: [ Kosong ]", bg=self.colors['bg_card'], fg="#7F8C8D", wraplength=330, justify="left")
        self.label_queue_state.grid(row=1, column=0, columnspan=3, padx=8, pady=8, sticky="w")

        tk.Button(queue_box, text="Panggil & Layani Antrean Terdepan", bg="#D35400", fg="white", font=("Arial", 9, "bold"), command=self.handle_dequeue).grid(row=2, column=0, columnspan=3, pady=5, sticky="we", padx=10)

        toolbar = tk.Frame(right_side, bg="#F4F6F7")
        toolbar.pack(fill="x", pady=(0, 5))

        tk.Label(toolbar, text="Cari Judul:", bg="#F4F6F7", font=("Arial", 9, "bold")).pack(side="left", padx=2)
        self.input_search = tk.Entry(toolbar, width=20)
        self.input_search.pack(side="left", padx=5)

        tk.Button(toolbar, text="Cari (Linear Search)", bg="#F39C12", fg="white", font=("Arial", 8, "bold"), command=self.handle_search).pack(side="left", padx=2)
        tk.Button(toolbar, text="Reset View", bg="#7F8C8D", fg="white", font=("Arial", 8, "bold"), command=lambda: self.render_table_data()).pack(side="left", padx=5)
        tk.Button(toolbar, text="Urutkan ISBN (Selection Sort)", bg="#16A085", fg="white", font=("Arial", 8, "bold"), command=self.handle_sort).pack(side="right", padx=2)

        self.tree = ttk.Treeview(right_side, columns=("ISBN", "Judul", "Penulis", "Status"), show="headings", height=13)
        self.tree.heading("ISBN", text="ISBN / Kode Buku")
        self.tree.heading("Judul", text="Judul Katalog Buku")
        self.tree.heading("Penulis", text="Nama Penulis")
        self.tree.heading("Status", text="Status")
        self.tree.column("ISBN", width=90, anchor="center")
        self.tree.column("Judul", width=240, anchor="w")
        self.tree.column("Penulis", width=140, anchor="w")
        self.tree.column("Status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.handle_row_selection)

        stack_box = tk.LabelFrame(right_side, text=" Log Operasi Sistem Terkini (LIFO Stack) ", font=self.fonts['title'], bg=self.colors['bg_card'])
        stack_box.pack(fill="x", pady=(5, 0))

        self.log_viewer = tk.Text(stack_box, height=5, bg="#ECF0F1", fg="#2C3E50", font=("Courier New", 9))
        self.log_viewer.pack(fill="both", expand=True, padx=5, pady=5)
        self.log_viewer.config(state="disabled")
        self.render_stack_logs()

    def render_table_data(self, custom_dataset=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        dataset = custom_dataset if custom_dataset is not None else self.books_db.to_list()
        for book in dataset:
            self.tree.insert("", "end", values=(book.isbn, book.title, book.author, book.status))

    def render_stack_logs(self):
        self.log_viewer.config(state="normal")
        self.log_viewer.delete("1.0", tk.END)
        for timestamp, action in self.audit_stack.to_list_reversed():
            self.log_viewer.insert(tk.END, f"[{timestamp}] {action}\n")
        self.log_viewer.config(state="disabled")

    def render_queue_status(self):
        q_items = self.member_queue.to_list()
        if not q_items:
            self.label_queue_state.config(text="Antrean Saat Ini: [ Kosong ]", fg="#7F8C8D")
        else:
            line = " -> ".join([f"[{i+1}] {name}" for i, name in enumerate(q_items)])
            self.label_queue_state.config(text=f"Antrean: {line}", fg="#2C3E50")

    def handle_row_selection(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        fields = self.tree.item(selection[0])['values']
        self.clear_form_inputs()
        self.input_isbn.insert(0, str(fields[0]))
        self.input_title.insert(0, str(fields[1]))
        self.input_author.insert(0, str(fields[2]))

    def clear_form_inputs(self):
        self.input_isbn.delete(0, tk.END)
        self.input_title.delete(0, tk.END)
        self.input_author.delete(0, tk.END)

    def handle_create(self):
        isbn = self.input_isbn.get().strip()
        title = self.input_title.get().strip()
        author = self.input_author.get().strip()

        if not isbn or not title or not author:
            messagebox.showwarning("Gagal Simpan", "Seluruh data input wajib diisi lengkap!")
            return

        if self.bst_index.search(isbn) is not None:
            messagebox.showerror("Duplikasi ISBN", f"Gagal menambahkan, Buku dengan ID '{isbn}' sudah ada!")
            return

        new_book = Book(isbn, title, author)
        self.books_db.append(new_book)
        self.bst_index.rebuild(self.books_db.to_list())
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"CREATE: Sukses menambah buku '{title}' [ISBN: {isbn}]"))

        self.clear_form_inputs()
        self.render_table_data()
        self.render_stack_logs()
        messagebox.showinfo("Sukses", "Buku baru berhasil ditambahkan!")

    def handle_update(self):
        isbn = self.input_isbn.get().strip()
        title = self.input_title.get().strip()
        author = self.input_author.get().strip()

        if not isbn:
            messagebox.showwarning("Gagal", "Silakan masukkan nomor ISBN target yang ingin diperbarui!")
            return

        found_node = self.bst_index.search(isbn)
        if found_node is None:
            messagebox.showerror("Tidak Ditemukan", f"Buku dengan ISBN '{isbn}' tidak terdaftar.")
            return

        target_book = found_node.book
        if title: target_book.title = title
        if author: target_book.author = author

        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"UPDATE: Mengubah informasi rincian buku ISBN {isbn}"))
        self.clear_form_inputs()
        self.render_table_data()
        self.render_stack_logs()
        messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")

    def handle_delete(self):
        isbn = self.input_isbn.get().strip()
        if not isbn:
            messagebox.showwarning("Gagal", "Pilih data buku dari tabel untuk dihapus!")
            return

        is_deleted = self.books_db.delete(isbn)
        if not is_deleted:
            messagebox.showerror("Gagal", f"Buku dengan ISBN '{isbn}' tidak ditemukan.")
            return

        self.bst_index.rebuild(self.books_db.to_list())
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"DELETE: Menghapus buku ber-ISBN {isbn} dari katalog."))
        self.clear_form_inputs()
        self.render_table_data()
        self.render_stack_logs()
        messagebox.showinfo("Sukses", f"Buku dengan ISBN '{isbn}' telah dihapus dari sistem.")

    def handle_sort(self):
        current_data = self.books_db.to_list()
        sorted_data = selection_sort(current_data)
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), "SORT: Mengurutkan tabel katalog via Selection Sort murni."))
        self.render_table_data(sorted_data)
        self.render_stack_logs()

    def handle_search(self):
        query = self.input_search.get().strip()
        if not query:
            messagebox.showwarning("Kosong", "Masukkan kata kunci judul buku!")
            return

        all_records = self.books_db.to_list()
        filtered_results = linear_search(all_records, query)
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"SEARCH: Menelusuri kata kunci '{query}' lewat Linear Search."))
        self.render_stack_logs()

        if not filtered_results:
            messagebox.showinfo("Info Pencarian", f"Tidak ada judul buku yang mengandung kata '{query}'.")
        else:
            self.render_table_data(filtered_results)

    def handle_enqueue(self):
        member_name = self.input_member.get().strip()
        if not member_name:
            messagebox.showwarning("Kosong", "Ketik nama member terlebih dahulu!")
            return

        self.member_queue.enqueue(member_name)
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"QUEUE: '{member_name}' masuk antrean meja admin."))
        self.input_member.delete(0, tk.END)
        self.render_queue_status()
        self.render_stack_logs()

    def handle_dequeue(self):
        served_member = self.member_queue.dequeue()
        if served_member is None:
            messagebox.showinfo("Antrean Kosong", "Tidak ada antrean pengunjung saat ini.")
            return
        self.audit_stack.push((datetime.now().strftime("%H:%M:%S"), f"DEQUEUE: Memanggil & melayani member '{served_member}'."))
        self.render_queue_status()
        self.render_stack_logs()
        messagebox.showinfo("Panggilan Layanan", f"Panggilan: Silakan member atas nama '{served_member}' merapat ke meja admin!")

if __name__ == "__main__":
    app_window = tk.Tk()
    app_engine = LibrarySystemGUI(app_window)
    app_window.mainloop()
