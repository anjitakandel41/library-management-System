from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
import time

# -----------------------------
#  Path to geckodriver
# -----------------------------
service = Service(r"C:\SeleniumDrivers\geckodriver.exe")  # include .exe and use raw string

# -----------------------------
# 2️ Start Firefox browser
# -----------------------------
driver = webdriver.Firefox(service=service)

# -----------------------------
# 3️ Open your Flask app
# -----------------------------
driver.get("http://127.0.0.1:5000")
driver.maximize_window()
time.sleep(1)

# ================== STUDENT REGISTRATION ==================
driver.find_element(By.ID, "signUpButton").click()
time.sleep(1)

driver.find_element(By.NAME, "fName").send_keys("Auto")
driver.find_element(By.NAME, "lName").send_keys("Tester")
driver.find_element(By.NAME, "email").send_keys("autotest@example.com")
driver.find_element(By.NAME, "password").send_keys("12345")

# If role is a text input
driver.find_element(By.NAME, "role").send_keys("student")  

# If role is a dropdown, you should use Select:
# from selenium.webdriver.support.ui import Select
# Select(driver.find_element(By.NAME, "role")).select_by_visible_text("student")

driver.find_element(By.CLASS_NAME, "btn").click()
time.sleep(2)

# ================== STUDENT LOGIN ==================
driver.find_element(By.NAME, "email").send_keys("autotest@example.com")
driver.find_element(By.NAME, "password").send_keys("12345")
driver.find_element(By.CLASS_NAME, "btn").click()
time.sleep(2)

# ================== VERIFY DASHBOARD ==================
if "Library Dashboard" in driver.page_source:
    print("Student dashboard loaded successfully!")
else:
    print("Dashboard not loaded. Check your HTML or Flask app.")

# -----------------------------
# 4️ Close the browser
# -----------------------------
driver.quit()
