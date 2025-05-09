from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import os

# Mở trình duyệt Chrome
driver = webdriver.Chrome()
driver.get("https://alonhadat.com.vn/nha-dat/can-ban/biet-thu-nha-lien-ke/3/da-nang.html")

# Kiểm tra xem file CSV đã tồn tại chưa, nếu có thì xóa để tránh bị ghi đè
if os.path.exists("alonhadat.csv"):
    os.remove("alonhadat.csv")

# Tạo file CSV mới và chuẩn bị viết dữ liệu
with open("alonhadat.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    # Ghi tiêu đề cột vào file CSV
    writer.writerow(["Tiêu đề", "Mô tả", "Địa chỉ", "Diện tích", "Giá"])

    page = 1  # Biến đếm số trang hiện tại
    while True:
        print(f"Đang xử lý trang {page}...")

        try:
            # Chờ cho đến khi tất cả các bài viết trên trang hiện tại được tải xong
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "content-item"))
            )

            # Lấy tất cả các bài viết trên trang hiện tại
            items = driver.find_elements(By.CLASS_NAME, "content-item")
            for item in items:
                # Lấy dữ liệu của từng bài viết
                title = item.find_element(By.CLASS_NAME, "ct_title").text if item.find_elements(By.CLASS_NAME, "ct_title") else ""
                desc = item.find_element(By.CLASS_NAME, "content").text if item.find_elements(By.CLASS_NAME, "content") else ""
                address = item.find_element(By.CLASS_NAME, "address").text if item.find_elements(By.CLASS_NAME, "address") else ""
                area = item.find_element(By.CLASS_NAME, "ct_dt").text if item.find_elements(By.CLASS_NAME, "ct_dt") else ""
                price = item.find_element(By.CLASS_NAME, "ct_price").text if item.find_elements(By.CLASS_NAME, "ct_price") else ""

                # Ghi dữ liệu của bài viết vào file CSV
                writer.writerow([title, desc, address, area, price])

            # Tìm nút ">>" để chuyển sang trang tiếp theo
            next_links = driver.find_elements(By.LINK_TEXT, ">>")
            if next_links:
                # Nếu tìm thấy nút ">>", click vào nó để chuyển sang trang kế tiếp
                next_links[0].click()
                page += 1  # Tăng số trang
                time.sleep(2)  # Chờ 2 giây để trang tải xong
            else:
                # Nếu không tìm thấy nút ">>", tức là đã đến trang cuối
                print("Đã đến trang cuối.")
                break  # Dừng vòng lặp

        except Exception as e:
            # Xử lý lỗi nếu có sự cố trong khi lấy dữ liệu hoặc chuyển trang
            print(f"Lỗi khi xử lý trang {page}: {e}")
            break  # Dừng vòng lặp nếu có lỗi

# Đóng trình duyệt sau khi hoàn tất
driver.quit()

# In thông báo hoàn tất
print("Đã hoàn tất lưu dữ liệu vào alonhadat.csv")
