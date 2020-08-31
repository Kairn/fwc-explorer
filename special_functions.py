# special_functions.py #
# =====================================================================
# DEFINE SPECIAL FUNCTIONS THAT ARE CALLED INDEPENDENTLY BY SPECIAL COMMANDS.
# THESE FUNCTIONS REPORT ON THE MORE GENERAL INFORMATION ABOUT THE TOURNAMENT.
# 

from collections import Counter


def display_news(all_matches):
	"""List the results of the latest three matches."""
	
	fin = []
	
	for match in all_matches:
		if match.Finished:
			fin.append(match)
	
	if not fin:
		print("\nNo match history")
	else:
		fin = sorted(fin, key=lambda i: i.Index, reverse=True)
		while len(fin) > 3:
			fin.pop()
		else:
			print("\n********** Latest Results **********\n")
			for f_match in fin:
				f_match.display_result()
				
	print("")
	return 0


def display_up_schedule(all_matches):
	"""List the time schedule for the nearest three upcoming matches if any."""
	
	ufin = []
	
	for match in all_matches:
		if not match.Finished:
			ufin.append(match)
	
	if not ufin:
		print("\nNo known schedule")
	else:
		ufin = sorted(ufin, key=lambda i: i.Index, reverse=False)
		while len(ufin) > 3:
			ufin.pop()
		else:
			print("\n********** Upcoming Matches **********\n")
			for uf_match in ufin:
				if uf_match.T0 != "" and uf_match.T1 != "":
					uf_match.display_schedule()
				
	print("")
	return 0


def display_awards(all_matches, wc_awards):
	"""List all the awards given to players and teams."""
	
	if not all_matches[-1].Finished or all_matches[-1].Type != "Final":
		print("\nNot available until World Cup is over.\n")
		return 0
	
	print("\n********** World Cup Awards **********\n")
	
	for award, winner in wc_awards.items():
		award += ":"
		print("{:30}{}".format(award, winner))
		
	print("")
	return 0


def display_top_scorers(all_matches):
	"""List all players that have scored from most to least."""
	
	all_names = []
	for match in all_matches:
		if match.Finished:
			for goal in match.Goals:
				if goal.Type == "N":
					all_names.append(goal.Player)
	
	if all_names:
		scorer_cnt = Counter(all_names)
		scorer_list = scorer_cnt.most_common(len(scorer_cnt))
		scorer_list = [("Total", len(all_names))] + scorer_list
	else:
		print("No goals yet\n")
		return 0
	
	print("\n********** Best Scorers **********\n")
	print("{:2}   {:^25}      {}".format(" #", "Name", "Goals"))
	
	amt = 9999
	rank = -1
	for name, amount in scorer_list:
		if amount < amt:
			rank += 1
			amt = amount
		print("{:2}   {:^25}      {}".format(rank, name, amount))
	
	print("")	
	return 0


def display_ranking(all_matches):
	"""List the final rankings for all participating teams."""
	
	if not all_matches[-1].Finished or all_matches[-1].Type != "Final":
		print("\nNot available until World Cup is over.\n")
		return 0
	
	print("\n********** Team Rankings **********\n")
	rnk_struct = "Champion:         {0}\nRunners-up:       {1}\n"
	rnk_struct += "Third Place:      {2}\nFourth Place:     {3}\n"
	rnk_struct += "No. 5 - No. 8:    {4[0]}, {4[1]}, {4[2]}, {4[3]}\n"
	rnk_struct += "No. 9 - No. 16:   {5[0]}, {5[1]}, {5[2]}, {5[3]}, "
	rnk_struct += "{5[4]}, {5[5]}, {5[6]}, {5[7]}\n"
	
	b8 = []
	b16 = []
	for match in all_matches:
		if match.Type == "Final":
			n1 = match.Winner
			n2 = match.Loser
		elif match.Type == "3rd Place Playoff":
			n3 = match.Winner
			n4 = match.Loser
		elif match.Type == "Round of 8":
			b8.append(match.Loser)
		elif match.Type == "Round of 16":
			b16.append(match.Loser)
	
	rnk_final = rnk_struct.format(n1, n2, n3, n4, b8, b16)
	print(rnk_final)
	
	return 0


def display_structure(all_groups):
	"""List all participating teams in group strcuture."""
	
	print("\n********** All Groups **********\n")
	
	grp_struct = "{:=^20}\n"
	grp_struct += "{:^20}\n" * 4
	grp_struct += "{:=^20}\n"
	
	for group in all_groups:
		g_name = "Group " + group.ID
		g0 = group.Teams[0]
		g1 = group.Teams[1]
		g2 = group.Teams[2]
		g3 = group.Teams[3]
		g_end = group.ID + " Group"
		
		grp = grp_struct.format(g_name, g0, g1, g2, g3, g_end)
		print(grp)
	
	return 0


