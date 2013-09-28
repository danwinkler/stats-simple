var node;
var dataType;

var width = 800;
var height = 200;

var g;

var renderFunctions = {};

$(function() {
	$.ajax({ url: "/nodes",
		dataType: "json",
		success: nodesData
	});
	
	$("#time-frame").change(function() {
		$.ajax({ url: "/data/"+node+"/"+dataType+"/"+$("#time-frame").val(),
			dataType: "json",
			success: graph
		});
	});
});

function nodesData(data, textStatus, jqXHR) 
{
	$("#node-list-content").empty();
	for( var i = 0; i < data.length; i++ )
	{
		var c = "node-item-" + data[i]['id'];
		var html = "";
		html += '<div class="node-item ' + c + '">';
		html += '<span class="node-id">' + data[i]['id'] + '</span>';
		html += '<span class="node-name">' + data[i]['name'] + '</span>';
		html += '<a href="javascript:;" class="node-link">View</a>';
		html += '</div>';
		$("#node-list-content").append( html );
		$("." + c + " .node-link").on( "click", { node: data[i]['id'], url: "/nodeinfo/"+data[i]['id'] }, function( event ) {
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
	for( var i = 0; i < data.length; i++ )
	{
		var c = "info-item-" + data[i]['name'];
		var html = "";
		html += '<div class="info-item ' + c + '">';
		html += '<span class="info-key">' + data[i]['name'].replace("_", " ") + '</span>';
		html += '<a href="javascript:;" class="info-link">View</a>';
		html += '</div>';
		$("#info-list-content").append( html );
		var url = "/data/"+node+"/"+data[i]['name']+"/"+$("#time-frame").val();
		$("." + c + " .info-link").on( "click", { dataType: data[i]['type'], url: url }, function( event ) {
			dataType = event.data.dataType;
			var url = event.data.url;
			$.ajax({ url: url,
				dataType: "json",
				success: graph
			});
		});
	}
	$("#info-list-content .info-item").last().addClass( "info-item-last" );
	$("#info-list").slideDown();
}

function graph( data, textStatus, jqXHR )
{
	$("#chart").empty();
	$("#y-axis").empty();
	renderFunctions[dataType]( data );
	
	$("#main-canvas-wrapper").slideDown();
}