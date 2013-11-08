// auto color palette
var palette = new Rickshaw.Color.Palette();

// set up data series for each supply type - call upon database here

// list of data lists
var seriesData = [
	[],		// water
	[],		// flashlight & batteries
	[],		// phone charger
	[],		// first aid kit
	[]		// food
];

// generates random data for seriesData
var random = new Rickshaw.Fixtures.RandomData(15);

for (var i=0; i<15; i++) {
	random.addData(seriesData);
}

// instantiate the graph
var graph = new Rickshaw.Graph({
	element: document.getElementById("chart"),
	width: 960,
	height: 300,
	renderer: "line",
	series: [
		{
			name: "Flashlight & Batteries",
			color: palette.color(),
			data: seriesData[0]
		},
		{
			name: "Cell Phone Charger",
			color: palette.color(),
			data: seriesData[1]
		},
		{
			name: "First Aid Kit",
			color: palette.color(),
			data: seriesData[2]
		},
		{
			name: "Food",
			color: palette.color(),
			data: seriesData[3]
		},
		{
			name: "Water",
			color: palette.color(),
			data: seriesData[4]
		}
	]
});

graph.render();

// show data point info
var hoverDetail = new Rickshaw.Graph.HoverDetail({
	graph: graph
});

// graph legend
var legend = new Rickshaw.Graph.Legend({
	graph: graph,
	element: document.getElementById("legend")
});

// allows toggling between keys of legend
var shelving = new Rickshaw.Graph.Behavior.Series.Toggle({
	graph: graph,
	legend: legend
});

// graph axes
var axes = new Rickshaw.Graph.Axis.Time({
	graph: graph
});

axes.render();