class Book:
    def __init__(self, book_id, name, quantity):
        self.id = book_id
        self.name = name
        self.quantity = quantity

    def borrow_copy(self):
        if self.quantity <= 0:
            return False
        self.quantity -= 1
        return True

    def return_copy(self):
        self.quantity += 1
        return True

    def __str__(self):
        return f"Book ID: {self.id}, Name: {self.name}, Quantity: {self.quantity}"

    def __repr__(self):
        return f"Book({self.id}, {self.name}, {self.quantity})"

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["id"], data["name"], data["quantity"])

    def update_quantity(self, new_quantity):
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        self.quantity = new_quantity

    def is_available(self):
        return self.quantity > 0

    def get_details(self):
        return f"Book ID: {self.id}, Name: {self.name}, Quantity: {self.quantity}"


class User:
    def __init__(self, user_id, name):
        self.id = user_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        if book in self.borrowed_books:
            return False
        if book.borrow_copy():
            self.borrowed_books.append(book)
            return True
        return False

    def return_book(self, book):
        if book in self.borrowed_books:
            book.return_copy()
            self.borrowed_books.remove(book)
            return True
        return False

    def get_borrowed_books(self):
        return [book.get_details() for book in self.borrowed_books]

    def __str__(self):
        return f"User ID: {self.id}, Name: {self.name}, Borrowed Books: {len(self.borrowed_books)}"


class Admin:
    def __init__(self, admin_id, name):
        self.id = admin_id
        self.name = name

    def add_book(self, library, book):
        library.add_book(book)

    def remove_book(self, library, book):
        library.remove_book(book)

    def update_book_quantity(self, book, new_quantity):
        book.update_quantity(new_quantity)

    def __str__(self):
        return f"Admin ID: {self.id}, Name: {self.name}"

    def menu(self):
        print("Admin Menu:")
        print("1. Add Book")
        print("2. Remove Book")
        print("3. Update Book Quantity")
        print("4. View All Books")
        print("5. Exit")

    def control_book_borrowing(self, library, user, book):
        if user.borrow_book(book):
            print(f"{user.name} borrowed {book.name}.")
        else:
            print(f"{book.name} is not available for borrowing.")

    def control_book_returning(self, library, user, book):
        if user.return_book(book):
            print(f"{user.name} returned {book.name}.")
        else:
            print(f"{user.name} has not borrowed {book.name}.")
