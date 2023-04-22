from flask import render_template
from flaskr import backend
from flask import Flask, flash, request, redirect, url_for
#-> IMPORT CLOUD STORAGE Too

def make_endpoints(app):
    back = backend.Backend()
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    """Goes to home page"""
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
    
    """Goes to about page"""    
    @app.route("/about")
    def about():
        content = back.get_wiki_page("about")
        img1 = back.get_image("india.jpg")
        img2 = back.get_image("samantha.jpg")
        img3 = back.get_image("orlando.jpg")
        return render_template("about.html", content=content, img1=img1, img2=img2, img3=img3)

    """Goes to Pages section, if argument is provided then it will go to argument's page"""
    @app.route("/pages/")
    @app.route("/pages/<subpage>")
    def pages(subpage=None):
        if subpage == None:
            files = back.get_all_page_names()
            return render_template("pages.html", content=files)
        else:
            content = back.get_wiki_page(subpage)
            #get charcarter image
            charimg = back.get_imageChar(subpage+ ".png")
            return render_template("content.html", content=content, page_name=subpage,charimg=charimg)
    
    """Goes to sign up page"""
    @app.route("/signup", methods = ["GET"])
    def signup():
        return render_template("signup.html")

    """Goes to login page"""
    @app.route("/login", methods = ["GET"])
    def login():
        if request.method == "GET":
            back.sign_in("samUser")
        return render_template("login.html")

    @app.route("/logout", methods = ["GET"])
    def logout():
        if request.method == "GET":
            back.sign_in("NON EXITEN USER POSSIBLE HERE")
        return render_template("logout.html")

    """Goes to upload page, receives an input file and then calls the upload method with said input file"""
    @app.route("/upload" , methods = ['GET',"POST"])
    def upload():
        if request.method == "POST":
            file = request.form.get("file")
            back.upload(file)
            #If 
            if request.form.get("actionbutton"):
                back.delete_user_img()   
        return render_template("upload.html",username=back.getUserName())    