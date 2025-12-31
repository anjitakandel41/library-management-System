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
wait = WebDriverWait(driver, 10)

# -----------------------------
# Open app
# -----------------------------
driver.get("http://127.0.0.1:5000")
driver.maximize_window()

# ================== REGISTER ==================
wait.until(EC.element_to_be_clickable((By.ID, "signUpButton"))).click()

wait.until(EC.visibility_of_element_located((By.NAME, "fName"))).send_keys("Auto")
driver.find_element(By.NAME, "lName").send_keys("Tester")
driver.find_element(By.NAME, "email").send_keys("autotest@example.com")
driver.find_element(By.NAME, "password").send_keys("12345")
driver.find_element(By.NAME, "role").send_keys("student")

# Click REGISTER button (use specific selector)
wait.until(EC.element_to_be_clickable((By.ID, "registerBtn"))).click()

# ================== GO TO LOGIN PAGE ==================
wait.until(EC.element_to_be_clickable((By.ID, "loginButton"))).click()

# ================== LOGIN ==================
email = wait.until(EC.visibility_of_element_located((By.NAME, "email")))
password = driver.find_element(By.NAME, "password")

email.clear()
password.clear()

email.send_keys("autotest@example.com")
password.send_keys("12345")

wait.until(EC.element_to_be_clickable((By.ID, "loginBtn"))).click()

# ================== VERIFY DASHBOARD ==================
wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
print("✅ Login successful. Dashboard loaded.")

# -----------------------------
# Close
# -----------------------------
time.sleep(3)
driver.quit()
