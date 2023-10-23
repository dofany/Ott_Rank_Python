import platform
import os
import urllib.request
import shutil
import ssl
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By

class Crawling:
    def __init__(self):
        # 사용자 운영 체제(OS) 확인
        self.user_os = platform.system()

    def download_and_extract_chromedriver(self):

        # SSL 인증서 검증 비활성화
        ssl._create_default_https_context = ssl._create_unverified_context

        # 최신 버전의 ChromeDriver URL
        chrome_driver_url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"

        # ChromeDriver 버전 가져오기
        response = urllib.request.urlopen(chrome_driver_url)
        version = response.read().decode("utf-8").strip()

        # ChromeDriver 다운로드 URL 생성
        if self.user_os == "Windows":
            download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
        elif self.user_os == "Linux":
            download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip"
        elif self.user_os == "Darwin":
            download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip"

        # ChromeDriver 다운로드
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", "chromedriver.zip")
        with urllib.request.urlopen(download_url) as response, open(download_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # 압축 해제 경로 설정
        if self.user_os == "Windows":
            extraction_path = os.path.join(os.path.expandvars("%ProgramFiles(x86)%"), "chromedriver")
        elif self.user_os == "Linux":
            extraction_path = os.path.join(os.path.expanduser("~"), "chromedriver")
        elif self.user_os == "Darwin":
            extraction_path = os.path.join(os.path.expanduser("~"), "chromedriver")

        # 압축 해제
        with zipfile.ZipFile(download_path, "r") as zip_ref:
            zip_ref.extractall(extraction_path)

        # 압축 해제한 ChromeDriver 파일 경로
        chrome_driver_path = os.path.join(extraction_path, "chromedriver")

        return chrome_driver_path

    def setup_chromedriver(self):
        # ChromeDriver 파일 경로
        chrome_driver_path = self.download_and_extract_chromedriver()

        # ChromeDriver 초기화
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행할 경우
        driver = webdriver.Chrome(options=options)

        return driver

    def run_script(self):
        driver = self.setup_chromedriver()

        if driver:
            # 웹페이지 접속
            url = "https://m.kinolights.com/ranking/kino"
            driver.get(url)

            items = driver.find_elements(By.XPATH, "//*[@id=\"contents\"]/div[2]/div[1]/div/div/ul[2]/li")

            combined_output = ""

            for item in items:
                # 텍스트 추출
                text_element = item.find_element(By.XPATH, ".//a/span[1]/span[3]")  # 텍스트 엘리먼트 선택
                text = text_element.text.strip()

                text_element = item.find_element(By.XPATH, ".//a/span[2]")  # 텍스트 엘리먼트 선택
                change_rank = text_element.text.strip()
                
                # 이미지 추출
                img_element = item.find_element(By.XPATH, ".//a/span[1]/span[1]/picture/img")  # 이미지 엘리먼트 선택
                img_src = img_element.get_attribute("src")  # 이미지의 src 속성 가져오기
                
                combined_output += f"{text}\n{change_rank}\n{img_src}\n"

            print(combined_output)
            # WebDriver 종료
            driver.quit()


if __name__ == "__main__":
    handler = Crawling()
    handler.run_script()
