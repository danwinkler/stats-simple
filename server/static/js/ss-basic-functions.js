function add_zero_data_in_gaps( data, blank, time )
{
	var timeDict = { "hour": 60*60, "day": 60*60*24, "month": 60*60*24*30, "year": 60*60*24*365 };
	
	var now = Math.round(new Date().getTime() / 1000);
	var timeSpan = time.split( ":" );
	
	//Don't add data at ends if it's forever
	if( timeSpan[0] != "forever" )
	{
		timeSpan = timeDict[timeSpan[0]] * parseInt(timeSpan[1]);
		var begin = now-timeSpan;
		
		if( data[0]['time'] - begin > 20*60 )
		{
			data.splice( 0, 0, {'time':begin, 'value': blank} );
		}
		
		if( now - data[data.length-1]['time'] > 20*60 )
		{
			data.push( {'time':now, 'value': blank} );
		}
	}
	
	//Add blanks in gaps
	for( var i = 0; i < data.length-1; i++ )
	{
		var d1 = data[i];
		var d2 = data[i+1];
		var timeDiff = d2['time'] - d1['time'];
		if( timeDiff > 20*60 )
		{
			data.splice( i+1, 0, { 'time': d2['time']-60, 'value': blank } );
			data.splice( i+1, 0, { 'time': d1['time']+60, 'value': blank } );
			i += 2;
		}
	}
	
	return data;
}

function xAxis( graph )
{
	return new Rickshaw.Graph.Axis.Time( { 
		graph: graph,
		timeFixture: new Rickshaw.Fixtures.Time.Local()
	} );
}

function yAxis( graph, element )
{
	return new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		orientation: 'left',
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
		element: $(".y-axis", element).get(0),
	} );
}

function hoverDetail( graph )
{
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
}

function addNotes( graph, element, notes )
{
	var annotator = new Rickshaw.Graph.Annotate({
		graph: graph,
		element: $(".chart-timeline", element).get(0)
	});

	for( var i = 0; i < notes.length; i++ )
	{
		var note = notes[i];
		annotator.add( note['time'], note['note'] );
	}
	return annotator;
}

function getGraphWidth( element )
{
	if( graphWidth == "device" )
	{
		return $(element).width() - $(".y-axis", element).width();
	}
	return graphWidth;
}

function render_cpu_percent( data, notes, element, time ) 
{
	if( data.length < 1 ) return;

	var procCount = data[0]['value'].length;

	if( data.length > 1000 )
	{
		var new_data = [];
		for( var i = 0; i < data.length-10; i += 10 )
		{
			var d = data[i]['value'];
			for( var j = 1; j < 10; j++ )
			{
				for( var k = 0; k < procCount; k++ )
				{
					d[k] += data[i+j]['value'][k];
				}
			}
			for( var k = 0; k < procCount; k++ )
			{
				d[k] = d[k] / 10.0;
			}
			new_data.push( { 'time': data[i+5]['time'], 'value': d } );
		}
		data = new_data;
	}

	blank = [];
	for( var i = 0; i < procCount; i++ ) { blank.push( 0 ); }
	data = add_zero_data_in_gaps( data, blank, time );
	
	var palette = new Rickshaw.Color.Palette();
	var series = [];
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
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'stack',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );

	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['cpu_percent'] = render_cpu_percent;

function render_virtual_memory( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','available','percent','used','free'];
	
	blank = {};
	for( var i = 0; i < types.length; i++ ) { blank[types[i]] = 0; }
	data = add_zero_data_in_gaps( data, blank, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];
	
	//TODO: let user choose what type of memory to view
	
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value']['available'] / (1024*1024);
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Avaiable Memory", data: rickData, color: palette.color() } );
	
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'line',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['virtual_memory'] = render_virtual_memory;

function render_swap_memory( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','used','free','percent','sin','sout'];
	
	blank = {};
	for( var i = 0; i < types.length; i++ ) { blank[types[i]] = 0; }
	data = add_zero_data_in_gaps( data, blank, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];

	//TODO: let user choose what kind of memory to view
	
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value']['available'] / (1024*1024);
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Available Memory", data: rickData, color: palette.color() } );
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'stack',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['swap_memory'] = render_swap_memory;

function render_web_response_time( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	data = add_zero_data_in_gaps( data, 0, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value'];
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Response Time", data: rickData, color: palette.color() } );
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'stack',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['web_response_time'] = render_web_response_time;

function render_all_disks( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','used','free','percent'];
	
	if( data.length > 1000 )
	{
		var new_data = [];
		for( var i = 0; i < data.length-10; i += 10 )
		{
			var d = data[i]['value'];
			for( var j = 1; j < 10; j++ )
			{
				for( var k = 0; k < d.length; k++ )
				{
					var disk = d[k];
					for( var l = 0; l < types.length; l++ )
					{
						var t = types[l];
						d[disk][t] += data[i+j]['value'][disk][t];
					}
				}
			}
			for( var k = 0; k < d.length; k++ )
			{
				var disk = d[k];
				for( var l = 0; l < types.length; l++ )
				{
					var t = types[l];
					d[disk][t] = d[disk][t] / 10.0;
				}
			}
			new_data.push( { 'time': data[i+5]['time'], 'value': d } );
		}
		data = new_data;
	}

	blank = {};
	for( var i = 0; i < data[0].length; i++ ) 
	{ 
		var disk = data[0][i];
		for( var j = 0; j < types.length; j++ ) 
		{ 
			blank[disk][types[j]] = 0; 
		} 
	}
	data = add_zero_data_in_gaps( data, blank, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];
	for( var i = 0; i < data.length; i++ )
	{
		for( var disk in data[i]['value'] )
		{
			var x = data[i]['time'];
			var y = data[i]['value'][disk]['percent'];
			var foundS = false;
			for( var j = 0; j < series.length; j++ )
			{
				if( series[j].name == disk )
				{
					series[j].data.push( { x: x, y: y } );
					founds = true;
					break;
				}
			}
			if( !foundS ) 
			{
				series.push( { name: disk, data: [{ x: x, y: y }], color: palette.color() } );
			}
		}
	}
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'line',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['all_disks'] = render_all_disks;

function render_float( data, notes, element, time ) 
{
	if( data.length < 1 ) return;
	
	data = add_zero_data_in_gaps( data, 0, time );

	var palette = new Rickshaw.Color.Palette();
	var series = [];
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value'];
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Value", data: rickData, color:  'steelblue' } );
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
		width: getGraphWidth( element ),
		height: graphHeight,
		renderer: 'stack',
		series: series,
		interpolation: "step"
	} );
	
	var x_axis = xAxis( graph );

	var y_axis = yAxis( graph, element );
	
	hoverDetail( graph );

	var annotator = addNotes( graph, element, notes );
	
	graph.render();
}
renderFunctions['web_correct_response'] = render_float;