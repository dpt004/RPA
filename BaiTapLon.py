from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Khởi tạo trình duyệt Chrome
driver = webdriver.Chrome()
driver.get("https://alonhadat.com.vn/nha-dat/can-ban/biet-thu-nha-lien-ke/3/da-nang.html")

# Mở file CSV để ghi
with open("alonhadat.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file)
    writer.writerow(["Tiêu đề", "Mô tả", "Địa chỉ", "Diện tích", "Giá"])

    page = 1
    while True:
        print(f"📄 Đang xử lý trang {page}...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "content-item"))
            )
            items = driver.find_elements(By.CLASS_NAME, "content-item")

            for item in items:
                try:
                    title = item.find_element(By.XPATH, './/div[@class="ct_title"]/a').text.strip()
                except:
                    title = ""

                try:
                    desc = item.find_element(By.XPATH, './/div[@class="content"]/div[2]').text.strip()
                except:
                    desc = ""

                try:
                    address = item.find_element(By.CLASS_NAME, "address").text.strip()
                except:
                    address = ""

                try:
                    area = item.find_element(By.CLASS_NAME, "ct_dt").text.strip()
                except:
                    area = ""

                try:
                    price = item.find_element(By.CLASS_NAME, "price").text.strip()
                except:
                    price = ""

                writer.writerow([title, desc, address, area, price])

            # Tìm nút '>>' để chuyển trang
            try:
                next_btn = driver.find_element(By.XPATH, '//a[text()=">>"]')
                next_btn.click()
                page += 1
                time.sleep(2)
            except:
                print("✅ Đã đến trang cuối cùng.")
                break

        except Exception as e:
            print(f"❌ Lỗi khi xử lý trang {page}: {e}")
            break

driver.quit()
print("✅ Đã lưu toàn bộ dữ liệu vào alonhadat.csv")
 