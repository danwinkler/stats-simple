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
		series: series,
	} );
	
	var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );

	var y_axis = new Rickshaw.Graph.Axis.Y( {
		graph: graph,
		orientation: 'left',
		tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
		element: document.getElementById('y-axis'),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['cpu_percent'] = render_cpu_percent;

function render_virtual_memory( data ) 
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
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['virtual_memory'] = render_virtual_memory;

function render_swap_memory( data ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','used','free','percent','sin','sout'];
	var palette = new Rickshaw.Color.Palette();
	var series = [];
	
	var rickData = [];
	for( var i = 0; i < data.length; i++ )
	{
		var x = data[i]['time'];
		var y = data[i]['value']['percent'];
		rickData.push( { x: x, y: y } );
	}
	series.push( { name: "Percent of Memory Used", data: rickData, color: palette.color() } );
	
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
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['swap_memory'] = render_swap_memory;

function render_web_response_time( data ) 
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
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['web_response_time'] = render_web_response_time;

function render_all_disks( data ) 
{
	if( data.length < 1 ) return;
	
	var types = ['total','used','free','percent'];
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
		element: document.querySelector("#chart"),
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
		element: document.getElementById('y-axis'),
	} );
	
	new Rickshaw.Graph.HoverDetail( {
		graph: graph
	} );
	
	graph.render();
}
renderFunctions['all_disks'] = render_all_disks;