from flask import Flask,request, render_template,redirect, url_for ,request, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timedelta


app = Flask(__name__)

app.secret_key = 'SECRET_KEY'
app.permanent_session_lifetime = timedelta(minutes=1)


def get_database():
 
   CONNECTION_STRING ="localhost" # this is the ip address
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING,27017)   #27017 is the port number

   # Create the database for our example (we will use the same database throughout the tutorial
   
   return client['UserDetails']


@app.route('/')
@app.route('/homeintro')
def intro_page():
    return render_template('homeintro.html')

@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/home')
def home_page():
    image_path = url_for('static', filename='download.jpg')

    return render_template('home.html', image_path=image_path)


@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/addcontact', methods=['GET', 'POST'])
def addcontact():
    if request.method == 'POST':
        # Retrieve the user's email from the query parameters
        user_email = request.args.get('email')
        
        # Retrieve and save the contact data associated with the user
        db_name = get_database()
        contact_collection = db_name['Contact']
        
        name = request.form['contact_name']
        phone = request.form['contact_number']
        
        contact = {'name': name, 'phone': phone, 'user_email': user_email}
        contact_collection.insert_one(contact)
        
        return redirect(url_for('home_page'))
    image_path = url_for('static', filename='download.jpg')
    return render_template('addcontact.html', image_path=image_path)


@app.route('/seecontacts')
def seecontacts():
    if 'email' not in session:
        return redirect(url_for('login_page'))

    # Retrieve the user's email from the session
    user_email = session['email']
    
    # Retrieve and display the contacts associated with the user
    db_name = get_database()
    contact_collection = db_name['Contact']
    
    contacts = contact_collection.find({'user_email': user_email})

    image_path = url_for('static', filename='download.jpg')
    return render_template('seecontact.html', contacts=contacts, image_path=image_path)



@app.route('/add_user', methods=['POST'])
def add_place():

    db_name=get_database()
    user_collection=db_name['User']


    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    
    place = {'place_name': name, 'email': email, 'password': password }
    user_collection.insert_one(place)
    return redirect(url_for('login_page'))


@app.route('/authenticate', methods=['POST'])
def authenticate():

    db_name=get_database()
    user_collection=db_name['User']



    email = request.form['email']
    password = request.form['password']
    userone = user_collection.find_one({'email': email,'password':password})  

    if(userone):
        session['email'] = email
        session.permanent = True 
        return redirect(url_for('home_page'))
    else:
        return redirect(url_for('login_page'))
    
@app.route('/logout')
def logout():
    session.clear()  # Clear session data
    return redirect(url_for('login_page'))  # Redirect to the login page



app.run(host='0.0.0.0', port=8080)

