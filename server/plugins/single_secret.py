from ss_plugin import *
import psutil

def single_secret_auth_send( options=None ):
	return options

def single_secret_auth_receive( options=None, request=None, content=None ):
	return content == options

send_auth['single_secret'] = single_secret_auth_send
receive_auth['single_secret'] = single_secret_auth_receive