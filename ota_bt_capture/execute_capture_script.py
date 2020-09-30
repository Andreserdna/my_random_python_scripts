import threading
import time
import os
import subprocess
import sys
from datetime import datetime

#Assuming the script got sent over
#In order for this script to run, DUT must have a test image
#TODO implement am unique file name, once file hits the limit create a new file
	# find usual size for btmon capture
	# make sure data is valid, try pairing a device when process is in the BG
#TODO use datettime to create a new file and loop until user quits
#TODO retrieve user address and copy to a non sudo location
#create logic when user .. until KeyboardInterrupt\
#date_string = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
#timestamp = str(now.strftime("%Y%m%d_%H-%M-%S"))
timestr = time.strftime("%Y%m%d-%H%M%S")
filepath = ("/home/chronos/user/Downloads/bt_snoop_{}.log".format(timestr))#.format(date_string))


if os.path.exists(filepath):
	print("found existing file, deleting to create a new one")
	os.remove(filepath)
	with open(filepath,'w'):pass
else:
	if not os.path.exists(filepath):
		print("Created {} and saved under {}".format(filepath,filepath[1:29]))
		with open(filepath,'w'):pass

threads_list = list()
current_file_size = os.path.getsize(filepath)
#setting the max btmon size to be 50 MB
#max_file_size = 50000000
max_file_size = 100000
max_file_size2 = 1000


class BtThread(threading.Thread):
	def __init__(self,thread_name,delay,filepath):
		threading.Thread.__init__(self)
		self.thread_name = thread_name
		self.delay = delay
		self.filepath = filepath
	def run(self):
		print("Starting thread {}".format(self.thread_name))
		initiate_btmon(self.thread_name,self.delay)
		check_file_size(self.thread_name,self.delay,self.filepath)
		print("Finished running threads")


def initiate_btmon(thread_name,delay):
	try:
		cap_command = ("sudo btmon -w {} > /dev/null 2>&1 &".format(filepath)) #> /dev/null 2>&1 &
		time.sleep(delay)
		#subprocess.Popen([cap_command])
		subprocess.call([cap_command],shell=True)
	except ValueError as error:
		print("Issue initializing btmon!", error)

def check_file_size(thread_name,delay,filepath):
	global increment
	global current_file_size
	global max_file_size

	while current_file_size < max_file_size:
		time.sleep(delay)
		print("Current file size is: ", current_file_size)
		new_file_size = os.path.getsize(filepath)
		print("adding {} bytes to file: ".format(new_file_size))
		current_file_size = current_file_size + new_file_size
		print("updating file size is: ",current_file_size)
		increment = current_file_size - new_file_size
		print("Capture file incremented by {} bytes".format(increment))
		current_file_size += current_file_size - increment

		if current_file_size >= max_file_size:
			print("File has reached its limit,creating a new btmon")
			break

	print("Threads have Finished recording data, exit script ended")
	return

def main():

	bt_thread = BtThread("bt_capture",2,filepath)
	file_size_thread = BtThread("file_size",2,filepath)
	threads_list.append(bt_thread)
	threads_list.append(file_size_thread)
	bt_thread.start()
	file_size_thread.start()

	for thread in threads_list:
		thread.join()
	print("current file size is ", current_file_size)
if __name__ == '__main__':
	main()