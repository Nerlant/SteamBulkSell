from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from getpass import getpass
import time

username = input("Enter username: ")
password = getpass()

driver = webdriver.Firefox()
driver.get("https://steamcommunity.com/login")

username_field = driver.find_element_by_id("steamAccountName")
password_field = driver.find_element_by_id("steamPassword")

username_field.send_keys(username)
password_field.send_keys(password)

sign_in_field = driver.find_element_by_id("SteamLogin")
sign_in_field.click()

WebDriverWait(driver, 360).until(
    expected_conditions.url_contains("https://steamcommunity.com/id/")
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

    active_inventory_page = driver.find_element_by_id("active_inventory_page")
    ctn = list(filter(lambda x: x.value_of_css_property("display") != "none",
                      active_inventory_page.find_elements_by_class_name("inventory_ctn")))[0]

    inventory_pages = ctn.find_elements_by_class_name("inventory_page")

    current_inventory_page = list(filter(lambda x: x.value_of_css_property("display") == "block", inventory_pages))[0]
    item_holders = current_inventory_page.find_elements_by_class_name("itemHolder")

    continue_on_same_page = False

    for holder in item_holders:
        if "disabled" in holder.get_attribute("class"):
            continue

        holder.click()

        i = driver.execute_script("return g_ActiveInventory.selectedItem")
        if i["classid"] == selected_item["classid"]:
            sell_item = i
            print("found item on page")
            driver.execute_script("SellCurrentSelection()")
            subscriber_agreement_checkbox = driver.find_element_by_id("market_sell_dialog_accept_ssa")
            if not subscriber_agreement_checkbox.is_selected():
                subscriber_agreement_checkbox.click()
            price_text = driver.find_element_by_id("market_sell_currency_input")
            price_text.send_keys(price)
            sell_accept = driver.find_element_by_id("market_sell_dialog_accept")
            sell_accept.click()
            sell_ok = driver.find_element_by_id("market_sell_dialog_ok")
            sell_ok.click()
            time.sleep(5)

            # Click OK button on "Additional Confirmation Needed"
            for btn in driver.find_elements_by_xpath("//span[text()='OK']"):
                if btn.size["width"] != 0 and btn.size["height"] != 0:
                    btn.click()

            items_sold += 1

            if items_sold == number_to_sell:
                driver.close()
                print(f"Sold {items_sold} items.")
                exit(0)

            # sell succeeded
            if driver.find_element_by_id("market_headertip_itemsold").value_of_css_property("display") != "none":
                continue_on_same_page = True
                break

    # if end of inventory, break
    if current_page == driver.execute_script("return g_ActiveInventory.m_cPages") - 1:
        print('End of inventory reached')
        break

    if not continue_on_same_page:
        driver.execute_script("g_ActiveInventory.NextPage()")
        time.sleep(2)
