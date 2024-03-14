from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib

# 검색어 입력
query = input("검색어 입력: ")

# 이미지 개수 입력
num_images = int(input("수집할 이미지 개수 입력: "))

# 드라이버 설정 및 검색
chrome_options = webdriver.ChromeOptions()
chrome_options.binary = "C://chromedriver_win32/chromedriver.exe"  # 드라이버 실행파일 경로
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com/imghp")
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys(query)
search_bar.submit()

# 스크롤 및 "결과 더보기" 버튼 클릭
PAUSE_TIME = 1.5
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollBy(0, 5000)")
    time.sleep(PAUSE_TIME)

    try:
        see_more_button = driver.find_element(By.CSS_SELECTOR, ".mye4qd")
        see_more_button.click()
    except NoSuchElementException:
        break

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break

    last_height = new_height

# 이미지 수집 및 저장
img_elements = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")

for idx, img in enumerate(img_elements):
    if idx >= num_images:
        break  # 원하는 이미지 개수만큼 수집되면 중단

    try:
        img.click()
        time.sleep(PAUSE_TIME)

        # 이미지 URL 가져오기 (예시)
        img_element = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')

        imageSrc = img_element.get_attribute('src')

        # 이미지 다운로드
        try:
            urllib.request.urlretrieve(imageSrc, f'{query}_{idx+1}.png')
            print(f"{query} : {idx+1}/{len(img_elements)} proceed...")
        except urllib.error.URLError as e:
            print(f"Error in {idx}: Download error - {e}")

    except Exception as e:
        print(f"Error in {idx}: {e}")

driver.quit()

print("done")
