from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import dateparser
from dateparser import parse
from stopwatch import Stopwatch

#global firstName


def main():
    months = {1: "Jan", 2: "Feb", 3: "Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    global firstName
    global lastName
    global month
    global day
    global year
    global phoneNumber
    global email
    firstName = input("What's your first name? ")
    lastName = input("What's your last name? ")
    while(True):
        date = parse(input("When were you born? (format : MM/DD/YY) "))
        if(date != None):
            break
        else:
            print("Invalid format. Please try again")
    month = str(months[date.month])
    year = str(date.year)
    day = str(date.day)
    phoneNumber = input("What's your phone number? ")
    email = input("What's your email address? ")
    time.sleep(1)
    print("\n--Opening GoHealth site--\n")
    options = Options()
    options.headless = True;
    driver = webdriver.Chrome("/Users/rayanrizvi/Desktop/gohealth/chromedriver", options = options)
    counter = 1
    stopwatch = Stopwatch()
    while True :
        if(counter != 1) :
            print("\n")
        stopwatch.start()
        print("Booking attempt " + str(counter) + " for " + str(firstName) + ". Minutes passed: " + str(int((stopwatch.duration)/60)))
        counter = counter + 1
        #driver.get("https://www.gohealthuc.com/bayarea/san-francisco/lombard")
        driver.get("https://www.gohealthuc.com/bayarea/peninsula/redwood-city")
        try :
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.disclaimer"))
            )
            print("Outcome: Booking failed")
            print("Waiting 30 seconds")
            time.sleep(30)
        except TimeoutException :
            book(driver)
            stopwatch.stop()
            print("Outcome: Booking succeeded");
            break;



def book(driver) :
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.save-spot__button"))
        )

    driver.execute_script("document.querySelector('a.save-spot__button').click()")
    select = Select(WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "edit-reason-id"))
        ))

    #select.select_by_visible_text("COVID-19 Related")
    select.select_by_index(1)
    firstNameObj = driver.find_element_by_id("edit-first-name")
    firstNameObj.send_keys(firstName)
    lastNameObj = driver.find_element_by_id("edit-last-name")
    lastNameObj.send_keys(lastName)
    monthObj = Select(driver.find_element_by_id("edit-dob-month"))
    monthObj.select_by_visible_text(month)
    dayObj = Select(driver.find_element_by_id("edit-dob-day"))
    dayObj.select_by_visible_text(day)
    yearObj = Select(driver.find_element_by_id("edit-dob-year"))
    yearObj.select_by_visible_text(year)
    number = driver.find_element_by_id("edit-phone-number")
    number.send_keys(phoneNumber)
    emailAdd = driver.find_element_by_id("edit-email")
    emailAdd.send_keys(email)
    saveSpot = driver.find_element_by_id("edit-submit")
    saveSpot.click()
        
        
if __name__ == "__main__" :
   main()
