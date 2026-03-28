import os
import time
from datetime import datetime

import pytest
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class TestWebForm:
    @pytest.fixture(autouse=True)
    def setup(self):

        options = webdriver.ChromeOptions()
        if os.environ.get("CI") == "true":
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # Set a default window size for headless mode
            options.add_argument("--window-size=1920,1080")
        """Set up the Chrome driver before each test."""
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 10)
        yield
        self.driver.quit()

    def get_date_time(self):
        """Helper to get current date and time formatted as a string."""
        return datetime.now().strftime("%Y-%m-%d_%H:%M")

    def test_submit_web_form(self):
        """Test the Selenium web form with various input types."""
        driver = self.driver
        driver.get("https://www.selenium.dev/selenium/web/web-form.html")

        # Verify page title
        assert "Web form" in driver.title
        print(f"Web title: {driver.title}")

        # Text input
        text_box = driver.find_element(By.ID, "my-text-id")
        text_box.send_keys("Entro QA")
        assert text_box.get_attribute("value") == "Entro QA"

        # Password input
        password_box = driver.find_element(By.NAME, "my-password")
        password_box.send_keys("P@ssw0rd!")

        # Textarea input
        text_area_box = driver.find_element(By.NAME, "my-textarea")
        text_area_box.send_keys("This is a test textarea input.")

        # Check if disabled text box is indeed disabled
        disable_text_box = driver.find_element(By.NAME, "my-disabled")
        assert not disable_text_box.is_enabled(), "Text box should be disabled"

        # Check if readonly text box is indeed readonly
        readonly_text_box = driver.find_element(By.NAME, "my-readonly")
        initial_value = readonly_text_box.get_attribute("value")
        readonly_text_box.send_keys("Trying to edit")
        assert readonly_text_box.get_attribute("value") == initial_value, (
            "Readonly box value should not change"
        )

        # Dropdown (Select)
        dropdown_element = driver.find_element(By.NAME, "my-select")
        select = Select(dropdown_element)
        select.select_by_visible_text("One")
        assert select.first_selected_option.text == "One"

        # Datalist
        datalist_input = driver.find_element(By.NAME, "my-datalist")
        datalist_input.send_keys("Chicago")

        # File Upload
        # Ensure the image exists or handle the missing file case
        image_path = os.path.abspath("images/sagwa-odod-anim.gif")
        if os.path.exists(image_path):
            file_input = driver.find_element(By.NAME, "my-file")
            file_input.send_keys(image_path)
        else:
            print(f"Warning: File not found at {image_path}")

        # Checkboxes and Radios
        driver.find_element(By.ID, "my-check-1").click()
        driver.find_element(By.ID, "my-check-2").click()
        radio_2 = driver.find_element(By.ID, "my-radio-2")
        radio_2.click()
        assert radio_2.is_selected()

        # Color picker
        color_picker = driver.find_element(By.NAME, "my-colors")
        color_picker.send_keys("#ff0000")

        # Date picker
        date_picker = driver.find_element(By.NAME, "my-date")
        date_picker.send_keys("02/14/2026" + Keys.TAB)

        # Range (Slider)
        slider_element = driver.find_element(By.NAME, "my-range")
        self.move_slider_to_value(slider_element, 10)

        # Screenshots before submission
        date_now = self.get_date_time()
        os.makedirs("images", exist_ok=True)
        before_path = f"images/before_submitting_{date_now}.png"
        driver.save_screenshot(before_path)

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, "button")
        submit_button.click()

        # Verify submission message
        message = self.wait.until(EC.visibility_of_element_located((By.ID, "message")))
        assert message.text == "Received!"

        # Screenshot after submission
        after_path = f"images/after_submitting_{date_now}.png"
        driver.save_screenshot(after_path)

        # Final wait to see result (optional)
        time.sleep(2)

    def move_slider_to_value(self, slider_element, target_value):
        """Moves a slider element to a target value using ActionChains."""
        min_val = float(slider_element.get_attribute("min") or 0)
        max_val = float(slider_element.get_attribute("max") or 100)
        current_val = float(slider_element.get_attribute("value") or 0)
        width = slider_element.size["width"]

        if max_val == min_val:
            return

        # Calculate pixel offset based on target value relative to current value
        offset = ((target_value - current_val) / (max_val - min_val)) * width

        actions = ActionChains(self.driver)
        actions.click_and_hold(slider_element).move_by_offset(
            offset, 0
        ).release().perform()
