try:
	from ss_plugin import *
	import psutil
	import os

	def all_disks_collector():
		dict = {}
		for part in psutil.disk_partitions():
			if os.name == 'nt':
				if 'cdrom' in part.opts or part.fstype == '':
					# skip cd-rom drives with no disk in it; they may raise
					# ENOENT, pop-up a Windows GUI error for a non-ready
					# partition or just hang.
					continue
			usage = psutil.disk_usage(part.mountpoint)
			dict[part.device] = { "total": usage.total, "used": usage.used, "free": usage.free, "percent": usage.percent }
		return dict

	collectors['all_disks'] = all_disks_collector
except Exception, e:
	print "Could not load all_disks.py: " + str(e)