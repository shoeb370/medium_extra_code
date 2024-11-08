import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_investor_url():
    url = "https://ticker.finology.in/investor"
    
    payload = {}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'max-age=0',
      # 'cookie': 'ASP.NET_SessionId=jskdpi42nxgj03r4tdw4vxf3; ext_name=ojplmecpdpgccookcobabopnaifgidhf',
      'priority': 'u=0, i',
      'referer': 'https://ticker.finology.in/',
      'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    
    response = requests.request("GET", url, headers=headers, data=payload)
    
    print(response.text)
    return response

def extract_invester_url(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    cont = soup.find('div',{"class":'row filterlist'})
    list_cont = cont.find_all('div',{'class':'col-12 col-md-3'})
    # inv_link = [i.find('a',{'class':'bundlelink'})['href'] for i in list_cont]
    inv_link_list = []; investor_name_list = []
    for i in range(len(list_cont)):
        try:
            investor_link = 'https://ticker.finology.in/' + list_cont[i].find('a',{'class':'bundlelink'})['href']
            inv_link_list.append(investor_link)
        except:
            inv_link_list.append(np.nan)
        
        try:
            inv_name = list_cont[i].find('h4',{"class":'text-center my-2 superInvestorName'}).text
        except:
            inv_name = np.nan
        investor_name_list.append(inv_name)
    
    investor_df = pd.DataFrame({
        'Investor_Name': [investor_name_list],
        'Investor_Link': [inv_link_list]
        })
    
    investor_df.to_csv('Investor_Link.csv', index=False)

if __name__ == '__main__':
    response = get_investor_url()
    if response.status_code == 200:
        extract_invester_url(response)    
