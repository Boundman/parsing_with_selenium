from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


path_to_driver = 'C:/chromedriver.exe'  # Put here path to your driver file
browser = webdriver.Chrome(path_to_driver)
url = 'https://www.allmusic.com/advanced-search'  # Main page of chosen for myself site
browser.get(url)  # Open link at the browser

input_text = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[1]/section[1]/div/div[1]/input")  # Here is xpath to object of search genre/style field

genre_name = "Reggae"  # Here you should input needed genre
input_text.send_keys(genre_name)  # Input genre at the search field by this script
time.sleep(1)  # You should wait a little bit for page fully download (you may increase time if your internet is slow)

xpath_to_checkbox = "//*[@id='genreid:MA0000002820']"  # Put here xpath to checkbox genre that you need (At the browser: Select checkbox, do rightclick on it, search element and then at the HTML code choose this checkbox, do rightclick on it, copy, xpath
genre_checkbox = browser.find_element_by_xpath("." + xpath_to_checkbox)  # Here checkbox will be found
genre_checkbox.click()  # Here it will be clicked
time.sleep(2)  # Wait a little bit, albums will be downloaded

arrayyy = []
iter_arr = [1, 2, 3, 4, 5, 6] + [6]*100  # All pages at the site

file = open('BD_' + genre_name.lower() + '.txt', 'a', encoding='utf-8')  # Create a file; in this file will be stored all songs of this genre

for i in iter_arr:  # We will go through all pages of chosen genre
    try:
        for j in range(40):  # 40 - because at the one page 40 albums

            year = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[2]/div[1]/table/tbody/tr[" + str(j + 1) + "]/td[2]").text  # Find album release year
            artist = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[2]/div[1]/table/tbody/tr[" + str(j + 1) + "]/td[3]").text  # Find creator of album
            album = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[2]/div[1]/table/tbody/tr[" + str(j + 1) + "]/td[4]").text  # Find name of the album

            album_href = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[2]/div[1]/table/tbody/tr[" + str(j+1) + "]/td[4]/a[1]").get_attribute('href')  # Here we will find link at the album page
            browser.execute_script("window.open('" + str(album_href) + "','_blank');")  # Open album page at the new tab
            browser.switch_to_window(browser.window_handles[-1])  # Choose this tab

            for k in range(15):  # 15 songs from album - that will be enough for us
                try:
                    song_name = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[3]/div/table/tbody/tr[" + str(k+1) + "]/td[4]/div[1]/a").text  # Find song name
                    arrayyy.append({
                        'name': song_name,
                        'year': year,
                        'artist': artist,
                        'album': album,
                        'genre': genre_name
                    })

                    file.write(arrayyy[-1]['name'] + '?' + arrayyy[-1]['artist'] + '?' + arrayyy[-1]['album'] + '?' + arrayyy[-1]['year'] + '?' + arrayyy[-1]['genre'] + '\n')  # Here we write all data about current song at the created previously file

                except NoSuchElementException as error:  # Strange thing at the site, some songs from albums has one xpath and the others another; therefore we try at first one, if don`t work - another
                    try:
                        song_name = browser.find_element_by_xpath(
                            ".//*[@id='cmn_wrap']/div[1]/div[2]/section[3]/div[1]/table/tbody/tr[" + str(
                                k + 1) + "]/td[3]/div[1]/a[1]").text
                        arrayyy.append({
                            'name': song_name,
                            'year': year,
                            'artist': artist,
                            'album': album,
                            'genre': genre_name
                        })

                        file.write(
                            arrayyy[-1]['name'] + '?' + arrayyy[-1]['artist'] + '?' + arrayyy[-1]['album'] + '?' +
                            arrayyy[-1]['year'] + '?' + arrayyy[-1]['genre'] + '\n')

                    except NoSuchElementException as err:
                        print('NO MORE SONGS AT ALBUM')
                        print(err)
                        break

            browser.close()  # Here we close last tab, tab with last album
            browser.switch_to_window(browser.window_handles[0])  # And then switch to the tab with all albums

        print(arrayyy)
    except NoSuchElementException as e:
        print("SOMETHING WENT WRONG")
        print(e)

    try:
        element = browser.find_element_by_xpath(".//*[@id='cmn_wrap']/div[1]/div[2]/section[2]/div[3]/div/a[" + str(i+1) + "]")  # Find a number of the next page with the albums
        browser.execute_script("arguments[0].click();", element)  # Switch to this page
    except NoSuchElementException as e:
        print("SOMETHING WENT WRONG")
        print(e)
        break
    time.sleep(6)  # It need to pretty long time to load all albums from the next page

file.close()  # Just close our file
browser.close()  # Close last page
