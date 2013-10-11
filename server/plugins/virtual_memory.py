try:
	from ss_plugin import *
	import psutil

	def virtual_memory_collector():
		m = psutil.virtual_memory()
		dict = {}
		dict["total"] = m.total
		dict["available"] = m.available
		dict["percent"] = m.percent
		dict["used"] = m.used
		dict["free"] = m.free
		return dict

	collectors['virtual_memory'] = virtual_memory_collector
except Exception, e:
	print "Could not load virtual_memory.py: " + str(e)