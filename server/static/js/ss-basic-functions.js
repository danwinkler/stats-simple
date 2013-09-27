function render_cpu_percent( data ) 
{
	g.beginPath();
	for( var i = 0; i < data.length-1; i++ )
	{
		var a = data[i]['value'];
		var b = data[i+1]['value'];
		for( var j = 0; j < a.length; j++ )
		{
			g.moveTo( i * (width/data.length), height - (a[j] * (height/100.0)) );
			g.lineTo( (i+1) * (width/data.length), height - (b[j] * (height/100.0)) );
		}
	}
	g.stroke();
}
renderFunctions['cpu_percent'] = render_cpu_percent;
