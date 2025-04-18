# ___________________________________
# | Buckshot Roulette: Text Edition |
# |---------------------------------|
# |Based on a game by: Mike Klubnika|
# |    Rewritten by: PI0NEERING     |
# ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
# Does it work? Yes.
# Does it work well? (¬_¬")
# Did you summon a demon to help you write this? WHO TOLD YOU ABOUT THA-I mean no no, definitely not.

# ===Modules===
import sys, time, os, random, math, stopwatch


# ===Functions===
# Credits
def showCredits():
	typewriter("Based on 'Buckshot Roulette' by Mike Klubnika\n")
	typewriter("Rewritten in python by PI0NEERING\n")
	typewriter("Motivation by forces beyond human comprehension\n")
	typewriter("Played by YOU!\n")
	input("Press ENTER to close...")
	quit()
# ---Wins---
# No endless win
def noEndlessWin(cashTotal = 0):
	clear()
	if cashTotal == 0:
		cashTotal = 70000 - math.copysign(1, stat_deathAmt) * (stat_deathAmt + 1) * 2 * 1000 - stat_beerDrank * 330 * 1.5 - stat_cigSmoked * 220 # Huge thank you to Airis on the ARG Wiki team for giving me the formulas for win calculation.
	typewriter("A machine brings down a briefcase from the ceiling...")
	input("Press Enter to open briefcase.")
	typewriter("You open the briefcase. Inside are stacks of money, there is too much to count.")
	print(f"""STATS:
Shots fired:.......{stat_shotsFired}
Shells ejected.....{stat_shellsEjected}
Doors kicked.......{stat_doorsKicked}
Cigarettes smoked..{stat_cigSmoked}
mL of beer drank...{stat_beerDrank*330}
Total cash: {cashTotal}""")
	input("Press Enter to exit.")
	showCredits()
# Endless mode win
def endlessWin(): # Huge thank you to Airis on the ARG Wiki team for giving me the formulas for win calculation.
	global lastCash
	global currentRound
	
	if lastCash is None:
		if 0 <= int(stat_time.elapsed) <= 1049.85:
			endCash = 70000 - (40000 / 600) * int(stat_time.elapsed)
		elif int(stat_time.elapsed) > 1049.85:
			endCash = 10
		else:
			print("Money no make sense!")
	else:
		endCash = lastCash * 2
	if lastCash is None: typewriter(f"Your total money is {endCash}.")
	else: typewriter(f"You went from {lastCash} to {endCash}!")
	typewriter("Double or Nothing?", False, 0.7)
	selection = input("Y/N >>>")
	if selection.lower() == "y":
		currentRound = 1
		lastCash = endCash
	elif selection.lower() == "n":
		noEndlessWin(endCash)
	else:
		print("Invalid input!")
		endlessWin()
# Pre-turn checks
def preTurnCheck():
	global currentRound
	global stat_deathAmt
	global shotgunSawed
	global continue_point
	
	shotgunSawed = False
	print(f"PHealth {player_health_bar}\n"
	      f"DHealth {dealer_health_bar}\n"
	      f"Seq {sequenceArray}\n")
	if len(sequenceArray) == 0:
		if currentRound == 3 or endlessMode:
			genShells()
		else:
			genShells(True)
		playerTurn()
	if player_health_bar <= 0:
		stat_time.stop()
		clear()
		time.sleep(3)
		typewriter("YOU DIED", True, 0.5)
		stat_deathAmt += 1
		continue_point = "start_no_pills"
	elif dealer_health_bar <= 0:
		clear()
		stat_time.stop()
		typewriter("Blood splatters cover your vision. Time seems to slow as you see the dealer sent flying backward into the darkness.\n")
		if currentRound < 3:
			currentRound += 1
			typewriter("...", True)
			typewriter("\n\nHe gets back up.", True)
			genHealth()
			showHealth()
			time.sleep(1.5)
			if currentRound == 2 and not endlessMode: genItems(2)
			elif currentRound == 3 or endlessMode: genItems(4)
			showItems()
			time.sleep(3)
			genShells()
			time.sleep(1.5)
			stat_time.start()
			playerTurn()
		elif not endlessMode:
			noEndlessWin()
		elif endlessMode:
			endlessWin()
