from ss_collect import *
import psutil

def swap_memory_collector():
	return psutil.swap_memory()

collectors['swap_memory'] = swap_memory_collector