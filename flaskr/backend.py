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

class Backend:

    def __init__(self):
        #The ID of  GCS bucket with users info
        self.users_bucket_name = "users_passwords_project1"
        # The ID of GCS bucket with pages
        self.pages_bucket_name = "project1_wiki_content"
        # Instantiates a client
        self.storage_client = storage.Client()
        # Creates the new bucket
        self.pages_bucket = self.storage_client.bucket(self.pages_bucket_name)
        
        #upload
        self.bucket = self.storage_client.bucket("project1_wiki_content")
        self.blobs = list(self.bucket.list_blobs())

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

    def get_all_page_names(self):
        #Returns a list with the names of all pages
        blobs = self.storage_client.list_blobs(self.pages_bucket_name)
        files = []
        # Note: The call returns a response only when the iterator is consumed.
        for blob in blobs:
            if blob.name.startswith("P"):
                files.append(blob.name[6:-4])

        return files[1:]


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
        if file.filename in self.blobs:
            flash('file alredy in folder')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            upload_blob = self.pages_bucket.blob("Pages/" + file.filename)
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
        

    def get_image(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Authors/" + imagename
        return img
        
    