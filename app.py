import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog


    @app.route('/', methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime( "%d-%m-%Y")
        # Insert the document into the MongoDB collection
            app.db.entries.insert_one({
                "content": entry_content,
                "date": formatted_date
            })

        # Retrieve all entries from the MongoDB collection
    
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%d-%m-%Y").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        # Render the template with the entries

        return render_template("home.html", entries=entries_with_date)
        
    return app

