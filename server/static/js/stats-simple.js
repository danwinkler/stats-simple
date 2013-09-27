var node;
var dataType;

var width = 800;
var height = 600;

var g;

var renderFunctions = {};

$(function() {
	$.ajax({ url: "/nodes",
		dataType: "json",
		success: nodesData
	});
	
	$("canvas").attr( "width", width );
	$("canvas").attr( "height", height );
	
});

function nodesData(data, textStatus, jqXHR) 
{
	$("#node-list").empty();
	for( var i = 0; i < data.length; i++ )
	{
		var c = "node-item-" + data[i]['id'];
		var html = "";
		html += '<div class="node-item ' + c + '">';
		html += '<span class="node-id">' + data[i]['id'] + '</span>';
		html += '<span class="node-name">' + data[i]['name'] + '</span>';
		html += '<a href="javascript:;" class="node-link">View</a>';
		html += '</div>';
		$("#node-list").append( html );
		var url = "/nodeinfo/"+data[i]['id'];
		var cnode = data[i]['id'];
		$("." + c + " .node-link").click(function() {
			node = cnode;
			$.ajax({ url: url,
				dataType: "json",
				success: nodeInfo
			});
		});
	}
}

function nodeInfo(data, textStatus, jqXHR) 
{
	$("#info-list").empty();
	for( var i = 0; i < data.length; i++ )
	{
		var c = "info-item-" + data[i];
		var html = "";
		html += '<div class="info-item ' + c + '">';
		html += '<span class="info-key">' + data[i] + '</span>';
		html += '<a href="javascript:;" class="info-link">View</a>';
		html += '</div>';
		$("#info-list").append( html );
		var url = "/data/"+node+"/"+data[i];
		var cdataType = data[i];
		$("." + c + " .info-link").click(function() {
			dataType = cdataType;
			$.ajax({ url: url,
				dataType: "json",
				success: graph
			});
		});
	}
}

function graph( data, textStatus, jqXHR )
{
	var canvas = document.getElementById("main-canvas");
	g = canvas.getContext("2d");
	
	renderFunctions[dataType]( data );
}