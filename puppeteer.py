from selenium import webdriver

# 사파리 웹 드라이버 활성화
webdriver.Safari(executable_path='/usr/bin/safaridriver')

# 사파리 웹 드라이버 생성
driver = webdriver.Safari()

# 크롤링하려는 SPA 페이지 URL로 이동
driver.get('https://m.kinolights.com/ranking/kino')

# 페이지가 완전히 로드될 때까지 대기 (예: 5초)
driver.implicitly_wait(5)

element = driver.find_element_by_xpath("//*[@id='contents']/div[2]/div[1]/div/div/ul[2]")
text = element.text
print(text)

driver.quit()