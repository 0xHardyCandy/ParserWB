
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

def get_source_html(url):
    driver = webdriver.Chrome()
    driver.get(url)

    driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Прокрутка вниз
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Пауза, пока загрузится страница.
            time.sleep(0.1)
            # Вычисляем новую высоту прокрутки и сравниваем с последней высотой прокрутки.
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                time.sleep(3)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
            last_height = new_height

        with open("E:\Py projects\parser/source-page.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_items_urls(file_path):
    with open(file_path,encoding="utf-8") as file:
        src=file.read()
    soup = BeautifulSoup(src, "lxml")
    items = soup.findAll("div", class_='feedback__info')

    alltop=[]

    for item in items:
        top = []
        if item.find('span', class_ = 'feedback__rating stars-line star5'):
            rate = 5
        elif item.find('span', class_ = 'feedback__rating stars-line star1'):
            rate = 1
        elif item.find('span', class_ = 'feedback__rating stars-line star2'):
            rate = 2
        elif item.find('span', class_ = 'feedback__rating stars-line star3'):
            rate = 3
        elif item.find('span', class_ = 'feedback__rating stars-line star4'):
            rate = 4
        for s in item:
            if s.text != " " and "  ":
                top.append(s.text)
        top[1]=rate
        alltop.append(top)

    photos=[]
    comments = []
    items = soup.findAll("div", class_='feedback__content')

    for item in items:
        content=[]
        if item.find('ul', class_="feedback__photos"):
            photos.append('Yes')
        else:
            photos.append('No')
        if item.find('p', class_='feedback__text'):
            for s in item:
                if s.text != " " and "  ":
                    content.append(s.text)
            content = content[2]
            comments.append(content)

        else:
            comments.append('---')


    names=[]
    for i in alltop:
        names.append(i[0])
    rates =[]
    for i in alltop:
        rates.append(i[1])
    dates =[]
    for i in alltop:
        dates.append(i[2].split("  ")[0])
    colors = []
    for i in alltop:
        colors.append(i[2].split("  ")[1])






    df = pd.DataFrame({'Date': dates,'Name': names, 'Rate': rates, 'Type': colors, 'Photo': photos,  'Text': comments})
    df.to_excel('./review.xlsx')
    print("Отзывы сохранены в review.xlsx")




    # items = soup.findAll("p", class_="feedback__text")
    # comments = []
    # for item in items:
    #     comments.append(item.text)
    # items= soup.findAll("p", class_="feedback__header")
    # names = []
    # for item in items:
    #     names.append(item.text)
    #
    # items = soup.findAll("span",class_="feedback__date")
    # date = []
    # for item in items:
    #     date.append(item.text)






def main():
    a = input("Введите артикул: ")
    get_source_html(url=(f'https://www.wildberries.ru/catalog/{a}/feedbacks'))
    get_items_urls(file_path="E:\Py projects\parser\source-page.html")
if __name__ == "__main__":
    main()
