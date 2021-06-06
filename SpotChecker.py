import time
from datetime import datetime
from selenium import webdriver
from playsound import playsound


class SpotChecker:
    """ Small script that clicks through the vaccination portal of Lower Saxony to check for a spontaneous open spot for vaccination. """

    def __init__(self):

        self.waiting_time_step = 0.5
        self.website = "https://www.impfportal-niedersachsen.de/portal/#/appointment/public"
        self.birthday = "01.01.2000"
        self.plz = "30159"

        self.driver = webdriver.Chrome('chromedriver\chromedriver.exe')  # Path to the chromedriver. Specifying it prevents having to put it into Windows' PATH variable. Driver can be found here: https://sites.google.com/chromium.org/driver/. Requires installed Chrome.
        self.driver.get(self.website)  # Initialize.

    def check_for_spot(self):
        self._navigate()
        self._take_screenshot()
        self._notify_about_spot()
        self._exit()


    def _navigate(self):
        """ Navigate through the website. """

        helper_xpath_next_button = '/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]'

        navigation_flow = [
            {"description": "start_smallprint_accept", "xpath": '//*[@id="mat-checkbox-1"]/label/span[1]', "do_click": True}
            , {"description": "start_next", "xpath": '/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[2]/div/button[2]/span[1]', "do_click": True}
            , {"description": "second_next", "xpath": helper_xpath_next_button, "do_click": True}
            , {"description": "enter_birthday", "xpath": '//*[@id="mat-input-2"]', "enter_text": self.birthday}
            , {"description": "birthday_next", "xpath": helper_xpath_next_button, "do_click": True}
            , {"description": "work_related_yes", "xpath": '//*[@id="mat-radio-2"]', "do_click": True}
            , {"description": "work_related_understood", "xpath": '//*[@id="mat-dialog-0"]/confirm-dialog/mat-dialog-content/div/button', "do_click": True}
            , {"description": "work_related_next", "xpath": helper_xpath_next_button, "do_click": True}
            , {"description": "some_text_next", "xpath": helper_xpath_next_button, "do_click": True}
            , {"description": "enter_plz", "xpath": '//*[@id="mat-input-0"]', "enter_text": self.plz}
            , {"description": "some_text_next", "xpath": '/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[1]/div/div[1]/div[3]/div/button', "do_click": True}
        ]

        for i in navigation_flow:
            self._do_action(xpath=i.get("xpath"), do_click=i.get("do_click"), enter_text=i.get("enter_text"))

    def _do_action(self, xpath: str = None, do_click: bool = False, enter_text: str = None):
        """ Find element on website and interact with it. """

        element = self.driver.find_element_by_xpath(xpath)

        if do_click is True:
            element.click()

        if enter_text is not None:
            element.send_keys(enter_text)

        time.sleep(self.waiting_time_step)

    def _take_screenshot(self):
        """ Take a screenshot of the website. """

        time.sleep(1)  # Better chance that page is fully loaded.

        ts_now = datetime.now().strftime("%Y-%m-%d %H.%M.%S")
        self.driver.get_screenshot_as_file("checks/" + ts_now + ".png")

    def _notify_about_spot(self):
        """ Notify, if there are appointments available. """

        no_spots = self.driver.find_element_by_xpath('/html/body/my-app/div/div[3]/mat-sidenav-container/mat-sidenav-content/appointment-public-view/div/form/div[1]/div/div[1]/div[5]/div[2]/div/div/div[2]/div[2]')
        no_spots_text = no_spots.text

        if no_spots_text is None or no_spots_text != "Keine Termine verfügbar":
            playsound('alert\curse.mp3')  # Play a sound in case the text above is not present or different.

    def _exit(self):
        time.sleep(10) # Let the user actually see something!
        self.driver.quit()