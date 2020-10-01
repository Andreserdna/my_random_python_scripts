import os
import sys
import matplotlib.pyplot as plt
#text_file_list = list()

class ExtractData:
	#lets extract the data from the text files
	def __init__(self,text_path):
		self.text_path = text_path
		self.extension = ".txt"
		self.text_file_list = list()
		self.text_key_and_value = dict()
		self.pmax_values = list()
		self.pmax_string = "Pmax"
		self.text_file_count = 0

	def checkIfPathValid(self,text_path):
		#Checks if the user path is valid. If not, exit this script
		try:
			if os.path.exists(text_path):
				print("Valid Path provided")
				return True
			else:
				print("Path you provided is not valid, check you directory and try again")
			return False
		except FileNotFoundError as e:
			print(e)
	def check_for_text_files(self,text_path):
		#this function is checking for text files in a specifed path, it returns the name of all the
		#files ending with a txt extension
		if self.checkIfPathValid(self.text_path) == True:
			print("Fetching all text files in the provided directory")
			for r,d,f in os.walk(text_path):
				for files in f:
					#checking for all files that end with .TXT since phong provided all upper case, i am using .upper()
					if files.endswith(self.extension.upper()):
						print(files, " ends with text, appending to list!")
						append_file = os.path.join(self.text_path,files)
						self.text_file_list.append(append_file)
						self.text_file_count = self.text_file_count + 1
			return(self.text_file_list)
		else:
			print("Path was not valid")
			sys.exit()
	def data_parsing(self):
		#lets begin the data parsing
		try:
			#checking if the number of text files match what is in the list
			#if true, begin extracting pmax values and storing them in self.pmax_values
			if len(self.text_file_list) == self.text_file_count:
				for text_file in self.text_file_list:
					with open(text_file,"r") as my_file:
						lines = my_file.readlines()
						for line in lines:
							#stripping the white spaces from the text document
							line = line.strip()
							if line.startswith(self.pmax_string):
								#print("Current pmax value is ", line[9:])
								self.pmax_values.append(float(line[9:]))
								my_file.close()
				return(self.pmax_values)
		except FileNotFoundError as e:
			print(e)
		finally:
			print("Pmax values data has been stored to the list")

	# def check_pmax_data(self):
	# 	for value in self.pmax_values:
	# 		print(value,type(value))
class PlotData(ExtractData):

	def __init__(self,ext_class):
		self.pmax_values = ext_class.pmax_values


	# def print_data(self):
	# 	print("printing as objected inherated")
	# 	for item in self.pmax_values:
	# 		print()
	# 		print(item)
	def plot_data_to_graph(self):
		data = self.pmax_values
		plt.xlabel("X-Axis")
		plt.ylabel("Y-Axis")
		plt.title("This is a test graph")

		for item in data:
			plt.plot(item)
		plt.legend()
		plt.show()
def main():
	hardCodedPath = "/home/atamayo/Scripts/test_data"
	#user_path = sys.argv[1]

	c = ExtractData(hardCodedPath)
	p = PlotData(c)
	try:
		c.check_for_text_files(hardCodedPath)
		c.data_parsing()
		#c.check_pmax_data()


		p.plot_data_to_graph()
	except ValueError as e:
		print(e)

if __name__ == '__main__':
	main()
