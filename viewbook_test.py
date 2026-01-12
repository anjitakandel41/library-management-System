from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# -----------------------------
# Setup
# -----------------------------
service = Service(r"C:\SeleniumDrivers\geckodriver.exe")
driver = webdriver.Firefox(service=service)
wait = WebDriverWait(driver, 15)

# -----------------------------
# Open LMS
# -----------------------------
driver.get("http://127.0.0.1:5000")
driver.maximize_window()

# ================== OPEN LOGIN FORM ==================
wait.until(EC.element_to_be_clickable((By.ID, "loginButton"))).click()

# ================== LOGIN ==================
email = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

email.clear()
password.clear()

email.send_keys("autotest@example.com")
password.send_keys("12345")

wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

# ================== VERIFY DASHBOARD ==================
wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
print(" Login successful")

# ================== VIEW BOOK TEST ==================
wait.until(EC.element_to_be_clickable((By.ID, "viewBooksBtn"))).click()

# -----------------------------
# VERIFY BOOK LIST
# -----------------------------
books = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "book-item")))

print(" Total books found:", len(books))
print(" View Book automation test PASSED")

# -----------------------------
# Close
# -----------------------------
time.sleep(3)
driver.quit()
