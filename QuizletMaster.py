import sys, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def getTerms(url, content, browser):
    browser.set_window_size(width=800, height=1000)
    browser.get(url)
    browser.find_element_by_class_name('SiteHeader-signInBtn').click()
    username = browser.find_element_by_name('username')
    username.send_keys(content[0])
    password = browser.find_element_by_name('password')
    password.send_keys(content[1])
    time.sleep(2)
    words = browser.find_elements_by_css_selector('a.SetPageTerm-wordText')
    terms = browser.find_elements_by_css_selector('a.SetPageTerm-definitionText')
    list1 = []
    list2 = []
    for i in range(len(words)):
        list1.append(words[i].text)
        list2.append(terms[i].text)
    return list1, list2;


def main(url):

    with open('pass.txt') as txt:
        content = txt.readlines()

    browser = webdriver.Chrome()
    browser.set_window_size(width=800, height=1000)
    #Chinese_to_Pinyin, Pinyin_to_Chinese = getTerms(url, content, browser)
    list1, list2 = getTerms(url, content, browser)
    buttons = browser.find_elements_by_css_selector('a.SetPageModeButton-link')
    buttons[-2].click()

    time.sleep(2)
    browser.find_elements_by_css_selector('span.UIButton-wrapper')[0].click()
    #time.sleep(.1)
    results = browser.find_elements_by_css_selector('div.MatchModeQuestionGridTile-content')

    beforeHandle = browser.current_window_handle


    #i = 0

    while(True):
        try:
            results[0].click()
            current_text = results[0].text
            Chinese_word = False;
            English_word = False;
            tempIndex = 0;
            selected = False;
            if(list1.count(current_text)>0):
                tempIndex = list1.index(current_text)
                Chinese_word = True;
            elif(list2.count(current_text)>0):
                tempIndex = list2.index(current_text)
                English_word = True;
            for i in range(len(results)):
                if(Chinese_word):
                    if(results[i].text==list2[tempIndex]):
                        results[i].click()
                        Chinese_word = False;
                        del results[i]
                        selected = True;
                        break;
                elif(English_word):
                    if(results[i].text == list1[tempIndex]):
                        results[i].click()
                        del results[i]
                        English_word = False;
                        selected = True;
                        break;
            if(selected):
                del results[0];
                selected = False;
        except Exception as ex:
            browser.switch_to_window(beforeHandle)
            results = browser.find_elements_by_css_selector('div.MatchModeQuestionGridTile-content')
            print(str(len(results)) + " " + str(ex))
            print(str(len(results)))
            selected = False;
    input()

if __name__ == "__main__":
    url = sys.argv[1]
    main(url)
