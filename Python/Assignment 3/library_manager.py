# =========================================
# Name: Prachi Yadav
# date = 26-11-25
# batch = B.Tech CSE (AI/ML)
# title = Library Manager
# =========================================

import logging

# Create log file
logging.basicConfig(filename="library_log.txt",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# ==============================
# Task 1: Book Class
# ==============================
class Book:
    def __init__(self, title, author, isbn, status):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            logging.info(f"Book issued: {self.title}")
            print("Book issued successfully.")
        else:
            print("Book already issued.")

    def return_book(self):
        if self.status == "issued":
            self.status = "available"
            logging.info(f"Book returned: {self.title}")
            print("Book returned successfully.")
        else:
            print("Book already available.")


# ==============================
# Task 2: Library Inventory Class
# ==============================
class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book_obj):
        self.books.append(book_obj)
        logging.info(f"Book added: {book_obj.title}")

    def search_by_title(self, title):
        for bk in self.books:
            if bk.title == title:
                print(bk)
                return
        print("Book not found.")

    def search_by_isbn(self, isbn):
        for bk in self.books:
            if bk.isbn == isbn:
                print(bk)
                return
        print("Book not found.")

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        else:
            for bk in self.books:
                print(bk)

    # Save inventory to file
    def save_to_file(self, filename="library_output.txt"):
        try:
            with open(filename, "w") as file:
                for bk in self.books:
                    file.write(f"{bk.title},{bk.author},{bk.isbn},{bk.status}\n")
            print("Library saved to file.")
        except Exception as e:
            logging.error(f"Save error: {e}")
            print("Error saving file.")

    # Load inventory from file
    def load_from_file(self, filename="library_output.txt"):
        try:
            with open(filename, "r") as file:
                for line in file:
                    title, author, isbn, status = line.strip().split(",")
                    self.books.append(Book(title, author, isbn, status))
            print("Library loaded from file.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            logging.error(f"Load error: {e}")
            print("Error loading file.")


# ==============================
# Task 4: CLI Menu
# ==============================
def interactive_cli():
    inventory = LibraryInventory()

    while True:
        print("\n==== Library Menu ====")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book by Title")
        print("6. Search Book by ISBN")
        print("7. Save Library")
        print("8. Load Library")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            title = input("Enter title: ")
            author = input("Enter author: ")
            isbn = input("Enter ISBN: ")
            book_obj = Book(title, author, isbn, "available")
            inventory.add_book(book_obj)
            print("Book added.")

        elif choice == '2':
            isbn = input("Enter ISBN to issue: ")
            for bk in inventory.books:
                if bk.isbn == isbn:
                    bk.issue()
                    break
            else:
                print("Book not found.")

        elif choice == '3':
            isbn = input("Enter ISBN to return: ")
            for bk in inventory.books:
                if bk.isbn == isbn:
                    bk.return_book()
                    break
            else:
                print("Book not found.")

        elif choice == '4':
            inventory.display_all()

        elif choice == '5':
            title = input("Enter title to search: ")
            inventory.search_by_title(title)

        elif choice == '6':
            isbn = input("Enter ISBN to search: ")
            inventory.search_by_isbn(isbn)

        elif choice == '7':
            inventory.save_to_file()

        elif choice == '8':
            inventory.load_from_file()

        elif choice == '9':
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


# Run program
if __name__ == "__main__":
    interactive_cli()