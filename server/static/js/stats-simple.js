var node;
var timeFrame = "hour:1";

var renderFunctions = {};

$(function() {

	if( graphWidth != "device" ) 
	{
		graphWidth = parseInt( graphWidth );
	}

	$.ajax({ 
		url: "/alerts/hour:12",
		dataType: "json",
		success: function( alerts, textStatus, jqXHR) {
			if( alerts.length > 0 )
			{
				$("#alerts").show();
				$("#alerts").append( '<span class="alert-title">Alerts - Last 12 Hours</span>' );
				$("#alerts").append( '<div class="alert alert-header">' +
						'<span class="alert-time">Time</span>' +
						'<span class="alert-level">Level</span>' +
						'<span class="alert-name">Name</span>' +
						'<span class="alert-value">Value</span>' +
					'</div>' );
				for( var i = 0; i < alerts.length; i++ )
				{
					var alert = alerts[i];
					html = "";
					html += '<div class="alert">';

					var date = new Date( alert['time'] * 1000 );

					html += '	<span class="alert-time">' + date.getHours() + ":" + date.getMinutes() + '</span>';
					html += '	<span class="alert-level">' + alert['level'] + '</span>';
					html += '	<span class="alert-name">' + alert['name'] + '</span>';
					html += '	<span class="alert-value">' + alert['value'] + '</span>';
					html += '</div>';
					$("#alerts").append( html );
				}
				$("#alerts .alert").last().addClass( "alert-last" );
			}
		}
	});

	if( nodeSelect ) 
	{
		$("#chart-display").hide();
		$("#node-list").show();
		$("#group-list").show();
		$.ajax({ url: "/groups",
			dataType: "json",
			success: groupData
		});
		$.ajax({ url: "/nodes",
			dataType: "json",
			success: nodesData
		});
	}
	else
	{
		html = "";
		html += ' 	<select class="global-time-frame">';
		html += ' 		<option value="hour:1">Last Hour</option>';
		html += ' 		<option value="hour:2">Last 2 Hours</option>';
		html += ' 		<option value="hour:3">Last 3 Hours</option>';
		html += ' 		<option value="hour:6">Last 6 Hours</option>';
		html += ' 		<option value="day:1">Last Day</option>';
		html += ' 		<option value="day:3">Last 3 Days</option>';
		html += ' 		<option value="day:7">Last Week</option>';
		html += ' 		<option value="month:1">Last Month</option>';
		html += ' 		<option value="month:6">Last 6 Months</option>';
		html += ' 		<option value="month:12">Last Year</option>';
		html += ' 		<option value="forever:0">Forever</option>';
		html += ' 	</select>';
		html += '<table>';
		for( var i = 0; i < screenInfo.length; i++ )
		{
			var row = screenInfo[i];
			html += '<tr>';
			for( var j = 0; j < row.length; j++ )
			{
				var column = row[j];
				html += '<td><div class="chart-wrapper ' + chartSelector( column[0], column[1] ) + '"></div></td>';
			}
			html += '</tr>';
		}
		html += '</table>';
		$("#chart-display").html( html );

		$(".global-time-frame").change(function() {
			$(".time-frame").val( $(this).val() );
			$(".time-frame").trigger( "change" );
		});
		
		for( var i = 0; i < screenInfo.length; i++ )
		{
			var row = screenInfo[i];
			for( var j = 0; j < row.length; j++ )
			{
				var column = row[j];
				graph( "." + chartSelector( column[0], column[1] ), column[0], column[1] );
			}
		}
	}
});

function chartSelector( node, name )
{
	return 'chart-' + node.replace( /\./g, "-" ) + "-" + name.replace( /\./g, "-" );
}

function groupData(data, textStatus, jqXHR)
{
	$("#group-list").empty();
	for( var i = 0; i < data.length; i++ )
	{
		var c = "group-item-" + data[i];
		var html = "";
		html += '<span class="group-item ' + c + '">';
		html += '<a href="javascript:;" class="group-link">' + data[i] + '</a>';
		html += '</span>';
		$("#group-list").append( html );
		$("." + c + " .group-link").on( "click", { group: data[i] }, function( event ) {
			var url = "/nodes/" + event.data.group;
			$.ajax({ url: url,
				dataType: "json",
				success: nodesData
			});
		});
	}
}

function nodesData(data, textStatus, jqXHR) 
{
	$("#node-list-content").empty();
	for( var i = 0; i < data.length; i++ )
	{
		var c = "node-item-" + data[i]['id'];
		var html = "";
		html += '<div class="node-item ' + c + '">';
		html += '<span class="node-id">' + data[i]['id'] + '</span>';
		html += '<span class="node-group">' + data[i]['group'] + '</span>';
		html += '<span class="node-name">' + data[i]['name'] + '</span>';
		html += '<a href="javascript:;" class="node-link">View</a>';
		html += '</div>';
		$("#node-list-content").append( html );
		$("." + c + " .node-link").on( "click", { node: data[i]['name'], url: "/nodeinfo/"+data[i]['id'] }, function( event ) {
			node = event.data.node;
			var url = event.data.url;
			$.ajax({ url: url,
				dataType: "json",
				success: nodeInfo
			});
		});
	}
	$("#node-list-content .node-item").last().addClass( "node-item-last" );
}

