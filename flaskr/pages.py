from flask import render_template
from flaskr import backend

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
        back.get_all_page_names()
        return render_template("about.html", content=content)
    
    @app.route("/pages")
    def pages():
        return render_template("pages.html")

    @app.route("/signup")
    def signup():
        return render_template("signup.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        return render_template("logout.html")

    @app.route("/upload")
    def upload():
        return render_template("upload.html")    