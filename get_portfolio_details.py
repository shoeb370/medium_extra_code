import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_request(url):    
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
    
    # print(response.text)
    return response
def get_soup(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def read_file():
    df = pd.read_csv('Investor_Link.csv')
    return df
    
def get_investor_name_short_desc(soup):
    short_desc = ''; name = ''
    inv_desc_raw = soup.find_all('div',{'class':'companyheader'})
    inv_desc = [i for i in inv_desc_raw if '<h1>' in str(i)]
    if inv_desc !=[]:
        name = inv_desc[0].find('h1').text.strip()
        short_desc_raw = inv_desc[0].find_all('p')
        short_desc_raw = [i.text.strip() for i in short_desc_raw]
        short_desc = ' '.join(short_desc_raw)
    return name,short_desc

def get_table_data(soup):
    try:
        table = soup.find("table")
        html_table = str(table)
        portfolio_df = pd.read_html(html_table)[0]
    except:
        portfolio_df =pd.DataFrame()        
    return portfolio_df

if __name__ == '__main__':
    link_df = read_file()
    final_df = pd.DataFrame()
    for i in range(len(link_df)):
        url = link_df['Investor_Link'].iloc[i]
        response = get_request(url)
        if response.status_code == 200:
            soup = get_soup(response)
            name, short_desc = get_investor_name_short_desc(soup)
            portfolio_df = get_table_data(soup)
            portfolio_df['Investor_Name'] = name
            portfolio_df['short_desc'] = short_desc
            portfolio_df['Investor_Link'] = url
            final_df = pd.concat([final_df, portfolio_df], ignore_index=True)
    final_df = final_df.drop(columns=['S.No.'])
    final_df.to_csv('Final_Indepth.csv', index=False)
