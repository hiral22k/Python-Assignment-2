import csv
import os

FILE_NAME = "catalog.csv"


# ---------------- BOOK CLASS ----------------
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} | {self.author} | ISBN: {self.isbn} | {self.status}"

    def is_available(self):
        return self.status == "available"

    def issue(self):
        if not self.is_available():
            raise ValueError("Book is already issued!")
        self.status = "issued"

    def return_book(self):
        if self.is_available():
            raise ValueError("Book is not issued yet!")
        self.status = "available"


# ---------------- INVENTORY MANAGER ----------------
class LibraryInventory:
    def __init__(self):
        self.books = []
        self.load_data()

    # Load from CSV
    def load_data(self):
        if not os.path.exists(FILE_NAME):
            return      # No file yet

        try:
            with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    title, author, isbn, status = row
                    self.books.append(Book(title, author, isbn, status))
        except Exception:
            print("Error reading file. Starting with empty inventory.")
            self.books = []

    # Save to CSV
    def save_data(self):
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for b in self.books:
                writer.writerow([b.title, b.author, b.isbn, b.status])

    # Add book
    def add_book(self, book):
        if self.search_by_isbn(book.isbn):
            raise ValueError("Book with this ISBN already exists!")
        self.books.append(book)
        self.save_data()

    # Search by title
    def search_by_title(self, title):
        title = title.lower()
        return [b for b in self.books if title in b.title.lower()]

    # Search by ISBN
    def search_by_isbn(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    # Display all
    def display_all(self):
        return self.books

    # Issue book
    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("No such book!")
        book.issue()
        self.save_data()

    # Return book
    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("No such book!")
        book.return_book()
        self.save_data()


# ---------------- CLI INTERFACE ----------------
def main():
    inventory = LibraryInventory()

    while True:
        print("\n===== LIBRARY INVENTORY MANAGER =====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            isbn = input("ISBN: ")

            try:
                inventory.add_book(Book(title, author, isbn))
                print("Book added.")
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            isbn = input("Enter ISBN to issue: ")
            try:
                inventory.issue_book(isbn)
                print("Book issued.")
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            isbn = input("Enter ISBN to return: ")
            try:
                inventory.return_book(isbn)
                print("Book returned.")
            except Exception as e:
                print("Error:", e)

        elif choice == "4":
            books = inventory.display_all()
            if not books:
                print("No books found.")
            else:
                for b in books:
                    print(b)

        elif choice == "5":
            t = input("Enter title to search: ")
            results = inventory.search_by_title(t)
            if not results:
                print("No match found.")
            else:
                for b in results:
                    print(b)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()