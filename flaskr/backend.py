from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
#hasing library
import bcrypt
from csv import writer

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
        self.blobs = list(self.pages_bucket.list_blobs())
        if file.filename in self.blobs:
            flash('file alredy in folder')
            return redirect(request.url)
        self.bucket = self.storage_client.bucket("project1_wiki_content")
        if file and allowed_file(file.filename):
            if file.filename[-3:] == 'txt':
                upload_blob = self.pages_bucket.blob("Pages/" + file.filename)
                upload_blob.upload_from_file(file)
            else:
                upload_blob = self.pages_bucket.blob("Uploaded/" + file.filename)
                upload_blob.upload_from_file(file)
        return 

    def sign_up(self, username, password):
        
        #getting the prefix to hash and salt
        preFix = bcrypt.gensalt()

        #hashed password
        hashedPassword = bcrypt.hashpw(password, preFix)

        #hashed username
        hashedUsername = bcrypt.hashpw(username, preFix)

        client = storage.Client()
        
        bucket = client.bucket("users_bucket_name")

        #initializing file name
        fileofUser = f"(hashedUsername).txt"

        #creating user's file
        blob = bucket.blob(fileofUser)
        
        #writing password into user's file to store it 
        if hashedUsername not in self.users_bucket_name:
            #opening user file to write in password
            with open(blob,'a') as userFile:
                writer_object = writer(userFile)
                #writing hashed password into the user's row
                writer_object.writerow(hashedPassword)
 
                # Close the file object
                userFile.close()
                
            return True

        else:
            return False


    def sign_in(self, username, password):

        client = storage.Client()
        bucket = client.bucket("users_bucket_name")
        blob = bucket.blob(username)

        

        try:
            with blob.open('r') as username:
                hashedData = username.read()

        except:
            return "User Doesn't exist"

        #if user Data found it exist
        if hashedData == username:
            return True

        return False
        

    """gets images from the bucket folder""" 
    def get_image(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Authors/" + imagename
        return img
    def get_uploaded(self):
        PREFFIX_REMOVE = 9
        blobs = self.storage_client.list_blobs(self.pages_bucket_name)
        files = []
        # Note: The call returns a response only when the iterator is consumed.
        for blob in blobs:
            if blob.name.startswith("U"):
                files.append("https://storage.cloud.google.com/project1_wiki_content/Uploaded/" + blob.name[PREFFIX_REMOVE:])

        return files[1:]