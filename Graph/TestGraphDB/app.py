from flask import Flask, render_template

app = Flask(__name__)

# plot data points on graph
@app.route("/")
def supply_graph():
	return render_template("graph.html")

# plot coordinates on map
@app.route("/map")
def geocode():
	pass

if __name__ == "__main__":
    app.run(debug = True)