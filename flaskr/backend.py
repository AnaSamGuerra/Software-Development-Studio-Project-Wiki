from google.cloud import storage
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
#hasing library
import bcrypt
from csv import writer
from collections import defaultdict

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
        # adding username bucket
        self.usernames_bucket = self.storage_client.bucket(self.users_bucket_name)
        #sing in should be false when loading the page for the first time
        self.logedin = False
        self.username = ""

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

    """Writes into User file what file was uploded by them"""
    def track_imguser_Uploads(self,username,imagefile):       
        blob = self.usernames_bucket.blob(username +".txt")
        with blob.open('r') as f:
            content = f.read()
        content = content +'\n'+imagefile
        with blob.open('w') as f:
            f.write(content)
        return

    """Check if file is allowed and uploads it to upload folder """
    def upload(self,file):
        ALLOWED_EXTENSIONS = {'txt','png', 'jpg'}
        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        #checking for file already uploded 
        self.blobs = list(self.pages_bucket.list_blobs())
        if file.filename in self.blobs:
            return redirect(request.url)
        self.bucket = self.storage_client.bucket("project1_wiki_content")
        if file and allowed_file(file.filename):
            if file.filename[-3:] == 'txt':
                upload_blob = self.pages_bucket.blob("Pages/" + file.filename)
                upload_blob.upload_from_file(file)
            else:
                #all uploded pictures are under the uploded folder to be displayed
                self.track_imguser_Uploads(self.getUserName(),file.filename)
                upload_blob = self.pages_bucket.blob("Uploaded/" + file.filename)
                upload_blob.upload_from_file(file)
        return 

    # for reference in deletigin blobshttps://stackoverflow.com/questions/10555080/delete-files-from-google-cloud-storage
    """Deleats all of an specific user uploded images"""
    def delete_user_img(self):
        blob = self.usernames_bucket.blob(self.getUserName() +".txt")
        with blob.open('r') as f:
            content = f.readlines()
        for line in range(1,len(content)):
            blob = self.pages_bucket.blob("Uploaded/" + content[line].strip())
            blob.delete()
        blob = self.usernames_bucket.blob(self.getUserName() +".txt")
        with blob.open('w') as f:
            f.write(content[0])
        return

    '''no used at the moment'''
    def sign_up(self, username, password):
        pass

    '''Sing in with a pre exiting user found in the bucket'''
    def sign_in(self,givenusername):
        self.blobs = list(self.usernames_bucket.list_blobs())
        for blob in self.blobs:
            if givenusername + ".txt" == blob.name:
                self.logedin = True
                self.username = givenusername
        return 

    '''checks if user is singed in'''
    def isusersignedin(self):
        return self.logedin

    '''gets the name of the current user'''
    def getUserName(self):
        return str(self.username)
        
    """gets images from the bucket folder""" 
    def get_image(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Authors/" + imagename
        return img

    """gets images for character's pages""" 
    def get_imageChar(self,imagename):
        img = "https://storage.cloud.google.com/project1_wiki_content/Uploaded/" + imagename
        return img


    """Gets search results, takes a query and returns matching"""
    def get_search_results(self, query):
        blobs = self.storage_client.list_blobs(self.pages_bucket_name)
        possible_results = defaultdict(int)
        files = []
        query = query.lower()
        PREFFIX_REMOVE = 6
        SUFFIX_REMOVE = -4
        for blob in blobs:
            if blob.name.startswith("P"):
                file_name = blob.name[6:-4].lower()
                for i in range(len(file_name)):
                    if i < len(query) and query[i] == file_name[i]:
                        possible_results[file_name] += 1
                if possible_results[file_name] > (len(query) // 2):
                    files.append(blob.name[PREFFIX_REMOVE:SUFFIX_REMOVE])

        return files
    """Gets uploaded files"""  
    def get_uploaded(self):
        PREFFIX_REMOVE = 9
        blobs = self.storage_client.list_blobs(self.pages_bucket_name)
        files = []
        # Note: The call returns a response only when the iterator is consumed.
        for blob in blobs:
            if blob.name.startswith("U"):
                files.append("https://storage.cloud.google.com/project1_wiki_content/Uploaded/" + blob.name[PREFFIX_REMOVE:])
        return files[1:]

