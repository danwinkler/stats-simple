$(function() {
	$.ajax({ url: "/nodes",
		dataType: "json",
		success: function(data, textStatus, jqXHR) {
			$("#node-list").empty();
			for( var i = 0; i < data.length; i++ )
			{
				html = "";
				html += '<div class="node-item">';
				html += '<span class="node-id">' + data[i]['id'] + '</span>';
				html += '<span class="node-name">' + data[i]['name'] + '</span>';
				html += '</div>';
				$("#node-list").append( html );
			}
		}
	});
});