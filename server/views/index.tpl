<html>
	<head>
		<title>stats-simple</title>
		<link href='//fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" type="text/css" href="{{cfg["webpath"]}}/static/css/rickshaw.css">
		<link rel="stylesheet" type="text/css" href="{{cfg["webpath"]}}/static/css/jquery.dynatable.css">
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
		</script>

		<script src="//code.jquery.com/jquery-1.10.2.min.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/dotimeout.min.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/d3.v3.min.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/rickshaw.js"></script>
		<script src="{{cfg["webpath"]}}/static/js/jquery.dynatable.js"></script>
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
		<div id="alerts">
			
		</div>
		<div id="group-list">

		</div>
		<div id="node-list">
			<table id="node-list-table">
				<thead class="node-item-header">
					<th class="node-id">id</th>
					<th class="node-group">group</th>
					<th class="node-name">name</th>
				</thead>
				<tbody>

				</tbody>
			</table>
		</div>
		<div id="info-list">
			<div id="info-list-content"></div>
		</div>
		<div id="chart-display">
		</div>
	</body>
</html>