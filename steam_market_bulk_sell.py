from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from getpass import getpass
import time


username = input("Enter username: ")
password = getpass()

driver = webdriver.Firefox()
driver.get("https://steamcommunity.com/login/home/?goto=login")
time.sleep(10)

username_field = driver.find_element(by=By.XPATH, value="//input[@type='text']")
password_field = driver.find_element(by=By.XPATH, value="//input[@type='password']")


username_field.send_keys(username)
password_field.send_keys(password)

sign_in_field = driver.find_element(by=By.XPATH, value="//button[@type='submit']")

sign_in_field.click()

WebDriverWait(driver, 360).until(
    expected_conditions.url_contains("https://steamcommunity.com/profiles/")
)

inventory_url = driver.current_url + "/inventory/"
driver.get(inventory_url)
WebDriverWait(driver, 360).until(
    expected_conditions.url_matches(inventory_url)
)

input("Select item to sell and press enter.")

selected_item = driver.execute_script("return g_ActiveInventory.selectedItem")
print(f'Selected item: {selected_item["description"]["name"]}')

number_to_sell = int(input("Enter number of items to sell: "))
price = input("Enter price of item to sell (what you will receive): ")

# go to start of inventory
while driver.execute_script("return g_ActiveInventory.m_iCurrentPage") != 0:
    driver.execute_script("g_ActiveInventory.PreviousPage()")

items_sold = 0

while True:
    current_page = driver.execute_script("return g_ActiveInventory.m_iCurrentPage")

    active_inventory_page = driver.find_element(by=By.ID, value="active_inventory_page")
    ctn = list(filter(lambda x: x.value_of_css_property("display") != "none",
                      active_inventory_page.find_elements(by=By.CLASS_NAME, value="inventory_ctn")))[0]

    inventory_pages = ctn.find_elements(by=By.CLASS_NAME, value="inventory_page")

    current_inventory_page = list(filter(lambda x: x.value_of_css_property("display") == "block", inventory_pages))[0]
    item_holders = current_inventory_page.find_elements(by=By.CLASS_NAME, value="itemHolder")

    continue_on_same_page = False

    for holder in item_holders:
        if "disabled" in holder.get_attribute("class"):
            continue

        holder.click()

        i = driver.execute_script("return g_ActiveInventory.selectedItem")
        if i["description"]["market_hash_name"] == selected_item["description"]["market_hash_name"]:
            sell_item = i
            print("found item on page")
            driver.execute_script("SellCurrentSelection()")
            subscriber_agreement_checkbox = driver.find_element(by=By.ID, value="market_sell_dialog_accept_ssa")
            if not subscriber_agreement_checkbox.is_selected():
                subscriber_agreement_checkbox.click()
            price_text = driver.find_element(by=By.ID, value="market_sell_currency_input")
            price_text.send_keys(price)
            sell_accept = driver.find_element(by=By.ID, value="market_sell_dialog_accept")
            sell_accept.click()

            WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.ID, "market_sell_dialog_ok"))).click()

        

            try:
                WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.XPATH, "//span[text()='OK']"))).click()
            except TimeoutException:
                print('No additional confirmation needed.')

            items_sold += 1

            if items_sold == number_to_sell:
                driver.close()
                print(f"Sold {items_sold} items.")
                exit(0)

            # sell succeeded
            if driver.find_element(by=By.ID, value="market_headertip_itemsold").value_of_css_property("display") != "none":
                continue_on_same_page = True
                break
        else:
            print(i["classid"])
            print(selected_item["classid"])
            print(i["class"])
            print(i)

    # if end of inventory, break
    if current_page == driver.execute_script("return g_ActiveInventory.m_cPages") - 1:
        print('End of inventory reached')
        break

    if not continue_on_same_page:
        driver.execute_script("g_ActiveInventory.NextPage()")
        time.sleep(3)