from ss_plugin import *
import psutil

def swap_memory_collector():
	m = psutil.swap_memory()
	dict = {}
	dict["total"] = m.total
	dict["used"] = m.used
	dict["free"] = m.free
	dict["percent"] = m.percent
	dict["sin"] = m.sin
	dict["sout"] = m.sout
	return dict
	
collectors['swap_memory'] = swap_memory_collector