# Generate shells
def genShells(dealerSaysAmt=False, dontShuffleASCIIShells=False):
	global sequenceArray
	
	total_shells = random.randint(2, 8)
	amount_live = max(1, total_shells // 2)
	amount_blank = total_shells - amount_live
	sequenceArray = []
	shotASCIIArray = []
	for i in range(amount_live):
		sequenceArray.append("live")
	for i in range(amount_blank):
		sequenceArray.append("blank")
	for i in sequenceArray:
		if i == "live":
			shotASCIIArray.append(""" __
|##|
|##|
|##|
****""")
		if i == "blank":
			shotASCIIArray.append(""" __
|  |
|  |
|  |
****""")
	random.shuffle(sequenceArray)
	if not dontShuffleASCIIShells:
		# Shuffle ASCII shells
		random.shuffle(shotASCIIArray)
	for i in shotASCIIArray:
		print(i)
	if dealerSaysAmt:
		print("--DEALER:--")
		typewriter(str(amount_live)+" live "+str(amount_blank)+" blank.", True)
# Typewriter effect
def typewriter(text, pauseAfterText=False, typeSpeed=0.1):
	if not fastText:
		for character in text:
			sys.stdout.write(character)
			sys.stdout.flush()
			time.sleep(typeSpeed)
		if pauseAfterText:
			time.sleep(2)
	else:
		print(text)
# Clear screen.
def clear():
	if os.name == 'nt':
		_ = os.system('cls')
	else:
		_ = os.system('clear')
#Generate health
def genHealth(amt=None):
	global startingHealth
	global dealer_health_bar
	global player_health_bar
	
	if not amt:
		startingHealth = random.randint(2, 5)
	else:
		startingHealth = amt
	dealer_health_bar = startingHealth
	player_health_bar = startingHealth
# Show health screen
def showHealth():
	clear()
	print("__________________________________")
	print(f"| DEALER          |        {player_name.ljust(6)}|")
	print("|--------------------------------|")
	print(f"|{dealer_health_bar}                              {player_health_bar}|")
	print("|                                |")
	print("‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
# Generate items
def genItems(amt, keepOldInv=False):
	global playerInv
	global dealerInv
	global dealerExplains
	if keepOldInv:
		oldDealerInv = dealerInv
		oldPlayerInv = playerInv
	
	dealerInv = []
	playerInv = []
	if dealerExplains:
		dealerExplains = False
		print("--DEALER:--")
		typewriter("LETS MAKE THIS MORE INTERESTING...\n", True)
		typewriter("2 ITEMS EACH.\n", True)
		typewriter("MORE ITEMS EACH LOAD.\n", True)
	for i in range(amt): dealerInv.append(random.randint(1, 5))
	for i in range(amt): playerInv.append(random.randint(1, 5))
	if keepOldInv:
		playerInv.append(oldPlayerInv)
		dealerInv.append(oldDealerInv)
#	Items:
#	1=Handsaw
#	2=Magnifying Glass
#	3=Handcuffs
#	4=Beer
#	5=Cigs
# Show items
def showItems():
	global playerHandsawAmt
	global playerMagniAmt
	global playerHandcuffAmt
	global playerBeerAmt
	global playerCigAmt
	
	playerHandsawAmt = 0
	playerMagniAmt = 0
	playerHandcuffAmt = 0
	playerBeerAmt = 0
	playerCigAmt = 0
	
	for i in playerInv:
		if str(i) == "1":
			playerHandsawAmt += 1
		elif str(i) == "2":
			playerMagniAmt += 1
		elif str(i) == "3":
			playerHandcuffAmt += 1
		elif str(i) == "4":
			playerBeerAmt += 1
		elif str(i) == "5":
			playerCigAmt += 1
	print(f"""1. Handsaw(s): {playerHandsawAmt}
2. Magnifying Glass(es): {playerMagniAmt}
3. Handcuff(s): {playerHandcuffAmt}
4. Beer(s): {playerBeerAmt}
5. Cig(s): {playerCigAmt}""")
# Players turn
def playerTurn():
	# STATS
	global stat_shotsFired
	global stat_shellsEjected
	global stat_doorsKicked
	global stat_cigSmoked
	global stat_beerDrank

	global dealer_health_bar
	global player_health_bar
	global playerHandcuffed
	global dealerHandcuffed
	global shotgunSawed
	
	global playerHandcuffAmt
	global playerMagniAmt
	global playerHandsawAmt
	global playerBeerAmt
	global playerCigAmt
	
	preTurnCheck()
	if player_health_bar <= 0:
		clear()
		if playerHandcuffed:
			typewriter("You are handcuffed, this turn is skipped.")
			playerHandcuffed = False
			dealerTurn()
		typewriter("It is your turn.\nOptions:\n")
		print("1. Check health.")
		print("2. Pickup shotgun.")
		if currentRound > 1 and len(playerInv) > 0 or endlessMode and len(playerInv) > 0:
			print("3. Use items.")
		selection = input(">>> ")
		if selection == "1": # Show health bars
			showHealth()
			input("Press ENTER to continue.\n")
			playerTurn()
		elif selection == "2":
			clear()
			typewriter("You pick up the shotgun.\n")
			print(''' ,______________________________________
|_________________,----------._ [____]  ""-,__  __....-----=====
               (_(||||||||||||)___________/   ""                |
                  `----------' #$$$$$$[ ))"-,                   |
                                       ""    `,  _,--....___    |
                                               `/           """''')
			typewriter("What do you do?\nOptions:\n")
			print("1. Shoot yourself.")
			print("2. Shoot dealer.")
			selection = input(">>> ")
			if selection == "1":
				if sequenceArray[0] == "live":
					if not shotgunSawed: player_health_bar -= 1
					else: player_health_bar -= 2
					sequenceArray.pop(0)
					typewriter("You aim the shotgun at yourself...\n\n")
					time.sleep(3)
					typewriter("*BOOM*", True)
					stat_shotsFired += 1
					stat_shellsEjected += 1
					dealerTurn()
				elif sequenceArray[0] == "blank":
					sequenceArray.pop(0)
					typewriter("You aim the shotgun at yourself...\n\n")
					time.sleep(3)
					typewriter("*click*", True)
					stat_shellsEjected += 1
					playerTurn()
			elif selection == "2":
				if sequenceArray[0] == "live":
					if not shotgunSawed: dealer_health_bar -= 1
					else:
						dealer_health_bar -= 2
						shotgunSawed = False
					sequenceArray.pop(0)
					typewriter("You aim the shotgun at the dealer...\n\n")
					time.sleep(3)
					typewriter("*BOOM*", True) # "Hey, it's not my fault, book the kid with the keyboard!" - The POSTAL Dude (Postal 2)
					stat_shotsFired += 1
					stat_shellsEjected += 1
					dealerTurn()
				
				elif sequenceArray[0] == "blank":
					sequenceArray.pop(0)
					typewriter("You aim the shotgun at the dealer...\n\n")
					time.sleep(3)
					typewriter("*click*", True)
					stat_shellsEjected += 1
					dealerTurn()
			else:
				print("Invalid selection.")
				playerTurn()
		elif selection == "3" and currentRound > 1 and len(playerInv) > 0 or selection == "3" and endlessMode and len(playerInv) > 0:
			print("You have the following item(s):")
			showItems()
			selection = input("What item do you want to use?\n>>> ")
			if selection == "1":
				if playerHandsawAmt >= 1 and not shotgunSawed:
					playerInv.remove(1)
					playerHandsawAmt -= 1
					shotgunSawed = True
				else:
					typewriter("This item is not available right now.", True)
			elif selection == "2":
				if playerMagniAmt >= 1:
					playerInv.remove(2)
					playerMagniAmt -= 1
					typewriter("...\n\n", True)
					typewriter(sequenceArray[0], True)
				else:
					typewriter("This item is not available right now.", True)
			elif selection == "3":
				if playerHandcuffAmt >= 1:
					playerInv.remove(3)
					playerHandcuffAmt -= 1
					dealerHandcuffed = True
				else:
					typewriter("This item is not available right now.", True)
			elif selection == "4":
				if playerBeerAmt >= 1:
					playerInv.remove(4)
					playerBeerAmt -= 1
					stat_beerDrank += 1
					stat_shellsEjected +=1
					typewriter("You rack the shotgun...\n\n", True)
					typewriter(sequenceArray.pop(0), True)
				else:
					typewriter("This item is not available right now.", True)
			elif selection == "5":
				if playerCigAmt >= 1:
					playerInv.remove(5)
					playerCigAmt -= 1
					player_health_bar += 1
					stat_cigSmoked += 1
				else:
					typewriter("This item is not available right now.", True)
		else:
			typewriter("Invalid selection.", True)
			playerTurn()
# Dealer turn
def dealerTurn():
	global dealerAction
	global dealer_health_bar
	global player_health_bar
	global knownShell, playerHandcuffed, shotgunSawed, dealerHandcuffed
	
	preTurnCheck()
	amtBlank = 0
	amtLive = 0
	for i in sequenceArray:
		if i == "blank": amtBlank += 1
		if i == "live": amtLive += 1
	if dealerHandcuffed:
		dealerHandcuffed = False
		typewriter("The dealer is handcuffed, this turn is skipped.", True)
	if player_health_bar <= 0:
		knownShell = ""
		clear()
		typewriter("It is the dealer's turn.")
		
		if currentRound > 1 or endlessMode:
			for i in dealerInv:
				if i == 5 and dealer_health_bar < startingHealth:
					typewriter("\nThe dealer picks up a cigarette pack, flips open a lighter, and smokes a cigarette.", True)
					dealer_health_bar += 1
					dealerInv.remove(i)
					showHealth()
					break
				elif i == 2 and len(sequenceArray) > 1:
					typewriter("\nThe dealer smashes a magnifying glass and checks the current round.", True)
					if sequenceArray[0] == "live":
						knownShell = "live"
					else:
						knownShell = "blank"
					dealerInv.remove(i)
					break
				elif i == 4 and knownShell == "blank" and len(sequenceArray) > 1:
					typewriter("\nThe dealer chugs a beer can then racks the shotgun.\n\nThe round is: " + sequenceArray.pop(0), True)
					dealerInv.remove(i)
					break
				elif i == 3 and not playerHandcuffed and len(sequenceArray) > 1:
					typewriter("\nThe dealer handcuffs you.", True)
					playerHandcuffed = True
					dealerInv.remove(i)
					break
				elif i == 1 and not shotgunSawed and knownShell == "live":
					typewriter("\nThe dealer flips open a handsaw and cuts off the shotgun’s tip.", True)
					shotgunSawed = True
					dealerInv.remove(i)
					break
		if amtLive >= amtBlank: dealerAction = 1
		else: dealerAction = 2
		if dealerAction == 1:
			if sequenceArray[0] == "live":
				typewriter("\nThe dealer points the shotgun at you...\n\n")
				time.sleep(3)
				typewriter("*BOOM*", True)
				sequenceArray.pop(0)
				if shotgunSawed:
					player_health_bar -= 2
				elif not shotgunSawed:
					player_health_bar -= 1
				playerTurn()
			elif sequenceArray[0] == "blank":
				typewriter("\nThe dealer points the shotgun at you...\n\n")
				time.sleep(3)
				typewriter("*click*", True)
				sequenceArray.pop(0)
				playerTurn()
		elif dealerAction == 2:
			if sequenceArray[0] == "live":
				typewriter("\nThe dealer points the shotgun at himself...\n\n")
				time.sleep(3)
				typewriter("*BOOM*", True)
				sequenceArray.pop(0)
				if shotgunSawed:
					dealer_health_bar -= 2
				elif not shotgunSawed:
					dealer_health_bar -= 1
				playerTurn()
			elif sequenceArray[0] == "blank":
				typewriter("\nThe dealer points the shotgun at himself...\n\n")
				time.sleep(3)
				typewriter("*click*", True)
				sequenceArray.pop(0)
				dealerTurn()
# ===Variables===
# ---GAME SETUP---
endlessMode = False
currentRound = 1
player_name = ""
player_health_bar = 0
dealer_health_bar = 0
playerHandcuffed = False
dealerHandcuffed = False
dealerExplains = True
dealerInv = []
playerInv = []
lastCash = None
# ---STAT VARS---
stat_shotsFired = 0
stat_shellsEjected = 0
stat_doorsKicked = 0
stat_cigSmoked = 0
stat_beerDrank = 0
stat_deathAmt = 0
stat_time = stopwatch.Stopwatch()
# ---DEV OPTIONS---
continue_point = "menu"
devTest = False
fastText = False

# ===Main program===
# continue_point helps me start specific parts of the sequence, so I can repeat several interactions.
while continue_point:
	if devTest: # For testing functions and other interactions, NOTE: REMOVE IN RELEASE VERSION
		showCredits()
	if continue_point == "menu": # This idea was made originally by Mikk, you can find him on https://mikeklubnika.com/games/buckshot_roulette. I DO NOT OWN ANY CHARACTERS NOR THE IDEA, THIS IS A FANGAME!
		print("""___________________________________
| Buckshot Roulette: Text Edition |
|---------------------------------|
|Based on a game by: Mike Klubnika|
|    Rewritten by: PI0NEERING     |
‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾""")
		input("Press ENTER to continue.\n")
		continue_point = "start"
	elif continue_point == "start":
		# Intro sequence
		clear()
		typewriter("You wake up in a dirty bathroom, club music blares in the background. In front of you is a door and a pill bottle.\nOptions:\n", False, 0.05)
		print("1. Pickup pill jar.")
		print("2. Kick down door")
		selection = input(">>> ")
		if selection == "1":
			continue_point = "pill_jar"
		elif selection == "2":
			stat_doorsKicked += 1
			continue_point = "walkway"
		else:
			typewriter("Invalid choice. Try again.", True)
			continue_point = "start"
	elif continue_point == "pill_jar":
		# DoN mode activation
		clear()
		typewriter("You pick up the pill jar.\n")
		print("        _______")
		print("       |       |")
		print("       |       |")
		print("      /         \\")
		print("     | Quaaludes |")
		print("     |tabletoplam|")
		print("     |tablets,SUS|")
		print("     |    1 MG   |")
		print("      \\_________/")
		typewriter("\nDo you eat it?")
		print(" (Y/N)")
		pillSelection = input(">>> ").lower()
		if pillSelection == "y":
			# "Oops. Zat vas not medizin!" - TF2 Medic
			typewriter("Consciousness begins to elude you...", True)
			endlessMode = True
			pillSelection = None
			continue_point = "start_no_pills"
		elif pillSelection == "n":
			typewriter("You decide against consuming the pills.", True) # *Adjusts tie angrily* "We'll... see about... that."- The G-Man
			selection = None
			continue_point = "start"
		else:
			typewriter("Invalid choice. Try again.", True)
			continue_point = "pill_jar"
	elif continue_point == "start_no_pills":
		# Intro without pills for death and when you take pills
		clear()
		typewriter("You wake up in a dirty bathroom, club music blares in the background. In front of you is a door.\n")
		input("Press ENTER to kick down door.")
		stat_doorsKicked += 1
		continue_point = "walkway"
	elif continue_point == "walkway":
		clear()
		if not endlessMode and not stat_deathAmt >= 1:
			typewriter("You exit the bathroom.\nYou appear to be on a catwalk of some kind, overlooking a large open area reminding you of a warehouse.\nA man smoking a cigarette is leaning over the railing, looking at the flashing lights below.\nBehind the man is a door, leading to your fate.\nOptions:\n", False, 0.05)
			print("1. Go back to the bathroom")
			print("2. Kick down door")
			selection = input(">>> ")
			if selection == "1":
				continue_point = "start"
			elif selection == "2":
				continue_point = "waiver"
			else:
				typewriter("Invalid choice. Try again.", True)
		elif endlessMode or stat_deathAmt >= 1:
			typewriter("You exit the bathroom.\nYou appear to be on a catwalk of some kind, overlooking a large open area reminding you of a warehouse.\nAt the end of the catwalk is a door, leading to your fate.\nOptions:\n", False, 0.05)
			input("Press ENTER to kick down door.")
			stat_doorsKicked += 1
			continue_point = "waiver"
	elif continue_point == "waiver":
		if not len(player_name) > 0:
			clear()
			typewriter("You kick down the door and walk into a small room with a large green table in the center.\nOn the table is a general release of liability form.\n", False, 0.05)
			print("--DEALER:--")
			typewriter("PLEASE SIGN THE WAIVER.\n", True)
			player_name = input("NAME (MAX 5 CHARS)>>> ")
			if len(player_name) > 5 or len(player_name) == 0:
				typewriter("\nToo many/few letters in name, try again.", True)
				player_name = ""
				continue_point = "waiver"
			else:
				continue_point = "main"
		else:
			print("--DEALER:--")
			typewriter("WELCOME BACK.\n", True)
			stat_deathAmt += 1
			continue_point = "main"
	elif continue_point == "main":
		clear()
		stat_time.start()
		if currentRound == 1 and not endlessMode:
			genHealth(2)
			showHealth()
		elif endlessMode:
			genItems(random.randint(1, 4))
			showItems()
			time.sleep(1.5)
			genHealth()
			showHealth()
		time.sleep(1.5)
		if currentRound == 3 or endlessMode:
			genShells()
			time.sleep(2)
		else:
			genShells(True)
			if fastText:
				time.sleep(2)
		clear()
		if currentRound == 1 and not endlessMode:
			print("--DEALER:--")
			typewriter("THEY ENTER THE CHAMBER IN AN UNKNOWN SEQUENCE.", True)
		typewriter("\n\nThe dealer loads the shells into the shotgun.",True , 0.05)
		clear()
		playerTurn()
		input("STOP")
#typewriter("LETS MAKE THIS MORE INTERESTING...")
