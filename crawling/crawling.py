
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from .categories import category2url
from typing import *
import json
import time

DRIVER_PATH = './chromedriver'


def get_element_by_xpath(parent: Union[WebElement, WebDriver], xpath: str) -> Optional[WebElement]:
    elems = parent.find_elements_by_xpath(xpath)
    if len(elems) == 0:
        return None
    else:
        return elems[0]


def crawl_musinsa_item_page(driver: WebDriver, link: str) -> Dict:
    driver.get(url=link)

    name = get_element_by_xpath(driver, '//*[@id="page_product_detail"]/div[3]/div[3]/span/em')
    name = name.text if name is not None else None

    product_info = driver.find_element_by_xpath('//*[@id="product_order_info"]')
    brand = get_element_by_xpath(product_info, '//div[1]/ul/li[1]/p[2]/strong/a')
    brand = brand.text if brand is not None else None
    season = get_element_by_xpath(product_info, '//div[1]/ul/li[2]/p[2]/strong')
    season = season.text if season is not None else None

    tags_list = get_element_by_xpath(product_info, '//div[1]/ul/li[7]/p')
    tags_list = tags_list.find_elements_by_class_name('listItem') if tags_list is not None else []
    tags = []
    for tag in tags_list:
        tags.append(tag.text)

    like = get_element_by_xpath(driver, '//*[@id="product-top-like"]/p[2]/span')
    like = like.text if like is not None else None

    price = get_element_by_xpath(driver, '//*[@id="goods_price"]')
    price = price.text if price is not None else None

    image_box = get_element_by_xpath(driver, '//*[@id="bigimg"]')
    images = [image_box.get_attribute('src')]
    while True:
        driver.execute_script("rollImage('1','7', 'bigimg');")
        image_box = get_element_by_xpath(driver, '//*[@id="bigimg"]')
        image = image_box.get_attribute('src')
        if image == images[0]:
            break
        images.append(image)

    return {
        'name': name,
        'brand': brand,
        'season': season,
        'like': like,
        'tags': tags,
        'price': price,
        'images': images,
    }


def get_musinsa_item_links(driver: WebDriver) -> List[str]:
    elem_list = driver.find_element_by_xpath('//*[@id="searchList"]')
    elem_list = elem_list.find_elements_by_class_name('li_box')
    links = []
    for elem in elem_list:
        link = elem.find_element_by_name('goods_link').get_attribute('href')
        links.append(link)
    return links


def crawl_musinsa_category(driver: WebDriver, category: str, start_page: int, running_iteration: int,
                           delay: float, save_dir: str = 'output'):
    if category not in category2url:
        print(f'there is no category {category}')
        return
    category_url = category2url[category]

    driver.implicitly_wait(time_to_wait=5.0)
    wait = WebDriverWait(driver, 10)

    for it in range(running_iteration):
        driver.get(url=category_url)
        time.sleep(delay)
        driver.execute_script(f"listSwitchPage(document.f1,{start_page + it});")
        elems = driver.find_elements_by_class_name('error-network-wrap')
        if len(elems) != 0:
            print(f'there is no page#{start_page+it}')
            break
        current_url = driver.current_url
        links = get_musinsa_item_links(driver)
        result = []
        for link in links[:10]:
            time.sleep(delay)
            result.append(crawl_musinsa_item_page(driver, link))

        time.sleep(delay)
        with open(f'{save_dir}/data_{category}_{start_page + it}.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(result, ensure_ascii=False))

    driver.close()
