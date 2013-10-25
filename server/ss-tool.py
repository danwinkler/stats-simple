import argparse
import sqlite3
import sys
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser( formatter_class=RawTextHelpFormatter, description='''
Stats-Simple Command Line Tool
Available commands:
rm-node
''' )

parser.add_argument("command", help="The command you want to run")
parser.add_argument("arg")

args = parser.parse_args()

def rm_node( node ):
	conn = sqlite3.connect( "db.db" )
	conn.row_factory = sqlite3.Row
	db = conn.cursor()
	
	print "Finding node..."
	node_row = db.execute('SELECT id from nodes where name=?', (node,)).fetchone()
	if node_row == None:
		print "No row with name: " + node
		sys.exit()

	node_id = int(node_row['id'])

	print "Deleting data..."
	rows = db.execute('DELETE FROM data WHERE node=?', (node_id,) )
	conn.commit()
	print "Deleting notes..."
	rows = db.execute('DELETE FROM notes WHERE node=?', (node_id,) )
	conn.commit()
	print "Deleting node..."
	rows = db.execute('DELETE FROM nodes WHERE id=?', (node_id,) )
	conn.commit()
	conn.close()
	print "Done!"

def no_command( args ):
	print "Bad Command: " + str(args.command)

{ "rm-node": rm_node }.get( args.command, no_command )( args.arg )