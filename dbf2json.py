import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler    
      
import dbfread
import sys
import json
import iso8601
import datetime

if __name__ == "__main__":
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    

def on_created(event):
    print(f"hey, {event.src_path} has been created!")

def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")

def on_modified(event):
    print(f"modified {event.src_path}!")

def on_moved(event):
    print(f"ok ok ok, someone moved {event.src_path} to {event.dest_path}")
    
my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved
    
path = "."
go_recursively = True
my_observer = Observer()
my_observer.schedule(my_event_handler, path, recursive=go_recursively)

my_observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()


class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, datetime.date):
			return o.strftime('%Y-%m-%d')

if __name__ == '__main__':
	try:
		dbf_fn = input('DBF: ')
		json_fn = input('json: ')
		try:
			json_fn = sys.argv[2]
		except IndexError:
			pass
	except IndexError:
		sys.stderr.write('usage: dbf2json <dbf_filename_input> (json_filename_input)\n\t json filename is optional, will write to stdout if not given or -. If - is given for input, it will read from stdin\n')
		sys.stderr.flush()
		sys.exit(1)
	
	def get_handle(fn, mode, do_open=True):
		if fn == '-':
			if mode == 'r':
				if do_open:
					return sys.stdin
				else:
					return '/dev/stdin'
			elif mode == 'w':
				if do_open:
					return sys.stdout
				else:
					return '/dev/stdout'
		else:
			if do_open:
				return open(fn, mode)
			else:
				return fn

	in_filename = get_handle(dbf_fn, 'r', do_open=False)
	out_handle = get_handle(json_fn, 'w')

	output = [rec for rec in dbfread.open(in_filename)]

	json.dump(output, out_handle, indent=4, sort_keys=True, cls=JSONEncoder)
	out_handle.flush()
	out_handle.close()
	sys.exit(0)
