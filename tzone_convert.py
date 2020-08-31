# tzone_convert.py #
# =====================================================================
# DEFINE A TIME ZONE TABLE FOR CALCULATING THE LOCAL MATCH TIME IN
# DIFFERENT AREAS OF THE WORLD.
# 
# TIME ZONES ARE IDENTIFIED BY THEIR ABBREVIATIONS(WIKIPEDIA SOURCE).
# THEIR VALUES ARE THE DEVIATIONS FROM COORDINATED UNIVERSAL TIME(UTC).
# CERTAIN AREAS WILL HAVE AN EXTRA ID FOR DAYLIGHT SAVING TIME
# (e.g. EDT is the daylight saving time version for EST).
# 
# A MAIN FUNCTION IS BUILT FOR TESTING WITH TESTING SAMPLES.
# TEST RUN COMMAND: python3 tzone_convert.py
# 

tz_sheet = {
	"ACDT": 10.5, "ACST": 9.5, "ACT": -5, "ADT": -3, "AEDT": 11, 
	"AEST": 10, "AFT": 4.5, "AKDT": -8, "AKST": -9, "AMST": -3, 
	"ABMT": -4, "AMT": 4, "ART": -3, "AST": -4, "AWST": 8, "AZT": 4, 
	"BDT": 8, "BIOT": 6, "BIT": -12, "BOT": -4, "BRST": -2, "BRT": -3, 
	"BST": 6, "BTT": 6, "CAT": 2, "CCT": 6.5, "CDT": -5, "CEST": 2, 
	"CET": 1, "CIT": 8, "CKT": -10, "COST": -4, "COT": -5, "CST": -6, 
	"CT": 8, "CXT": 7, "EAST": -6, "EAT": 3, "ECT": -5, "EDT": -4, 
	"EEST": 3, "EET": 2, "EGST": 0, "EGT": -1, "EIT": 9, "EST": -5, 
	"FET": 3, "FJT": 12, "FKT": -4, "FNT": -2, "GAMT": -9, "GET": 4, 
	"GFT": -3, "GILT": 12, "GIT": -9, "GMT": 0, "GST": -2, "GYT": -4, 
	"HDT": -9, "HST": -10, "HKT": 8, "HMT": 5, "ICT": 7, "IDT": 3, 
	"IOT": 3, "IRDT": 4.5, "IRKT": 8, "IRST": 3.5, "INST": 5.5, "IST": 1, 
	"ISRT": 2, "JST": 9, "KALT": 2, "KGT": 6, "KOST": 11, "KRAT": 7, 
	"KST": 9, "MDT": -6, "MET": 1, "MEST": 2, "MHT": 12, "MIST": 11, 
	"MIT": -9.5, "MMT": 6.5, "MSK": 3, "MST": 8, "MTST": -7, "MUT": 4, 
	"MVT": 5, "MYT": 8, "NCT": 11, "NDT": -2.5, "NFT": 11, "NPT": 5.75, 
	"NST": -3.5, "NT": -3.5, "NUT": -11, "NZDT": 13, "NZST": 12, 
	"OMST": 6, "ORAT": 5, "PDT": -7, "PET": -5, "PGT": 10, "PHOT": 13, 
	"PHT": 8, "PKT": 5, "PST": -8, "PEST": 8, "PYST": -3, "PYT": -4, 
	"RET": 4, "SAKT": 11, "SAMT": 4, "SAST": 2, "SBT": 11, "SCT": 4, 
	"SDT": -10, "SGT": 8, "SRT": -3, "SST": 8, "TAHT": -10, "THA": 7, 
	"TFT": 5, "TJT": 5, "TKT": 13, "TLT": 9, "TMT": 5, "TRT": 3, 
	"TOT": 13, "TVT": 12, "UTC": 0, "UYST": -2, "UYT": -3, "UZT": 5, 
	"VET": -4, "VLAT": 10, "VOLT": 4, "WAKT": 12, "WAST": 2, "WAT": 1, 
	"WEST": 1, "WET": 0, "WIT": 7, "WST": 8, "YAKT": 9, "YEKT": 5
}


def tz_digest(t_MID, t_ult, t_rlt):
	"""Calculate the match time in user's time zone."""
	
	ti_msg = "{} {:02} @ {:02}:{:02} {}"
	
	# parse the match ID.
	mo = int(t_MID[:2])
	day = int(t_MID[2:4])
	hr = int(t_MID[4:6])
	mi = 0
	
	# calculate the time difference.
	if t_ult.title() == "Local":
		ti_diff = 0
	else:
		ti_diff = tz_sheet[t_ult] - t_rlt
	
	if isinstance(ti_diff, float):
		mi = int((ti_diff - int(ti_diff)) * 60)
		ti_diff = int(ti_diff)
	if mi < 0:
		hr -= 1
		mi = abs(mi)

	hr = hr + ti_diff
	if 0 <= hr < 24:
		pass
	elif hr < 0:
		day -= 1
		hr += 24
	elif hr >= 24:
		day += 1
		hr -= 24
	
	if 1 <= day <= 30:
		pass
	elif day == 0:
		mo = 6
		day = 30
	elif day == 31:
		mo = 7
		day = 1
	
	if mo == 6:
		mo = "June"
	elif mo == 7:
		mo = "July"
	
	ti_msg = ti_msg.format(mo, day, hr, mi, t_ult)
	
	return ti_msg


def tz_setup():
	"""Return a valid user local time zone value."""
	
	while True:
		user_tz = input("\nPlease enter your time zone (e.g. EDT):\n")
		if user_tz.upper() in tz_sheet.keys():
			user_tz = user_tz.upper()
			break
		elif user_tz.title() == "Local":
			user_tz = user_tz.title()
			break
		else:
			print("\nInvalid time zone, please try again.")
			print("Enter 'Local' to use Host's local time.\n")
			continue
	
	print("\n{} is now your time zone.".format(user_tz))
	return user_tz


if __name__ == "__main__":
	
	test_set = [
	("061418", "EST", 3), ("061418", "EDT", 3), ("061418", "NPT", 4), 
	("061521", "CDT", 4), ("061517", "CT", 3), ("061518", "CCT", 4),
	("061518", "Local", 4)
	]
	
	print("\n")
	for mid, ult, rlt in test_set:
		print(tz_digest(mid, ult, rlt))
	print("\n")
