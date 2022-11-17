import random, logging, re, sys, os, random, base64, time, json, hashlib
from urllib.parse import urlencode, quote_plus, unquote
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
#from screenshot import Screenshot as WASHOT
import argparse
import csv 
#https://sister.agenziaentrate.gov.it/Servizi/SceltaServizio.do?area=Consultazioni%20e%20Certificazioni
username = "SCRGLG95L19E919H" 
passw = "gPASSERI27."
login_link = "https://iampe.agenziaentrate.gov.it/sam/UI/Login?realm=/agenziaentrate"
action_link = "https://sister.agenziaentrate.gov.it/Visure/Informativa.do?tipo=/T/TM/VCVC_"
second_action_xpath = '//ul[@id="menu-left"]/li/a[text()="Immobile"]'
command_executor = "http://135.181.83.47:4444/wd/hub"
driver = None
login_link_tab = '//a[@aria-controls="tab-form"]'
login_link_tab_sister = '//a[@aria-controls="tab-sister"]'
input_username = '//input[@id="username-sister"]'
input_passw = '//input[@id="password-sister"]'
btn_passw = '//div[@id="tab-sister"]//button[contains(@class,"btn-accedi")]'
property_list = []
option_selection1=input('what Territorio do you want to scrape ? ')

def log(f,msg):
    print("%s ==> %s" %(f,msg))

def get_driver():
	#options
    myproxy = None
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    #options.add_argument("--disable-blink-features")
   # options.add_argument("--disable-infobars")
    #prefs = {"profile.default_content_setting_values.notifications" : 2}
    #options.add_experimental_option("prefs",prefs)
    #options.add_argument("--disable-blink-features=AutomationControlled")
   # options.add_argument('--headless')
    #options.add_argument('-no-sandbox')
    #options.add_argument('-disable-dev-shm-usage')
    #options.add_argument("--start-maximized")
    #ua = UserAgent()
    #options.add_argument('--user-agent="%s"' % ua.random)
    if myproxy:
        options.add_argument('--proxy-server=%s' % myproxy)
    else:
        log(sys._getframe().f_code.co_name,'PROXY IS NOT USED!')
    
    
    
    
    try:
        driver = webdriver.Chrome(
            options=options,
            #command_executor=command_executor,
            desired_capabilities={
                'applicationName':'nodewin_tr_1',
                'browserName': 'chrome',
                'javascriptEnabled': True,
                'acceptInsecureCerts': True,
                'platform': 'WINDOWS'
            }
        )
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'driver not working: %s, %s, %s'% (t,val,tb))
        return False
    return driver
    
def stop_driver(driver):
    if not driver:
        log(sys._getframe().f_code.co_name,'no driver to quit')
        return True
    
    
    try:
        driver.find_element_by_xpath('//a[contains(@href,"CloseSessionsSis")]').click()
        time.sleep(10)
        log(sys._getframe().f_code.co_name,'logout_link_btn click is ok: %s'% login_link_tab)
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'logout_link_btn failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        driver.quit()
        log(sys._getframe().f_code.co_name,'driver quit is done')
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'driver quit failed: %s, %s, %s'% (t,val,tb))
        return False
    
    return True
 

