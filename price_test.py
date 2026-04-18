from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://jp.mercari.com/search?keyword=keyboard")

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-testid='item-cell']"))
    )
except:
    pass

time.sleep(2)

# 最初の商品要素を取得
item = driver.find_element(By.CSS_SELECTOR, "li[data-testid='item-cell']")

# 商品カード全体のテキストを見る
print("[商品カード全体のテキスト]")
print(item.text)
print("\n" + "="*50 + "\n")

# HTML 全体を見る
print("[商品カード HTML（最初の1500文字）]")
html = item.get_attribute('outerHTML')
print(html[:1500])

driver.quit()
