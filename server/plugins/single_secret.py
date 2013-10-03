from ss_collect import *
import psutil

def single_secret_auth_send( cfg, options ):
	return options

def single_secret_auth_receive( cfg, options, request, content ):
	return content == options

send_auth['single_secret'] = single_secret_auth_send
receive_auth['single_secret'] = single_secret_auth_receive