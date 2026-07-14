class Book:
    def __init__(self, book_id, name, quantity):
        self.id = book_id
        self.name = name
        self.quantity = quantity

    def is_available(self):
        return self.quantity > 0

    def borrow(self):
        if self.quantity > 0:
            self.quantity -= 1
            return True
        return False

    def return_copy(self):
        self.quantity += 1

    def matches_prefix(self, prefix):
        return self.name.lower().startswith(prefix.lower())

    def __str__(self):
        return f"ID: {self.id} | {self.name} ({self.quantity} copies)"


class User:
    MAX_BOOKS = 3

    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.borrowed_books = []

    def can_borrow(self):
        return len(self.borrowed_books) < User.MAX_BOOKS

    def borrow_book(self, book):
        if not self.can_borrow() or book in self.borrowed_books or not book.borrow():
            return False
        self.borrowed_books.append(book)
        return True

    def return_book(self, book):
        if book not in self.borrowed_books:
            return False
        self.borrowed_books.remove(book)
        book.return_copy()
        return True

    def show_details(self):
        print(f"  User: {self.name} (ID: {self.id})")
        print(f"  Borrowed ({len(self.borrowed_books)}/{User.MAX_BOOKS}):")
        if not self.borrowed_books:
            print("    None")
        else:
            for b in self.borrowed_books:
                print(f"    - {b.name}")


class Admin:
    def __init__(self):
        self.books = []
        self.users = []

    def find_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def find_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def show_menu(self):
        print("\n" + "=" * 40)
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print(" 1. Add Book")
        print(" 2. Show All Books")
        print(" 3. Search Books")
        print(" 4. Add User")
        print(" 5. Borrow Book")
        print(" 6. Return Book")
        print(" 7. Show Users")
        print(" 8. Exit")

    def get_choice(self):
        while True:
            choice = input("\nEnter your choice: ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= 8:
                    return choice
            print("Invalid choice. Try again.")

    def add_book(self):
        print("\n=== Add Book ===")
        book_id = input("Book ID: ").strip()
        if self.find_book(book_id):
            print("That ID already exists.")
            return
        while True:
            name = input("Book name: ").strip()
            if name:
                break
            print("Name cannot be empty.")
        while True:
            qty = input("Quantity: ").strip()
            if qty.isdigit() and int(qty) > 0:
                qty = int(qty)
                break
            print("Must be a positive number.")
        self.books.append(Book(book_id, name, qty))
        print(f"Added '{name}'!")

    def add_user(self):
        print("\n=== Add User ===")
        user_id = input("User ID: ").strip()
        if self.find_user(user_id):
            print("That ID already exists.")
            return
        while True:
            name = input("User name: ").strip()
            if name:
                break
            print("Name cannot be empty.")
        self.users.append(User(user_id, name))
        print(f"Added '{name}'!")

    def show_books(self):
        print("\n=== Library Books ===")
        if not self.books:
            print("No books yet.")
            return
        for book in sorted(self.books, key=lambda b: b.name.lower()):
            print(f"  {book}")

    def search_books(self):
        prefix = input("Enter prefix: ").strip().lower()
        found = [b for b in self.books if b.name.lower().startswith(prefix)]
        print()
        if not found:
            print("No matching books.")
            return
        for book in sorted(found, key=lambda b: b.name.lower()):
            print(f"  {book}\n")

    def borrow_book(self):
        print("\n=== Borrow Book ===")
        try:
            uid = int(input("User ID: ").strip())
            bid = int(input("Book ID: ").strip())
        except ValueError:
            print("IDs must be whole numbers.")
            return
        user = self.find_user(uid)
        book = self.find_book(bid)
        if not user:
            print("User not found.")
            return
        if not book:
            print("Book not found.")
            return
        if user.borrow_book(book):
            print(f"{user.name} borrowed '{book.name}'!")
        else:
            print("Can't borrow. (Limit reached, already borrowed, or no copies)")

    def return_book(self):
        print("\n=== Return Book ===")
        try:
            uid = int(input("User ID: ").strip())
            bid = int(input("Book ID: ").strip())
        except ValueError:
            print("IDs must be whole numbers.")
            return
        user = self.find_user(uid)
        book = self.find_book(bid)
        if not user:
            print("User not found.")
            return
        if not book:
            print("Book not found.")
            return
        if user.return_book(book):
            print(f"{user.name} returned '{book.name}'!")
        else:
            print("This user doesn't have that book.")

    def show_users(self):
        print("\n=== Users ===")
        if not self.users:
            print("No users yet.")
            return
        for user in sorted(self.users, key=lambda u: u.name.lower()):
            print("-" * 35)
            user.show_details()

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_choice()
            if choice == 1:
                self.add_book()
            elif choice == 2:
                self.show_books()
            elif choice == 3:
                self.search_books()
            elif choice == 4:
                self.add_user()
            elif choice == 5:
                self.borrow_book()
            elif choice == 6:
                self.return_book()
            elif choice == 7:
                self.show_users()
            elif choice == 8:
                print("\nThanks for visiting the library!")
                break


if __name__ == "__main__":
    Admin().run()