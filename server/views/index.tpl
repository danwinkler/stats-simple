<html>
	<head>
		<title>stats-simple</title>
		<link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
		<link rel="stylesheet" type="text/css" href="{{root}}/static/css/rickshaw.css">
		<link rel="stylesheet" type="text/css" href="{{root}}/static/css/stats-simple.css">
		
		<script src="http://code.jquery.com/jquery-1.10.2.min.js"></script>
		<script src="{{root}}/static/js/d3.v3.min.js"></script>
		<script src="{{root}}/static/js/rickshaw.js"></script>
		<script src="{{root}}/static/js/stats-simple.js"></script>
		<script src="{{root}}/static/js/ss-basic-functions.js"></script>
		<script>
			var screenInfo = {{!data}};
			var nodeSelect = {{user_select}};
		</script>
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