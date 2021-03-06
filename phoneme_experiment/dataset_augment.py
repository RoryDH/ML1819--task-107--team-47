# takes a file which has been generated by link below via stdin:
# 	http://www.speech.cs.cmu.edu/tools/lextool.html

import sys, json, unidecode

letter_count = 0
alphabet = {}
output = {}

for line in sys.stdin:
	line = line.strip()
	x = line.split("\t")
	sounds = []
	if len(x) > 1:
		phonemes = x[1].split(" ")
		for sound in phonemes:
			if sound not in alphabet:
				alphabet[sound] = letter_count
				letter_count += 1
			#sounds.append(sound)
			sounds.append(alphabet[sound])
		output[x[0].lower()] = sounds

data = None
with open("../users.json", "r") as read_file:
    data = json.load(read_file)

users = {}
for screen_name, user in data.items():
	# if no phonemes generated for that user
	un_name = unidecode.unidecode(user["twitter_profile"]["name"]).lower()
	if len(un_name.split()) == 0:
		continue
	un_first_name = un_name.split()[0]
	un_screen_name = unidecode.unidecode(screen_name).lower()
	if un_name not in output or un_screen_name not in output:
		continue

	if un_first_name not in output:
		continue
	userdata = {}
	userdata["screen_name"] = screen_name
	userdata["screen_name_phonemes"] = output[un_screen_name]
	userdata["name_phonemes"] = output[un_name]
	userdata["first_name_phonemes"] = output[un_first_name]

	to_copy = ["name", "description", "profile_background_color", "profile_link_color", "profile_sidebar_border_color", "profile_sidebar_fill_color", "profile_text_color"]

	userdata["gender"] = user["gender"]
	for i in to_copy:
		userdata[i] = user["twitter_profile"][i]

	users[screen_name] = userdata

with open('users.min.json', 'w') as outfile:
    json.dump(users, outfile)


