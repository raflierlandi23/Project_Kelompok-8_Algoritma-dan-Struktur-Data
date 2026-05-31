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
