import tkinter as tk
import tkinter.font as tkFont
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# import easyocr
# from html2image import Html2Image



# Function to find out if the image has a LG or Samsung product or not 
# def Calculate_Images(brand,image_url):
#     hti = Html2Image()
#     image_url = "https:"+image_url
    
#     hti.screenshot(url=image_url, save_as='output.png')
#     # url = "https://media.extra.com/i/aurora/Discount_LargeAppliance_HS_E_4.webp"

#     reader = easyocr.Reader(['en'], gpu=True)
#     # Process the image using easyocr
#     result = reader.readtext("output.png", detail=0)
#     # Print the result
#     # print(result)

#     count = 0
#     for res in result:
#         if brand in res:
#             count+=1
#             break
#     print(count)
#     return count 


# def CheckBrand(brand,list_of_images):
#     counter = 0 
#     for im_list in list_of_images:
#         rtnCount = Calculate_Images(brand,im_list)
#         if rtnCount == 1:
#             counter+=1
#     return counter

class SWSG_Search_By_Keyword:
    
    
    def InfiniteScrolling(self,driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(4)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            pass
        last_height = new_height
            

    def fetch_pdp(self,driver, url,check_once):
    
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0
            sku = ""
            mpn = ""
            

            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(5)
                # driver.set_page_load_timeout(30)
                
                # try:
                #     ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
                #     model_id = ids.get_attribute("content")
                # except:
                #     # driver.close()
                #     driver.switch_to.window(driver.window_handles[0])
                #     model_id = ""
                
                # ---------------------For SKU --------------------------------
                try:
                    sku_div = driver.find_element(By.CSS_SELECTOR,".ruk_rating_snippet")
                    sku = sku_div.get_attribute("data-sku")
                except:
                    pass
                print(sku)
                try:
                    mpn_div = driver.find_element(By.XPATH,"//*[contains(text(), 'الموديل')]")
                    mpn = mpn_div.text
                    mpn = mpn.replace("الموديل","")
                    mpn= mpn.replace(":","")
                except:
                    pass
                print(mpn)

                # ---------------------For videos -----------------------------
                try:
                    total_videos_tag = driver.find_elements(By.CSS_SELECTOR,"div[class='video-wrapper']")
                    total_videos = len(total_videos_tag)
                except:
                    total_videos = 0 
                # print("Total total_videos)
                # print("videos:",total_videos)
                # ----------------------Ending Video---------------------------

                
            
                try:
                    product_info = driver.find_element(By.CSS_SELECTOR,".product-info-price")
                    rating = product_info.find_element(By.CSS_SELECTOR,".tf-rating").text
                    review = product_info.find_element(By.CSS_SELECTOR,".tf-count").text

                except:
                    rating = 0
                    review = 0
                
                # print("Rating:",rating)
                # print("Review:",review)

                try:
                    # list_of_images = set()
                    try:
                        images_list_container = driver.find_element(By.CSS_SELECTOR,".image-gallery-thumbnails-container")
                        list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                        # for imag in list_of_img_tags:
                        #     list_of_images.add(imag.get_attribute("src"))

                        total_images = len(list_of_img_tags)  
                    except:
                        total_images = 0
    
                except:
                    # driver.switch_to.window(driver.window_handles[0])
                    total_images=0

                if total_videos >=1 and total_images>total_videos:
                    total_images-=total_videos
                # print(total_images)

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return total_images,rating,review,total_videos,sku,mpn
            except:
                driver.switch_to.window(driver.window_handles[0])
                return total_images,rating,review,total_videos,sku,mpn
    

    def extract_data_by_keyword(self,driver, url,cat_name,search_keyword,check_once,all_data):
    
        driver.get(url)
        # Get scroll height
        # self.InfiniteScrolling(driver)

        time.sleep(5)
        

        all_divs  = driver.find_elements(By.CSS_SELECTOR, ".home-products_grid_item-3F-")
        print(len(all_divs))
        # print(len(all_divs))

        count =1
        number_of_products = 0
        for div in all_divs:
        # get all elements with the tag "a"
            title = div.find_element(By.CSS_SELECTOR,".home-product_name-ZHO")
            # print(title.text)
            link = div.find_element(By.TAG_NAME,"a")
            # img = div.find_element(By.CSS_SELECTOR,"img[class='product-image-photo']")
            price = div.find_element(By.CSS_SELECTOR,".productFullDetail-productPrice-1Js").text
              
            if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("إل جى")!= -1 or title.text.find("ال جي") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى")!= -1)  else "Dyson"
                title_name = title.text
                # image_url = img.get_attribute("src")
                img_link = link.get_attribute("href")
                
                total_images,rating,review,total_videos,sku,mpn = self.fetch_pdp(driver,img_link,check_once)
                print("Total Videos:",total_videos)
                print("Total Images:",total_images)
                if number_of_products < 20:
                    data = {
                            "Date": datetime.today(),
                            "Region": "MEA",
                            "Country": "KSA",
                            "Retailer": "SWSG",
                            "category":  cat_name,
                            "keyword": search_keyword,
                            "brand": brand_name,
                            "Rank": count,
                            "mpn": mpn,
                            "sku": sku,
                            "title":title_name,
                            "link": img_link,
                            "price":price
                            # "image url":image_url,
                    }
                    print("Brand:",data["brand"],"Rank:",data["Rank"])
                    check_once+=1    
                    all_data.append(data)
                elif number_of_products>20:
                    break
            count+=1
            number_of_products +=1
        return all_data,check_once



   
    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        # -------------------------------------------------------------------------------------
        # For Search Keywords
        # Reading the excel sheet
        df = pd.read_excel("SWSG/search_keywords/by_search_keywords.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []
        list_of_keywords = []


        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['keywords']:
            list_of_keywords.append(dt)
            testing_url = f"https://swsg.co/ar/search.html?query={dt}&page=1"
            list_of_urls.append(testing_url)
        # print(df)

        # Created an empty dataframe

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        all_data = []
        while i < len(list_of_urls):

            
            # storing the extracted data in df to be used in future
            all_data,check_once =self.extract_data_by_keyword(driver,list_of_urls[i],list_of_categories[i],list_of_keywords[i],check_once,all_data)
            i+=1
            check_once+=1
        # Closing the browser 
        driver.quit()
        dataframe_final = pd.DataFrame(all_data)
        # Printing the dataframe with all the data 
        print(dataframe_final)

        # Storing the dataframe in the text.xlsx file 
        # dataframe_final.to_excel(excel_writer = "output_SWSG/_SWSG_search_by_keyword.xlsx")

        dataframe_final.to_excel(excel_writer = f"SWSG/output_SWSG/{datetime.today().date()}_SWSG_search_by_keyword.xlsx")

        # self.UploadFileOnGoogleDrive(file_path)



class SWSG_Search_By_Category:
    
    def nextpagecheck(self,driver):
        total_pages = 1
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR,"button[aria-label='move to the next page'")
                button.click()
                time.sleep(10)
                total_pages +=1
            except:
                break
        return total_pages
    def fetch_pdp(self,driver, url,check_once):
    
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0
            sku = ""
            mpn = ""

            

            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(5)
                # driver.set_page_load_timeout(30)
                
                # try:
                #     ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
                #     model_id = ids.get_attribute("content")
                # except:
                #     # driver.close()
                #     driver.switch_to.window(driver.window_handles[0])
                #     model_id = ""
                
                # ---------------------For SKU --------------------------------
                try:
                    sku_div = driver.find_element(By.CSS_SELECTOR,".ruk_rating_snippet")
                    sku = sku_div.get_attribute("data-sku")
                except:
                    pass
                print(sku)
                try:
                    mpn_div = driver.find_element(By.XPATH,"//*[contains(text(), 'الموديل')]")
                    mpn = mpn_div.text
                    mpn = mpn.replace("الموديل","")
                    mpn= mpn.replace(":","")
                except:
                    pass
                print(mpn)

                # ---------------------For videos -----------------------------
                try:
                    total_videos_tag = driver.find_elements(By.CSS_SELECTOR,"div[class='video-wrapper']")
                    total_videos = len(total_videos_tag)
                except:
                    total_videos = 0 
                # print("Total total_videos)
                # print("videos:",total_videos)
                # ----------------------Ending Video---------------------------

                
            
                try:
                    product_info = driver.find_element(By.CSS_SELECTOR,".product-info-price")
                    rating = product_info.find_element(By.CSS_SELECTOR,".tf-rating").text
                    review = product_info.find_element(By.CSS_SELECTOR,".tf-count").text

                except:
                    rating = 0
                    review = 0
                
                # print("Rating:",rating)
                # print("Review:",review)

                try:
                    # list_of_images = set()
                    try:
                        images_list_container = driver.find_element(By.CSS_SELECTOR,".image-gallery-thumbnails-container")
                        list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                        # for imag in list_of_img_tags:
                        #     list_of_images.add(imag.get_attribute("src"))

                        total_images = len(list_of_img_tags)  
                    except:
                        total_images = 0
    
                except:
                    # driver.switch_to.window(driver.window_handles[0])
                    total_images=0

                if total_videos >=1 and total_images>total_videos:
                    total_images-=total_videos
                # print(total_images)

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return total_images,rating,review,total_videos,sku,mpn
            except:
                driver.switch_to.window(driver.window_handles[0])
                return total_images,rating,review,total_videos,sku,mpn
    

    def InfiniteScrolling(self,driver):
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(4)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            pass
        last_height = new_height

    def SearchingCategory(self,driver,Url_Link,cat_name,all_data,check_once):
        url = Url_Link
        driver.get(url)

        time.sleep(10)
        
        # Get scroll height
  
        # time.sleep(5)
        
        all_divs  = driver.find_elements(By.CSS_SELECTOR, ".home-products_grid_item-3F-")
        count =1
        number_of_products =0 
        
        for div in all_divs:
            # get all elements with the tag "a"
                title = div.find_element(By.CSS_SELECTOR,".home-product_name-ZHO")
                # print(title.text)
                link = div.find_element(By.TAG_NAME,"a")
                # img = div.find_element(By.CSS_SELECTOR,"img[class='product-image-photo']")
                price = div.find_element(By.CSS_SELECTOR,".productFullDetail-productPrice-1Js").text
                
                if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("ال جي") != -1 or title.text.find("ال جي") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                    brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("ال جي") != -1)  else "Dyson"
                    title_name = title.text
                    # image_url = img.get_attribute("src")
                    img_link = link.get_attribute("href")
                    
                    
                    
                    total_images,rating,review,total_videos,sku,mpn = self.fetch_pdp(driver,img_link,check_once)
                    check_once+=1    
                    
                    
                    if number_of_products < 20:
                        data_without_image = {
                            "Date": datetime.today(),
                            "Region": "MEA",
                            "Country": "KSA",
                            "Retailer": "SWSG",
                            "category":  cat_name,
                            # "keyword": search_keyword,
                            "brand": brand_name,
                            "Rank": count,
                            "mpn": mpn,
                            "sku": sku,
                            "title":title_name,
                            "link": img_link,
                            "price":price
                            # "image url":image_url,
                        }
                        all_data.append(data_without_image)

                    
                count+=1
                number_of_products+=1
        
        
        return all_data,check_once
    
    
    # Searching Category by Image count (SWSG Only)
   
    
    # for dt in all_data:
    #     print(dt["images_count"]) 

    # close the web driver

    def __init__(self):
        df = pd.read_excel("SWSG/categories/search_by_category.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        except_count = 0
        all_data = []
        all_data_with_images_count=[]

        while i < len(list_of_urls):
        # while i < 1:
            all_data,check_once = self.SearchingCategory(driver,list_of_urls[i],list_of_categories[i],all_data,check_once)
            i+=1

        df = pd.DataFrame(all_data)

        df.to_excel(excel_writer = f"SWSG/output_SWSG/{datetime.today().date()}_SWSG_search_by_category.xlsx")


  

class SWSG_Search_By_Category_SWSGOnly:
    
    def nextpagecheck(self,driver):
        total_pages = 1
        while True:
            try:
                button = driver.find_element(By.CSS_SELECTOR,"button[aria-label='move to the next page'")
                button.click()
                time.sleep(5)
                total_pages +=1
            except:
                break
        print(total_pages)
        return total_pages
    
    def fetch_pdp(self,driver, url,check_once):
    
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0
            sku = ""
            mpn = ""

            

            # try:
            if check_once == 0:
                driver.execute_script("window.open('');")
                check_once+=1
            driver.switch_to.window(driver.window_handles[1])
            driver.get(url)
            time.sleep(5)
            # driver.set_page_load_timeout(30)
            
            # try:
            #     ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
            #     model_id = ids.get_attribute("content")
            # except:
            #     # driver.close()
            #     driver.switch_to.window(driver.window_handles[0])
            #     model_id = ""
            
            # ---------------------For SKU --------------------------------
            try:
                sku_div = driver.find_element(By.CSS_SELECTOR,".ruk_rating_snippet")
                sku = sku_div.get_attribute("data-sku")
            except:
                pass
            print(sku)
            try:
                mpn_div = driver.find_element(By.XPATH,"//*[contains(text(), 'الموديل')]")
                mpn = mpn_div.text
                mpn = mpn.replace("الموديل","")
                mpn= mpn.replace(":","")
            except:
                pass
            print(mpn)
            # ---------------------For videos -----------------------------
            try:
                total_videos_tag = driver.find_elements(By.CSS_SELECTOR,"div[class='video-wrapper']")
                total_videos = len(total_videos_tag)
            except:
                total_videos = 0 
            # print("Total total_videos)
            # print("videos:",total_videos)
            # ----------------------Ending Video---------------------------
            
        
            try:
                product_info = driver.find_element(By.CSS_SELECTOR,".product-info-price")
                rating = product_info.find_element(By.CSS_SELECTOR,".tf-rating").text
                review = product_info.find_element(By.CSS_SELECTOR,".tf-count").text
            except:
                rating = 0
                review = 0
            
            # print("Rating:",rating)
            # print("Review:",review)
            try:
                # list_of_images = set()
                try:
                    images_list_container = driver.find_element(By.CSS_SELECTOR,".image-gallery-thumbnails-container")
                    list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                    # for imag in list_of_img_tags:
                    #     list_of_images.add(imag.get_attribute("src"))
                    total_images = len(list_of_img_tags)  
                except:
                    total_images = 0

            except:
                # driver.switch_to.window(driver.window_handles[0])
                total_images=0
            if total_videos >=1 and total_images>total_videos:
                total_images-=total_videos
            # print(total_images)
            # driver.close()
            driver.switch_to.window(driver.window_handles[0])
            return total_images,rating,review,total_videos,sku,mpn
            # except:
            #     driver.switch_to.window(driver.window_handles[0])
            #     return total_images,rating,review,total_videos,sku,mpn
    


    def InfiniteScrolling(self,driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    # Searching Category by Image count (SWSG Only)
    def SearchingCategoryBySWSGOnly(self,driver,Url_Link,cat_name,all_data_with_images_count,check_once):
        url = Url_Link
        driver.get(url)
        time.sleep(10)
        
        # Get scroll height
        # self.InfiniteScrolling(driver)
        total_pages = self.nextpagecheck(driver)
        time.sleep(5)
        pg = 1
        while pg <= total_pages:
            url = Url_Link + f"?page={pg}"
            driver.get(url)
        

            time.sleep(10)
            all_divs  = driver.find_elements(By.CSS_SELECTOR, ".home-products_grid_item-3F-")

            count =1
            number_of_products =0 
            
            for div in all_divs:
            # get all elements with the tag "a"
                title = div.find_element(By.CSS_SELECTOR,".home-product_name-ZHO")
                # print(title.text)
                link = div.find_element(By.TAG_NAME,"a")
                # img = div.find_element(By.CSS_SELECTOR,"img[class='product-image-photo']")
                price = div.find_element(By.CSS_SELECTOR,".productFullDetail-productPrice-1Js").text
                    
                if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("إل جى")!= -1 or title.text.find("ال جي") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                    brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى")!= -1)  else "Dyson"
                    title_name = title.text
                    # image_url = img.get_attribute("src")
                    img_link = link.get_attribute("href")
                    
                    total_images,rating,review,total_videos,sku,mpn = self.fetch_pdp(driver,img_link,check_once)
                    check_once+=1    
                    
                    data = {
                        "Date": datetime.today(),
                        "Region": "MEA",
                        "Country": "KSA",
                        "Retailer": "SWSG",
                        "category":  cat_name,
                        # "keyword": search_keyword,
                        "brand": brand_name,
                        "mpn": mpn,
                        "sku": sku,
                        "title":title_name,
                        "link": img_link,
                        "price":price,
                        "rating_count": rating,
                        "review_count": review,
                        "images_count": total_images,
                        "video_count": total_videos,
                        # "flex_match": "Yes" if flex_count==True else "No"
                        "flex_match": "No"
                        # "image url":image_url
                    }
                    

                    all_data_with_images_count.append(data)
                count+=1
                number_of_products+=1
            pg+=1
        return all_data_with_images_count,check_once
    
    
    # for dt in all_data:
    #     print(dt["images_count"]) 

    # close the web driver

    def __init__(self):
        df = pd.read_excel("SWSG/categories/search_by_category_using_swsgonly.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        except_count = 0
        all_data = []
        all_data_with_images_count=[]

        while i < len(list_of_urls):
        # while i < 1:
            all_data_with_images_count,check_once = self.SearchingCategoryBySWSGOnly(driver,list_of_urls[i],list_of_categories[i],all_data_with_images_count,check_once)
            i+=1

   
        df_with_image_count = pd.DataFrame(all_data_with_images_count)

        # df_with_image_count.to_excel(excel_writer = "output_SWSG/search_by_category_with_image_count.xlsx")
        # df.to_excel(excel_writer = "output_SWSG/search_by_category.xlsx")
        # # print(df)


        df_with_image_count.to_excel(excel_writer = f"SWSG/output_SWSG/{datetime.today().date()}_SWSG_search_by_category_with_image_count.xlsx")
    


  

# Extra



class Search_By_Category_with_extraonly:
    # initialize the web driver
    def fetch_pdp(self,driver, url,check_once):
            model_id = ""
            sku = ""
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                # driver.get("https://www.extra.com/ar-sa/white-goods/refrigerators/large/lg-refrigerator-17-2cu-ft-freezer-6cu-ft-inverter-compressor-white/p/100301826?algoliaQueryId=72960fa904f7563872a35aaefe1aa6ac")
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
                    ids = driver.find_element(By.CLASS_NAME,"head-attributes").get_attribute('textContent')
                    print(ids)
                    content_extraction = ids.replace("Model No: ","")
                    content_extraction = content_extraction.replace("رقم الموديل: ","")
                    content_extraction = content_extraction.replace("SKU: ", "")
                    content_extraction = content_extraction.replace("الرقم التسلسلي: ","")
                    content_extraction = content_extraction.replace("NJ0","")
                    content_extraction = content_extraction.replace("NK0","")
                    content_extraction = content_extraction.replace("NK1","")
                    content_extraction = content_extraction.replace("NR1","")
                    content_extraction = content_extraction.replace("NRO","")
                    content_extraction = content_extraction.replace("SN2","")
                    content_extraction=content_extraction.split(" ")
                    model_id = content_extraction[0]
                    sku = content_extraction[1]
                    print("Model ID: ", model_id)
                    print("SKU: ", sku)
                    
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                    sku = ""
                
                
                
                rating = 0
                review = 0
                try:
                    pop_up_box = driver.find_element(By.CLASS_NAME,"product-rating-container")
                    # Cant find the content inside the popup so we have  to add wait 
                    rating_review_container = pop_up_box.find_element(By.CLASS_NAME, "rating-overall").get_attribute('textContent')
                    rating_review_text = rating_review_container.replace(" التقييمات", "")
                    rating_review_text= rating_review_text.split(" ")
                    # rating_div = driver.find_element(By.CSS_SELECTOR,".reviews-visual")
                    rating = rating_review_text[0]
                    review = float(rating_review_text[1])
                    print("Rating:",rating_review_text[0])
                    print("Reviews:",rating_review_text[1])
                    # rating = float(rating_review_container.find_element(By.CLASS_NAME,"rating").get_attribute('textContent'))
                    # review = rating_review_container.find_element(By.CLASS_NAME,"reviews").get_attribute('textContent')
                    # print("Reviews:",review,"Rating:",rating)
                # except Exception as exc:
                except:
                    print("Rating:", rating, "Review:",review)
                    rating = 0
                    review = 0
                try:
                    list_of_images = set()
                    
                    while True:
                        try:
                            button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.TAG_NAME, "button"))
                            )
                            button.click()
                            time.sleep(5)
                            break
                        except:
                            break
                    
                    
                    images_list_container = driver.find_element(By.ID,"splide04")
                    list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                    for imag in list_of_img_tags:
                        list_of_images.add(imag.get_attribute("src"))
                
                    total_images = len(list_of_images)  
                    if total_images == 0:
                        images_list_container = driver.find_element(By.ID,"splide02")
                        list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                        for imag in list_of_img_tags:
                            list_of_images.add(imag.get_attribute("src"))
                    
                        total_images = len(list_of_images)  
                except:
                    driver.switch_to.window(driver.window_handles[0])
                    total_images=0
                print("Images:",total_images)
                # ---------------------For videos -----------------------------
                total_video_play_btn = 0
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-key-and-specifications-footer"))
                    )
                    text = element.text
                    print(text)

                    
                    # element = driver.find_element(By.XPATH, "//*[text()='تفاصيل أكثر عن المنتج']")

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", element)
                    print("Scrolling")
                    time.sleep(5)
                    # Click the element
                    driver.find_element(By.XPATH,"//*[text()='تفاصيل أكثر عن المنتج']").click()
                    
                    print("Clicked")
                    time.sleep(5)
                    total_videos_flex_ = driver.find_elements(By.TAG_NAME,"video")
                    print("total video tags:",len(total_videos_flex_))
                    total_videos_flex = driver.find_elements(By.CSS_SELECTOR,".flix-videoHtml.flix-show-formobile")
                    
                    total_videos += len(total_videos_flex_) -  len(total_videos_flex)
                
                except:
                    print("flix video not found")
                    pass
                try:
                    driver.find_element(By.CLASS_NAME,"video_play_btn")
                    total_videos +=1
                    total_video_play_btn = 1
                except:
                    pass
                
                
                # ----------------------Ending Video---------------------------
                
                print("videos:",total_videos)
                if total_video_play_btn > 0:
                    total_images -= total_video_play_btn
                # ----------------------Ending Video---------------------------
                flex_count = False
                try:
                    flex_count = True if driver.find_element(By.ID,"flix-inpage") else False
                    # print(flex_count)
                except:
                    flex_count = False
                    pass
                # driver.close()
                
                try: 
                    flex_id = driver.find_element(By.ID,"flix-inpage")
                    # Get the model id from flex_media
                    # Compare it 
                    # If match mpn_match = True
                    # Else
                    mpn_match = False
                    model_id_lower = model_id.lower()
                    mpn_match = False
                    if flex_id.find_element(By.CSS_SELECTOR,".flix-model-title").text.lower().find(model_id_lower):
                        mpn_match = True
                        print("Mpn matched")
                except:
                    mpn_match = False
                
                driver.switch_to.window(driver.window_handles[0])
                
                return model_id,sku,total_images,rating,review,total_videos,flex_count,mpn_match
            except:
                print("ERROR")
                driver.switch_to.window(driver.window_handles[0])
                return model_id,sku,total_images,rating,review,total_videos,flex_count,mpn_match
    # navigate to a website

    # url = "https://uae.sharafdg.com/c/home_appliances/laundry/washing_machines/"


    def extract_data_by_category(self,driver, url,cat_name,check_once,total_pages):

        
        all_data = []
        each_page = 0
        print (total_pages)
        while each_page<total_pages: 
            # Second last li of ul with id="hits-pagination"
            
            # Find out the total pages in the products
            
            # https://www.extra.com/en-sa/electronics/television/c/1-109
            Pages = f"/facet/?q=:relevance&text=&pageSize=96&pg={each_page}&sort=relevance"
            print(url+Pages)
            driver.get(url+Pages)
                # driver.set_page_load_timeout(30)
           
            
            ids = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR,".product-list"))
                    )
            # try:
            # ids = driver.find_element(By.CSS_SELECTOR,".product-list")
        
            all_divs  = ids.find_elements(By.CLASS_NAME, "main-section")
            
            for div in all_divs:
            # get all elements with the tag "a"
                
                title = div.find_element(By.CSS_SELECTOR, ".product-name-data")
                link = div.find_element(By.TAG_NAME,"a")
                # img_div = div.find_element(By.CSS_SELECTOR,".image-container")
                # multiple_img = img_div.find_elements(By.TAG_NAME,"img")
                # for im in multiple_img:
                #     image_url = im.get_attribute("src")
                #     break
                price = div.find_element(By.CLASS_NAME,"price")
                if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("إل جى")!= -1 or title.text.find("ال جي") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                
                    
                    title_name = title.text
                    price_ = price.text,
                    

                    img_link = link.get_attribute("href")
                    # full_title_arr = title.text.split()
                    brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى")!= -1)  else "Dyson"
                    
                    
                    mpn,sku,total_images,rating,review,total_videos,flex_count,mpn_match = self.fetch_pdp(driver,link.get_attribute("href"),check_once)
                    check_once+=1
                    print(flex_count)
                    
                    data = {
                        "Date": datetime.today(),
                        "Region": "MEA",
                        "Country": "KSA",
                        "Retailer": "Extra",
                        "category":  cat_name,
                        "brand": brand_name,
                    
                        "mpn": mpn,
                        "sku": sku,
                        "title":title_name,
                        "link": img_link,
                        "price":price_,
                        "rating_count": rating,
                        "review_count": int(review),
                        "images_count": total_images,
                        "video_count": total_videos,
                        # "image url":image_url,
                        "flex_match": "Yes" if flex_count==True else "No",
                        "mpn_match": "Yes" if mpn_match== True else "No"
                    }
                    print(data)
                    all_data.append(data)
            each_page+=1
            
            # except:
            #     pass
                
            # print(all_data)

            # close the web driver

        df = pd.DataFrame(all_data)
        # print(df)
        
        return df



   



    def __init__(self):
        # Reading the excel sheet
        df = pd.read_excel("Extra/categories/search_by_category_with_extra.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        except_count = 0
        while i < len(list_of_urls):
            # Finding the number of pages
            # And adding a list of 
            # storing the extracted data in df to be used in future
            driver.get(list_of_urls[i]+"/facet/?q=:relevance&text=&pageSize=96&pg=0&sort=relevance")
            time.sleep(4)
            try:
                all_pages_ul = driver.find_element(By.CLASS_NAME,"ul_container")
                # Pagination id = "hits-pagination"
                list_of_li = all_pages_ul.find_elements(By.TAG_NAME,"li")
                # print(int(list_of_li[-2].text))
                total_pages = int(list_of_li[len(list_of_li)-2].text)
                # print(total_pages)
                rtnData=self.extract_data_by_category(driver,list_of_urls[i],list_of_categories[i],check_once,total_pages)
                
                # appending the extracted data in the empty dataframe 
                dataframe_final = pd.concat([dataframe_final,rtnData])
                # dataframe_final.append(df)
                
                # printing dataframe final to show that the data is storing perfectly 
                print(dataframe_final) 
                # Printing completed to show that the urls are fetching the data 
                # print("completed")
                i+=1
                check_once+=1
            except:
                print("Except")
                except_count+=1
                if except_count >5:
                    total_pages = 1
                    rtnData=self.extract_data_by_category(driver,list_of_urls[i],list_of_categories[i],check_once,total_pages)
                    
                    # appending the extracted data in the empty dataframe 
                    dataframe_final = pd.concat([dataframe_final,rtnData])
                    # dataframe_final.append(df)
                    
                    # printing dataframe final to show that the data is storing perfectly 
                    # print(dataframe_final) 
                    # Printing completed to show that the urls are fetching the data 
                    # print("completed")
                    i+=1
                    except_count =0
                    check_once+=1
        # Closing the browser 

        driver.quit()

        # Printing the dataframe with all the data 
        print(dataframe_final)

        # Storing the dataframe in the text.xlsx file 
        dataframe_final.to_excel(excel_writer = f"Extra/output/{datetime.today().date()}_search_by_category_with_extraonly.xlsx")


        # self.UploadFileOnGoogleDrive(file_path)


class Search_By_category_without_extraonly:
    
    # initialize the web driver
    def fetch_pdp(self,driver, url,check_once):
            model_id = ""
            sku = ""
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(5)
                # driver.set_page_load_timeout(30)
                
                try:
                    ids = driver.find_element(By.CLASS_NAME,"head-attributes").get_attribute('textContent')
                    print(ids)
                    content_extraction = ids.replace("Model No: ","")
                    content_extraction = content_extraction.replace("رقم الموديل: ","")
                    content_extraction = content_extraction.replace("SKU: ", "")
                    content_extraction = content_extraction.replace("الرقم التسلسلي: ","")
                    content_extraction = content_extraction.replace("NJ0","")
                    content_extraction = content_extraction.replace("NK0","")
                    content_extraction = content_extraction.replace("NK1","")
                    content_extraction = content_extraction.replace("NR1","")
                    content_extraction = content_extraction.replace("NRO","")
                    content_extraction = content_extraction.replace("SN2","")
                    content_extraction=content_extraction.split(" ")
                    model_id = content_extraction[0]
                    sku = content_extraction[1]
                    print("Model ID: ", model_id)
                    print("SKU: ", sku)
                    
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                    sku = ""

                # ---------------------For videos -----------------------------
                total_video_play_btn = 0
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-key-and-specifications-footer"))
                    )
                    text = element.text
                    print(text)

                    
                    # element = driver.find_element(By.XPATH, "//*[text()='تفاصيل أكثر عن المنتج']")

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", element)
                    print("Scrolling")
                    time.sleep(5)
                    # Click the element
                    driver.find_element(By.XPATH,"//*[text()='تفاصيل أكثر عن المنتج']").click()
                    
                    print("Clicked")
                    time.sleep(5)
                    total_videos_flex_ = driver.find_elements(By.TAG_NAME,"video")
                    print("total video tags:",len(total_videos_flex_))
                    total_videos_flex = driver.find_elements(By.CSS_SELECTOR,".flix-videoHtml.flix-show-formobile")
                    
                    total_videos += len(total_videos_flex_) -  len(total_videos_flex)
                
                except:
                    print("flix video not found")
                    pass
                try:
                    driver.find_element(By.CLASS_NAME,"video_play_btn")
                    total_videos +=1
                    total_video_play_btn = 1
                except:
                    pass
                
                
                # ----------------------Ending Video---------------------------
                
                print("videos:",total_videos)
                if total_video_play_btn > 0:
                    total_images -= total_video_play_btn
                # ----------------------Ending Video---------------------------


                
                
                rating = 0
                review = 0
                try:
                    # rating_div = driver.find_element(By.CSS_SELECTOR,".reviews-visual")
                    rating = float(driver.find_element(By.CSS_SELECTOR,".js-pdp-ratings").get_attribute('textContent'))
                    review = driver.find_element(By.CSS_SELECTOR,".js-pdp-rreviews").get_attribute('textContent')
                    print(review,rating)
                except:
                    rating = 0
                    review = 0
                try:
                    list_of_images = set()
                 
                    images_list_container = driver.find_element(By.CLASS_NAME,"nav-container")
                    list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                    for imag in list_of_img_tags:
                        list_of_images.add(imag.get_attribute("src"))
                
                    total_images = len(list_of_images)  
                  
                except:
                    
                    total_images=0

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,sku,total_images,rating,review,total_videos
            except:
                return model_id,sku,total_images,rating,review,total_videos
    

    # url = "https://uae.sharafdg.com/c/home_appliances/laundry/washing_machines/"


    def extract_data_by_category(self,driver, url,cat_name,check_once):

        # url = "https://uae.sharafdg.com/?q=Air%20Purifier&post_type=product"
        # driver.get("https://www.extra.com/en-sa/tvs-entertainment/c/8003")
        # time.sleep(4)
        # slider=  driver.find_element(By.CSS_SELECTOR,".amp-dc-slider-slides.js_slides.slick.js-ampslider.slick-initialized.slick-slider.slick-dotted")
        # banner_images = slider.find_elements(By.TAG_NAME,"img")
        # print(len(banner_images))
        # for imag in banner_images:
        #     banner_src_path = imag.get_attribute("data-srcset")
        #     print("Image path:",banner_src_path)
        #     Calculate_Images(banner_src_path)
        driver.get(url)

        time.sleep(4)
        try:
            ids = driver.find_element(By.CLASS_NAME,"product-list")
        
            all_divs  = ids.find_elements(By.CLASS_NAME, "main-section")

            all_data = []
            count =1
            number_of_products = 0 
            for div in all_divs:
            # get all elements with the tag "a"
                
                title = div.find_element(By.CSS_SELECTOR, ".product-name-data")
                link = div.find_element(By.TAG_NAME,"a")
                # img_div = div.find_element(By.CSS_SELECTOR,".image-container")
                # multiple_img = img_div.find_elements(By.TAG_NAME,"img")
                # for im in multiple_img:
                #     image_url = im.get_attribute("src")
                #     break
                price = div.find_element(By.CLASS_NAME,"price")
                if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("إل جى") != -1 or title.text.find("ال جي") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                    title_name = title.text
                    price_ = price.text
                    img_link = link.get_attribute("href")
                    # full_title_arr = title.text.split()
                    brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى")!= -1)  else "Dyson"
                    
                    mpn,sku,total_images,rating,review,total_videos = self.fetch_pdp(driver,link.get_attribute("href"),check_once)
                    check_once+=1
                    
                    if number_of_products < 20:
                        data = {
                            "Date": datetime.today(),
                            "Region": "MEA",
                            "Country": "KSA",
                            "Retailer": "Extra",
                            "category":  cat_name,
                            "brand": brand_name,
                            "Rank": count,
                            "mpn": mpn,
                            "sku": sku,
                            "title":title_name,
                            "link": img_link,
                            "price":price_
                            # "image url":image_url,
                        }
                
                        all_data.append(data)
                count+=1
                number_of_products+=1
            
            
            
            
            
            # print(all_data)

            # close the web driver


            df = pd.DataFrame(all_data)
            # print(df)
            return df
        except:
            return False



    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        # Reading the excel sheet
        df = pd.read_excel("Extra/categories/search_by_category.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        while i < len(list_of_urls):

            # storing the extracted data in df to be used in future
            rtnData=self.extract_data_by_category(driver,list_of_urls[i],list_of_categories[i],check_once)
            if type(rtnData) == bool:
                pass
            else:
            # appending the extracted data in the empty dataframe 
                dataframe_final = pd.concat([dataframe_final,rtnData])
                # dataframe_final.append(df)
                
                # printing dataframe final to show that the data is storing perfectly 
                print(dataframe_final) 

                # Printing completed to show that the urls are fetching the data 
                print("completed")
                i+=1
            check_once+=1

        # Closing the browser 
        driver.quit()

        # Printing the dataframe with all the data 
        print(dataframe_final)

        # Storing the dataframe in the text.xlsx file 
        # dataframe_final.to_excel(excel_writer = "output/search_by_category_without_extraonly.xlsx")




        dataframe_final.to_excel(excel_writer = f"Extra/output/{datetime.today().date()}_search_by_category_without_extraonly.xlsx")
        




        # self.UploadFileOnGoogleDrive(file_path)


class Search_By_Keyword_without_extraonly:
# initialize the web driver


    def fetch_pdp(self,driver, url,check_once):
            model_id = ""
            sku = ""
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(5)
                # driver.set_page_load_timeout(30)
                
                try:
                    ids = driver.find_element(By.CLASS_NAME,"head-attributes").get_attribute('textContent')
                    print(ids)
                    content_extraction = ids.replace("Model No: ","")
                    content_extraction = content_extraction.replace("رقم الموديل: ","")
                    content_extraction = content_extraction.replace("SKU: ", "")
                    content_extraction = content_extraction.replace("الرقم التسلسلي: ","")
                    content_extraction = content_extraction.replace("NJ0","")
                    content_extraction = content_extraction.replace("NK0","")
                    content_extraction = content_extraction.replace("NK1","")
                    content_extraction = content_extraction.replace("NR1","")
                    content_extraction = content_extraction.replace("NRO","")
                    content_extraction = content_extraction.replace("SN2","")
                    content_extraction=content_extraction.split(" ")
                    model_id = content_extraction[0]
                    sku = content_extraction[1]
                    print("Model ID: ", model_id)
                    print("SKU: ", sku)
                    
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                    sku = ""

                


                
                
                rating = 0
                review = 0
                try:
                    # rating_div = driver.find_element(By.CSS_SELECTOR,".reviews-visual")
                    rating = float(driver.find_element(By.CSS_SELECTOR,".js-pdp-ratings").get_attribute('textContent'))
                    review = driver.find_element(By.CSS_SELECTOR,".js-pdp-rreviews").get_attribute('textContent')
                    print(review,rating)
                except:
                    rating = 0
                    review = 0
                try:
                    list_of_images = set()
                 
                    images_list_container = driver.find_element(By.CLASS_NAME,"nav-container")
                    list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                    for imag in list_of_img_tags:
                        list_of_images.add(imag.get_attribute("src"))
                
                    total_images = len(list_of_images)  
                  
                except:
                    
                    total_images=0

                # ---------------------For videos -----------------------------
                total_video_play_btn = 0
                try:
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-key-and-specifications-footer"))
                    )
                    text = element.text
                    print(text)

                    
                    # element = driver.find_element(By.XPATH, "//*[text()='تفاصيل أكثر عن المنتج']")

                    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", element)
                    print("Scrolling")
                    time.sleep(5)
                    # Click the element
                    driver.find_element(By.XPATH,"//*[text()='تفاصيل أكثر عن المنتج']").click()
                    
                    print("Clicked")
                    time.sleep(5)
                    total_videos_flex_ = driver.find_elements(By.TAG_NAME,"video")
                    print("total video tags:",len(total_videos_flex_))
                    total_videos_flex = driver.find_elements(By.CSS_SELECTOR,".flix-videoHtml.flix-show-formobile")
                    
                    total_videos += len(total_videos_flex_) -  len(total_videos_flex)
                
                except:
                    print("flix video not found")
                    pass
                try:
                    driver.find_element(By.CLASS_NAME,"video_play_btn")
                    total_videos +=1
                    total_video_play_btn = 1
                except:
                    pass
                
                
                # ----------------------Ending Video---------------------------
                
                print("videos:",total_videos)
                if total_video_play_btn > 0:
                    total_images -= total_video_play_btn
                # ----------------------Ending Video---------------------------
                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,sku,total_images,rating,review,total_videos
            except:
                driver.switch_to.window(driver.window_handles[0])
                return model_id,sku,total_images,rating,review,total_videos
    

    def extract_data_by_keyword(self,driver, url,cat_name,search_keyword,check_once):
        # url = "https://uae.sharafdg.com/?q=Air%20Purifier&post_type=product"
        driver.get(url)
        time.sleep(4)
        ids = driver.find_element(By.CLASS_NAME,"product-list")
        
        all_divs  = ids.find_elements(By.CLASS_NAME, "main-section")

        all_data = []
        count =1
        number_of_products=0
        for div in all_divs:
        # get all elements with the tag "a"
            title = div.find_element(By.CSS_SELECTOR, ".product-name-data")
            link = div.find_element(By.TAG_NAME,"a")
            # img_div = div.find_element(By.CSS_SELECTOR,".image-container")
            # multiple_img = img_div.find_elements(By.TAG_NAME,"img")
            # for im in multiple_img:
            #     image_url = im.get_attribute("src")
            #     break
            price = div.find_element(By.CLASS_NAME,"price")
            
            if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1 )  else "Dyson"
                title_name = title.text
                price_ = price.text,
                img_link = link.get_attribute("href")
                full_title_arr = title.text.split()
                if number_of_products < 20:
                    mpn,sku,total_images,rating,review,total_videos  = self.fetch_pdp(driver,link.get_attribute("href"),check_once)
                    print(rating)
                    print(review)
                    data = {
                        "Date": datetime.today(),
                        "Region": "MEA",
                        "Country": "KSA",
                        "Retailer": "Extra",
                        "category":  cat_name,
                        "keyword": search_keyword,
                        "brand": brand_name,
                        "Rank": count,
                        "mpn": mpn,
                        "sku": sku,
                        "title":title_name,
                        "link": img_link,
                        "price":price_
                        # "image url":image_url,
                    }
                    check_once+=1    
                    all_data.append(data)
            count+=1
            number_of_products+=1
        # print(all_data)

        # close the web driver


        df = pd.DataFrame(all_data)
        # print(df)
        return df


    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        # -------------------------------------------------------------------------------------
        # For Search Keywords
        # Reading the excel sheet
        df = pd.read_excel("Extra/search_keywords/by_search_keywords.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []
        list_of_keywords = []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['keywords']:
            list_of_keywords.append(dt)
            testing_url = f"https://www.extra.com/ar-sa/search?q={dt}:relevance&text={dt}&pageSize=96&pg=0&sort=relevance"
            list_of_urls.append(testing_url)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()

        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0

        while i < len(list_of_urls):

            
            # storing the extracted data in df to be used in future
            rtnData=self.extract_data_by_keyword(driver,list_of_urls[i],list_of_categories[i],list_of_keywords[i],check_once)
            if type(rtnData) == bool:
                pass
            else:
            # appending the extracted data in the empty dataframe 
                dataframe_final = pd.concat([dataframe_final,rtnData])
                # dataframe_final.append(df)
                
                # printing dataframe final to show that the data is storing perfectly 
                # print(dataframe_final) 

                # Printing completed to show that the urls are fetching the data 
                print("completed")
                i+=1
            check_once+=1
        # Closing the browser 
        driver.quit()

        # Printing the dataframe with all the data 
        print(dataframe_final)

        # Storing the dataframe in the text.xlsx file 
        # dataframe_final.to_excel(excel_writer = "output/search_by_keyword_without_extraonly.xlsx")




        dataframe_final.to_excel(excel_writer = f"Extra/output/{datetime.today().date()}_search_by_keyword_without_extraonly.xlsx")
# Extra Ends Here



# Almanea -------------------------
class Almanea_Search_By_Keyword:
    def extract_data_by_keyword(self,driver, url,cat_name,search_keyword,check_once,all_data):
    
        driver.get(url)
        # Get scroll height
        # InfiniteScrolling()

        time.sleep(5)
        try:
            main_id  = driver.find_element(By.CSS_SELECTOR, ".products.list.items.product-items")
        except:
            return all_data,check_once
        all_divs  = main_id.find_elements(By.TAG_NAME, "li")

        # print(len(all_divs))

        count =1
        number_of_products = 0
        for div in all_divs:
        # get all elements with the tag "a"
            title = div.find_element(By.CSS_SELECTOR,".product.name.product-item-name")
            # print(title.text)
            link = div.find_element(By.CSS_SELECTOR,".product-item-link")
            # img = div.find_element(By.TAG_NAME,"img")
            price = div.find_element(By.CSS_SELECTOR,".price")

            if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1  or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1 )  else "Dyson"
                price = price.text
                title_name = title.text
                # image_url = img.get_attribute("src")
                img_link = link.get_attribute("href")
                
                
                sku_div = div.find_element(By.CSS_SELECTOR,"form[data-role='tocart-form']")
                sku = sku_div.get_attribute("data-product-sku")

                # total_images,rating,review,total_videos = fetch_pdp(driver,img_link,check_once)
                
                if number_of_products < 20:
                    data = {
                            "Date": datetime.today(),
                            "Region": "MEA",
                            "Country": "KSA",
                            "Retailer": "Almanea",
                            "category":  cat_name,
                            "keyword": search_keyword,
                            "brand": brand_name,
                            "Rank": count,
                            "mpn": "",
                            "sku": sku,
                            "title":title_name,
                            "link": img_link,
                            "price":price,
                            # "image url":image_url,
                    }
                    check_once+=1    

                    all_data.append(data)
                elif number_of_products >20:
                    break
            count+=1
            number_of_products+=1
        return all_data,check_once



   
    def __init__(self):
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        # -------------------------------------------------------------------------------------
    
        df = pd.read_excel("Almanea/search_keywords/by_search_keywords.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []
        list_of_keywords = []


        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['keywords']:
            list_of_keywords.append(dt)
            
            testing_url = f"https://almanea.sa/ar/catalogsearch/result/index/?cat=&q={dt}&product_list_limit=all"
            list_of_urls.append(testing_url)

        i=0 
        check_once = 0
        all_data = []
        while i < len(list_of_urls):

            
            # storing the extracted data in df to be used in future
            all_data,check_once =self.extract_data_by_keyword(driver,list_of_urls[i],list_of_categories[i],list_of_keywords[i],check_once,all_data)
            i+=1
            check_once+=1
        # Closing the browser 
        driver.quit()
        dataframe_final = pd.DataFrame(all_data)
        # Printing the dataframe with all the data 
        print(dataframe_final)


        dataframe_final.to_excel(excel_writer = f"Almanea/output/{datetime.today().date()}_Almanea_search_by_keyword.xlsx")






class Almanea_Search_By_Category:
    
    # def InfiniteScrolling(self,driver):
    #     last_height = driver.execute_script("return document.body.scrollHeight")
    #     while True:
    #         # Scroll down to bottom
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #         # Wait to load page
    #         time.sleep(4)

    #         # Calculate new scroll height and compare with last scroll height
    #         new_height = driver.execute_script("return document.body.scrollHeight")
    #         if new_height == last_height:
    #             break
    #         last_height = new_height
    def ShowAllProducts(self,driver):
        
        while True:
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".button.full-button.w-full.secondary.secondary-full.px-1.border.border-blue-dark"))
                    )
                    button.click()
                    time.sleep(4)
                except:
                    break
     
        
    def SearchingCategory(self,driver,Url_Link,cat_name,all_data,check_once):
        url = Url_Link
        driver.get(url)
        # self.ShowAllProducts(driver)
        # Get scroll height
        # self.InfiniteScrolling(driver)

        time.sleep(5)
        # ids = driver.find_element(By.ID,"moreLoadedProducts")
       
        try:
            main_id  = driver.find_element(By.CSS_SELECTOR, ".products.list.items.product-items")
        except:
            return all_data,check_once
        all_divs  = main_id.find_elements(By.TAG_NAME, "li")

        # print(len(all_divs))

        count =1
        number_of_products =0 
        
        for div in all_divs:
        # get all elements with the tag "a"
            title = div.find_element(By.CSS_SELECTOR,".product.name.product-item-name")
            # print(title.text)
            link = div.find_element(By.CSS_SELECTOR,".product-item-link")
            # img = div.find_element(By.CSS_SELECTOR,"img[class='product-image-photo lazy-loaded transition']")

            price = div.find_element(By.CSS_SELECTOR,".price")

            if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1  or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                
                brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1 )  else "Dyson"
                price = price.text
                title_name = title.text
                # image_url = img.get_attribute("src")
                img_link = link.get_attribute("href")
                
                sku_div = div.find_element(By.CSS_SELECTOR,"form[data-role='tocart-form']")
                sku = sku_div.get_attribute("data-product-sku")
                
                check_once+=1    
                
                
                if number_of_products < 20:
                    data_without_image = {
                        "Date": datetime.today(),
                        "Region": "MEA",
                        "Country": "KSA",
                        "Retailer": "Almanea",
                        "category":  cat_name,
                        # "keyword": search_keyword,
                        "brand": brand_name,
                        "Rank": count,
                        "mpn": "",
                        "sku": sku,
                        "title":title_name,
                        "link": img_link,
                        "price":price,
                        # "image url":image_url,
                    }
                    all_data.append(data_without_image)

                
            count+=1
            number_of_products+=1
        return all_data,check_once
    
    
    # Searching Category by Image count (SWSG Only)
   
    
    # for dt in all_data:
    #     print(dt["images_count"]) 

    # close the web driver

    def __init__(self):
        df = pd.read_excel("Almanea/categories/search_by_category_latest.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        driver.get("https://almanea.sa/en/")
        list_of_images = []
        elements = driver.find_elements(By.CSS_SELECTOR,"rs-sbg")
        for elm in elements:
            data_lazyload_value = elm.get_attribute('data-lazyload')
            list_of_images.append(data_lazyload_value)
            
       
        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        except_count = 0
        all_data = []
        all_data_with_images_count=[]

        while i < len(list_of_urls):
        # while i < 1:
            all_data,check_once = self.SearchingCategory(driver,list_of_urls[i],list_of_categories[i],all_data,check_once)
            i+=1

        df = pd.DataFrame(all_data)
     


        df.to_excel(excel_writer = f"Almanea/output/{datetime.today().date()}_Almanea_search_by_category.xlsx")


  

class Almanea_Search_By_Category_AlmaneaOnly:
    

    def fetch_pdp(self,driver,url,check_once):
    
            total_images = 0
            rating = 0
            review = 0
            total_videos = 0
            sku = ""
            flex_count = False
            mpn_match = False
            model_id=""
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                # driver.get("https://www.almanea.sa/product/lg-4k-uhd-50-inch-77-series-quad-core-processor-active-hdr-cinema-screen-arabic-ai-50up7750pvb-p-0902250411")
                page_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );")
                # Scroll to the middle of the page
                scroll_position = page_height / 2
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                # try:
                #     ids = driver.find_element(By.XPATH,"//meta[@itemprop='mpn']")
                #     model_id = ids.get_attribute("content")
                # except:
                #     # driver.close()
                #     driver.switch_to.window(driver.window_handles[0])
                #     model_id = ""
                
                try:
                    # ids = driver.find_element(By.CSS_SELECTOR,".font-semibold.text-xl.my-2")
                    # sku = driver.find_element(By.CLASS_NAME,"font-semibold text-xl my-2").text
                    sku_div = driver.find_element(By.XPATH, "//h5[text()='كود المنتج']")
                    sku = sku_div.text
                    sku = sku.replace("كود المنتج :", "")
                except:
                    pass
                print("Sku:", sku)
                # try:
                script_element = driver.find_element(By.CSS_SELECTOR, "script[data-flix-mpn]")
                data_flix_mpn_value = script_element.get_attribute("data-flix-mpn")
                model_id = data_flix_mpn_value
                # except:
                #     pass
                print("Model number:",model_id)
                flex_count = False
                try:
                    flex_count = True if driver.find_element(By.CSS_SELECTOR,"a[title='Flixmedia Minisite'") else False
                    print(flex_count)
                except:
                    flex_count = False
                    pass
                # ---------------------For videos -----------------------------
                try:
                    swiper_id = driver.find_element(By.CSS_SELECTOR,".swiper-wrapper")
                    total_videos = swiper_id.find_elements(By.TAG_NAME,"video")
                    total_videos = len(total_videos)
                    
                except:
                    total_videos = 0
                    pass

                try:

                    total_videos_flex_ = driver.find_elements(By.TAG_NAME,"video")

                    total_videos_flex = driver.find_elements(By.CSS_SELECTOR,".flix-videoHtml.flix-show-formobile")
                    
                    total_videos += len(total_videos_flex_) -  len(total_videos_flex)
                    
                except:
                    pass

                
                # ----------------------Ending Video---------------------------
                try:
                    total_v = driver.find_elements(By.ID,"flix_product_video")
                    total_videos += len(total_v)
                except:
                    print("No play videos")
                

            
                try:
                    rating_div = 0
                    rating= 0
            
                except:
                    rating = 0

                try:
                    review_div = 0
                    review = 0
                except:
                    review = 0 
                try:
                    list_of_images = set()
                    try:
                        images_list_container = driver.find_element(By.CSS_SELECTOR,".swiper-wrapper")
                        list_of_img_tags = images_list_container.find_elements(By.TAG_NAME,"img")
                        for imag in list_of_img_tags:
                            list_of_images.add(imag.get_attribute("src"))

                        total_images = len(list_of_images)  
                    except:
                        total_images = 0
                except:
                    # driver.switch_to.window(driver.window_handles[0])
                    total_images=0
                print("Videos:",total_videos, " \tImages:",total_images," \tmpn:",model_id," \t")
                print(total_images) 

                model_id_lower = model_id.lower()
                mpn_match = False
                print (driver.find_element(By.CSS_SELECTOR,".flix-model-title").text.lower())
                if driver.find_element(By.CSS_SELECTOR,".flix-model-title").text.lower().find(model_id_lower):
                    mpn_match = True
                    print("Mpn matched")
                try:
                    # video_frames = driver.find_elements(By.CSS_SELECTOR,".flix-videodiv.inpage_selector_video")
                    video_frames = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".flix-videodiv.inpage_selector_video"))
                    )
                    for video_f in video_frames:
                        ifrm = video_f.find_element(By.TAG_NAME,"iframe")
                        driver.switch_to.frame(ifrm)
                        iframeVideoPresent = 1 if driver.find_elements(By.CSS_SELECTOR,".jw-preview.jw-reset") else 0 
                        total_videos += iframeVideoPresent
                        driver.switch_to.default_content()
                        print("Found vid",iframeVideoPresent)
                    print("Total Videos:",total_videos)
                    # total_videos += len(total_video_inpage)
                    # print("Play:",len(total_video_inpage))
                except:
                    print("No Inpage videos")
                # print("videos:",total_videos)

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return total_images,review,rating,total_videos,flex_count,mpn_match,model_id,sku
            except:
                driver.switch_to.window(driver.window_handles[0])
                return total_images,review,rating,total_videos,flex_count,mpn_match,model_id,sku

    def InfiniteScrolling(self,driver):
        end_height = driver.execute_script("return document.body.scrollHeight")
        print(end_height)
        starting_height = 0
        new_scroll_position = end_height - 1000

        last_height = new_scroll_position
        while True:
            # Get the current scroll height
      

            # Scroll to the new position
            driver.execute_script(f"window.scrollTo({starting_height}, {last_height});")

            # Wait for the page to load
            time.sleep(5)

            end_height = driver.execute_script("return document.body.scrollHeight")
            new_scroll_position = end_height - 1000
            new_height = new_scroll_position
            # Calculate the new scroll height
            

            # If the new scroll height is the same as the old one, we've reached the end of the page
            if new_height == last_height:
                break
            starting_height = last_height
            last_height = new_height

    def ShowAllProducts(self,driver):
        
        while True:
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".button.full-button.w-full.secondary.secondary-full.px-1.border.border-blue-dark"))
                    )
                    button.click()
                    time.sleep(4)
                except:
                    break

    
    
    def SearchingCategoryByAlmaneaonly(self,driver,Url_Link,cat_name,all_data_with_images_count,check_once):
        url = Url_Link
        print(url)
        driver.get(url)
       
        self.InfiniteScrolling(driver)
        time.sleep(5)
        # try:
        try:
            main_id  = driver.find_element(By.CSS_SELECTOR, "div[class='grid grid-cols-4 lg:grid-cols-3 md:grid-cols-2 gap-2']")
        except:
            return all_data_with_images_count,check_once
        all_divs = main_id.find_elements(By.CSS_SELECTOR, "div")

        # Filter out only the direct child div elements
        child_divs = [div for div in all_divs if div.find_element(By.XPATH, "./parent::*") == main_id]
        # all_divs  = main_id.find_elements(By.CSS_SELECTOR, "div[class='text-zinc-700 border p-2 rounded-md relative h-full flex flex-col justify-between undefined overflow-hidden']")
        all_divs = child_divs
        
        print("Total Divs:",len(all_divs))

        total_conditions_exec = 1
        count =1
        number_of_products =0 
        
        for div in all_divs:
                
                if len(all_divs) == total_conditions_exec:
                        break
                else:
        # get all elements with the tag "a"
            # cond = True
            # while(cond):
                # try:
                    # title = div.find_element(By.CSS_SELECTOR,"a.font-semibold.text-right") 
           
                        print(total_conditions_exec)
                        title = div.find_element(By.CSS_SELECTOR,"a[class='cursor-pointer font-semibold text-right']") 
                        # print(title.text)
                        # link = div.find_element(By.CSS_SELECTOR,"a[class='cursor-pointer']")
                        # img = div.find_element(By.CSS_SELECTOR,"img[class='product-image-photo lazy-loaded transition']")
                        price = div.find_element(By.CSS_SELECTOR,".text-red.text-center")

                        if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) or (title.text.find("إل جي") != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1 or title.text.find('LG') != -1) or (title.text.find("دايسون") != -1 or title.text.find('Dyson') != -1):
                            brand_name = "samsung" if (title.text.find('سامسونج') != -1 or title.text.find('SAMSUNG') != -1) else "LG" if (title.text.find("إل جي") != -1 or title.text.find('LG') != -1 or title.text.find("ال جي") != -1 or title.text.find("إل جى") != -1)  else "Dyson"
                            print(brand_name)
                            price = price.text
                            title_name = title.text
                            # image_url = img.get_attribute("src")
                            img_link = title.get_attribute("href")
                            print(img_link)
                        
                            
                            total_images,review,rating,total_videos,flex_count,mpn_match,model_id,sku = self.fetch_pdp(driver,img_link,check_once)
                            
                            check_once+=1    
                            # print(review)
                            # print(rating)
                            data = {
                                "Date": datetime.today(),
                                "Region": "MEA",
                                "Country": "KSA",
                                "Retailer": "Almanea",
                                "category":  cat_name,
                                # "keyword": search_keyword,
                                "brand": brand_name,
                                "mpn": model_id,
                                "sku": sku,
                                "title":title_name,
                                "link": img_link,
                                "price":price,
                                "rating_count": rating,
                                "review_count": review,
                                "images_count": total_images,
                                "video_count": total_videos,
                                "flex_match": "Yes" if flex_count==True else "No",
                                "mpn_match": "Yes" if mpn_match== True else "No"
                                # "image url":image_url
                            }
                            

                            all_data_with_images_count.append(data)
                        count+=1
                        total_conditions_exec+=1
                        number_of_products+=1
                    # cond = False
                
                  
        return all_data_with_images_count,check_once
    
    
    # for dt in all_data:
    #     print(dt["images_count"]) 

    # close the web driver

    def __init__(self):
        df = pd.read_excel("Almanea/categories/search_by_category_latest.xlsx")

        # Created the empty list to store the list of urls 
        list_of_urls = []
        list_of_categories= []

        for dt in df['category_names']:
            list_of_categories.append(dt)

        # Looping through each url to fetch the data 
        for dt in df['urls']:
            list_of_urls.append(dt)
        # print(df)

        # Created an empty dataframe
        dataframe_final = pd.DataFrame()
       
        driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
        driver.maximize_window()
        # Looping through each url in the list and extracting the data 
        i=0 
        check_once = 0
        except_count = 0
        all_data = []
        all_data_with_images_count=[]

        while i < len(list_of_urls):
        # while i < 1:
            all_data_with_images_count,check_once = self.SearchingCategoryByAlmaneaonly(driver,list_of_urls[i],list_of_categories[i],all_data_with_images_count,check_once)
            i+=1

   
        df_with_image_count = pd.DataFrame(all_data_with_images_count)

      


        df_with_image_count.to_excel(excel_writer = f"Almanea/output/{datetime.today().date()}_Almanea_search_by_category_with_image_count.xlsx")
        
