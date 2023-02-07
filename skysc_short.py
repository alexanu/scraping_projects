# https://github.com/agespido/SkyScraper/blob/main/src/sky.py



"""
Html: 
<span class="BpkText_bpk-text__ZWIzZ BpkText_bpk-text--caption__NDJhY Price_totalPrice__MTJhN">Gesamt 2.318 €</span>

Selector:
#app-root > div.FlightsDayView_row__NjQyZ > div > div > div > div:nth-child(1) > div.FlightsResults_dayViewItems__ZDFlO > div:nth-child(1) > div > div > a > div > div.BpkTicket_bpk-ticket__paper__ZTQxN.BpkTicket_bpk-ticket__stub__Y2M3M.Ticket_stub__NGYxN.BpkTicket_bpk-ticket__stub--padded__ZTlkM.BpkTicket_bpk-ticket__stub--horizontal__YjRhZ > div > div > span

JS Path: document.querySelector("#app-root > div.FlightsDayView_row__NjQyZ > div > div > div > div:nth-child(1) > div.FlightsResults_dayViewItems__ZDFlO > div:nth-child(1) > div > div > a > div > div.BpkTicket_bpk-ticket__paper__ZTQxN.BpkTicket_bpk-ticket__stub__Y2M3M.Ticket_stub__NGYxN.BpkTicket_bpk-ticket__stub--padded__ZTlkM.BpkTicket_bpk-ticket__stub--horizontal__YjRhZ > div > div > span")

XPath:
//*[@id="app-root"]/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div/a/div/div[2]/div/div/span

Full XPath:
/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div/div/div[1]/div[3]/div[1]/div/div/a/div/div[2]/div/div/span

"""


domain_codes = ['de','nl','uk','ua'] # domain
destination_codes = ['sana'] # destination
departure_dates = ['230404','230405'] # dep_date
return_dates = ['230414','230415'] # ret_date

url = f'https://www.skyscanner.{domain}/transport/fluge  /muc/{destination}/{dep_date}/{ret_date}/?adults=2&adultsv2=2&cabinclass=economy&children=1&childrenv2=7%7c1&duration=1320&inboundaltsenabled=false&infants=1&outboundaltsenabled=false&preferdirects=false&ref=home&rtn=1'
        https://www.skyscanner.de      /transport/flights/muc/sana         /230404/230414        /?adultsv2=2&cabinclass=economy&childrenv2=7%7c3&duration=1320&inboundaltsenabled=false&outboundaltsenabled=false&rtn=1&stops=!oneStop,!twoPlusStops



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller
import warnings
from time import sleep
import random
import os
import ssl
ssl._create_default_https_context = ssl._create_unverified_context





def wait(min = 2, max = 4):
	if max <= min:
		max = min + 1
	sleep(random.uniform(min, max))

def init_driver():
	warnings.filterwarnings("ignore", category=DeprecationWarning) # Ignore deprecation warnings
	# geckodriver_autoinstaller.install()
	options = Options()
	options.headless = True
	cap = DesiredCapabilities().FIREFOX
	cap["marionette"] = True
	driver = webdriver.Firefox(capabilities=cap, options=options)
	return driver

PAYLOAD = '?adultsv2=2&cabinclass=economy&childrenv2=7%7c3&duration=1320&inboundaltsenabled=false&outboundaltsenabled=false&rtn=1&stops=!twoPlusStops'


domain_codes = ['de/transport/fluge',
				'es/transport/fluge', 'nl','uk','ua'] # domain
destination_codes = ['sana'] # destination
departure_dates = ['230404','230405'] # dep_date
return_dates = ['230414','230415'] # ret_date

dep_date = '230404' # Use as a first date to iterate over
ret_date = '230414'
domain = 'de/transport/fluge'

DEPARTURE_AIRPORT = 'muc'
airport_dict = {
	'sana': 'SANDIEGO',
}
destination = list(airport_dict.keys())[0]

url = f'https://www.skyscanner.{domain}/{DEPARTURE_AIRPORT}/{destination}/{dep_date}/{ret_date}/{PAYLOAD}'
driver = init_driver()
driver.get(url)
x_path_price = '/html/body/div[3]/div[4]/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div[1]/div/div[2]/div/div/span'
WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, x_path_price)))
price = driver.find_element(By.XPATH, '//*[@id="dayview-first-result"]/div/div[3]/div/div/div/span').text

driver.quit()

from selenium import webdriver
driver = webdriver.Firefox()
driver.get(url)
price = driver.find_element(By.XPATH, x_path_price).text
