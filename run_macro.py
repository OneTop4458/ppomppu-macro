# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from urllib import parse
import os
import json
import base64
import time

def main():
    try:
        config = getConfig() # 설정 파일 가져오기
        AutoExit = config['AutoExit'] # 자동 종료 설정 여부 가져오기
        Headless = config['Headless'] # Headless 설정 여부 가져오기
        if(Headless == "True"): # Headless 모드 동작
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu")
        else:
            options = None
        driver = getDriver(options) # 크롬 드라이버 로드
        id = base64.b64decode(config['userId']) # id, pw의 base64 decode
        id = id.decode("UTF-8")
        pw = base64.b64decode(config['userPw'])
        pw = pw.decode("UTF-8")
        driver.get('https://www.ppomppu.co.kr/zboard/login.php')
        loginPpomppu(driver, id, pw) # 뽐뿌 로그인
        time.sleep(1)
        driver.get("https://www.ppomppu.co.kr/myinfo/coupon/ppom_coupon_charge.php") # 이벤트 목록으로 이동
        print("LOG : 이벤트 목록 이동 성공")
        checkPop(driver) # 팝업 검사
        checkEvent(driver) # 이벤트 목록 찾기
        getConfigComment() # 댓글 목록 가져오기
        writeComment(driver,0) # 댓글 작성
        driver.quit()
    except Exception as e:
        print('LOG: Error [%s]' % (str(e)))
    else:
        print("LOG: Main Process in done.")
    finally:
        if(AutoExit == "False"): # 자동 종료가 아니라면
            os.system("Pause")

def getDriver(options=None):
    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.implicitly_wait(3)
    print("LOG: Chrome 드라이버 로딩 성공")
    return driver

def getConfig():
    try:
        with open('config.json') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print('LOG: Error in reading config file, {}'.format(e))
        return None
    else:
        return json_data

def getConfigComment():
    global commentList
    commentFile = open("config_comment.txt", "r", encoding='UTF8')
    lines = commentFile.readlines()
    lines = list(map(lambda s: s.strip(), lines))
    commentFile.close()
    commentList = lines
    print("LOG: commentList 가져오기 성공")

def loginPpomppu(driver, id, pw):
    WebDriverWait(driver,1000).until(EC.presence_of_element_located((By.XPATH, "//*[@id='user_id']"))).send_keys(id) #찾을때까지 기다림
    driver.find_element_by_xpath("//*[@id='password']").send_keys(pw)
    driver.find_element_by_class_name("log_btn").click()
    
    print("LOG : 로그인 성공")

def checkPop(driver):
    try:
        driver.find_element_by_id("close_notice_auth").click()
        print("LOG : 팝업 감지 및 제거 완료")
        return True
    except NoSuchElementException:
        print("LOG : 팝업 없음")
        return False

def checkEvent(driver):
    try:
        global ul
        global li
        global liSize
        ul = driver.find_element_by_class_name("ppom_charge_event").find_element_by_tag_name("ul")
        li = ul.find_elements_by_tag_name('li')
        liSize = len(li)
        print("LOG : 이벤트 목록 %d 개 검색 완료"%liSize)
        print("------------------------------------------------")
        i = 0
        while(liSize):
            print("%d 번째 목록 입니다 :"%(i+1))
            print(li[i].find_element_by_class_name('conts').text)
            print(" ")
            i += 1
            if(i >= liSize):
                break
        print("------------------------------------------------")
        print("LOG : 이벤트 목록 조회 성공")
        return True
    except NoSuchElementException:
        print("LOG : 이벤트 목록 조회 실패")
        return False

def writeComment(driver,i):
    try:
        temp = 0
        while(liSize):
            print("이벤트 갯수 : %d"%liSize)
            print("매크로 동작 횟수 : %d"%i)
            print("%d 번째 이벤트에 댓글을 작성합니다"%(i+1))
            time.sleep(1)
            ul = driver.find_element_by_class_name("ppom_charge_event").find_element_by_tag_name("ul")
            li = ul.find_elements_by_tag_name('li')
            print(li[i].find_element_by_class_name('conts').text)
            li[i].click()
            i += 1
            # 질문/요청 게시판 skip 코드 시작
            url = parse.urlparse(driver.current_url)
            url.geturl()
            query = dict(parse.parse_qs(url.query))
            
            if(query['id'] == ['help']): #추출한 query에 id가 없으면 exception 발생함
                print("------------------------------------------------")
                print("LOG : 질문/요청 게시판에는 댓글을 작성하지 않습니다!")
                print("------------------------------------------------")
                time.sleep(2)
                driver.get("https://www.ppomppu.co.kr/myinfo/coupon/ppom_coupon_charge.php")
                if(i >= liSize):
                    print("LOG : 총 %d 건의 댓글을 모두 작성완료 했습니다 [실패건이 있다면 포함하여 카운트됨]"%i)
                    break
                return True
            # 질문/요청 게시판 skip 코드 끝
            editorFrame = driver.find_element_by_css_selector('.cheditor-editarea-wrapper iframe')
            driver.switch_to_frame(editorFrame)
            editor = driver.find_element_by_xpath("/html/body")

            commentSize = len(commentList)
            if(temp >= commentSize):
                temp = 0
            editor.send_keys(commentList[temp])
            print("------------------------------------------------")
            print("LOG : 댓글 [%s] 입력"%commentList[temp])
            print("------------------------------------------------")
            temp += 1

            driver.switch_to_default_content()
            time.sleep(3)
            driver.find_element_by_xpath("//*[@id='button_vote']").click() #기다림이 좀 필요함
            time.sleep(2)
            print("LOG : 댓글작성 및 추천 성공")
            time.sleep(2)
            print(" ")
            print(" ")
            time.sleep(2)
            print(" ")
            print(" ")
            driver.get("https://www.ppomppu.co.kr/myinfo/coupon/ppom_coupon_charge.php")
            if(i >= liSize):
                print("LOG : 총 %d 건의 댓글을 모두 작성완료 했습니다 [실패건이 있다면 포함하여 카운트됨]"%i)
                break
        return True
    except:
        try:
            alert = driver.switch_to_alert()
            message = alert.text
            alert.accept()
        except:
            print("LOG : 댓글 작성 실패")
            print("LOG : %s"%message)
            driver.get("https://www.ppomppu.co.kr/myinfo/coupon/ppom_coupon_charge.php")
            checkPop(driver)
            writeComment(driver,i)

if __name__ == '__main__':
    main()