# Almanea Ends here 





# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("OSM SAUDI")
        
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

       

        extra_btn=tk.Button(root)
        extra_btn["anchor"] = "center"
        extra_btn["bg"] = "#0279c1"
        extra_btn["borderwidth"] = "0px"
        ft = tkFont.Font(family='Arial Narrow',size=13)
        extra_btn["font"] = ft
        extra_btn["fg"] = "#ffffff"
        extra_btn["justify"] = "center"
        extra_btn["text"] = "eXtra"
        extra_btn["relief"] = "raised"
        extra_btn.place(x=90,y=190,width=150,height=70)
        extra_btn["command"] = self.start_tasks_extra
        
    

        
        SWSG=tk.Button(root)
        SWSG["anchor"] = "center"
        SWSG["bg"] = "#009841"
        SWSG["borderwidth"] = "0px"
        
        SWSG["font"] = ft
        SWSG["fg"] = "#ffffff"
        SWSG["justify"] = "center"
        SWSG["text"] = "SWSG"
        SWSG["relief"] = "raised"
        SWSG.place(x=250,y=190,width=150,height=70)
        SWSG["command"] = self.start_tasks_SWSG

    
        Almanea_BTN=tk.Button(root)
        Almanea_BTN["anchor"] = "center"
        Almanea_BTN["bg"] = "#05294d"
        Almanea_BTN["borderwidth"] = "0px"
        
        Almanea_BTN["font"] = ft
        Almanea_BTN["fg"] = "#ffffff"
        Almanea_BTN["justify"] = "center"
        Almanea_BTN["text"] = "Almanea"
        Almanea_BTN["relief"] = "raised"
        Almanea_BTN.place(x=410,y=190,width=150,height=70)
        Almanea_BTN["command"] = self.start_tasks_almanea

    def extra_btn_command(self):

        list_of_extra = [
            Search_By_Category_with_extraonly,
            # Search_By_category_without_extraonly,
            # Search_By_Keyword_without_extraonly
            
            ]
        # list_of_extra = [Search_By_Category_with_extraonly]
        
        thread_list = [threading.Thread(target=func) for func in list_of_extra]

        # start all the threads
        for thread in thread_list:
            thread.start()

 

    def SWSG_command(self):

        list_of_SWSG = [
                        # SWSG_Search_By_Keyword
                        # ,
                        # SWSG_Search_By_Category
                        # ,
                        SWSG_Search_By_Category_SWSGOnly
                        ]

        thread_list = [threading.Thread(target=func) for func in list_of_SWSG]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_tasks_SWSG(self):
        thread = threading.Thread(target=self.SWSG_command)
        thread.start()

 
    def Almanea_command(self):

        list_of_almanea = [
                        #  Almanea_Search_By_Keyword
                        #  ,
                        #  Almanea_Search_By_Category
                        #  ,
                         Almanea_Search_By_Category_AlmaneaOnly,
                         ]
        # list_of_almanea = [Almanea_Search_By_Keyword]

        thread_list = [threading.Thread(target=func) for func in list_of_almanea]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()

  
   
    def start_tasks_almanea(self):
        thread = threading.Thread(target=self.Almanea_command)
        thread.start()

    
    
    def start_tasks_extra(self):
        thread = threading.Thread(target=self.extra_btn_command)
        thread.start()   

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
    
