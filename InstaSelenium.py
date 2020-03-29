import random
import urllib.parse
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from config.public import comments


class InstaSelenium:
    def __init__(self, username, password):
        self.browser = webdriver.Chrome()
        self.username = username
        self.password = password

    def sign_in(self):
        self.browser.maximize_window()
        self.browser.get('https://www.instagram.com/accounts/login/')

        try:
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input = self.browser.find_element_by_name('username')
        finally:
            pass

        password_input = self.browser.find_element_by_name('password')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(4)  # seconds

    def follow_with_username(self, username):
        self.browser.maximize_window()
        url = 'https://www.instagram.com/{0}/'.format(username)

        while True:
            self.browser.get(url=url)
            time.sleep(4)  # seconds
            if urllib.parse.unquote(self.browser.current_url) == url:
                break

        time.sleep(4)  # seconds
        follow_button = self.browser.find_element_by_css_selector('button')
        if follow_button.text != 'Following':
            follow_button.click()
            time.sleep(4)  # seconds
        else:
            print("You are already following this user")

    def quit(self):
        time.sleep(4)  # seconds
        self.browser.quit()

    def like_tag(self, tag_name):
        self.browser.maximize_window()

        url = 'https://www.instagram.com/explore/tags/{0}/'.format(tag_name)
        while True:
            self.browser.get(url=url)
            time.sleep(4)  # seconds
            if urllib.parse.unquote(self.browser.current_url) == url:
                break

        time.sleep(4)  # seconds
        short_code_list = self.browser.find_elements_by_css_selector('div.v1Nh3')
        if len(short_code_list) == 0:
            self.browser.get('https://www.instagram.com/explore/tags/{0}'.format(tag_name))
            short_code_list = self.browser.find_elements_by_css_selector('div.v1Nh3')
        for one_short_code in short_code_list:
            one_short_code.click()

            time.sleep(4)  # seconds
            # If the robot had already liked the post, continue to the next post
            if self.browser.find_element_by_css_selector('span.fr66n button.wpO6b svg').get_attribute('aria-label') == 'Unlike':
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                continue
            self.browser.find_element_by_css_selector('span.fr66n button.wpO6b').send_keys(Keys.RETURN)
            webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
            time.sleep(1)  # seconds
            webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)  # seconds

    def comment_on_tags(self, tag_name):
        time.sleep(4)  # seconds
        # self.browser.maximize_window()
        url = 'https://www.instagram.com/explore/tags/{0}/'.format(tag_name)
        while True:
            self.browser.get(url=url)
            time.sleep(4)  # seconds
            if urllib.parse.unquote(self.browser.current_url) == url:
                break

        short_code_list = self.browser.find_elements_by_css_selector('div.v1Nh3')
        print('posts counts : ' + str(len(short_code_list)))
        for one_short_code in short_code_list:
            try:
                comment_text = random.choice(comments)
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                one_short_code.click()
                time.sleep(8)
                self.browser.find_element_by_css_selector('textarea.Ypffh').click()
                self.browser.find_element_by_css_selector('textarea.Ypffh').clear()
                self.browser.find_element_by_css_selector('textarea.Ypffh').send_keys(comment_text)
                self.browser.find_element_by_css_selector('textarea.Ypffh').send_keys(Keys.ENTER)

                time.sleep(4)
                webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                time.sleep(5)
            except NoSuchElementException as e:
                print('comment_text1 : ' + str(comment_text))
                continue
            except Exception as e:
                print('comment_text2 : ' + str(comment_text))
                self.browser.find_element_by_css_selector('textarea.Ypffh').click()
                self.browser.find_element_by_css_selector('textarea.Ypffh').send_keys(comment_text)
                self.browser.find_element_by_css_selector('textarea.Ypffh').send_keys(Keys.ENTER)
                continue