#this fct gets the prop_list for the folgios   
def get_link(driver, link, t, args):
    try:
        driver.get(link)
        log(sys._getframe().f_code.co_name,'link opened and waiting: %s'% link)
        time.sleep(int(t))
        
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'link did not open: %s, %s, %s'% (t,val,tb))
        try:
            driver.quit()
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'driver quit failed: %s, %s, %s'% (t,val,tb))
        return False
    
    
    try:
        driver.find_element_by_xpath('//a[contains(text(),"Conferma Lettura")]').click()
        time.sleep(5)
        log(sys._getframe().f_code.co_name,'conferma link click is ok: %s'% login_link_tab)
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'conferma link failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        driver.find_element_by_xpath('//select[@name="listacom"]/option[contains(text(),"'+option_selection1+'")]').click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'selection 1 is ok   click is ok: %s'% login_link_tab)
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'bologna selection link failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        driver.find_element_by_xpath('//form[@name="DataRichiestaForm"]//input[contains(@value,"Applica")]').click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'bologna form btn click is ok: %s'% login_link_tab)
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'bologna form btn link failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        driver.find_element_by_xpath('//ul[@id="menu-left"]//a[contains(text(),"Elenco immobili")]').click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'Elenco immobili link click is ok: %s'% login_link_tab)
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'Elenco immobili link click failed: %s, %s, %s'% (t,val,tb))
        #fixred
    foglios =args.foglio.split(',')
    #args.foglio.split(',')
    for foglio in foglios:
        property_list = []
        try:
            driver.find_element_by_xpath('//select[@name="tipoCatasto"]/option[contains(text(),"Fabbricati")]').click()
            time.sleep(3)
            log(sys._getframe().f_code.co_name,'catasto selection click is ok: %s'% login_link_tab)
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'catasto selection link failed: %s, %s, %s'% (t,val,tb))
            
        try:
            driver.find_element_by_xpath('//select[@name="comuneCat"]/option[contains(@value,"'+option_selection1+'")]').click()
            time.sleep(3)
            log(sys._getframe().f_code.co_name,'commune selection click is ok: %s'% login_link_tab)
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'commune selection link failed: %s, %s, %s'% (t,val,tb))
            
        
        try:
            input_x = driver.find_element_by_xpath('//input[@name="foglio"]')
            input_x.send_keys(foglio)
            time.sleep(1)
            log(sys._getframe().f_code.co_name,'input_foglio enter is ok: %s'% 'xxxx')
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'input_foglio enter failed: %s, %s, %s'% (t,val,tb))
            
        try:
            driver.find_element_by_xpath('//input[@name="selPartita"]').click()
            time.sleep(5)
            log(sys._getframe().f_code.co_name,'Partita e Categoria click is ok: %s'% login_link_tab)
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'Partita e Categoria click failed: %s, %s, %s'% (t,val,tb))
            
        try:
            driver.find_element_by_xpath('//select[@name="partSpeciale"]/option[contains(text(),"Tutte")]').click()
            time.sleep(3)
            log(sys._getframe().f_code.co_name,'partSpeciale selection click is ok: %s'% login_link_tab)
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'partSpeciale selection link failed: %s, %s, %s'% (t,val,tb))
            
        
        try:
            driver.find_element_by_xpath('//select[@name="categoria"]/option[@value="$"]').click()
            time.sleep(3)
            log(sys._getframe().f_code.co_name,'categoria selection click is ok: %s'% login_link_tab)
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'categoria selection link failed: %s, %s, %s'% (t,val,tb))
        
        try:
            driver.find_element_by_xpath('//input[@name="ricerca"]').click()
            time.sleep(3)
            log(sys._getframe().f_code.co_name,'ricerca btn click is ok: %s'% 'xxxx')
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'ricerca btn failed: %s, %s, %s'% (t,val,tb))
            
        
        try:
            rows = driver.find_elements_by_xpath('//tr[contains(@class,"riga")]')
            print('len of rows is ',len(rows))
            print('type  of rows is ',type(rows))
            #for refreshing the browser
            ii=1

            for row in rows:

                if(ii%50==0):driver.refresh();input('50 row are done , type ok  to prevent the end of the sessions')

                try:
                    ii+=1
                    correct_row = row.find_element_by_xpath('//td[@class="centrato"]')
                except:
                    correct_row = False
                if correct_row:
                    cols = row.find_elements_by_xpath("./td")
                    temp = [] # Temproary list
                    for col in cols:
                        if(temp==[] and col.text!=''):temp.append('')
                        temp.append(col.text)
                    property_list.append(temp)            
                else:
                    log(sys._getframe().f_code.co_name,'tr rigascura has no TD with class centrato')
        except:
            t,val,tb = sys.exc_info()
            log(sys._getframe().f_code.co_name,'extract rows failed: %s, %s, %s'% (t,val,tb))
            return []
    
        script_dir = os.path.dirname(os.path.realpath('__file__'))
        rel_path = "files/foglio_%s.csv" % str(foglio)
        abs_file_path = os.path.join(script_dir, rel_path)
        log(sys._getframe().f_code.co_name,'abs_file_path: %s' % abs_file_path)
        with open(abs_file_path, "w") as f:
            writer = csv.writer(f)
            writer.writerows(property_list)

        print('the type of the property_list is => ',type(property_list))
        print('the len of the property_list is => ',len(property_list))
        print('property_list[0] => ',property_list[0])
        #prop list


        df = pd.DataFrame(property_list,columns=['zz','Foglio','Particella','Subalterno','Zona','Partita','Rendita','Indirizzo'])
        print('property_list has been generated ')

        df.to_csv('property_list.csv')
        df.to_excel('property_list.xlsx')

            
    
    return property_list
    
