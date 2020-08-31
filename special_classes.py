# special_classes.py #
# =====================================================================
# DEFINE GROUP & MATCH DATA TYPES TO PARSE RAW JSON DATA.
# MOST FUNCTIONS IN THE PROGRAM WILL USE THESE DATA OBJECTS
# TO READ THE NECESSARY INFORMATION.
# 

from tzone_convert import *


class Match:
	"""Initialize special Match objects from raw json data."""
	
	def __init__(self, j_match, user_tz):
		"""Use titlecase for all data attributes."""
		
		self.ID = j_match.ID
		self.Index = j_match.Index
		self.Tzone = j_match.Tzone
		self.Teams = j_match.Teams
		self.Type = j_match.Type
		self.Group = j_match.Group
		self.Finished = j_match.Finished
		self.Goals = j_match.Goals
		self.Winner = j_match.Winner
		self.Stadium = j_match.Stadium
		self.Man_of_the_Match = j_match.Man_of_the_Match
		
		self.user_tz = user_tz
		self.auto_calc()
		
	def auto_calc(self):
		"""Deduce match facts and store them for further calls."""
		
		self.T0 = self.Teams[0]
		self.Score0 = 0
		self.Pscore0 = 0
		self.T1 = self.Teams[1]
		self.Score1 = 0
		self.Pscore1 = 0
		self.PSO = False
		
		if self.Finished:
			
			# deduce the loser of the match.
			if self.Winner not in self.Teams:
				self.Loser = "Draw"
			else:
				if self.Teams[0] == self.Winner:
					self.Loser = self.Teams[1]
				else:
					self.Loser = self.Teams[0]
			
			# deduce if penalty shoot-out occurred.
			if self.Goals:
				for goal in self.Goals:
					if goal.Type != "P":
						continue
					else:
						self.PSO = True
						break
				else:
					self.PSO = False
			
			# calculate the score.
			if self.Goals:
				for goal in self.Goals:
					if goal.Type != "P":
						if goal.Team == self.T0:
							self.Score0 += 1
						elif goal.Team == self.T1:
							self.Score1 += 1
					else:
						if goal.Team == self.T0:
							self.Pscore0 += 1
						elif goal.Team == self.T1:
							self.Pscore1 += 1
		
	def display_result(self, t_team="default"):
		"""Display match result with the selected team shown first."""
		
		msg0 = "{:15}{} - {}{:>15}".format(
		self.T0, self.Score0, self.Score1, self.T1
		)
		msg1 = "{:15}{} - {}{:>15}".format(
		self.T1, self.Score1, self.Score0, self.T0
		)
		msg_p0 = "{:15}{}({}P) - {}({}P){:>15}".format(
		self.T0, self.Score0, self.Pscore0,
		self.Score1, self.Pscore1, self.T1
		)
		msg_p1 = "{:15}{}({}P) - {}({}P){:>15}".format(
		self.T1, self.Score1, self.Pscore1,
		self.Score0, self.Pscore0, self.T0
		)
		
		if self.Finished:
			if t_team == "default" or t_team == self.T0:
				if self.PSO:
					print(msg_p0)
				else:
					print(msg0)
			else:
				if self.PSO:
					print(msg_p1)
				else:
					print(msg1)
	
	def display_schedule(self, t_team="default"):
		"""Display date and time for the match adjusted for 
		time zone difference."""
		
		ltime = tz_digest(self.ID, self.user_tz, self.Tzone)
		msg0 = "{:15}VS.{:>15}     will be held on {}".format(self.T0, 
		self.T1, ltime)
		msg1 = "{:15}VS.{:>15}     will be held on {}".format(self.T1, 
		self.T0, ltime)
		
		if not self.Finished:
			if t_team == "default" or t_team == self.T0:
				print(msg0)
			else:
				print(msg1)
	
	def display_goals(self, t_team="default"):
		"""Show all goals scored by the selected team."""
		
		g_msg = "Goal {}:    at {:03}'        by {:25}   for {:12}"
		og_msg = "Goal {}:    at {:03}'(OG)    by {:25}   for {:12}"
		pg_msg = "Penalty {}:     by {:25}   for {:12}"
		gn = 1
		pn = 1
		
		for goal in self.Goals:
			if goal.Type != "P":
				if goal.Team == self.T0 and t_team != self.T1:
					if goal.Type == "N":
						print(g_msg.format(gn, goal.When, goal.Player, goal.Team))
						gn += 1
					else:
						print(og_msg.format(gn, goal.When, goal.Player, goal.Team))
						gn += 1
				elif goal.Team == self.T1 and t_team != self.T0:
					if goal.Type == "N":
						print(g_msg.format(gn, goal.When, goal.Player, goal.Team))
						gn += 1
					else:
						print(og_msg.format(gn, goal.When, goal.Player, goal.Team))
						gn += 1
				else:
					continue
			else:
				if goal.Team == self.T0 and t_team != self.T1:
					print(pg_msg.format(pn, goal.Player, goal.Team))
					pn += 1
				elif goal.Team == self.T1 and t_team != self.T0:
					print(pg_msg.format(pn, goal.Player, goal.Team))
					pn += 1
				else:
					continue
	
	def display_full_detail(self):
		"""Show all available information about the match."""
		
		if self.Type == "Group":
			mty = "Group {} Match".format(self.Group)
		else:
			mty = self.Type
		
		fd_msg = mty + "\nStadium:   {}".format(self.Stadium)
		print(fd_msg)
		
		if self.Finished:
			print("\nResult:")
			self.display_result()
			print("\nGoals:")
			self.display_goals()
			print("\nMan of the Match:   {}".format(self.Man_of_the_Match))
		else:
			print("Match Schedule:")
			self.display_schedule()


class Group:
	"""Initialize special Group objects from raw json data."""
	
	def __init__(self, j_group, jm_list, user_tz):
		
		self.ID = j_group.ID
		self.Teams = j_group.Teams
		self.MIDs = j_group.Matches
		
		self.Matches = []
		for mid in self.MIDs:
			for jmatch in jm_list:
				if mid == jmatch.ID:
					self.Matches.append(Match(jmatch, user_tz))
		
	def display_standings(self):
		"""Calculate various stats for each team and display them in 
		standardized format."""
		
		title = "Team            MP   W   D   L   GF   GD   Pts"
		std = "{:<16}{:>2}   {}   {}   {}   {:>2}  {:>3}   {:>3}"
		print(title)
		
		for team in self.Teams:
			mp = 0
			w = 0
			d = 0
			l = 0
			gf = 0
			gd = 0
			pts = 0
			for match in self.Matches:
				if match.Finished:
					if team in match.Teams:
						mp += 1
						if team == match.Winner:
							w += 1
							pts += 3
						elif match.Winner == "Draw":
							d += 1
							pts += 1
						else:
							l += 1
						for goal in match.Goals:
							if goal.Team == team and goal.Type != "P":
								gf += 1
								gd += 1
							elif goal.Team != team and goal.Type != "P":
								gd -= 1
			
			tstd = std.format(team, mp, w, d, l, gf, gd, pts)
			print(tstd)
	
	def display_m_standings(self):
		"""Reuse Match class methods to display match info."""
		
		fin = []
		ufin = []
		
		for match in self.Matches:
			if match.Finished:
				fin.append(match)
			else:
				ufin.append(match)
		
		if fin:
			print("Finished Matches:")
			for fmatch in fin:
				fmatch.display_result()
		
		if ufin:
			print("\nUpcoming Matches:")
			for umatch in ufin:
				umatch.display_schedule()

