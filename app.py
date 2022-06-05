from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app" 
mongo = PyMongo(app)

@app.route("/") # root route
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection created when converting Jupyter scraping code to Python Script; assign that path to themars variable for use later.
   return render_template("index.html", mars=mars) # return an HTML template using an index.html file; assign that path to themars variable

@app.route("/scrape") # route for scraped pages
def scrape():
   mars = mongo.db.mars # new variable that points to Mongo database
   mars_data = scraping.scrape_all() # new variable to hold scraped data referencing the scrape_all function in the scraping.py file
   mars.update_one({}, {"$set":mars_data}, upsert=True) # insert data unless an identical record already exists (upsert=True)
   return redirect('/', code=302) #navigate page back to / (root)

if __name__ == "__main__": # if we're in the main class
   app.run() # run the app