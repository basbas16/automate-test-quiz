import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def item_selector(driver, target_text):
    # Scroll until an element with text "Entronica Channel" is visible
    ui_selector = f'new UiScrollable(new UiSelector().scrollable(true)).scrollIntoView(newUiSelector().text("{target_text}"))'

    # Execute the native Android command
    driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui_selector)


def get_video_name(video_elements):

    video_name = []
    for index, video in enumerate(video_elements):
        description = video.get_attribute("content-desc")
        print(f"Video {index + 1}: {description}")
        title = description.split(" - ")[0]
        print(f"Title: {title}")
        video_name.append(title)
        print("-" * 30)

    return video_name


def scroll(driver, direction="down"):
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
    if direction == "down":
        driver.swipe(start_x, start_y, end_x, end_y, 800)

    else:
        driver.swipe(end_x, end_y, start_x, start_y, 800)


def run_test():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"
    options.app_package = "com.google.android.youtube"
    options.app_activity = (
        "com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity"
    )
    options.load_capabilities(
        {
            "unicode_keyboard": True,
            "reset_keyboard": True,
            "auto_grant_permissions": True,
        }
    )

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        print("Android Emu Connected")
        wait = WebDriverWait(driver, 30)

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

        channel_xpath = '//*[contains(@content-desc, "Go to channel")]'

        click_channel = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, channel_xpath))
        )

        click_channel.click()
        video_content_xpath = '//*[contains(@content-desc, "Videos")]'

        video_content = wait.until(
            EC.element_to_be_clickable((AppiumBy.XPATH, video_content_xpath))
        )

        video_content.click()

        time.sleep(5)

        scroll(driver=driver)

        video_xpath = '//*[contains(@content-desc, "play video")]'

        list_all_video = driver.find_elements(AppiumBy.XPATH, video_xpath)
        len_all_video = len(list_all_video)

        if len_all_video > 1:
            print("Channel have more than 1 video")
            print(f"Video in channel = {len_all_video}")
        else:
            print("Channel has no video")

        video_list = get_video_name(list_all_video)
        print(video_list)

        # scroll(driver, "up")
        time.sleep(5)

        video_name = video_list[0]
        video_xpath = f"//*[contains(@content-desc, '{video_name}')]"

        video = wait.until(EC.element_to_be_clickable((AppiumBy.XPATH, video_xpath)))
        video.click()

    except Exception as e:
        print(f"Failed: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Start Testing")
    run_test()