def login(driver):
    log(sys._getframe().f_code.co_name,'login func is started.')
    #driver = get_link(driver, login_link, 5, None)
    try:
        driver.get(login_link)
        log(sys._getframe().f_code.co_name,'link opened and waiting: %s'% login_link)
        time.sleep(5)
        
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'link did not open: %s, %s, %s'% (t,val,tb))
        return False
    
    
    try:
        driver.find_element_by_xpath(login_link_tab).click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'login_link_tab click is ok: %s'% login_link_tab)
    except:
        log(sys._getframe().f_code.co_name,'login_link_tab failed: %s, %s, %s'% (t,val,tb))
        return False
    
    try:
        driver.find_element_by_xpath(login_link_tab_sister).click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'login_link_tab_sister click is ok: %s'% login_link_tab_sister)
    except:
        log(sys._getframe().f_code.co_name,'login_link_tab_sister failed: %s, %s, %s'% (t,val,tb))
        return False
    
    try:
        input_usernameobj = driver.find_element_by_xpath(input_username)
        input_usernameobj.send_keys(username)
        time.sleep(1)
        log(sys._getframe().f_code.co_name,'input_username enter ok: %s'% login_link_tab_sister)
    except:
        log(sys._getframe().f_code.co_name,'input_username enter failed: %s, %s, %s'% (t,val,tb))
        return False
    
    try:
        input_passwobj = driver.find_element_by_xpath(input_passw)
        input_passwobj.send_keys(passw)
        time.sleep(1)
        log(sys._getframe().f_code.co_name,'input_passw enter is ok: %s'% login_link_tab_sister)
    except:
        log(sys._getframe().f_code.co_name,'input_passw enter failed: %s, %s, %s'% (t,val,tb))
        return False
    
    try:
        btn_passwobj = driver.find_element_by_xpath(btn_passw)
        btn_passwobj.click()
        log(sys._getframe().f_code.co_name,'btn_passw click is ok: %s'% btn_passw)
        time.sleep(10)
        
    except:
        log(sys._getframe().f_code.co_name,'btn_passw click failed: %s, %s, %s'% (t,val,tb))
        return False
    
    return driver
    
