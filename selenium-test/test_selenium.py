import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def get_date_time():
    return datetime.now().strftime("%Y-%m-%d_%H:%M")


driver = webdriver.Chrome()
driver.maximize_window()

windows_size = driver.get_window_size()
windows_width_size = windows_size.get("width")
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

site_title = driver.title
print("Web title:", site_title)

driver.implicitly_wait(5)
text_box = driver.find_element(by=By.ID, value="my-text-id")
text_box.send_keys("Entro QA")
print(text_box.get_attribute("value"))
password_box = driver.find_element(by=By.NAME, value="my-password")
password_box.send_keys("P@ssw0rd!")
text_area_box = driver.find_element(by=By.NAME, value="my-textarea")
text_area_box.send_keys("This is a test textarea input.")

disable_text_box = driver.find_element(by=By.NAME, value="my-disabled")
if disable_text_box.is_enabled():
    print("Text box is Enabled")
else:
    print("Text box is Disable")

readonly_text_box = driver.find_element(by=By.NAME, value="my-readonly")
before_send_keys_text = readonly_text_box.get_attribute("value")
password_box.send_keys("After Test")
after_send_keys_text = readonly_text_box.get_attribute("value")
if before_send_keys_text != after_send_keys_text:
    print("Text box is not readonly")
else:
    print("Text box is readonly")

dropdown_element = driver.find_element(By.NAME, "my-select")
select = Select(dropdown_element)
select.select_by_visible_text("One")

my_datalist_dropdown_element = driver.find_element(By.NAME, "my-datalist")
my_datalist_dropdown_element.send_keys("Chicago")

file_path = os.path.abspath("images/sagwa-odod-anim.gif")
file_input = driver.find_element(By.NAME, "my-file")

file_input.send_keys(file_path)

driver.find_element(By.ID, "my-check-1").click()
driver.find_element(By.ID, "my-check-2").click()
driver.find_element(By.ID, "my-radio-2").click()

driver.find_element(By.NAME, "my-colors").send_keys("#ff0000")

# Format MM/DD/YYYY
date_format = driver.find_element(By.NAME, "my-date").send_keys("02/14/2026" + Keys.TAB)

slider_element = driver.find_element(By.NAME, "my-range")
slide_size = slider_element.size["width"]
print(slide_size)

max_value = float(slider_element.get_attribute("max") or 100)
min_value = float(slider_element.get_attribute("min") or 0)
print("max_value slider", max_value)
current_value = float(
    slider_element.get_attribute("value")
    or slider_element.get_attribute("aria-valuenow")
    or min_value
)

# Get the physical width of the element in pixels
slider_width = slider_element.size["width"]

# Calculate the total range and the proportion for the target value
value_range = max_value - min_value
# if value_range == 0:
#     return  # Avoid division by zero

# Calculate the target position as a proportion of the width
# This formula needs adjustment based on the specific slider's implementation
# A common approach is a simple ratio:
target_proportion = (10 - min_value) / value_range

# This is an alternative calculation of the offset for *relative* movement
# A positive offset moves right, a negative moves left
pixel_offset = (10 - current_value) / (max_value - min_value) * slider_width
# The snippet from uses a slightly different, site-specific formula for offset

actions = ActionChains(driver)
actions.click_and_hold(slider_element).move_by_offset(
    pixel_offset, 0
).release().perform()

date_now = get_date_time()
before_path = f"./images/before_submitting_{date_now}.png"
after_path = f"./images/after_submitting_{date_now}.png"
driver.save_screenshot(before_path)

submit_button = driver.find_element(By.CSS_SELECTOR, "button")
submit_button.click()
driver.save_screenshot(after_path)

time.sleep(5)
driver.quit()
