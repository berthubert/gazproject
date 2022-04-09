from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

prefs = {"download.default_directory" : "/home/ahu/git/gazproject/chrome/", 
         "savefile.default_directory" : "/home/ahu/git/gazproject/chrome/",
         "directory_upgrade": True}
chrome_options.add_experimental_option("prefs",prefs)


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/show#")

print(driver.title) # => "Google"

driver.implicitly_wait(0.5)

cookie_button = driver.find_element(By.ID, "close-button")
cookie_button.click()

driver.implicitly_wait(0.5)

login_link = driver.find_element(By.ID, "login-dialog-visible")
login_link.click()

driver.implicitly_wait(0.5)

#
f=open("account.txt","r")
lines=f.readlines()
usernamelogon=lines[0].strip()
passwordlogon=lines[1].strip()
f.close()

print(usernamelogon)
print(passwordlogon)
print("hi")

username = driver.find_element(By.ID, "username")
username.send_keys(usernamelogon)

password = driver.find_element(By.ID, "password")

password.send_keys(passwordlogon)

signin = driver.find_element(By.ID, "kc-login")
signin.click()

driver.implicitly_wait(0.5)
date=date.today().strftime("%d.%m.%Y")
#date="08.04.2022"
# year      https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/export?name=&defaultValue=true& viewType=TABLE&areaType=BZN&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAYTIMERANGE&dateTime.endDateTime='+date+'+00%3A00%7CUTC%7CDAYTIMERANGE&area.values=CTY%7C10YNL----------L!BZN%7C10YNL----------L&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=YEAR&exportType=CSV
driver.get('https://transparency.entsoe.eu/generation/r2/actualGenerationPerProductionType/export?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&datepicker-day-offset-select-dv-date-from_input=D&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAYTIMERANGE&dateTime.endDateTime='+date+'+00%3A00%7CUTC%7CDAYTIMERANGE&area.values=CTY%7C10YNL----------L!BZN%7C10YNL----------L&productionType.values=B01&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')

driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/export?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAY&border.values=CTY%7C10YNL----------L!BZN_BZN%7C10YNL----------L_BZN_BZN%7C10YBE----------2&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')
driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/export?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAY&border.values=CTY%7C10YNL----------L!BZN_BZN%7C10YNL----------L_BZN_BZN%7C10Y1001A1001A82H&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')
driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/export?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAY&border.values=CTY%7C10YNL----------L!BZN_BZN%7C10YNL----------L_BZN_BZN%7C10YDK-1--------W&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')
driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/export?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAY&border.values=CTY%7C10YNL----------L!BZN_BZN%7C10YNL----------L_BZN_BZN%7C10YGB----------A&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')
driver.get('https://transparency.entsoe.eu/transmission-domain/physicalFlow/export?name=&defaultValue=false&viewType=TABLE&areaType=BORDER_BZN&atch=false&dateTime.dateTime='+date+'+00%3A00%7CUTC%7CDAY&border.values=CTY%7C10YNL----------L!BZN_BZN%7C10YNL----------L_BZN_BZN%7C10YNO-2--------T&dateTime.timezone=UTC&dateTime.timezone_input=UTC&dataItem=ALL&timeRange=DEFAULT&exportType=CSV')

