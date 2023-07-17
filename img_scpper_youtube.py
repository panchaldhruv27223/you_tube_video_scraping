import requests
from bs4 import BeautifulSoup as bs 
from urllib.request import urlopen
import logging
from selenium import webdriver
import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from flask import Flask,url_for,redirect,render_template ,request
s=Service(ChromeDriverManager().install())
import datetime
import time
import csv

logging.basicConfig(filename= "logging_scpper.log" , level=logging.INFO , format="%(asctime)s %(name)s %(levelname)s %(message)s")
app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def welcome():
    return render_template("index.html")



@app.route("/p_data",methods=['GET','POST'])
def main():
    if(request.method == "POST"):
        try:
            driver = webdriver.Chrome(service=s)
            
            user_input = request.form['u_data']
            if (user_input == " ")or (len(user_input) ==0):
                return "we did not get query .. try again"
            
            logging.info("we got query")

            

            driver.get(f"https://www.youtube.com/@{user_input}/videos")
            
            try:
                logging.info("we are start on working.")
                links = driver.find_elements(By.TAG_NAME,"a")
                videolinks = []
                for i in links :
                    url = i.get_attribute('href')
                    videolinks.append(url)
                del videolinks[0:18]

                url_list =[]

                for i in videolinks:
                    if i == None:
                        continue
                    elif i not in url_list :
                        url_list.append(i)

                logging.info("we got videos link")
            except:
                logging.error("we are not able to get video link.")
            
            try:
                TI = driver.find_elements(By.CLASS_NAME,"style-scope ytd-rich-grid-media")
                logging.info("now we are at step two")
                title =[]
                view = []
                time = []
                mix_data =[]
                for i in TI :
                    mix_data.append(i.text)

                for i in mix_data[0:6]:
                    sp = i.split("\n")
                    title.append(sp[1])
                    view.append(sp[2])
                    time.append(sp[3])

            except:
                logging.error("we are not able to get title , view ...")

            try :
                logging.info("we are ready to go and find thumbnails")
                thumb = driver.find_elements(By.TAG_NAME,"img")
                thumb_img = []
                for i in thumb:
                    thumb_img.append(i.get_attribute("src"))
                del thumb_img[0:8]

                thumb_list = []
                for i in thumb_img:
                    if i == None:
                        continue
                    elif i not in thumb_list :
                        thumb_list.append(i)
            except:
                logging.error("we are not able to get thumbnails..")

            try:
                my_data= {}
                for_csv = []
                n = 0
                while n<50:
                    my_data[n] =[url_list[n],thumb_list[n],title[n],view[n],time[n]]
                    for_csv.append([url_list[n],thumb_list[n],title[n],view[n],time[n]])
                    n = n+1

                with  open("data.csv" , "w",encoding="utf-8") as f :
                    wr =csv.writer(f) 
                    
                    for i in for_csv:
                        wr.writerow(i)

            except:
                logging.error("we can not store data")

             
            
        
        except:
            logging.error("we are not able to execute user query")

        return render_template("result.html" , for_csv=my_data.items())

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)