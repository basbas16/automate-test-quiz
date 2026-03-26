import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def scroll_down(driver):
    # Get screen dimensions
    size = driver.get_window_size()
    width = size["width"]
    height = size["height"]
    # Define start and end points for scrolling down (bottom to top)
    start_x = width / 2
    start_y = height * 0.8  # 80% down the screen
    end_x = width / 2
    end_y = height * 0.2  # 20% up the screen
    # Perform the swipe (Duration is in milliseconds)
    driver.swipe(start_x, start_y, end_x, end_y, 800)


def run_test():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"

    options.app_package = "com.google.android.youtube"
    options.app_activity = (
        "com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity"
    )

    options.unicode_keyboard = True
    options.reset_keyboard = True
    options.auto_grant_permissions = True

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        print("Android Emu Connected")
        wait = WebDriverWait(driver, 20)

        search_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Search"))
        )

        search_icon.click()
        # 2. Wait for the Search Input field and type the query
        print("Typing search query...")
        search_input = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ID, "com.google.android.youtube:id/search_edit_text")
            )
        )
        search_input.send_keys("Entronica")

        # 3. Execute the search by pressing the 'Enter' key on the Android keyboard
        # 66 is the Android keycode for 'ENTER'
        print("Pressing Enter to search...")
        driver.press_keycode(66)
        # 4. Wait a bit to see the results

        time.sleep(5)

        expected_channel_name = "Entronica Channel"
        channel_xpath = (
            f'//*[contains(@content-desc, "Subscribe to {expected_channel_name}.")]'
        )

        element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, channel_xpath))
        )

        print(f"Validating if '{expected_channel_name}' is in search results...")
        # Get the text of the very first result
        # first_result_channel = element[0].text
        if element.is_displayed():
            print("✅ Validation Success: 'Entronica Channel' is displayed!")
        else:
            print("❌ Validation Failed: Channel element found but not visible.")

        # # Get the text of the very first result
        # print(f"The first video is by: {element}")
        print("Search completed!")
        print(f"elementId: {element.id}")

        channel_xpath = '//*[contains(@content-desc, "Go to channel")]'

        click_channel = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, channel_xpath))
        )

        click_channel.click()
        print(f"Click Channel: {click_channel}")
        video_content_xpath = '//*[contains(@content-desc, "Videos")]'

        video_content = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, video_content_xpath))
        )

        video_content.click()

        time.sleep(5)

        scroll_down(driver=driver)

        video_xpath = '//*[contains(@content-desc, "play video")]'

        list_all_video = wait.until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, video_xpath))
        )
        print(len(list_all_video))

    except Exception as e:
        print(f"Failed: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Start Testing")
    run_test()
