from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os

# Mở trình duyệt
driver = webdriver.Chrome()
driver.get("https://alonhadat.com.vn/nha-dat/can-ban/biet-thu-nha-lien-ke/3/da-nang.html")

# Xóa file cũ nếu có
if os.path.exists("alonhadat.csv"):
    os.remove("alonhadat.csv")

# Tạo file CSV
with open("alonhadat.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["Tiêu đề", "Mô tả", "Địa chỉ", "Diện tích", "Giá"])

    page = 1
    while True:
        print(f"Đang xử lý trang {page}...")

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "content-item"))
            )

            items = driver.find_elements(By.CLASS_NAME, "content-item")
            for item in items:
                title = item.find_element(By.CLASS_NAME, "ct_title").text if item.find_elements(By.CLASS_NAME, "ct_title") else ""
                desc = item.find_element(By.CLASS_NAME, "content").text if item.find_elements(By.CLASS_NAME, "content") else ""
                address = item.find_element(By.CLASS_NAME, "address").text if item.find_elements(By.CLASS_NAME, "address") else ""
                area = item.find_element(By.CLASS_NAME, "ct_dt").text if item.find_elements(By.CLASS_NAME, "ct_dt") else ""
                price = item.find_element(By.CLASS_NAME, "ct_price").text if item.find_elements(By.CLASS_NAME, "ct_price") else ""

                writer.writerow([title, desc, address, area, price])

            next_links = driver.find_elements(By.LINK_TEXT, ">>")
            if next_links:
                next_links[0].click()
                page += 1
                time.sleep(2)
            else:
                print("Đã đến trang cuối.")
                break

        except Exception as e:
            print(f"Lỗi khi xử lý trang {page}: {e}")
            break

driver.quit()
print("Đã hoàn tất lưu dữ liệu vào alonhadat.csv")
