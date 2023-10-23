import platform
import os
import urllib.request
import shutil
import ssl
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import tarfile
import sys
import json
from publisher import Publisher
import argparse

class Crawling:
    def __init__(self):
        # 사용자 운영 체제(OS) 확인
        self.parser = argparse.ArgumentParser(description="Web Crawling Script")
        self.parser.add_argument("--driver", choices=["chromedriver", "edgedriver", "geckodriver", "whaledriver", "safaridriver"], default="chromedriver", help="Choose a browser driver")
        self.user_os = platform.system()

    def download_and_extract_driver(self, driver_name):
        # SSL 인증서 검증 비활성화
        ssl._create_default_https_context = ssl._create_unverified_context

        # 드라이버 최신 버전 URL
        if driver_name == "chromedriver":
            driver_version_url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
            response = urllib.request.urlopen(driver_version_url)
            version = response.read().decode("utf-8").strip()
        elif driver_name == "edgedriver":
            driver_version_url = "https://msedgedriver.azureedge.net/LATEST_STABLE"
            response = urllib.request.urlopen(driver_version_url)
            version = response.read().decode("utf-8").strip()
        elif driver_name == "geckodriver":
            driver_version_url = "https://github.com/mozilla/geckodriver/releases/latest"
            response = requests.get(driver_version_url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            version_tag = soup.select_one("title")
            if version_tag:
                title_text = version_tag.text
                start_index = title_text.index("Release ") + len("Release ")
                end_index = title_text.index(" ·", start_index)
                version = title_text[start_index:end_index]
        elif driver_name == "whaledriver":
            driver_version_url = "https://storage.googleapis.com/whale-assests/whalechromedriver/LATEST_RELEASE"
            response = urllib.request.urlopen(driver_version_url)
            version = response.read().decode("utf-8").strip()

        # 드라이버 다운로드 URL 생성
        if self.user_os == "Windows":
            if driver_name == "chromedriver":
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
            elif driver_name == "edgedriver":
                download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_win64.zip"
            elif driver_name == "geckodriver":
                download_url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-win64.zip"
            elif driver_name == "whaledriver":
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/whalechromedriver_win32.zip"
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require download on Windows.")
        elif self.user_os == "Linux":
            if driver_name == "chromedriver":
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip"
            elif driver_name == "edgedriver":
                download_url = f"https://msedgedriver.azureedge.net/{version}/edgedriver_linux64.zip"
            elif driver_name == "geckodriver":
                download_url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-linux64.tar.gz"
            elif driver_name == "whaledriver":
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/whalechromedriver_linux64.zip"
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require download on Linux.")
        elif self.user_os == "Darwin":
            if driver_name == "chromedriver":
                download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_mac64.zip"
            elif driver_name == "edgedriver":
                raise ValueError("Edge driver does not support macOS.")
            elif driver_name == "geckodriver":
                download_url = f"https://github.com/mozilla/geckodriver/releases/download/v{version}/geckodriver-v{version}-macos.tar.gz"
            elif driver_name == "whaledriver":
                raise ValueError("Whale driver does not require download on macOS.")
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require download on macOS.")

        # 드라이버 다운로드
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", f"{driver_name}.zip")
        with urllib.request.urlopen(download_url) as response, open(download_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        # 압축 해제 경로 설정
        if self.user_os == "Windows":
            if driver_name == "chromedriver":
                extraction_path = os.path.join(os.path.expandvars("%ProgramFiles(x86)%"), driver_name)
            elif driver_name == "edgedriver":
                extraction_path = os.path.join(os.path.expandvars("%ProgramFiles(x86)%"), "MicrosoftWebDriver")
            elif driver_name == "geckodriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "whaledriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on Windows.")
        elif self.user_os == "Linux":
            if driver_name == "chromedriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "edgedriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "geckodriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "whaledriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on Linux.")
        elif self.user_os == "Darwin":
            if driver_name == "chromedriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "edgedriver":
                raise ValueError("Edge driver does not support macOS.")
            elif driver_name == "geckodriver":
                extraction_path = os.path.join(os.path.expanduser("~"), driver_name)
            elif driver_name == "whaledriver":
                raise ValueError("Whale driver does not require extraction on macOS.")
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on macOS.")

        # 압축 해제
        if driver_name == "chromedriver" or driver_name == "edgedriver" or driver_name == "whaledriver":
            with zipfile.ZipFile(download_path, "r") as zip_ref:
                zip_ref.extractall(extraction_path)
        elif driver_name == "geckodriver":
            with tarfile.open(download_path, "r:gz") as tar_ref:
                tar_ref.extractall(extraction_path)
        elif driver_name == "safaridriver":
            raise ValueError("Safari driver does not require extraction.")

        # 압축 해제한 드라이버 파일 경로
        if self.user_os == "Windows":
            if driver_name == "chromedriver":
                driver_path = os.path.join(extraction_path, f"{driver_name}.exe")
            elif driver_name == "edgedriver":
                driver_path = os.path.join(extraction_path, "msedgedriver.exe")
            elif driver_name == "geckodriver":
                driver_path = os.path.join(extraction_path, "geckodriver.exe")
            elif driver_name == "whaledriver":
                driver_path = os.path.join(extraction_path, "whalechromedriver.exe")
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on Windows.")
        elif self.user_os == "Linux":
            if driver_name == "chromedriver":
                driver_path = os.path.join(extraction_path, f"{driver_name}")
            elif driver_name == "edgedriver":
                driver_path = os.path.join(extraction_path, "msedgedriver")
            elif driver_name == "geckodriver":
                driver_path = os.path.join(extraction_path, "geckodriver")
            elif driver_name == "whaledriver":
                driver_path = os.path.join(extraction_path, "whalechromedriver")
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on Linux.")
        elif self.user_os == "Darwin":
            if driver_name == "chromedriver":
                driver_path = os.path.join(extraction_path, f"{driver_name}")
            elif driver_name == "edgedriver":
                raise ValueError("Edge driver does not support macOS.")
            elif driver_name == "geckodriver":
                driver_path = os.path.join(extraction_path, "geckodriver")
            elif driver_name == "whaledriver":
                raise ValueError("Whale driver does not require extraction on macOS.")
            elif driver_name == "safaridriver":
                raise ValueError("Safari driver does not require extraction on macOS.")

        return driver_path

    def setup_driver(self, driver_name):
        # 드라이버 파일 경로
        driver_path = self.download_and_extract_driver(driver_name)

        # 드라이버 초기화
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # 브라우저 창을 띄우지 않고 실행할 경우

        if driver_name == "chromedriver":
            driver = webdriver.Chrome(options=options)
        elif driver_name == "edgedriver":
            driver = webdriver.Edge(options=options)
        elif driver_name == "whaledriver":
            driver = webdriver.Chrome(options=options)
        elif driver_name == "geckodriver":
            driver = webdriver.Firefox(options=options)
        elif driver_name == "safaridriver":
            driver = webdriver.Safari()

        return driver

    def run_script(self):
        args = self.parser.parse_args()
        driver_name = args.driver
        if driver_name == "safaridriver":
            # Safari 드라이버는 별도로 다운로드 및 압축 해제할 필요 없음
            driver = webdriver.Safari()
        else:
            driver = self.setup_driver(driver_name)

        received_message = sys.argv[1]
        message_dict = json.loads(received_message)

        # "category" 키의 값을 추출
        category_value = message_dict.get("category")

        if driver:
            # 웹페이지 접속
            if(category_value == '통합') :
                url = "https://m.kinolights.com/ranking/kino"
            elif(category_value == '넷플릭스') :
                url = "https://m.kinolights.com/ranking/netflix"
            elif(category_value == '티빙') :
                url = "https://m.kinolights.com/ranking/tving"
            elif(category_value == '쿠팡플레이') :
                url = "https://m.kinolights.com/ranking/coupang"
            elif(category_value == '웨이브') :
                url = "https://m.kinolights.com/ranking/wavve"
            elif(category_value == '디즈니') :
                url = "https://m.kinolights.com/ranking/disney"
            elif(category_value == '왓차') :
                url = "https://m.kinolights.com/ranking/watcha"
            elif(category_value == '박스오피스') :
                url = "https://m.kinolights.com/ranking/boxoffice"
            driver.get(url)

            items = driver.find_elements(By.XPATH, "//*[@id=\"contents\"]/div[2]/div[1]/div/div/ul[2]/li")

            combined_output = ""

            for item in items:
                # 텍스트 추출
                text_element = item.find_element(By.XPATH, ".//a/span[1]/span[3]")  # 제목
                text = text_element.text.strip()

                text_element = item.find_element(By.XPATH, ".//a/span[2]")  # 변경 순위 
                change_rank = text_element.text.strip()
                
                # 이미지 추출
                img_element = item.find_element(By.XPATH, ".//a/span[1]/span[1]/picture/img")  # 이미지 엘리먼트 선택
                img_src = img_element.get_attribute("src")  # 이미지의 src 속성 가져오기
                
                combined_output += f"{text}\n{change_rank}\n{img_src}\n"

            print(combined_output)

            
        publisher = Publisher()
        publisher.main(combined_output)
        # WebDriver 종료
        driver.quit()


if __name__ == "__main__":
    handler = Crawling()
    handler.run_script()
