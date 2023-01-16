import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time



options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.headless = True
driver = webdriver.Chrome(options=options)

stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
)

data = {}

def write_json(data):
        with open('result.json', 'a', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)



def get_img_links(data):
        for post_url in data.values():
                driver.get(post_url['links'])
                block = driver.find_element(By.CLASS_NAME, 'gallery-root-n3_HK')
                img = block.find_elements(By.TAG_NAME, 'li')
                post_url["photos"] = []

                try:
                        for image in img:
                                link_images = image.find_element(By.TAG_NAME, 'img').get_attribute('src')
                                post_url['photos'].append(link_images)
                except:
                                post_url['photos'].append('')

                write_json(data)
                time.sleep(5)
        driver.quit()


def get_page_data(url):
        driver.get(url)
        block = driver.find_element(By.CLASS_NAME, 'index-root-KVurS')
        posts = block.find_elements(By.CLASS_NAME, 'iva-item-content-rejJg')
        for post in posts:
                title = post.find_element(By.TAG_NAME, 'h3').text
                costs = post.find_element(By.CLASS_NAME, 'iva-item-priceStep-uq2CQ').text
                links = post.find_element(By.CLASS_NAME, 'iva-item-titleStep-pdebR').find_element(By.TAG_NAME, 'a').get_attribute('href')
                data[title] = {
                        'title': title,
                        'costs': costs,
                        'links': links,
                }
        get_img_links(data)





def main():
        for page in range(1, 2):
                url = f'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok/1-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUjlk?p={page}'
                get_page_data(url)


if __name__ == '__main__':
        main()
