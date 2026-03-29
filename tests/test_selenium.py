import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_user_registration(driver):
    driver.get("http://localhost:5000/register")

    # Fill registration form
    driver.find_element(By.NAME, "email").send_keys("23bcnb31@kristujayanti.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.NAME, "confirm_password").send_keys("password123")

    # Submit
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for success message
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Registration successful")
    )

def test_user_login(driver):
    driver.get("http://localhost:5000/login")

    # Fill login form
    driver.find_element(By.NAME, "voter_id").send_keys("23bcnb31")
    driver.find_element(By.NAME, "password").send_keys("password123")

    # Submit
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for redirect to vote page
    WebDriverWait(driver, 10).until(
        EC.url_contains("/vote")
    )

def test_voting(driver):
    # Assuming user is logged in from previous test
    driver.get("http://localhost:5000/vote")

    # Select first candidate
    candidates = driver.find_elements(By.NAME, "candidate_id")
    if candidates:
        candidates[0].click()

        # Submit vote
        driver.find_element(By.TAG_NAME, "button").click()

        # Wait for success message
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "alert-success"), "Vote recorded successfully")
        )

def test_admin_login(driver):
    driver.get("http://localhost:5000/admin/login")

    # Fill admin login
    driver.find_element(By.NAME, "username").send_keys("admin")
    driver.find_element(By.NAME, "password").send_keys("admin123")

    # Submit
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for redirect to dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("/admin/dashboard")
    )