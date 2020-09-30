import os
import sys
import threading
import time
import subprocess
import pexpect
from pexpect import pxssh
import getpass
from subprocess import Popen,PIPE

class IniateBtmon():
	def __init__(self,dut_addr):
		self.dut_addr = dut_addr
		#TODO add logic to retrieve file location
		self.file_location = "/home/atamayo/work_scripts_test/execute_capture_script.py"
		self.local_save_path = "/tmp/"
		self.file_name = 'execute_capture_script.py'
		self.bin_bash = '/bin/bash -c'
		self.timeout = 15
		self.hostName = 'root@'
		self.password = 'test0000'
		self.ping_command = "ping -c 2 "
		self.ssh_command = 'ssh'
		self.copy_command = 'scp -r'
		self.capture_syslogs = 'generate_logs'
		self.dut_download_path = ':/home/chronos/user/Downloads/'
	def check_DUT_status(self,dut_addr):
		#function checks if the DUT is online, if the dut is offline, script will fail
		try:
			sub_call = subprocess.check_call([self.ping_command + self.dut_addr],shell=True)
			if sub_call == 0:
				print("\n root@{} is ONLINE".format(self.dut_addr))
				return True
			elif sub_call > 0:
				print("\n root@{} is OFFLINE".format(self.dut_addr))
				return False
		except subprocess.CalledProcessError as e:
			print(e)
	def pass_password(self,command,timeout):
		#This function is used to pass the password of the dut self.password in order to send files 
			try:
				child = pexpect.spawn(command,timeout=self.timeout)
				child.expect(["[pP]assword: "])
				child.sendline(self.password)
				child.expect(pexpect.EOF)
				child.close()				
				if child.exitstatus == 0:
					print("\nPassword was accepted!!")
					return True
				elif child.exitstatus > 0:
					print("\nFAILED to pass password")
					return False
			except pexpect.ExceptionPexpect as error:
				print("\tError with pexpect")
				print(error)
	def generate_pexpect_capture_file(self,pexpect_file=" "):
		timestr = time.strftime("%Y%m%d-%H%M%S")
		pexpect_file_path = (self.local_save_path + "pexpect_logs_{}.txt".format(timestr))
		btmon_logs = (self.dut_download_path + "btmon{}.logs".format(timestr))
		if os.path.exists(pexpect_file_path):
			print("found old pexpect_file creating a new one")
		else:
			with open(pexpect_file_path,"wb"):pass
			self.pexpect_file = pexpect_file_path
			return self.pexpect_file
	def execute_capture_using_pxssh(self,dut_addr,command):
		#using pxssh to execute the capture script, since pass_password_and_interact was not working
		#IMPLEMENT creating a new log file
		try:

			fout1 = (self.generate_pexpect_capture_file(self))
			fout = open(fout1,"wb")
			dut_shell = pxssh.pxssh(timeout=None)
			hostname = self.dut_addr
			username = self.hostName[0:4]
			password = self.password
			dut_shell.logfile = fout
			dut_shell.login(hostname,username,password)
			dut_shell.sendline(command)
			dut_shell.prompt()
			print(dut_shell.before)
			dut_shell.logout()
			return True
		except pxssh.ExceptionPxssh as e:
			print("pxssh failed on login.")
			print(e)
		print("BTMON/syslogs capture complete!!!")

	def pass_password_and_interact(self,hostname,command,timeout):
		#This function is used to interact with the shell insteadv of just sending a single command
			try:
				#CHANGE THIS FILE
				print("Attempting to call another function to create the loggs")
				child = pexpect.spawn(hostname,[command],timeout=self.timeout)
				child.expect(["[pP]assword: "])
				child.sendline(self.password)
				child.logfile_send = fout
				# child.logfile_send = fout
				send = child.expect(["Login incorrect",'[#]'])
				if send == 0:
					print("Permission denied on host")
					child.kill(0)
				if send == 1:
					print("Login OK, sending command : ",command)
				print(child.before)
				child.expect(pexpect.EOF)

				child.close()

				if child.exitstatus == 0:
					print("\nPassword was accepted!!")
					return True
				elif child.exitstatus == 1:
					print("\nFAILED to pass password")
					return False
			except pexpect.ExceptionPexpect as error:
				print("\tError with pexpect")
				print(error)


	def capture_syslogs_on_exit(self,dut_addr):
		#If user does keyboard interrupt, execute this block of code
		syslog_capture_comm = self.capture_syslogs
		try:
			print("Capturing system logs")
			if self.execute_capture_using_pxssh(dut_addr,syslog_capture_comm) == 1:
				print("generate_logs was completed successfully, saved under /tmp/ on the dut")
		except ValueError as error:
			print(error)

	def copy_capture_file(self,dut_addr):
		copy_check = self.check_DUT_status(dut_addr)
		if copy_check == True:
			try:
				print("copying capture files over to {}".format(self.dut_download_path))
				call_host_name = (self.hostName + self.dut_addr + self.dut_download_path)
				copy_command = (self.copy_command + " " + self.file_location + " " )
				combined_copy_call = copy_command + call_host_name
				self.pass_password(combined_copy_call,self.timeout)
				print("File copy was successfull")
				return True
			except ValueError as error:
				print(error)
				return False
		else:
			print("Copy was not successfull, cannot proceed any further, check your host IP address")
			return False

	def execute_btmon_capture(self,dut_addr):
		if self.copy_capture_file(dut_addr) == True:
			print("Initiating BTmon")
			ex_call = (self.ssh_command + " " + self.hostName + dut_addr + " " + 'nohup python3 ' + \
				self.dut_download_path[1:] + self.file_name + " " + "&")
			print(ex_call)
			try:
				print("Attempting to execute script remotely")
				execute_comm = self.pass_password(ex_call,self.timeout)
				if execute_comm == True:
					print("execute command was sent")
				else:
					print("execute script did not run")

			except ValueError as error:
				print(error)
	def execute_btmon_capture2(self,dut_addr):
		if self.copy_capture_file(dut_addr) == True:
			print("\nInitiating BTmon")
			capture_command = ('python3 -u - < ' + self.dut_download_path[1:] + self.file_name)
			long_command = ("/bin/bash -c \'python3 /home/chronos/user/Downloads/execute_capture_script.py\'")
			ex_call = (self.ssh_command + " " + self.hostName + dut_addr + " " +'|' + " " + 'python3 ' + self.dut_download_path[1:] + self.file_name)
			print("\n\tCurrent BTMON log capture size is at 50MB")
			print("\n\tCapturing BTMON logs in the DUT background, exit this script anytime to capture syslogs on exit")

			try:
				#self.pass_password_and_interact(host_command,long_command,timeout=self.timeout)
				print("BTMON on DUT initialized!!")
				self.execute_capture_using_pxssh(dut_addr,long_command)
				#todo implement capture logs even if it succeeded
				return True

			except KeyboardInterrupt:
				print("BTMON Capture was interrupted, generating \'generate_logs\' on dut ")
				self.capture_syslogs_on_exit(Uanswer)
				return False
			print("BTMON capture complete!! BTMOn logs were saved under: ",self.dut_download_path[1:])
			return True	

Uanswer = input("Enter dut address e.g x.x.x.x: ")
#Uanswer = "10.0.0.89"
c = IniateBtmon(Uanswer)
try:
	#c = IniateBtmon(Uanswer)

	if c.execute_btmon_capture2(Uanswer) == True:
		c.capture_syslogs_on_exit(Uanswer)
		print("\nBTMON and syslogs Capture was successfull")
	# begin = capture_logs(Uanswer)
	# begin.execute_btmon_capture(Uanswer)
except ValueError as e:
	print(e)