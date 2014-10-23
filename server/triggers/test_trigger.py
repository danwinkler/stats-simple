from ss_triggers import *
from trigger_helper import *

def test_trigger():
	make_alert( "Test trigger", "test trigger", 2 )

triggers['test_trigger'] = test_trigger