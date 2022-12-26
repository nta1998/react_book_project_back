from datetime import datetime
from flask import Flask,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json

app=Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50))
    Author = db.Column(db.String(35))
    Year_Published = db.Column(db.Date)
    Type = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    book_Loan = db.relationship("Loans", backref="book_loaner")
    def __init__(self, Name, Author, Year_Published, Type, active):
        self.Name = Name
        self.Author = Author
        self.Year_Published = Year_Published
        self.Type = Type
        self.active = active

class Customers(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(35))
    City = db.Column(db.String(35))
    Age = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    book_Loans = db.relationship("Loans",backref='customers')
    def __init__(self, Name, City, Age,active):
        self.Name = Name
        self.City = City
        self.Age = Age
        self.active = active

class Loans(db.Model):

    id = db.Column('Loans_id', db.Integer, primary_key=True)
    customers_id = db.Column(db.Integer,db.ForeignKey('customers.id'))
    BookID = db.Column(db.Integer,db.ForeignKey('books.id'))
    Loandate = db.Column(db.Date)
    Returndate = db.Column(db.Date)
    returned = db.Column(db.Boolean)

    
    def __init__(self, Loandate, Returndate, BookID,returned,customers_id):
        self.Loandate = Loandate
        self.customers_id = customers_id
        self.Returndate = Returndate
        self.BookID = BookID
        self.returned = returned

@app.route('/Books',methods=['GET'])
@app.route('/Books/add',methods=['POST'])
@app.route('/Book/change/<id>',methods=['DELETE','PUT'])
def crud_Books(id=-1):
    if request.method == "GET":
        all_books=[]
        for book in Books.query.all():
            all_books.append({'id':book.id,'Name':book.Name,'Author':book.Author,'Year_Published' : f'{book.Year_Published}', "Type":book.Type, "active":book.active})
        return (json.dumps(all_books))
    if request.method == "POST":
       request_data = request.get_json()
       Name = request_data['Name']
       Author = request_data['Author']
       print(request_data['Year_Published'])
       Year_Published = datetime.strptime(request_data['Year_Published'],'%Y-%m-%d').date()
       Type = request_data['Type']
       active = False
       newperson = Books(Name,Author,Year_Published,Type,active)
       db.session.add(newperson)
       db.session.commit()
       return []
    if request.method == "DELETE":
        the_book_del=Books.query.get(id)
        db.session.delete(the_book_del)
        db.session.commit()
        return{}
    if request.method == "PUT":
        the_put_book=Books.query.get(id)
        request_data = request.get_json()
        the_put_book.Name = request_data['Name']
        the_put_book.Author = request_data['Author']
        the_put_book.Year_Published = datetime.strptime(request_data['Year_Published'],'%Y-%m-%d').date()
        the_put_book.Type = request_data['Type']
        db.session.commit()
        return{}

@app.route('/Customers',methods=['GET'])
@app.route('/Customers/add',methods=['POST'])
@app.route('/Customers/change/<id>',methods=['DELETE','PUT'])
def crud_Customers(id=-1):
    if request.method == "GET":
        all_customers=[]
        for customer in Customers.query.all():
            all_customers.append({'id':customer.id,'Name':customer.Name,'City':customer.City,'Age':customer.Age,"active":customer.active})
        return (json.dumps(all_customers))
    if request.method == "POST":
       request_data = request.get_json()
       Name = request_data['Name']
       City = request_data['City']
       Age = request_data['Age']
       active = False
       newperson = Customers(Name,City,Age,active)
       db.session.add(newperson)
       db.session.commit()
       return []
    if request.method == "DELETE":
        the_customer_del=Customers.query.get(id)
        db.session.delete(the_customer_del)
        db.session.commit()
        return{}
    if request.method == "PUT":
        the_customer_del=Customers.query.get(id)
        request_data = request.get_json()
        the_customer_del.Name = request_data['Name']
        the_customer_del.City = request_data['City']
        the_customer_del.Age = request_data['Age']
        db.session.commit()
        return{}
@app.route('/Loans',methods=['GET'])
@app.route('/Loans/add',methods=['POST'])
@app.route('/Loans/change/<id>',methods=['DELETE','PUT'])
def crud_Loans(id=-1):
    if request.method == "GET":
        all_loaner=[]
        for loaner in Loans.query.all():
            all_loaner.append({'id':loaner.id,'Loandate':f"{loaner.Loandate}",'Returndate':f"{loaner.Returndate}",'customers_id':loaner.customers_id,'BookID':loaner.BookID, "cosName":loaner.customers.Name , "bookName":loaner.book_loaner.Name ,"returned":loaner.returned })
        return (json.dumps(all_loaner))
    if request.method == "POST":
       request_data = request.get_json()
       print(request_data)
       customers_id = request_data['customers_id']
       BookID = request_data['BookID']
       print(request_data['Returndate'])
       Loandate = datetime.strptime(request_data['Loandate'],'%Y-%m-%d').date()
       Returndate = datetime.strptime(request_data['Returndate'],'%Y/%m/%d').date()
       returned = False
       newperson = Loans(Loandate,Returndate,BookID,returned,customers_id)
       db.session.add(newperson)
       db.session.commit()
       return []
    if request.method == "DELETE":
        the_loans_del=Loans.query.get(id)
        db.session.delete(the_loans_del)
        db.session.commit()
        return{}
    if request.method == "PUT":
        the_loans_del=Loans.query.get(id)
        request_data = request.get_json()
        the_loans_del.Loandate = datetime.strptime(request_data['Loandate'],'%Y-%m-%d').date()
        the_loans_del.Returndate = datetime.strptime(request_data['Returndate'],'%Y-%m-%d').date()
                         
       
        db.session.commit()
        return{}
@app.route('/Loans/returned/<id>',methods=['DELETE','PUT'])
def returned_crod(id):
    if request.method == "PUT":
        the_loans_del=Loans.query.get(id)
        request_data = request.get_json()
        the_loans_del.returned = request_data['returned']
        db.session.commit()
        return{}
    
@app.route('/')
def is_on():
    return '<h1>all good</h1>'
if __name__==('__main__'):
    with app.app_context():
        db.create_all()
    app.run(debug=True)