function nodeInfo(data, textStatus, jqXHR) 
{
	$("#info-list-content").empty();
	$("#info-list-content").append( '<div class="info-title">' + node + '</div>' );
	for( var i = 0; i < data.length; i++ )
	{
		var c = "info-item-" + data[i]['name'].replace( /\./g, "-" );
		var html = "";
		html += '<div class="info-item ' + c + '">';
		html += '<span class="info-key">' + data[i]['name'].replace(/_/g, " ") + '</span>';
		html += '<a href="javascript:;" class="info-link">View</a>';
		html += '</div>';
		$("#info-list-content").append( html );
		var url = "/data/"+node+"/"+data[i]['name']+"/"+$("#time-frame").val();
		//Add click listener
		$("." + c + " .info-link").on( "click", { dataType: data[i]['type'], dataName: data[i]['name'], url: url }, function( event ) {
			dataType = event.data.dataType;
			dataName = event.data.dataName;
			var url = event.data.url;
			graph( "#chart-display", node, dataName );
			$("#chart-display").slideDown();
		});
	}
	$("#info-list-content .info-item").last().addClass( "info-item-last" );
	$("#info-list").slideDown();
}

var getNodeId = function( nodeName, callback )
{
	$.ajax({ 
		url: "/nodeid/" + nodeName,
		dataType: "json",
		success: function(node, textStatus, jqXHR) {
			callback( node );
		}
	});
};

var getDataType = function( dataName, callback )
{
	$.ajax({ 
		url: "/typeof/" + dataName,
		dataType: "json",
		success: function( dataType, textStatus, jqXHR) {
			callback( dataType );
		}
	});
};

var getData = function( nodeId, dataName, time, callback )
{
	$.ajax({ 
		url: "/data/" + nodeId + "/" + dataName + "/" + time,
		dataType: "json",
		success: function( data, textStatus, jqXHR) {
			callback( data );
		}
	});
};

var getNotes = function( nodeId, time, callback )
{
	$.ajax({ 
		url: "/notes/" + nodeId + "/" + time,
		dataType: "json",
		success: function( notes, textStatus, jqXHR) {
			callback( notes );
		}
	});
};

function graph( selector, nodeName, name, time )
{
	if( typeof time === 'undefined' ) time = timeFrame;
	
	getNodeId( nodeName, function( nodeId ) { 
		getDataType( name, function( dataType ) {
			getData( nodeId, name, time, function( data ) {
				getNotes( nodeId, time, function( notes ) {
					var html = "";
					html += ' <div class="chart-header">';
					html += ' 	<div class="chart-title">' + nodeName + ": " + name.replace( /_/g, " " ) + '</div>';
					html += ' 	<select class="time-frame">';
					html += ' 		<option value="hour:1">Last Hour</option>';
					html += ' 		<option value="hour:2">Last 2 Hours</option>';
					html += ' 		<option value="hour:3">Last 3 Hours</option>';
					html += ' 		<option value="hour:6">Last 6 Hours</option>';
					html += ' 		<option value="day:1">Last Day</option>';
					html += ' 		<option value="day:3">Last 3 Days</option>';
					html += ' 		<option value="day:7">Last Week</option>';
					html += ' 		<option value="month:1">Last Month</option>';
					html += ' 		<option value="month:6">Last 6 Months</option>';
					html += ' 		<option value="month:12">Last Year</option>';
					html += ' 		<option value="forever:0">Forever</option>';
					html += ' 	</select>';
					html += ' </div>';
					html += ' <div class="y-axis"></div>';
					html += ' <div class="chart"></div>';
					html += ' <div class="chart-clear"></div>';
					html += ' <div class="chart-timeline"></div>';
					$(selector).html( html );
					if( graphWidth == "device" )
					{
						$(selector).css( "display", "block" ); 
					}
					$(".time-frame option[value='" + time + "']", selector).attr( "selected", "selected" );
					renderFunctions[dataType]( data, notes, selector, time );
					$(".time-frame", selector).change(function() {
						$(".chart-header", selector).append( '<img class="ajax-loader" src="/static/img/ajax-loader.gif"></img>' );
						graph( selector, nodeName, name, $(this).val() );
						timeFrame = $(this).val();
					});
					$.doTimeout( "refresh-" + selector, 60000, function() {
						graph( selector, nodeName, name, $(".time-frame", selector).val() );
					});
				});
			});
		});
	});
}