#Bet365 grayhounds scraping 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from time import gmtime, strftime
import csv
import re

def start_bet365():
    print("============ Data Scraping now, so please wait for a while.! ===========")
    file_name = csv_make()
    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox(firefox_profile=profile)

    driver.implicitly_wait(30)

    driver.set_window_size(1124, 850)
    driver.get('https://www.bet365.com.au/#/AS/B4/')
    time.sleep(1)
    try:
        # australia = driver.find_element_by_xpath(".//div[contains(@class, 'wcl-CommonElementStyle_PrematchCenter wc-RacingSplashPage_CenterColumn')]/div[@class='rsl-RacingSplashLegacyModule ']/div[1]/div[@class='rsl-MarketGroup '][2]")
        # australia.find_element_by_xpath(".//div[@class='rsl-MarketGroup_Open ']/div[1]/div[2]").click()
        # time.sleep(3)
        australia = ''
        australia = driver.find_element_by_xpath(".//div[@class='wcl-CommonElementStyle_PrematchCenter wc-RacingSplashPage_CenterColumn ']/div[@class='rsl-RacingSplashLegacyModule ']/div[1]/div[@class='rsl-MarketGroup '][2]")
        aust_find = australia.find_elements_by_xpath(".//div[@class='rsl-MarketGroup_Open ']/div[@class='rsl-RacingMarketGroupChild rsl-Market ']/div[@class='rsl-Market_Open ']/div[@class='rsl-RaceMeeting ']")
        array = [[]]
        array.clear()#2D array initialization 
        
        for i in range(len(aust_find)):
            try:
                            
                if aust_find[i].find_element_by_xpath('.//div[@class="rsl-MeetingHeader "]/div[@class="rsl-MeetingHeader_LeftContainer "]/div[contains(@class, "sl-MeetingHeader_Chevron")]'):
                    track_name = aust_find[i].find_element_by_xpath(".//div[@class='rsl-MeetingHeader ']/div[@class='rsl-MeetingHeader_LeftContainer ']/div[@class='rsl-MeetingHeader_RaceName ']").text
            
                    aust_find[i].find_element_by_xpath(".//div[@class='rsl-MeetingHeader ']/div[@class='rsl-MeetingHeader_LeftContainer ']/div[@class='rsl-MeetingHeader_RaceName ']").click()
                    time.sleep(1)

                    page_url = driver.current_url
                    driver.get(page_url)
                    temp = driver.find_element_by_xpath(".//div[@class='rlm-RacingCouponLegacyModule ']/div[@class='gl-MarketGrid ']")
                    
                    bets = temp.find_elements_by_xpath('//div[contains(@class,"gll-MarketGroup rlm-CouponRacingMarketGroupScroll rcm-CouponRacingMarketGroup")]')
                    
                    for bet in bets:
                        race = bet.find_element_by_xpath(".//div[1]/div[1]/div[1]").text 
                        race_name = race[:7]
                        bet_content = bet.find_elements_by_xpath(".//div[2]/div[1]/div[3]/div[@class='rl-RacingCouponParticipantGreyhoundAus ']")
                        
                        try:
                            bet_time = bet.find_element_by_xpath('.//div[2]/div[1]/div[2]/div[contains(@class, "rlm-RacingStreamingClosableContainer")]/div[1]/div[1]/div[1]').text
                        except:
                            bet_time = bet.find_element_by_xpath('.//div[2]/div[1]/div[2]/div[1]/div[1]').text

                        for bet_con in bet_content:
                            try:
                                
                                bet_tem = bet_con.find_element_by_xpath('.//div[contains(@class, "rl-RacingCouponParticipantGreyhoundAus_Wrapper")]')
                                bet_all = bet_tem.find_element_by_xpath('.//div[contains(@class, "rl-RacingCouponParticipantGreyhoundAus_OddsContainer rl-RacingCouponParticipantGreyhoundAus_OddsColumns")]')
                                if bet_all.text.strip() != 'Scratched':
                                    bet_array = []
                                    bet_array.append(track_name)
                                    bet_array.append(race_name)
                                    bet_tab = bet_tem.find_element_by_xpath(".//div[@class='rl-Silk_DogAus rl-RacingCouponParticipantGreyhoundAus_Silk ']/div").get_attribute("class")
                                    tab_temp = bet_tab.strip()
                                    for tab in re.findall(r'-?\d+\.?\d*', tab_temp):
                                        bet_array.append(tab)
                                    
                                    bet_Selection = bet_tem.find_element_by_xpath(".//div[@class='rl-RacingCouponParticipantGreyhoundAus_HorseTrainerJockey rl-HorseTrainerJockey ']").text
                                    selection = bet_Selection[:-4]
                                    
                                    bet_array.append(selection)
                                    for box in re.findall(r'-?\d+\.?\d*', bet_Selection):
                                        bet_array.append(box)
                                    
                                    bet_tem.find_element_by_xpath(".//div[@class='rl-RacingCouponParticipantGreyhoundAus_Form ']/div[1][@class='rl-FormAus ']/div[@class='rl-FormAus_DetailsButton ']").click()
                                    time.sleep(0.5)
                                    
                                    bet_form = bet_con.find_element_by_xpath(".//div[2]/div[1]/div[3]")
                                    
                                    bet_array.append(bet_form.text)
                                    bet_all = bet_tem.find_element_by_xpath('.//div[contains(@class, "rl-RacingCouponParticipantGreyhoundAus_OddsContainer rl-RacingCouponParticipantGreyhoundAus_OddsColumns")]')
                                    bet_detail = bet_all.find_elements_by_xpath('.//div[contains(@class, "gll-Participant_General rl-RacingCouponParticipantAusOdds")]')
                                    
                                    for detail in bet_detail:
                                        bet_array.append(detail.text)
                                    bet_array.append(bet_time)
                                    array.append(bet_array)
                                    
                                    print(array)
                                else:
                                    pass
                            except:
                                pass
                    driver.execute_script("window.history.go(-1)") #driver back 
                    time.sleep(0.5)
                    # australia = driver.find_element_by_xpath(".//div[@class='wcl-CommonElementStyle_PrematchCenter wc-RacingSplashPage_CenterColumn ']/div[@class='rsl-RacingSplashLegacyModule ']/div[1]/div[@class='rsl-MarketGroup '][2]")
                    # australia.find_element_by_xpath(".//div[@class='rsl-MarketGroup_Open ']/div[1]/div[2]").click()
                    # time.sleep(0.5)
                    australia = ''
                    aust_find = ''
                    australia = driver.find_element_by_xpath(".//div[@class='wcl-CommonElementStyle_PrematchCenter wc-RacingSplashPage_CenterColumn ']/div[@class='rsl-RacingSplashLegacyModule ']/div[1]/div[@class='rsl-MarketGroup '][2]")
                    aust_find = australia.find_elements_by_xpath(".//div[@class='rsl-MarketGroup_Open ']/div[@class='rsl-RacingMarketGroupChild rsl-Market ']/div[@class='rsl-Market_Open ']/div[@class='rsl-RaceMeeting ']")
                    

                else:
                    pass
            except:
                pass
            
            try:
                # write csv file from array
                with open(file_name, 'a', newline='', encoding="utf-8") as f:
                    writer = csv.writer(f, delimiter=',')
                    for line in array:
                        writer.writerow(line)
                f.close()
                array.clear() # 1D array initialization 

            except:
                pass
    except:
        print("========= Server detected Bot. please wait for while!.=========")
        pass
    #driver close part
    driver.quit()

def csv_make(): #csv file making part
    try:
        # csv header part defination
        curdate = strftime("%Y-%m-%d %H-%M-%S", gmtime())
        print("Bet365 Scraping date and time:", curdate)
        file_name = 'bet365' + curdate + '.csv'
        header = ['Track', 'Race', 'Tab number', 'Selection', 'Box', 'Form', 'Tote Win', 'Tote Place', 'Fixed Win', 'Fixed Place', 'Time']

        # data save into CSV file
        with open(file_name, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)  # write the header
        f.close()
    except:
        pass

    return file_name

start_bet365()