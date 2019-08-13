# from flask import Flask, render_template, redirect, url_for
# import pymongo
# # from flask_pymongo import PyMongo
# import scrape_mars

# app = Flask(__name__)

# conn = 'mongodb://localhost:27017/mission_to_mars'
# client = pymongo.MongoClient(conn)

# # app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars"
# # mongo = PyMongo(app)


# @app.route("/")
# def index():
#     # mars = mongo.db.mars.find_one()
#     mars = client.db.mars.find_one()
#     return render_template("index.html", mars=mars)

# @app.route("/scrape")
# def scrape():
#     mars = client.db.mars
#     # mars = mongo.db.mars
#     mars_data = scrape_mars.scrape()
#     mars.update({}, mars_data, upsert=True)
#     return redirect(url_for('index'))

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)


app.config["MONGO_URI"] = "mongodb://localhost:27017/mission_to_mars'"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"


if __name__ == "__main__":
    app.run()