from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import time
import pyperclip
import datetime
from g4f.client import Client

user_data_dir = r'C:\\Users\\mkmis\\AppData\\Local\\Google\\Chrome\\User Data\\profile'
sen = input("Enter the person name :- ")
sender = sen.capitalize()
count = 0

sen_xpath = f'//span[@title="{sender}"]'


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
driver = webdriver.Chrome(chrome_options)
chrome_options.add_argument('--log-level=3')
wait = WebDriverWait(driver , 10)
driver.maximize_window()

# driver.execute_script("window.open('', '_blank');")

# driver.switch_to.window(driver.window_handles[1])
driver.get("https://web.whatsapp.com/")
time.sleep(10)


element = wait.until(EC.presence_of_element_located((By.XPATH, sen_xpath)))
element.click()

while count<=30:
    

    time.sleep(2)
    # print(sen_xpath)
    latest_message_element = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="pane-side"]/div[1]/div/div/div[1]/div/div/div/div[2]/div[2]/div[1]/span/span')))

    latest_message = latest_message_element[0].text
    print("Message -:", latest_message)
    if count==0:
        client = Client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages =  [  
            {'role':'system', 'content':'Your are the friendy chatbot. you have to do chat like a actual person do in whatsApp. Keep in mind your chat should normal and gental and reply the user in same lanuage'},
            {'role':'user','content': latest_message},  
            {'role':'assistant','content': 'you should chat in 2 or 3 word in chat to act like a actual person.'},
            
            ]

        )
        print(response.choices[0].message.content)
        reply = response.choices[0].message.content
        fin_reply = [reply]
        print(fin_reply)
       
    else:
        pass

    with open("Message.txt","r") as f:
        file = f.read()
    
    
    if latest_message in file and reply in fin_reply :
        count +=1
        print(count)
        if count == 20:
            with open("Message.txt","w") as f:
                pass
            driver.quit()
    else:
            
        with open("Message.txt","a", encoding="utf-8") as f:      
            files = f.write(f"Message-: {latest_message},\n Reply:-{reply}\n")
                
        count = 0
        time.sleep(2)
        
        msg = reply
                
        pyperclip.copy(msg)
        new_msg_box='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
        msg_box = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        element = driver.find_element(By.XPATH, msg_box)
        time.sleep(1) 
        element.send_keys(Keys.CONTROL,'v')
        # element.send_keys(reply)
        element.send_keys(Keys.ENTER)
print("Clearing logfile...")

