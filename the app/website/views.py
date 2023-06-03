from flask import Blueprint , render_template, request
from bson import objectid
import bson 
import pymongo
from pymongo import MongoClient
from flask_login import   current_user

cluster = MongoClient("mongodb+srv://iamnivedhav:N1vedha@cluster0.hfklgll.mongodb.net/?retryWrites=true&w=majority",serverSelectionTimeoutMS=5000)
db= cluster["myapp"]
products = db["products"]
users= db['users']
chat=db['chat']

views = Blueprint('views',__name__)

@views.route('/<user_id>')
def home(user_id):
    home_products= db.products.find()
    return render_template("home1.html",products=home_products,user_id = user_id)

@views.route('/about-us')
def about_us():
    return render_template("about-us.html")

@views.route('/<user_id>/search')
def search(user_id):
    return render_template("search.html",user_id=user_id)

@views.route('/product/<user_id>/<product_id>')
def product(user_id,product_id):
    no=int(product_id)
    product_details= db.products.find_one({"_id":no})
    return render_template("product.html",product_details=product_details ,user_id=user_id)

@views.route("/<user_id>/my-product")
def my_product(user_id):    
    n= int(user_id)
    my_products= db.products.find({"user_id":n})
    return render_template("my-product.html",my_products=my_products,user_id=user_id)


@views.route('view-product/<product_id>')
def view_product(product_id):  
    no=int(product_id)
    product_details= products.find_one({"_id":no})
    return render_template("view-product.html",product_details=product_details)

@views.route('/<user_id>/new-product', methods= ['GET','POST'])
def new_product(user_id):
   if request.method =='POST':
        product_name= request.form.get("name")
        catagory= request.form.get("catagory")
        sub_catagory= request.form.get("sub_catagory")
        description= request.form.get("description")  
        price= request.form.get("price")
        product_details={'_id':1011, 'user_id':100,'product_name':product_name, 'catagory':catagory, 'sub_catagory':sub_catagory,'price':price,'description':description}
        db.users.insert_one(product_details)
        flash("Product added successfully", category='success')

   return render_template("new-product.html",user_id=user_id)

@views.route('/chatuser/<user_id>/<product_id>', methods= ['GET','POST'])    
def chat_user(user_id,product_id):
    if request.method=="POST":
        message= request.form.get("message")
        sender='user'
        db.chat.insert_one({'message':message,'sender':sender})
        return render_template("chat.html",user_id=user_id,product_id=product_id)
    old_chats=db.chat.find({"user_id":user_id,'product_id':product_id})
    return render_template("chat_user.html",user_id=user_id,product_id=product_id)

@views.route('/chatproduct/<product_id>/<user_id>', methods= ['GET','POST'])    
def chat_product(user_id,product_id):
    if request.method=="POST":
        message= request.form.get("message")
        sender='product'
        db.chat.insert_one({'message':message,'sender':sender})
        return render_template("chat.html",user_id=user_id,product_id=product_id)
    old_chats=db.chat.find({"user_id":user_id,'product_id':product_id})
    return render_template("chat_product.html",user_id=user_id,product_id=product_id)

