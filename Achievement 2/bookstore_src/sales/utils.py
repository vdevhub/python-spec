from books.models import Book  # you need to connect parameters from books model


# define a function that takes the ID
def get_bookname_from_id(val):
    # this ID is used to retrieve the name from the record
    bookname = Book.objects.get(id=val)
    # and the name is returned back
    return bookname