def get_final_data(driver, foglio, particella, subalterno):
    
    try:
        driver.find_element_by_xpath(second_action_xpath).click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'second_action_xpath click is ok: %s'% second_action_xpath)
    except:
        log(sys._getframe().f_code.co_name,'second_action_xpath failed: %s, %s, %s'% (t,val,tb))
        return False
    
    
    
    try:
        driver.find_element_by_xpath('//select[@name="tipoCatasto"]/option[contains(text(),"Fabbricati")]').click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'catasto selection click is ok: %s'% 'Fabbricati')
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'catasto selection link failed: %s, %s, %s'% (t,val,tb))
        
    try:
        driver.find_element_by_xpath('//select[@name="denomComune"]/option[contains(@value,"'+option_selection1+'")]').click()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'denomComune selection click is ok: %s'% 'Fabbricati')
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'denomComune selection link failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        input_x = driver.find_element_by_xpath('//input[@name="foglio"]')
        input_x.send_keys(foglio)
        time.sleep(1)
        log(sys._getframe().f_code.co_name,'input_foglio enter is ok: %s'% str(foglio))
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'input_foglio enter failed: %s, %s, %s'% (t,val,tb))
        
    try:
        input_x = driver.find_element_by_xpath('//input[@name="particella1"]')
        input_x.send_keys(particella)
        time.sleep(1)
        log(sys._getframe().f_code.co_name,'input_particella1 enter is ok: %s'% str(particella))
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'input_particella1 enter failed: %s, %s, %s'% (t,val,tb))
        
    
    try:
        input_x = driver.find_element_by_xpath('//input[@name="subalterno1"]')
        input_x.send_keys(subalterno)
        time.sleep(1)
        log(sys._getframe().f_code.co_name,'input_subalterno1 enter is ok: %s'% str(subalterno))
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'input_subalterno1 enter failed: %s, %s, %s'% (t,val,tb))
        
    try:
        btn_search = driver.find_element_by_xpath('//input[@name="scelta" and @value="Ricerca"]')
        actions = ActionChains(driver)
        actions.move_to_element(btn_search)
        actions.click()
        actions.perform()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'ricerca btn click is ok: %s'% 'xxxx')
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'ricerca btn failed: %s, %s, %s'% (t,val,tb))
        
    try:
        btn_conferma = driver.find_element_by_xpath('//input[@name="confAssSub" and @value="Conferma"]')
        actions = ActionChains(driver)
        actions.move_to_element(btn_conferma)
        actions.click()
        actions.perform()
        time.sleep(3)
        log(sys._getframe().f_code.co_name,'Conferma btn click is ok: %s'% 'xxxx')
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'NO Conferma btn')
        
    try:
        d = {}
        titles = driver.find_elements_by_xpath('//table[@class="listaIsp4"]/tbody[1]/tr/th')
        for title in titles:
            d[title.text] = ""
        rows = driver.find_elements_by_xpath('//tr[contains(@class,"riga")]')
        for cc, row in enumerate(rows):
            z = {}
            o = []
            cols = row.find_elements_by_xpath("./*[name()='th' or name()='td']")
            temp = [] # Temproary list
            for col in cols:
                temp.append(col.text)
            ss = 0
            for k,v in d.items():
                if k:
                    z[k] = temp[ss]
                ss +=1
                        
            log(sys._getframe().f_code.co_name,'ROW for second action: %s'% (z))
            
            
            try:
                radio = row.find_element_by_xpath('./td/input[@name="visImmSel"]')
                actions = ActionChains(driver)
                actions.move_to_element(radio)
                actions.click()
                actions.perform()
                time.sleep(1)
                log(sys._getframe().f_code.co_name,'select row radio click is ok: %s'% login_link_tab)
            except:
                t,val,tb = sys.exc_info()
                log(sys._getframe().f_code.co_name,'select row radio click failed: %s, %s, %s'% (t,val,tb))
                
            
            try:######bug
                btn_intestati = driver.find_element_by_xpath('//input[@name="intestati" and @value="Intestati"]')
                actions = ActionChains(driver)
                actions.move_to_element(btn_intestati)
                actions.click()
                actions.perform()
                time.sleep(3)
                log(sys._getframe().f_code.co_name,'ROW Intestati btn click is ok: %s'% 'xxxx')
            except:
                t,val,tb = sys.exc_info()
                log(sys._getframe().f_code.co_name,'ROW Intestati btn failed: %s, %s, %s'% (t,val,tb))
            
            d2 = {}
            new_titles = driver.find_elements_by_xpath('//table[@class="listaIsp4"]/tbody[1]/tr/th')
            for new_title in new_titles:
                d2[new_title.text] = ""
            rows2 = driver.find_elements_by_xpath('//tr[contains(@class,"riga")]')
            for row2 in rows2:
                cols2 = row2.find_elements_by_xpath("./*[name()='th' or name()='td']")
                temp2 = [] # Temproary list
                for col2 in cols2:
                    temp2.append(col2.text)

                ss = 0
                #the bug is here
                print('the bug is here : => ')

                for k,v in d2.items():

                    if k:
                        z[k] = temp2[ss]
                    ss +=1
            o.append(z.values())
            print(type(o))
            script_dir = os.path.dirname(os.path.realpath('__file__'))
            rel_path = "files/foglio_%s_%s_%s_%d.csv" % (str(foglio),str(particella),str(subalterno), cc)
            abs_file_path = os.path.join(script_dir, rel_path)
            log(sys._getframe().f_code.co_name,'abs_file_path: %s' % abs_file_path)
            with open(abs_file_path, "w") as f:
                writer = csv.writer(f)
                writer.writerows(o)
                
            driver.execute_script("window.history.go(-1)")
            
    except:
        t,val,tb = sys.exc_info()
        log(sys._getframe().f_code.co_name,'extract rows failed: %s, %s, %s'% (t,val,tb))
        return []
        
    return True
    
