import os
import sys
from termcolor import colored
import csv
import pprint
import json

def write_to_csv(csv_location,row_names,player_name,player_stats,tier_dict):
	try:
		with open(csv_location,'wb') as csv_file:
			writer = csv.DictWriter(csv_file,fieldnames=row_names)
			writer.writeheader()
			writer.writerow(tier_dict)
			
			for i in range(4):	
				writer.writerow(combine_player_dict(player_name,player_stats))
		print colored("write successfull", 'white')
		csv_file.close()
	except SyntaxError as syn_error:
		print(syn_error)


def check_user_answer(answer):

	yes = {'yes','y','ye',''}
	no = {'no','n'}
	#
	while True:
		try:
			if answer in yes:
				return True
			elif answer in no:
				return False
			else:
				sys.stdout.write("Please respond with 'yes' or 'no' ")
				break
		except ValueError:
			print colored("Please enter a valid message",'red')

def input_player_name(player_name_dict):
#If user wishes 
    if len(player_name_dict["Name"]) <= 0:
        name = raw_input("Enter player Name: ")
        #TODO add error check for name input
        player_name_dict.update({"Name":name})
    	return player_name_dict
    elif len(player_name_dict["Name"]) >= 0:
        name = raw_input("Enter player Name: ")
    	player_name_dict.update({"Name": name})
    	return player_name_dict
    else:
    	print("Inside else statement INPUT_PLAYER_NAME")

def pretty_print(dict_item):
	print(json.dumps(dict_item, indent=4, sort_keys=True))

def player_tier_list(tier_dict):
	accepted_tier_list = [1,2,3]
#function to add tier number to the csv in order to distinguish player tiers
	for k,v in tier_dict.iteritems():
		if v <= 0:
			print("Please enter a tier number [1,2,3]")
			tier_num =int(input("Tier: "))
			tier_dict.update({"Tier":tier_num})
		elif v >= 0:
			print colored("Tier number present...OverWriting",'blue')
			tier_dict.update({"Tier":0})
			print("Please enter a tier number [1,2,3]")
			tier_num =int(input("Tier: "))
			tier_dict.update({"Tier":tier_num})
	return tier_dict


def input_stats(temp_dict):

  #This function is used to update the player stats. User must pass a dictionary object in order
  #for this function to execute properly
    for key,value in temp_dict.iteritems():
        if value <= 0:
            print("enter the stat for the following %s") % (key)
            stat_int1 = float(input(":"))
            temp_dict.update({key:stat_int1})
        elif value >= 0:
			print colored("Value present. OverWriting!", "blue")
			print("enter the stat for the following %s") % (key)
			stat_int1 = float(input(":"))
			temp_dict.update({key:stat_int1})
        #TODO make user input stats again depending on answer given by PLAYER CONFIRMATION FUNCTION
            
            #print 'Value already present for %s' % (key)
    return temp_dict


def combine_player_dict(player_name,player_stats):
	#z = dict(player_name.items()+ player_stats.items())
	return dict(player_name.items() + player_stats.items())



def main():
	pass

if __name__ == '__main__':


	temporary_stat_list = {}
	row_names = ["Tier","Name","FT","FG","3PM","AST","STL","PPG"]
	tier = {"Tier": 0 }
	player_name_dict = {"Name": ''}
	player_stats = {"FT":0,"FG":0,"3PM":0,"AST":0,"STL":0, "PPG": 0}



	add_player_answer = raw_input("Do you wish to add players?[y/N]: ").lower()
	if check_user_answer(add_player_answer) == True:
		player_tier_list(tier)
		print colored("How many players are you adding to tier %s", 'white') % tier["Tier"]

		number_of_players_to_add_to_tier = int(input("number of players: "))
		#INSERT FUNCTION HERE TO ADD NUMBER OF PLAYERS TO A VARIABLE. WITH THIS FUNCTION YOURE PROGRAM WILL BE FINSISHED. AT LEAST
		#VERSION 0.5. THIS FUNCTION ACCEPTS A INPUT AND ITERATES OVER THAT INPUT X AMOUNT OF TIMES.
		input_player_name(player_name_dict)

		input_stats(player_stats)
		pretty_print(player_name_dict)
		pretty_print(player_stats)
		correct_stat_answer = raw_input('Are the following stats correct[y/N]: ')
		while check_user_answer(correct_stat_answer):
			print colored("Writing to CSV file!",'blue')
			write_to_csv(csv_file_location,row_names,player_name_dict,player_stats,tier)
			break
		while not check_user_answer(correct_stat_answer):
			print colored("Lets try this again!",'red')
			input_player_name(player_name_dict)
			input_stats(player_stats)
			pretty_print(player_name_dict)
			pretty_print(player_stats)
			correct_stat_answer = raw_input('Are the following stats correct[y/N]: ')
			if check_user_answer(correct_stat_answer):
				write_to_csv(csv_file_location,row_names,player_name_dict,player_stats,tier)
				print colored("DONE",'green') 
	elif check_user_answer(add_player_answer) == False:
		print colored("Goodbye Foo",'yellow')			
