import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb+srv://keemeayo:oluwaliza@microblog-application.cmyj1li.mongodb.net/")
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
