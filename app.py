import datetime
from flask import Flask, render_template,request
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient("mongodb+srv://keemeayo:oluwaliza@microblog-application.cmyj1li.mongodb.net/")
app.db = client.microblog
entries= []


@app.route('/', methods=["GET", "POST"])
def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%d-%m-%y")
            entries.append((entry_content, formatted_date))
            app.db.entries.insert({
                "content": entry_content,
                "date": formatted_date
            })
        entries_with_date = [
            (
                 entry[0],
                 entry[1],
                 datetime.datetime.strptime(entry[1], "%d-%m-%y").strftime("%b %d"),
            )
        for entry in entries 
        ]
        return render_template("home.html", entries=entries_with_date)   
        