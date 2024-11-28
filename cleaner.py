from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import datetime

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#아이디랑 비밀번호를 큰따옴표나 작은따옴표로 묶어서 지정
user_id = 'id'
pw = 'password'

#글 지우려면 'posting', 댓글 지우려면 'comment'
# type = 'comment'
type = 'posting'

#창 띄우고 싶으면 True, 아니면 False
gui = False

#전체 갤러리 글을 지우고 싶으면 따옴표 없이 None 지정
#특정 갤러리 글만 지우고 싶으면, 갤로그에서 해당 갤 찍은다음 URL의 맨 끝에 있는 숫자를 galleryno에 적을 것
#예시: 치킨갤은 https://gallog.dcinside.com/아이디/posting/index?cno=112 처럼 112로 끝나므로 112 적으면 됨
galleryno = None
# galleryno = 72

#동시에 열어둘 탭 갯수
num_of_tabs = 4

#마지막에 쓴 글들 안 지우고 싶을 때
keeping_last = 3
# keeping_last = 1
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

options = webdriver.ChromeOptions()
if not gui:
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

started_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
number_at_start = None
accm = 0
timespent = 0

os.system('cls')

driver = webdriver.Chrome(options=options)

window_width = 800
window_height = 600
driver.set_window_size(window_width, window_height)
screen_width = driver.execute_script("return window.screen.availWidth;")
screen_height = driver.execute_script("return window.screen.availHeight;")
if gui:
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    driver.set_window_position(x_position, y_position)

driver.get("https://www.dcinside.com")
print("사이트 로드 완료")

time.sleep(2)
id_input = driver.find_element(By.ID, "user_id")
pw_input = driver.find_element(By.ID, "pw")

id_input.send_keys(user_id)
pw_input.send_keys(pw)
print("아이디, 비번 입력함")

login_button = driver.find_element(By.ID, "login_ok")
login_button.click()
print("로그인 버튼 누름")

time.sleep(2)

if galleryno is None: 
    url = f'https://gallog.dcinside.com/{user_id}/{type}'
else:
    url = f'https://gallog.dcinside.com/{user_id}/{type}/index?cno={galleryno}'

for _ in range(num_of_tabs):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)
    time.sleep(0.2)
    print(f'{_ + 1}번째 창 엶')

first_tab = driver.window_handles[0]
driver.switch_to.window(first_tab)  
driver.close()                      
driver.switch_to.window(driver.window_handles[0])

remaining_data = None
prev = datetime.datetime.now()
while True:
    for i in range(num_of_tabs):
        driver.switch_to.window(driver.window_handles[i])
        driver.refresh()

        buttons = driver.find_elements(By.CLASS_NAME, "btn_delete.btn_listdel.sp_img")
        total = driver.find_elements(By.CLASS_NAME, "num")[0]
        if int(total.text.strip('()')) == remaining_data:
            print("CAPTCHA 확인 필요!!!!")
            driver.quit()
            exit(1)
        if remaining_data == 0:
            print("지울 것이 더 없습니다.")
            driver.quit()
            exit(0)
        remaining_data = int(total.text.strip('()'))
        if number_at_start is None:
            number_at_start = remaining_data
        
        if i < len(buttons):
            buttons[num_of_tabs - i + (keeping_last - 1)].click()
            time.sleep(0.2)

            os.system('cls')

            alert = driver.switch_to.alert
            alert.accept()

            accm += 1

            current_time = datetime.datetime.now()
            time_elapsed = (current_time - prev).total_seconds()
            timespent += time_elapsed
            prev = current_time

            deletion_speed_per_sec = accm / timespent
            estm_time_seconds = remaining_data / deletion_speed_per_sec

            estm_time_h = int(estm_time_seconds // 3600)
            estm_time_m = int((estm_time_seconds % 3600) // 60)
            estm_time_s = int(estm_time_seconds % 60)
            estm_time_formatted = f'{estm_time_h}h {estm_time_m}m {estm_time_s}s'

            print(f'+-------------------------+---------------------+')
            print(f'| Started at              | {started_at} |')
            print(f'+-------------------------+---------------------+')
            print(f'| Current time            | {current_time.strftime("%Y-%m-%d %H:%M:%S")} |')
            print(f'+-------------------------+---------------------+')
            print(f'| No. of deleted data     | {accm:<19} |')
            print(f'+-------------------------+---------------------+')
            print(f'| Time elapsed for a data | {time_elapsed:.2f}s               |')
            print(f'+-------------------------+---------------------+')
            print(f'| Deletion speed          | {(deletion_speed_per_sec * 3600):<8.1f} / hour     |')
            print(f'+-------------------------+---------------------+')
            print(f'| Remaining data          | {(remaining_data - 1):<8} / {number_at_start:<8} |')
            print(f'+-------------------------+---------------------+')
            print(f'| Estm. time to finish    | {estm_time_formatted:<19} |')
            print(f'+-------------------------+---------------------+')
        else:
            print(f"{i}번 탭에 {i}번째 버튼이 없습니다.")
            exit(1)

        time.sleep(1.25)