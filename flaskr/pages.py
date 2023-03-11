from flask import render_template
from flaskr import backend
from flask import Flask, flash, request, redirect, url_for


def make_endpoints(app):
    back = backend.Backend()
    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        # TODO(Checkpoint Requirement 2 of 3): Change this to use render_template
        # to render main.html on the home page.
        return render_template("main.html")

    # TODO(Project 1): Implement additional routes according to the project requirements.
    
    @app.route("/about")
    def about():
        content = back.get_wiki_page("about")
        img1 = back.get_image("india.jpg")
        img2 = back.get_image("samantha.jpg")
        img3 = back.get_image("orlando.jpg")
        return render_template("about.html", content=content, img1=img1, img2=img2, img3=img3)

    @app.route("/pages/")
    @app.route("/pages/<subpage>")
    def pages(subpage=None):
        if subpage == None:
            files = back.get_all_page_names()
            return render_template("pages.html", content=files)

        else:
            content = back.get_wiki_page(subpage)
            return render_template("content.html", content=content, page_name=subpage)

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        return render_template("logout.html")

    @app.route("/upload" , methods = ['GET',"POST"])
    def upload():
        if request.method == "POST":
            file = request.form.get("file")
            back.upload(file)
        return render_template("upload.html")    