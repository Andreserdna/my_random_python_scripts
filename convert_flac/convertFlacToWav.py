#This scrip converts all flac files to WAV, 
#this is necessary in order to burn tracks to a CD

import os

extension = (".flac")
new_extension = (".wav")
ffMpegCall = ("ffmpeg -i ")
converted_folder = ("converted")

def remove_space(path):
	for r,d,f in os.walk(path):
		for files in f:
			print("removed white space for ", files)
			no_space_file = files.replace(" ","")
			if (no_space_file != files):
				os.rename(files,no_space_file)
			else:
				print("NO white spaces found")
def convert(path):
	#create_converted_path(path)
	for r,d,f in os.walk(path):
		for files in f:
			if files.endswith(extension):
				os.chdir(path)
				new_file = files.replace(" ","")
				final_file = new_file.replace(extension,new_extension)
				command = ffMpegCall + files + " " + converted_folder + '/' + final_file
				os.system(command)
def create_converted_path(path):
	final_path = os.path.join(path + converted_folder)
	if os.path.exists(final_path):
		print("converted path exists")
	else:
		print("Final converted path does not exist")
		os.mkdir(final_path)
		os.chdir(final_path)
		print("Created {} ".format(final_path))
		os.system("pwd")
def main():
	try:
		user_path = str(input("Please file path: "))
	except ValueError as e:
		print("Path not valid")
		print(e)
	create_converted_path(user_path)
	convert(user_path)

if __name__ == '__main__':
	main()