def display_bracket(all_matches):
	"""Draw the current knockout round bracket."""
	
	bkt_struct = "##{1[0]:^20} {1[1]:^20} {1[2]:^20} {1[3]:^20} {1[4]:^20}\n"
	bkt_struct += "  {0:20} {0:20} {0:20} {1[5]:^20} {1[6]:^20}\n"
	bkt_struct += "A1{2[0]:—^20}|\n"								#3
	bkt_struct += "  {0:20}|{3[0]:—^20}|\n"							#4
	bkt_struct += "B2{2[1]:—^20}|{0:20}|\n"							#5
	bkt_struct += "  {0:20} {0:20}|{4[0]:—^20}|\n"					#6
	bkt_struct += "C1{2[2]:—^20}|{0:20}|{0:20}|\n"					#7
	bkt_struct += "  {0:20}|{3[1]:—^20}|{0:20}|\n"					#8
	bkt_struct += "D2{2[3]:—^20}|{0:20} {0:20}|\n"					#9
	bkt_struct += "  {0:20} {0:20} {0:20}|{6[0]:—^20}|\n"			#10
	bkt_struct += "E1{2[4]:—^20}|{0:20} {0:20}|{0:20}|\n"			#11
	bkt_struct += "  {0:20}|{3[2]:—^20}|{0:20}|{0:20}|\n"			#12
	bkt_struct += "F2{2[5]:—^20}|{0:20}|{0:20}|{0:20}|\n"			#13
	bkt_struct += "  {0:20} {0:20}|{4[1]:—^20}|{0:20}|\n"			#14
	bkt_struct += "G1{2[6]:—^20}|{0:20}|{0:20} {0:20}|\n"			#15
	bkt_struct += "  {0:20}|{3[3]:—^20}|{0:20} {0:20}|\n"			#16
	bkt_struct += "H2{2[7]:—^20}|{0:20} {0:20} {0:20}|\n"			#17
	bkt_struct += "  {0:20} {0:20} {0:20} {0:20}|{8:—^20}\n"		#18
	bkt_struct += "B1{2[8]:—^20}|{0:20} {0:20} {0:20}|\n"			#19
	bkt_struct += "  {0:20}|{3[4]:—^20}|{0:20} {0:20}|\n"			#20
	bkt_struct += "A2{2[9]:—^20}|{0:20}|{0:20} {0:20}|\n"			#21
	bkt_struct += "  {0:20} {0:20}|{4[2]:—^20}|{0:20}|\n"			#22
	bkt_struct += "D1{2[10]:—^20}|{0:20}|{0:20}|{0:20}|\n"			#23
	bkt_struct += "  {0:20}|{3[5]:—^20}|{0:20}|{0:20}|\n"			#24
	bkt_struct += "C2{2[11]:—^20}|{0:20} {0:20}|{0:20}|\n"			#25
	bkt_struct += "  {0:20} {0:20} {0:20}|{6[1]:—^20}|\n"			#26
	bkt_struct += "F1{2[12]:—^20}|{0:20} {0:20}|\n"					#27
	bkt_struct += "  {0:20}|{3[6]:—^20}|{0:20}|\n"					#28
	bkt_struct += "E2{2[13]:—^20}|{0:20}|{0:20}|\n"					#29
	bkt_struct += "  {0:20} {0:20}|{4[3]:—^20}|\n"					#30
	bkt_struct += "H1{2[14]:—^20}|{0:20}|{0:20} {5[0]:—^20}|\n"		#31
	bkt_struct += "  {0:20}|{3[7]:—^20}|{0:20} {0:20}|{7:—^20}\n"	#32
	bkt_struct += "G2{2[15]:—^20}|{0:20} {0:20} {5[1]:—^20}|\n"		#33
	
	mts = [m for m in range(49)]	# padding numbers for easy indexing.
	mts += (sorted(all_matches, key=lambda i: i.Index))[48:]
	for mt in mts[49:]:
		mt.Teams = list(mt.Teams)
		if mt.Teams[0] == "":
			mt.Teams[0] = "TBD"
		if mt.Teams[1] == "":
			mt.Teams[1] = "TBD"
		if mt.Index == 63 or mt.Index == 64:
			if mt.Winner == "":
				mt.Winner = "TBD"
	
	titles = ["Round of 16", "Round of 8", "Semi_finals",
			  "Final", "Champion", "3rd Place Playoff", "3rd Place"]
	
	r16 = [mts[49].Teams[0], mts[49].Teams[1],
		   mts[50].Teams[0], mts[50].Teams[1],
		   mts[53].Teams[0], mts[53].Teams[1],
		   mts[54].Teams[0], mts[54].Teams[1],
		   mts[51].Teams[0], mts[51].Teams[1],
		   mts[52].Teams[0], mts[52].Teams[1],
		   mts[55].Teams[0], mts[55].Teams[1],
		   mts[56].Teams[0], mts[56].Teams[1]]
	
	r8 = [mts[57].Teams[0], mts[57].Teams[1],
		  mts[58].Teams[0], mts[58].Teams[1],
		  mts[59].Teams[0], mts[59].Teams[1],
		  mts[60].Teams[0], mts[60].Teams[1]]
	
	r4 = [mts[61].Teams[0], mts[61].Teams[1],
		  mts[62].Teams[0], mts[62].Teams[1]]
	
	r3o = [mts[63].Teams[0], mts[63].Teams[1]]
	r2 = [mts[64].Teams[0], mts[64].Teams[1]]
	r3 = mts[63].Winner
	r1 = mts[64].Winner
	
	bkt = bkt_struct.format("", titles, r16, r8, r4, r3o, r2, r3, r1)
	
	print("\n********** World Cup Bracket **********\n")
	print(bkt)
	
	return 0

