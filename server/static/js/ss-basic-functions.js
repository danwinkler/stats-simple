function render_cpu_percent( data ) 
{
	if( data.length < 1 ) return;
	
	var palette = new Rickshaw.Color.Palette();
	var series = [];
	var procCount = data[0]['value'].length;
	for( var j = 0; j < procCount; j++ )
	{
		var rickData = [];
		for( var i = 0; i < data.length; i++ )
		{
			var x = data[i]['time'];
			var y = data[i]['value'][j];
			rickData.push( { x: x, y: y } );
		}
		series.push( { name: "proc-"+j, data: rickData, color: palette.color() } );
	}
	
	var graph = new Rickshaw.Graph( {
		element: document.querySelector("#chart"),
		width: width,
		height: height,
		renderer: 'stack',
		series: series
	} );
	
	var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );

	var y_axis = new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		orientation: 'left',
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
		element: document.getElementById('y-axis'),
	} );
	
	graph.render();
}
renderFunctions['cpu_percent'] = render_cpu_percent;
