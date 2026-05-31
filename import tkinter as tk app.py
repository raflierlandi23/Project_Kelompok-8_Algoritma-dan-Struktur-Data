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

