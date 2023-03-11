from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename


# TODO(Project 1): Implement Backend according to the requirements.
#Upload usage 
app = Flask(__name__)

class Backend:
    
    """ The backend process all infomation taken from and returning it to pages.py for the information to be proccessed
    or displayes later trhough a html template and in some cases adding files to the buckets or retiving to from the buckets
    """

    def __init__(self):
        #The ID of  GCS bucket with users info
        self.users_bucket_name = "users_passwords_project1"
        # The ID of GCS bucket with pages
        self.pages_bucket_name = "project1_wiki_content"
        # Instantiates a client
        self.storage_client = storage.Client()
        # Creates the new bucket
        self.pages_bucket = self.storage_client.bucket(self.pages_bucket_name)
        
        #upload buckets and blobs 
        self.bucket = self.storage_client.bucket("project1_wiki_content")
        self.blobs = list(self.bucket.list_blobs())

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
        if file.filename in self.blobs:
            flash('file alredy in folder')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            upload_blob = self.pages_bucket.blob("Pages/" + file.filename)
            upload_blob.upload_from_file(file)
        return 
    #SIGN UP
    def sign_up(self):
        pass

    #SIGN UP
    def sign_in(self):
        pass

    """gets images from the bucket folder""" 
    def get_image(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Authors/" + imagename
        return img
        
    