# fwc_explorer.py #
# =====================================================================
# RUNNING THIS SCRIPT WILL LAUNCH THE MAIN PROGRAM.
# MAKE SURE ALL ASSOCIATED FILES ARE INCLUDED IN THE SAME DIRECTORY.
# 
# RUN COMMAND: python3 fwc_explorer.py
# 

import json
from attrdict import AttrDict

from tzone_convert import *
from command_functions import *
from special_classes import *

# load the help file.
with open("command_help.txt", "r") as hp:
	FULL_TEXT = hp.readlines()
	help_text = [line for line in FULL_TEXT]

# load the data file.
with open("fifa_data.json", "r") as jp:
	raw_data = json.load(jp)
	FULL_DATA = AttrDict(raw_data)
	
wc_meta = FULL_DATA.Meta
wc_matches = FULL_DATA.Matches
wc_groups = FULL_DATA.Groups
wc_awards = FULL_DATA.Awards


def initialize(all_matches, all_groups, parti_teams, wc_matches, wc_groups, user_tz):
	"""Setup/re-initialize match and group object lists."""
	
	all_matches.clear()
	all_groups.clear()
	
	for match in wc_matches:
		all_matches.append(Match(match, user_tz))
		pass

	for group in wc_groups:
		all_groups.append(Group(group, wc_matches, user_tz))
		for gt in group.Teams:
			parti_teams.append(gt.title())
		pass


def run_explorer(wc_meta, wc_matches, wc_groups, wc_awards):
	"""Display the welcome message and start a browsing session."""
	
	all_matches = []
	all_groups = []
	parti_teams = []
	parti_groups = ["A", "B", "C", "D", "E", "F", "G", "H"]
	
	welcome_msg = "\nWelcome to the {} {} World Cup Explorer."
	welcome_msg = welcome_msg.format(wc_meta.Year, wc_meta.Host)
	print(welcome_msg)
	
	# time zone setup.
	user_tz = tz_setup().upper()
	initialize(all_matches, all_groups, parti_teams, wc_matches, wc_groups, user_tz)
	
	print("\nPlease enter a command to browse data.")
	print("Read command_help.txt for instructions or enter Help.")
	
	# main loop.
	while True:
		u_command = input("\n$ ")
		
		if u_command.title() == "Quit":
			print("\nThank you for using the explorer, welcome back any time.\n\n")
			break
		elif u_command.title() == "Help":
			for line in help_text:
				print(line.strip())
			else:
				print("")
				continue
		elif u_command.title() == "Tzone":
			user_tz = tz_setup().upper()
			initialize(all_matches, all_groups, parti_teams, wc_matches, wc_groups, user_tz)
		else:
			error_code = read_command(u_command, all_matches, all_groups,
									  parti_teams, parti_groups, wc_awards)
			# print("\n{}\n".format(error_code))
			handle_error(error_code)
			continue


if __name__ == "__main__":
	run_explorer(wc_meta, wc_matches, wc_groups, wc_awards)
