from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from core.environment.host import get_host_for_selenium_testing
from core.selenium.common import initialize_driver, close_driver


def test_notepad_index():

    driver = initialize_driver()

    try:
        host = get_host_for_selenium_testing()

        # Open the index page
        driver.get(f'{host}/notepad')
        driver.set_window_size(979, 1063)
        driver.find_element(By.LINK_TEXT, "Login").click()
        driver.find_element(By.ID, "email").click()
        driver.find_element(By.ID, "email").send_keys("user1@example.com")
        driver.find_element(By.ID, "password").click()
        driver.find_element(By.ID, "password").send_keys("1234")
        driver.find_element(By.ID, "submit").click()
        driver.get("http://localhost:5000/notepad/create")
        driver.find_element(By.ID, "title").click()
        driver.find_element(By.ID, "title").send_keys("example")
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").send_keys("example")
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.LINK_TEXT, "Edit").click()
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").send_keys("example2")
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.CSS_SELECTOR, "button").click()
        driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        driver.find_element(By.LINK_TEXT, "Log out").click()
        driver.close()
  

        # Wait a little while to make sure the page has loaded completely
        time.sleep(4)

        try:

            pass

        except NoSuchElementException:
            raise AssertionError('Test failed!')

    finally:

        # Close the browser
        close_driver(driver)


# Call the test function
test_notepad_index()