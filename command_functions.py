# command_functions.py #
# =====================================================================
# DEFINE THE FUNCTION FOR INTERPRETING COMMANDS.
# DEFINE GROUP & TEAM & MATCH RELATED FUNCTIONS FOR THE PROGRAM.
# 
# ERROR CODE 0: NO ERROR.
# ERROR CODE 1: UNRECOGNIZED COMMAND OR INVALID SYNTAX.
# ERROR CODE 2: NO RESULTS FOUND.
# 

from special_functions import *


def read_command(t_command, all_matches, all_groups, parti_teams, parti_groups, wc_awards):
	"""Interpret user's command and return a function call."""
	
	error_code = 0
	
	command_list = str(t_command).title().split(" ")
	if command_list[-1] == "Verbose":
		verbose = True
		command_list.pop()
	else:
		verbose = False
	cn = len(command_list)
	
	if command_list[0] == "Match" and cn > 1:
		if command_list[1] == "Vs" and cn == 4:
			error_code = display_match_vs(command_list[2], command_list[3], all_matches)
		elif command_list[1] != "All":
			name_set = set(command_list[1:])
			error_code = display_match_ind(name_set, all_matches, parti_teams, verbose)
		else:
			error_code = display_match_all(all_matches, verbose)
		
	elif command_list[0] == "Team" and cn > 1:
		if command_list[1] != "All":
			name_set = set(command_list[1:])
			error_code = display_team_ind(name_set, all_matches, parti_teams, verbose)
		else:
			error_code = display_team_all(parti_teams, all_matches)
		
	elif command_list[0] == "Group" and cn > 1:
		if command_list[1] != "All":
			name_set = set(command_list[1:])
			error_code = display_group_std(name_set, all_groups, parti_groups, verbose)
		else:
			error_code = display_group_std(parti_groups, all_groups, parti_groups, verbose)
		
	else:
		if command_list[0] == "Structure" and cn == 1:
			error_code = display_structure(all_groups)
		elif command_list[0] == "Bracket" and cn == 1:
			error_code = display_bracket(all_matches)
		elif command_list[0] == "Ranking" and cn == 1:
			error_code = display_ranking(all_matches)
		elif command_list[0] == "Awards" and cn == 1:
			error_code = display_awards(all_matches, wc_awards)
		elif command_list[0] == "Scorers" and cn == 1:
			error_code = display_top_scorers(all_matches)
		elif command_list[0] == "News" and cn == 1:
			error_code = display_news(all_matches)
		elif command_list[0] == "Upcoming" and cn == 1:
			error_code = display_up_schedule(all_matches)
		else:
			error_code = 1
			
	return error_code


def handle_error(t_error_code):
	"""Report issue if user's command does not yield any positive result."""
	
	if t_error_code == 0 or not t_error_code:
		return None
	elif t_error_code == 1:
		print("\nError: unrecognized command or invalid syntax\n")
	elif t_error_code == 2:
		print("\nError: no results found\n")
	else:
		print("\nUnknown Error\n")


def display_match_vs(t_1, t_2, all_matches):
	"""Show details of the match(es) between the two teams."""
	
	found = []
	mn = 0
	
	for match in all_matches:
		if t_1 in match.Teams and t_2 in match.Teams:
			found.append(match)
			
	if not found:
		return 2
	else:
		print("\n----- {} VS {} Details -----".format(t_1.title(), t_2.title()))
		for f_match in found:
			mn += 1
			print("\n***** Match {} *****\n".format(mn))
			f_match.display_full_detail()
			print("")
			
		return 0


def display_match_ind(t_name_set, all_matches, parti_teams, verbose):
	"""Show match results for user selected teams."""
	
	r_set = []
	
	for t_team in t_name_set:
		if t_team in parti_teams:
			r_set.append(t_team)
		else:
			print("{} not found".format(t_team))
	
	if not r_set:
		return 2
	
	for r_team in r_set:
		print("\n----- Team {} Matches-----\n".format(r_team.title()))
		found = []
		found_uf = []
		for match in all_matches:
			if r_team in match.Teams:
				if match.Finished:
					found.append(match)
				else:
					found_uf.append(match)
		
		if found:
			print("Match History:")
			for f_match in found:
				f_match.display_result(r_team)
				if verbose:
					f_match.display_goals(r_team)
				print("")
		
		if found_uf:
			print("\nUpcoming Matches:")
			for uf_match in found_uf:
				if uf_match.T0 != "" and uf_match.T1 != "":
					uf_match.display_schedule(r_team)
			print("")
			
	return 0
	
	
