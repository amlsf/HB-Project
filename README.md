## SupplyCache
SupplyCache is a web application that helps communities locate resources after a disaster occurs. It maps resources available by residents and the areas affected by a disaster. User input can be via text message or web form. An archived events page builds data visualization for post-disaster analysis. SupplyCache uses Python, Flask, SQLAlchemy, Jinja, JavaScript (Heatmap, Rickshaw), HTML/CSS, Leaflet API, Twilio API, CloudMade API.

### Map
###### Leaflet + OpenStreetMap, Twilio, CloudMade, Heatmap, MarkerClustering
[Leaflet](http://leafletjs.com/) is an open source JavaScript library for maps: the map data is from [OpenStreetMap](http://www.openstreetmap.org/), an open source map created by communities with an emphasis on local knowledge, and map tiles (style) are from [CloudMade](http://cloudmade.com/). The heatmap layer uses [heatmap.js](http://www.patrick-wied.at/static/heatmapjs/) and is integrated into my project to display areas affected by a disaster. For example, the redder the area, the more severe the situation. Therefore, the user should avoid those areas when traveling to reach another person for a supply. The marker clustering function uses the [Marker Clustering plugin](https://github.com/Leaflet/Leaflet.markercluster). When zoomed out, the markers cluster together to better visualize the number of residents with supplies. User input is taken in via text message using [Twilio](https://www.twilio.com/) or through the provided web form.

![Main page](/screenshots/sc-img1.jpg)

### Data visualization
###### Rickshaw
Archived events are accessed via a login due to the sensitivity of the information provided. Once logged in, users will see a list of past events. Each event has a "view summary" button that expands to show a graph that displays supply trends over time. In addition, the graph legend allows the user to toggle between the different supplies. The graph uses [Rickshaw](http://code.shutterstock.com/rickshaw/), which is a JavaScript graphing toolkit built on D3. In addition, below the graph is a table that contains a general summarization of the data. The "view map" button takes the user to a separate map that repopulates the archived database for further analysis. For example, a user can see the heaviest hit areas during a particular disaster and determine what can be done better next time.

![Archive page](/screenshots/sc-img3.jpg)

### Database
###### Python, SQLAlchemy
User input is stored into a database using Python and SQLAlchemy. For demo purposes, the database has been seeded. The database is queried and used to populate the maps, graphs, and tables.

### Web Framework & User Interface
###### Flask with Python, JavaScript, jQuery, HTML/CSS (and Adobe Photoshop)

![About page](/screenshots/sc-img2.jpg)
