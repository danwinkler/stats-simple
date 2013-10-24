from ss_triggers import *
from trigger_helper import *

def cpu_load_too_high():
	nodes = get_nodes()
	for node in nodes:
		node_data = latest_node_data( node["id"], "CPU_Load", 600 )

		if len( node_data ) == 0:
			return
			
		data = []
		for nd in node_data:
			data.append( sum( nd['value'] ) / float(len( nd['value'] )) )
		avg = sum( data ) / float(len( data )) if len(data) > 0 else 0

		if avg > 70:
			make_alert( node["name"] + "-CPU_Load", node["name"] + " average CPU Load over last 5 minutes was " + str(avg), 2 )

triggers['cpu_load_too_high'] = cpu_load_too_high