from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"


main = PyMongo(app)

#  create route that renders index.html template
@app.route("/")
def index():
    mars = main.db.mars.find_one()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
    mars = main.db.mars
    mars_results = scrape_mars.scrape()
    mars.update(
        {},
        mars_results,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)