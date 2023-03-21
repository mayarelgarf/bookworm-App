import flask
import json
from flask import jsonify, redirect,render_template

app = flask.Flask('book')

#the review class
class review():
    def __init__(self,author,rating,text ):
        self.author = author
        self.rating = int(rating)
        self.text = text

    def to_dict(self):
        return{
            'author':self.author,
            'rating': self.rating,
            'text': self.text
        }
    
    @staticmethod
    # taking input from review form
    def write_review():
        reviewer= flask.request.args.get('reviewer')
        rating = flask.request.args.get('rating')
        text = flask.request.args.get('text')
        new_review= review(reviewer,rating,text)
        review_dict= new_review.to_dict()
    
        return review_dict

#get html page 
def get_html(page_name):
    html_file = open(page_name + ".html")
    content= html_file.read()
    html_file.close()
    return content


#route for the landing page
@app.route('/')
def landingpage():
    return get_html("landing")

#route for the Home page
@app.route('/home')
def homepage():
    return get_html('home')

#get all books from json file 
def get_books_from_json_file():
     bookdb= open('booklib.json','r')
     books =json.load(bookdb) 
     bookdb.close()
     return books
# save the updated book list with new review
def save_books_to_json_file(books):
    with open('booklib.json', 'r+') as bookdb:
              
               bookdb.seek(0)  # Move the file pointer to the beginning of the file
               json.dump(books, bookdb, indent=4)  # Write the updated data back to the file
               bookdb.truncate()  # Truncate the file to remove any extra data
               return True

#get the book matching the searched book from json file        
def retrieve_book():
    searched_book = flask.request.args.get('searchedBook')
    books = get_books_from_json_file()
    matching_book = {}
    for book in books:
        if searched_book.lower().replace(" ","") in str(book['title']).lower().replace(" ","") or searched_book.lower() == str(book['title']).lower().replace(" ","") :
            matching_book = book
    return matching_book
   
#display matching book page
@app.route('/book')
def bookpage():
    searched_book = retrieve_book()
    if searched_book == {}:
        return redirect('/notfound')
    else:
        book = searched_book
        return render_template('book.html', book= book)
    
#not found page route
@app.route('/notfound')
def notfoundpage():
    return get_html('notfound')


  

#route for the review page
@app.route('/review')
def reviewpage():
    page = get_html('review')
    book = flask.request.args.get('bookTitle').replace(' ','').lower()
    print(book)
    return page.replace('$$title$$',str(book))

#route for the thank youpage
@app.route('/thanks')
def thanks():
     booktitle = flask.request.args.get('title')
     print(booktitle)
     review_dict = review.write_review()
     books = get_books_from_json_file()
     for book in books:
        if booktitle == str(book['title']).replace(' ','').lower():
         book['reviews'].append(review_dict) 
         break
     save_books_to_json_file(books)  # write the updated list of books back to file
     return get_html('thanks')

# by the help of chat gpt
#delete a review
@app.route('/delete_review/<string:book_title>/<string:review_author>', methods=['DELETE'])
def delete_review(book_title, review_author):
    # Load the books from the JSON file
    books = get_books_from_json_file()

    # Find the book with the given title
    for book in books:
        if book['title'] == book_title:
            # Find the review with the given author and remove it
            for review in book['reviews']:
                if review['author'] == review_author:
                    book['reviews'].remove(review)
                    break

            # Save the updated books to the JSON file
            with open('booklib.json', 'w') as f:
                json.dump(books, f, indent=4)

            return jsonify({'success': True}), 200

    # If the book or review wasn't found, return an error
    return jsonify({'error': 'Book or review not found'}), 404
#admin page
@app.route('/admin')
def admin_page():
    books = get_books_from_json_file()
    return render_template('admin.html',books = books)

#update a review
@app.route('/update_review')
def update_review():
    books = get_books_from_json_file()
    book_title = flask.request.args.get('booktitle')
    review_author= flask.request.args.get('reviewAuthor')
    review_rating = flask.request.args.get('rating')
    review_text= flask.request.args.get('text')
    # Find the book with the given title
    for book in books:
        if book['title'] == book_title:
            # Find the review with the given author and remove it
            for review in book['reviews']:
                if review['author'] == review_author:
                    review['rating']= int(review_rating)
                    review['text']= review_text
                    break

    
    save_books_to_json_file(books)
    return redirect('/admin')
                    

