from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from selenium import webdriver
import threading
import time


# функция для проверки url страницы
def wait_url(driver, target_url):
    while True:
        current_url = driver.current_url
        if target_url in current_url:
            time.sleep(1)
            driver.quit()
            break
        time.sleep(1)


# основная программа
def start_browser():
    options = Options()
    options.add_argument("window-size=1500,1300")
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors=yes")

    # url который отслеживаем
    target_url = "https://pentagon.games/validate-email"

    data = open('data.txt', 'r')
    for i in data:
        # сохраняем данные в переменные
        i = i.split("*")
        name = i[0]
        email = i[1]
        password = i[2]
        url = i[3]

        # запускаем веб-драйвер
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # запускаем отдельный поток для отслеживания целевого URL
        url_thread = threading.Thread(target=wait_url, args=(driver, target_url))
        url_thread.start()

        # заполняем форму
        (driver.find_element(by=By.XPATH, value='/html/body/main/div[2]/div/div/div/form/div[2]/div[2]/div/input').
         send_keys(name))
        (driver.find_element(by=By.XPATH, value='/html/body/main/div[2]/div/div/div/form/div[3]/div[2]/div/input').
         send_keys(email))
        (driver.find_element(by=By.XPATH, value='/html/body/main/div[2]/div/div/div/form/div[4]/div[2]/div/div/input').
         send_keys(password))

        # ждем завершения потока отслеживания url перед завершением программы
        url_thread.join()
        print(email, "сделан")


# запуск основной функции
if __name__ == "__main__":
    start_browser()
