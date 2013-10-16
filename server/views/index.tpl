<html>
	<head>
		<title>stats-simple</title>
		<link href='//fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" type="text/css" href="{{cfg["webpath"]}}/static/css/rickshaw.css">
		<link rel="stylesheet" type="text/css" href="{{cfg["webpath"]}}/static/css/stats-simple.css">

		% if "css" in cfg:
			% for i in cfg["css"]:
				<link rel="stylesheet" type="text/css" href="{{cfg["webpath"]}}/static/css/{{!i}}">
			% end
		% end
		
		<script>
			var screenInfo = {{!data}};
			var nodeSelect = {{user_select}};
			var graphWidth = "{{cfg["graph_width"]}}";
			var graphHeight = {{cfg["graph_height"]}};
			
			if( graphWidth == "device" ) 
			{
				graphWidth = (window.innerWidth > 0) ? window.innerWidth : screen.width;
				//Account for container padding
				graphWidth -= 22;
			}
			else
			{
				graphWidth = parseInt( graphWidth );
			}
		</script>

		<script src="//code.jquery.com/jquery-1.10.2.min.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/d3.v3.min.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/rickshaw.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/stats-simple.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/ss-basic-functions.js"></script>

		% if "js" in cfg:
			% for i in cfg["js"]:
				<script src="{{cfg["webpath"]}}/static/js/{{!i}}"></script>
			% end
		% end

	</head>
	<body>
		<h1>Stats-Simple</h1>
		<div id="node-list">
			<div class="node-item node-item-header">
				<div class="node-id">ID</div>
				<div class="node-name">Name</div>
			</div>
			<div id="node-list-content">Loading...</div>
		</div>
		<div id="info-list">
			<div id="info-list-content"></div>
		</div>
		<div id="chart-display">
		</div>
	</body>
</html>