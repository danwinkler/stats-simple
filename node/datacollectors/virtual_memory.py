from ss_collect import *
import psutil

def virtual_memory_collector():
	return psutil.virtual_memory()

collectors['virtual_memory'] = virtual_memory_collector