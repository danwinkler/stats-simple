from ss_plugin import *
import psutil

def cpu_percent_collector():
	return psutil.cpu_percent( interval=1, percpu=True )

collectors['cpu_percent'] = cpu_percent_collector
	