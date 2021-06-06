# This was the first draft.

# Inspired by https://www.youtube.com/watch?v=f7LEWxX4AVI

# Small script that clicks through the vaccination portal of Lower Saxony to check for a spontaneous open spot for vaccination.

import time
from datetime import datetime
from selenium import webdriver
from playsound import playsound
import random

WAITING_TIME_PER_TRY = 600

WAITING_TIME_STEP = 0.25
PLZ = '21423'
BIRTHDAY = '01.01.2000'


def main():
    while True:
        check_for_spot(waiting_time=WAITING_TIME_STEP, plz=PLZ, birthday=BIRTHDAY)

        time.sleep(WAITING_TIME_PER_TRY + random.uniform(1, 50))  # Wait till checking again.


def check_for_spot(waiting_time: int, plz: str, birthday: str):

    driver = webdriver.Chrome('chromedriver\chromedriver.exe')  # Path to the chromedriver. Specifying it prevents having to put it into Windows' PATH variable. Driver can be found here: https://sites.google.com/chromium.org/driver/. Requires installed Chrome.
    driver.get('https://www.impfportal-niedersachsen.de/portal/#/appointment/public')

    time.sleep(waiting_time)


    start_smallprint_accept = driver.find_element_by_xpath('//*[@id="mat-checkbox-1"]/label/span[1]')
    start_smallprint_accept.click()

    time.sleep(waiting_time)

    start_next = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]/span[1]')
    start_next.click()

    time.sleep(waiting_time)

    second_next = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]')

    second_next.click()

    time.sleep(waiting_time)

    birthday_enter = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
    # birthday.click()
    birthday_enter.send_keys(birthday)

    time.sleep(waiting_time)

    birthday_next = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]')

    birthday_next.click()

    time.sleep(waiting_time)

    work_related_yes = driver.find_element_by_xpath('//*[@id="mat-radio-2"]')
    work_related_yes.click()

    time.sleep(waiting_time)  # This element takes a bit longer.

    work_related_understood = driver.find_element_by_xpath('//*[@id="mat-dialog-0"]/confirm-dialog/mat-dialog-content/div/button')
    work_related_understood.click()

    time.sleep(waiting_time)

    work_related_next = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]')
    work_related_next.click()

    time.sleep(waiting_time)

    some_text_next = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]')
    some_text_next.click()

    time.sleep(waiting_time)

    location_plz = driver.find_element_by_xpath('//*[@id="mat-input-0"]')
    location_plz.send_keys(plz)

    time.sleep(waiting_time)

    location_plz_search = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[1]/div/div[1]/div[3]/div/button')
    location_plz_search.click()

    time.sleep(1)

    ts_now = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
    driver.get_screenshot_as_file("checks/" + ts_now + ".png")

    time.sleep(waiting_time)

    no_spots = driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[1]/div/div[1]/div[5]/div[2]/div/div/div[2]/div[2]')
    no_spots_text = no_spots.text

    if no_spots_text is None or no_spots_text != "Keine Termine verfügbar":
        playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.
        playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.
        playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.
        playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.
        playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.

    time.sleep(10) # Let the user actually see something!

    driver.quit()


if __name__ == "__main__":
    main()
