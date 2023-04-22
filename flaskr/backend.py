from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
#hasing library
from cryptography.fernet import Fernet
from csv import writer
import csv

# TODO(Project 1): Implement Backend according to the requirements.
#Upload usage 
app = Flask(__name__)

# -> Add cloud as a dependency when creating backend class
class Backend:
    
    """ The backend process all infomation taken from and returning it to pages.py for the information to be proccessed
    or displayes later trhough a html template and in some cases adding files to the buckets or retiving to from the buckets
    """
        #-> Add bucket_provider as dependency 
    def __init__(self,storage_client = storage.Client()):
        #The ID of  GCS bucket with users info
        self.users_bucket_name = "users_passwords_project1"
        # The ID of GCS bucket with pages
        self.pages_bucket_name = "project1_wiki_content"

        # Instantiates a client
        self.storage_client = storage_client
        # Creates the new bucket
        self.pages_bucket = self.storage_client.bucket(self.pages_bucket_name)
        

        #bucket created for user passwords
        self.user_files = self.storage_client.bucket(self.users_bucket_name)
    
        #upload buckets and blobs 
        self.bucket = self.storage_client.bucket("project1_wiki_content")
        self.blobs = list(self.bucket.list_blobs())

        #creating key for hashing
        key = Fernet.generate_key()
        self.generatedKey = Fernet(key)

    #for creating the session id
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    #Session(app)


    """gets the content of a specific wiki page"""
    def get_wiki_page(self, name):
        #Pages that will not be on the 'Pages' folder from the GCS Bucket
        outside = {'home','about'}
        #Name of the text file to be access
        self.blob_name = name + ".txt"

        if name not in outside:
            self.blob = self.pages_bucket.blob("Pages/"  + self.blob_name)
        else:
            self.blob = self.pages_bucket.blob(self.blob_name)

        with self.blob.open("r") as f:
            self.content = f.read()

        return self.content

    """Gets all the page names into a list to be later displayed through pages.py"""
    def get_all_page_names(self):
        #Returns a list with the names of all pages
        blobs = self.storage_client.list_blobs(self.pages_bucket_name)
        files = []
        # Note: The call returns a response only when the iterator is consumed.
        for blob in blobs:
            if blob.name.startswith("P"):
                files.append(blob.name[6:-4])

        return files[1:]

    """Check if file is allowed and uploads it to upload folder """
    def upload(self,file):
        ALLOWED_EXTENSIONS = {'txt','png', 'jpg'}
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        #checking for file already uploded 
        self.blobs = list(self.bucket.list_blobs())

        if file.filename in self.blobs:
            flash('file alredy in folder')
            return redirect(request.url)
        self.bucket = self.storage_client.bucket("project1_wiki_content")


        if file.filename in self.blobs:
            flash('file alredy in folder')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            upload_blob = self.pages_bucket.blob("Pages/" + file.filename)
            upload_blob.upload_from_file(file)
        return 

  

    def sign_up(self, username, password):
   #remeber to get the username and password from pages self note

        #casting the password into a string because it's not for some reason when sent through the function
        password = str(password)

        #hashed password, and turning it into bytes
        hashedPassword = self.generatedKey.encrypt(bytes(password, 'utf-8'))
        
        #getting the bucket of the user's files 
        bucket_users = self.user_files

        #making a name that we will define the file with this name 
        fileofUser = f"{username}.txt"

            
        #users data stores into the blob that will be stored into the bucket
        blob_users = bucket_users.blob(fileofUser)

        #opening user file to write in password
        with blob_users.open("w") as file:

            #accessing bucket with user's passwords in it
            csv.writer(file).writerow(hashedPassword)
        
        
        return redirect('/about')

        

#putting in fernet to pass in the key that we encrypted the password with
    def sign_in(self, username, password,):
        
                
        bucket = self.user_files
        blob = list(self.bucket.list_blobs())

        for user in blob:
            #removing the .txt from part from the string and storing it in a variable for comparison
            fileWithoutTxt = user[:-4]

            #identifying if the username exist
            if username == fileWithoutTxt:
            #opens the user's file
                with user.open('r') as file:
                #checks for the password

                    for row in file:
                        #checking if the password entered is the same as the one entered 
                        #turning
                        if self.generatedKey.decrypt(row.decode('utf-8')) == password:

                        
                            #session is created for the user 
                            session[username] = request.form.get("username")

                            #sends the user to content page after login credentials are valid
                            return redirect('/content')
        
        #nothing was found so it renders the login page 
        return redirect('/login')


    #gets images from the bucket folder
    def get_image(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Authors/" + imagename
        return img
        
    