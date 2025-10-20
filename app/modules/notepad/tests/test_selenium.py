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
        driver.set_window_size(1712, 931)
        driver.find_element(By.CSS_SELECTOR, ".navbar-collapse").click()
        driver.find_element(By.CSS_SELECTOR, ".nav-link:nth-child(1)").click()
        driver.find_element(By.CSS_SELECTOR, ".row:nth-child(2) > .col-md-6 > .mb-3").click()
        driver.find_element(By.ID, "email").click()
        driver.find_element(By.ID, "email").send_keys("user1@example.com")
        driver.find_element(By.ID, "password").click()
        driver.find_element(By.ID, "password").send_keys("1234")
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.CSS_SELECTOR, ".sidebar-item:nth-child(12) .align-middle:nth-child(2)").click()
        driver.find_element(By.LINK_TEXT, "Create notepad").click()
        driver.find_element(By.CSS_SELECTOR, "form > div:nth-child(2)").click()
        driver.find_element(By.ID, "title").click()
        driver.find_element(By.ID, "title").send_keys("Prue")
        driver.find_element(By.ID, "title").send_keys(Keys.DOWN)
        driver.find_element(By.ID, "title").send_keys("Prueba de selenium")
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").send_keys("Funcionará ahora?")
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.LINK_TEXT, "Edit").click()
        driver.find_element(By.ID, "body").click()
        driver.find_element(By.ID, "body").send_keys("Funcionará ahora?\\nNo se")
        driver.find_element(By.ID, "submit").click()
        driver.find_element(By.CSS_SELECTOR, "button").click()
        driver.find_element(By.LINK_TEXT, "Doe, John").click()
        driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        driver.find_element(By.CSS_SELECTOR, ".text-dark").click()
        driver.find_element(By.CSS_SELECTOR, ".dropdown-item:nth-child(2)").click()

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
