from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

time.sleep(3)
language_select = driver.find_element(By.ID, "langSelect-EN")
language_select.click()
time_out = time.time() + 60 * 5
time.sleep(2)
i = 0
start_time = time.time()
difference = 5
while True:
    cookie_point = driver.find_element(By.XPATH, "//*[@id='cookies']").text.split(" ")
    cookie_score = cookie_point[0].replace(",", "")

    end_time = time.time()
    if end_time - start_time > difference:

        products_available = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
        products_list = [product.text for product in products_available]
        prices = []
        for i in range(len(products_list)):
            needed = driver.find_element(By.XPATH, value=f"//*[@id='productPrice{i}']").text
            needed = needed.replace(",", "")
            real_value = needed.split(" ")
            real_value_join = "".join(real_value)
            prices.append(int(real_value_join))
        can_buy = [price for price in prices if int(cookie_score) >= price]
        if len(can_buy) != 0:
            should_buy = max(can_buy)
            buy = prices.index(should_buy)
            affordable = driver.find_element(By.ID, value=f"product{buy}")
            affordable.click()

        difference += 5
    big_cookie = driver.find_element(By.ID, value="bigCookie")
    big_cookie.click()
    if time.time() >= time_out:
        final_score = driver.find_element(By.ID, "cookiesPerSecond")
        f_score = final_score.text
        print(f"cookies/second: {f_score}")
        driver.quit()
        break
