from time import sleep
from functions import get_dose_number, get_dose_preference, get_start_date, get_viable_centers, availability_checker, \
	get_state_id, get_district_id, get_age
import requests
import simplejson

counter = 0
age = get_age()
state_id_choice = get_state_id()
district_id_choice = get_district_id(state_id_choice)
dose_number = get_dose_number()
vaccine = get_dose_preference()
start_date = get_start_date()


def main():
	url = 'https://cowin.gov.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=' + district_id_choice + '&date=' + start_date

	request = requests.get(url)
	json_response = simplejson.loads(request.text)
	centers = json_response['centers']
	viable_centers = get_viable_centers(centers=centers, min_age=age)

	availability_checker(viable_centers=viable_centers, dose_number=dose_number, vaccine=vaccine, min_age=age)


while True:
	main()
	counter = counter + 1
	print('\nThis program has run', counter, 'time(s). Running in 20s ... \t(' + age + '+)',
		  '\n_________________________________________________________________________________________________\n')

	sleep(20)
