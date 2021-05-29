from datetime import timedelta, datetime
import pygame
from bcolors import bcolors
import requests
import simplejson


def get_age():
	print("For the age group of 18+, press 1, else for 45+, press 2. (Default 1)")
	age_group = input()
	if age_group == '2':
		age = '45'
	else:
		age = '18'
	print('Searching for', age + '+')
	return age


# gets dose number preference if any, defaults to 1.
def get_dose_number():
	print("Which dose number are you looking for? 1 or 2? Default 1")
	dose_number = input()
	if dose_number == '2':
		pass
	else:
		dose_number = '1'

	print('Preference: Dose Number', dose_number)
	return dose_number


# You can choose the vaccine you want to choose if want.
def get_dose_preference():
	print('Do you have a vaccine choice? 0 for No, 1 for Covishield, 2 for Covaxin, 3 for Sputnik V (Default 0)')
	preference = input()

	if preference == '1':
		vaccine = 'COVISHIELD'
	elif preference == '2':
		vaccine = 'COVAXIN'
	elif preference == '3':
		vaccine = 'SPUTNIK V'
	else:
		vaccine = ['COVISHIELD', 'COVAXIN', 'SPUTNIK V']

	print(f'Looking for vaccine(s): {vaccine}')
	return vaccine


# Gets start date preference from user. API returns 7 days including start date.
def get_start_date():
	print(
		"Enter the starting date FROM TODAY you want to search for, the script will start looking for slots from that day for 7 days.\n0 for today, 1 for tomorrow and so on (Max 10) (Default 0)")
	start_day = input()
	try:
		start_day = int(start_day) if start_day and int(start_day) in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10] else 0

	except ValueError:
		start_day = 0
	print(f'Searching for a week starting from {start_day} day(s) from today.')
	start_date = (datetime.now() + timedelta(days=start_day)).strftime('%d-%m-%Y')
	return start_date


# plays sound
def play_sound():
	pygame.mixer.init()
	pygame.mixer.music.load("audio.mp3")
	pygame.mixer.music.play()


# scans centers to get only age appropriate sessions and returns list of centers of those sessions.
def get_viable_centers(centers, min_age):
	viable_centers = []
	successful_session_found = False
	for center in centers:
		# print(f'Name: {center.get("name")}\t\t\t\t\t\t\t', end='\t')
		for session in center["sessions"]:
			# print(session['min_age_limit'])
			if str(session['min_age_limit']) == min_age:
				successful_session_found = True
		if successful_session_found:
			viable_centers.append(center)

	return viable_centers


# Color selection for command line.
def color_selector(vaccine):
	if vaccine == 'COVISHIELD':
		print(bcolors.FAIL, end='')

	elif vaccine == 'COVAXIN':
		print(bcolors.OKGREEN, end='')
	else:
		print(bcolors.OKBLUE, end='')


# Checks for available slots for dose number and vaccine type.
# We check fo min age limit again because some centers have multiple sessions of different age categories
def availability_checker(viable_centers, dose_number, vaccine, min_age):
	result_counter = 0
	for center in viable_centers:
		# print(center)
		for session in center.get('sessions'):
			if str(session['min_age_limit']) == min_age:
				if session["available_capacity_dose" + dose_number] > 0 and session["vaccine"] in vaccine:
					color_selector(session['vaccine'])
					print(
						f"Found: {session['date']} at {center['pincode']} {center['district_name']} {center['name']}, Availability: {session['available_capacity_dose' + dose_number]}, with vaccine {session['vaccine']}, for dose {dose_number}")
					play_sound()
					print(bcolors.ENDC)
					result_counter = result_counter + 1

	print(f'{bcolors.UNDERLINE}{bcolors.WARNING}{result_counter} result(s) found{bcolors.ENDC}')


# choose which state to choose district
def get_state_id():
	headers = {
		'authority': 'cdn-api.co-vin.in',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
		'sec-ch-ua-mobile': '?0',
		'dnt': '1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.19 Safari/537.36',
		'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'sec-fetch-site': 'none',
		'sec-fetch-mode': 'navigate',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'document',
		'accept-language': 'en-US,en;q=0.9',
	}
	response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/states', headers=headers)

	json_response_state = simplejson.loads(response.text)
	states = json_response_state['states']
	for state in states:
		print(f'State ID: {state.get("state_id")}\t\t\t\t\t\t\t\t\t\t\t\tState Name: {state["state_name"]}')
		print('________________________________________________________________________________________')

	print(
		'Enter the state ID corresponding to the state of the district you want to search for. Default 16 (Karnataka)')
	state_id_choice = input()
	try:
		state_id_choice = int(state_id_choice) if state_id_choice and int(state_id_choice) in range(1, 38) else 16

	except ValueError:
		state_id_choice = 16
	current_state = ''
	for state in states:
		if str(state['state_id']) == str(state_id_choice):
			current_state = state['state_name']
	print(f'Your state: {current_state} with ID {state_id_choice}\n\n')
	return str(state_id_choice)


# from state choice district can be chosen
def get_district_id(state_id_choice):
	headers = {
		'authority': 'cdn-api.co-vin.in',
		'pragma': 'no-cache',
		'cache-control': 'no-cache',
		'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
		'sec-ch-ua-mobile': '?0',
		'dnt': '1',
		'upgrade-insecure-requests': '1',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.19 Safari/537.36',
		'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
		'sec-fetch-site': 'same-origin',
		'sec-fetch-mode': 'no-cors',
		'sec-fetch-user': '?1',
		'sec-fetch-dest': 'image',
		'accept-language': 'en-US,en;q=0.9',
		'referer': 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/16',
	}

	response = requests.get('https://cdn-api.co-vin.in/api/v2/admin/location/districts/' + state_id_choice,
							headers=headers)
	json_response_district = simplejson.loads(response.text)
	districts = json_response_district['districts']
	for district in districts:
		print(f'District ID: {district.get("district_id")}\t\t\t\t\t\t\t\tDistrict Name: {district["district_name"]}')
		print('________________________________________________________________________________________')

	print(
		'Enter the district ID corresponding district you want to search for. Default 294 (BBMP)')
	district_id_choice = input()
	try:
		district_id_choice = int(district_id_choice) if district_id_choice and int(district_id_choice) in range(1,
																												900) else 294

	except ValueError:
		district_id_choice = 294
	current_district = ''
	for district in districts:
		if str(district['district_id']) == str(district_id_choice):
			current_district = district['district_name']
	print(f'Your district: {current_district} with ID {district_id_choice}\n\n')

	return str(district_id_choice)