def main():
    print("main func is started.")
    parser = argparse.ArgumentParser(description="parameters to file")
    
    parser.add_argument("--foglio", default="1")
    args = parser.parse_args()
    driver = get_driver()
    login(driver)
    property_list_csv = get_link(driver, action_link, 10, args)
    print('Property list',property_list_csv)
    
    try:
        foglios = args.foglio.split(',')
        for foglio in foglios:
            foglio_rows = []
            
            try:
                script_dir = os.path.dirname(os.path.realpath('__file__'))
                rel_path = "files/foglio_%s.csv" % str(foglio)
                abs_file_path = os.path.join(script_dir, rel_path)
                log(sys._getframe().f_code.co_name,'abs_file_path READ: %s' % abs_file_path)
                with open(abs_file_path) as f:
                    reader = csv.reader(f)
                    foglio_rows = list(reader)
                    
                log(sys._getframe().f_code.co_name,'foglio_rows is READ from : %s'% abs_file_path)
                log(sys._getframe().f_code.co_name,'foglio_rows : %s'% foglio_rows)
                
            except:
                t,val,tb = sys.exc_info()
                log(sys._getframe().f_code.co_name,'foglio_rows is NOT READ from : %s - %s, %s, %s'% (abs_file_path, t,val,tb))
                return False
            
            for foglio_row in foglio_rows:
                if not foglio_row:
                    log(sys._getframe().f_code.co_name,'EMPTY foglio_row %s SKIPPING tHIS'% (foglio_row))
                    continue
                # Particella csv[2]
                # Subalterno csv[3]
                try:
                    particella = foglio_row[2]
                except:
                    t,val,tb = sys.exc_info()
                    log(sys._getframe().f_code.co_name,'particella not found in foglio_rows %s, %s, %s'% (t,val,tb))
                
                try:
                    subalterno = foglio_row[3]
                except:
                    t,val,tb = sys.exc_info()
                    log(sys._getframe().f_code.co_name,'subalterno not found in foglio_rows %s, %s, %s'% (t,val,tb))
                
                try:
                    noNeed = foglio_row[5]
                    if noNeed.find('immobiliare soppressa') != -1:
                        log(sys._getframe().f_code.co_name,'Unita immobiliare soppressa WORD found in foglio_row %s SKIPPING tHIS'% (noNeed))
                        continue
                except:
                    t,val,tb = sys.exc_info()
                    log(sys._getframe().f_code.co_name,'noneed not found in foglio_rows %s, %s, %s'% (t,val,tb))
                
                if not particella or not particella:
                    log(sys._getframe().f_code.co_name,'subalterno OR particella not found in foglio_row %s SKIPPING tHIS'% (foglio_row))
                    continue
                
                final_data = get_final_data(driver, foglio, particella, subalterno)
                if final_data:
                    log(sys._getframe().f_code.co_name,'final_data for FOGLIO is done: %s' % str(foglio))
                else:
                    log(sys._getframe().f_code.co_name,'final_data for FOGLIO FAILED: %s' % str(foglio))
    except:
        t,val,tb = sys.exc_info()
        if t:
            log(sys._getframe().f_code.co_name,'FINAL DATA aCTIONS failed: %s, %s, %s'% (t,val,tb))
        else:
            log(sys._getframe().f_code.co_name,'FINAL DATA aCTIONS failed')
    
    time.sleep(120)
    stoppped = stop_driver(driver)
    
if __name__ == '__main__':
    main()