def display_match_all(all_matches, verbose):
	"""Show history in reverse chronological order, show scheduled future
	matches in chronological order."""
	
	fin = []
	ufin = []
	
	for match in all_matches:
		if match.Finished:
			fin.append(match)
		else:
			ufin.append(match)
	
	fin = sorted(fin, key=lambda i: i.Index, reverse=True)
	ufin = sorted(ufin, key=lambda i: i.Index, reverse=False)
	
	if fin:
		print("\n----- All Match History -----\n")
		for f_match in fin:
			f_match.display_result()
			if verbose:
				f_match.display_goals()
			print("")
			
	if ufin:
		print("\n----- Scheduled Upcoming Matches -----\n")
		for uf_match in ufin:
			if uf_match.T0 != "" and uf_match.T1 != "": 
				uf_match.display_schedule()
		print("")
		
	return 0


def display_team_ind(t_name_set, all_matches, parti_teams, verbose):
	"""Show team(s) stats and its match details if verbose."""
	
	r_set = []
	
	for t_team in t_name_set:
		if t_team in parti_teams:
			r_set.append(t_team)
		else:
			print("{} not found".format(t_team))
	
	if not r_set:
		return 2
	
	for r_team in r_set:
		display_team_stats(r_team, all_matches)
		fin = []
		for match in all_matches:
			if r_team in match.Teams and match.Finished:
				fin.append(match)
		fin = sorted(fin, key=lambda i: i.Index, reverse=False)
		if verbose:
			if fin:
				print("\n{} Match History:".format(r_team.title()))
				for f_match in fin:
					f_match.display_result(r_team)
			ufin = []
			for match in all_matches:
				if r_team in match.Teams and not match.Finished:
					ufin.append(match)
			if ufin:
				print("\n{} Match Schedule:".format(r_team.title()))
				for uf_match in ufin:
					uf_match.display_schedule(r_team)
		else:
			if fin:
				print("\nMost Recent:")
				fin[-1].display_result(r_team)
	print("")
	return 0


def display_team_all(parti_teams, all_matches):
	"""Show all teams' stats."""
	
	for team in parti_teams:
		display_team_stats(team, all_matches)
	
	print("")
	return 0


def display_team_stats(t_team, all_matches):
	"""Calculate and display various stats for a team based on the data."""
	
	print("\n----- Team {} Statistics-----\n".format(t_team.title()))
	a_found = []
	mp = 0
	gf = 0
	gd = 0
	w = 0
	d = 0
	l = 0
	
	for match in all_matches:
		if t_team in match.Teams:
			a_found.append(match)
	
	a_found = sorted(a_found, key=lambda i: i.Index, reverse=False)
	
	for a_match in a_found:
		if a_match.Finished:
			mp += 1
			if a_match.Winner == t_team:
				w += 1
			elif a_match.Winner == "Draw":
				d += 1
			else:
				l += 1
			for a_goal in a_match.Goals:
				if t_team == a_goal.Team and a_goal.Type != "P":
					gf += 1
					gd += 1
				elif t_team != a_goal.Team and a_goal.Type != "P":
					gd -= 1
	
	last = a_found[-1]
	
	if last.Type == "Group" and last.Finished:
		status = "disqualified in the group stage"
	elif last.Type == "Group" and not last.Finished:
		status = "still in the group stage"
	else:
		if not last.Finished and last.Type == "3rd Place Playoff":
			status = "disqualified in the semi_final"
		elif last.Finished and last.Type == "3rd Place Playoff":
			if last.Winner == t_team:
				status = "won the third place"
			else:
				status = "won the fourth place"
		elif not last.Finished and last.Type == "Final":
			status = "advanced to the final"
		elif last.Finished and last.Type == "Final":
			if last.Winner == t_team:
				status = "won the World Cup title"
			else:
				status = "won the second place"
		else:
			if not last.Finished:
				status = "advanced to the {}".format(last.Type)
			else:
				status = "disqualified in the {}".format(last.Type)
	
	stats_msg = "Current Status: {}\n".format(status)
	stats_msg += "Matches Played: {}\n".format(mp)
	stats_msg += "Wins: {}\n".format(w)
	stats_msg += "Losses: {}\n".format(l)
	stats_msg += "Draws: {}\n".format(d)
	stats_msg += "Total Goals: {}\n".format(gf)
	stats_msg += "Goal Difference: {}".format(gd)
	print(stats_msg)
	
	return 0


def display_group_std(t_name_set, all_groups, parti_groups, verbose):
	"""Show a group's current standings and the match results if verbose."""
	
	r_set = []
	
	for t_name in t_name_set:
		if t_name in parti_groups:
			r_set.append(t_name)
		else:
			print("{} not found".format(t_name))
	
	if not r_set:
		return 2
	
	g_list = []
	for r_group in r_set:
		for group in all_groups:
			if r_group == group.ID:
				g_list.append(group)
	g_list = sorted(g_list, key=lambda i: i.ID, reverse=False)
	
	for g_group in g_list:
		print("\n----- Group {} Standings -----\n".format(g_group.ID))
		g_group.display_standings()
		if verbose:
			print("\n----- Group {} Matches -----\n".format(g_group.ID))
			g_group.display_m_standings()
	
	print("")		
	return 0

