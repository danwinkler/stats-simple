try:
	from ss_plugin import *
	import random

	def tester_annotator():
		notes = ["Note A", "Note B", "Note C"]
		ret = []
		for note in notes:
			if random.random() > .9:
				ret.append( note )
		return ret

	annotators['tester_plugin'] = tester_annotator
except Exception, e:
	print "Could not load tester_plugin.py: " + str(e)