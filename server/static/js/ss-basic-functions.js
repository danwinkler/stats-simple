function render_cpu_percent( data, element ) 
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
		width: width,
		height: height,
		renderer: 'stack',
		series: series,
	} );
	
	var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );

	var y_axis = new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		orientation: 'left',
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
		element: $(".y-axis", element).get(0),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['cpu_percent'] = render_cpu_percent;

function render_virtual_memory( data, element ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','available','percent','used','free'];
	var palette = new Rickshaw.Color.Palette();
	var series = [];
	
	//TODO: let user choose what type of memory to view
	
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value']['percent'];
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Percent of Memory Used", data: rickData, color: palette.color() } );
	
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
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
		element: $(".y-axis", element).get(0),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['virtual_memory'] = render_virtual_memory;

function render_swap_memory( data, element ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','used','free','percent','sin','sout'];
	var palette = new Rickshaw.Color.Palette();
	var series = [];

	//TODO: let user choose what kind of memory to view
	
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value']['percent'];
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Percent of Memory Used", data: rickData, color: palette.color() } );
	
	var graph = new Rickshaw.Graph( {
		element: $(".chart", element).get(0),
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
		element: $(".y-axis", element).get(0),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['swap_memory'] = render_swap_memory;

function render_web_response_time( data, element ) 
{
	if( data.length < 1 ) return;
	
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
		element: $(".y-axis", element).get(0),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['web_response_time'] = render_web_response_time;

function render_all_disks( data, element ) 
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
				for( var disk in d )
				{
					for( var t in types )
					{
						d[disk][t] += data[i+j]['value'][disk][t];
					}
				}
			}
			for( var disk in d )
			{
				for( var t in types )
				{
					d[disk][t] = d[disk][t] / 10.0;
				}
			}
			new_data.push( { 'time': data[i+5]['time'], 'value': d } );
		}
		data = new_data;
	}

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
		width: width,
		height: height,
		renderer: 'line',
		series: series
	} );
	
	var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );

	var y_axis = new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		orientation: 'left',
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
		element: $(".y-axis", element).get(0),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['all_disks'] = render_all_disks;