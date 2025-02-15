
#Extraction of Complete fundamental data of stock from finology
import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import ticket_constant as constant #Contains all api headers
import pandas as pd

def get_req(url, headers):
    response = requests.get(url, headers)
    print(response.status_code)
    print(response.text)
    return response.status_code, response.text

def extract_price_summary(tree, stock_info):
    try:
        company_name = tree.xpath('//span[@id="mainContent_ltrlCompName"]//text()')[0]
    except:
        company_name = 'Not available'
    try:
        today_high = tree.xpath('//*[@id="mainContent_ltrlTodayHigh"]/text()')[0]
    except IndexError:
        today_high = 'Not available'
    try:
        today_low = tree.xpath('//*[@id="mainContent_ltrlTodayLow"]/text()')[0]
    except IndexError:
        today_low = 'Not available'
    try:
        week52High = tree.xpath('//*[@id="mainContent_ltrl52WH"]/text()')[0]
    except IndexError:
        week52High = 'Not available'
    try:
        week52Low = tree.xpath('//*[@id="mainContent_ltrl52WL"]/text()')[0]
    except IndexError:
        week52Low = 'Not available'
    stock_info['Company_name'] = company_name
    stock_info["Todays_High"] = today_high
    stock_info["Todays_Low"] = today_low
    stock_info['52_Week_High'] = week52High
    stock_info['52_Week_Low'] = week52Low
    return stock_info

def extract_company_essential(tree, stock_info):
    try:
        market_cap = tree.xpath('//small[text()="Market Cap"]/following-sibling::p/span/text()')[0]
    except IndexError:
        market_cap = 'Not available'
    try:
        enterprisevalue = tree.xpath("//span[@id='mainContent_ltrlEntValue']/span[@class='Number']/text()")[0]
    except IndexError:
        enterprisevalue = 'Not available'
    try:
        No_of_shares = tree.xpath("//div[@id='mainContent_updAddRatios']//div[contains(., 'No. of Shares')]//span[@class='Number']/text()")[0]
    except IndexError:
        No_of_shares = 'Not available'
    try:
        pe_ratio = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'P/E')]/following-sibling::p/text()")[0].strip()
    except IndexError:
        pe_ratio = 'Not available'
    try:
        pb_ratio = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'P/B')]/following-sibling::p/text()")[0].strip()
    except IndexError:
        pb_ratio = 'Not available'
    try:
        face_value = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'Face Value')]/following-sibling::p/text()")[0].strip()
    except IndexError:
        face_value = 'Not available'
    try:
        div_yield = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'Div. Yield')]/following-sibling::p/text()")[0].replace('\r', '').replace('\n', '').replace(' ','')
    except IndexError:
        div_yield = 'Not available'
    try:
        book_value = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'Book Value (TTM)')]/following-sibling::p/span[@class='Number']/text()")[0].strip()
    except IndexError:
        book_value = 'Not available'
    try:
        cash = tree.xpath('//span[@id="mainContent_ltrlCash"]//span//text()')[0]
    except IndexError:
        cash = 'Not available'
    try:
        debt = tree.xpath('//span[@id="mainContent_ltrlDebt"]//span//text()')[0]
    except IndexError:
        debt = 'Not available'
    try:
        promoter_holding = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'Promoter Holding')]/following-sibling::p/text()")[0].strip()
    except IndexError:
        promoter_holding = 'Not available'
    try:
        eps = tree.xpath("//div[@id='mainContent_updAddRatios']//small[contains(text(), 'EPS (TTM)')]/following-sibling::p/span[@class='Number']/text()")[0].strip()
    except IndexError:
        eps = 'Not available'
    try:
        sales_growth = tree.xpath('//div[.//span[@id="mainContent_lblSalesGrowthorCasa"]]/p/span[@class="Number"]/text()')[0]
    except IndexError:
        sales_growth = 'Not available'
    try:
        roe = tree.xpath('//div[.//small[contains(text(), "ROE")]]/p/span[@class="Number"]/text()')[0].strip()
    except IndexError:
        roe = 'Not available'
    try:
        roce_value = tree.xpath('//div[@id="mainContent_updAddRatios"]//div[.//small[contains(text(), "ROCE")]]//span[@class="Number"]/text()')[0].strip()
    except IndexError:
        roce_value = 'Not available'    
    try:
        profit_growth_value = tree.xpath('//div[@id="mainContent_updAddRatios"]//div[.//small[contains(text(), "Profit Growth")]]//span[@class="Number"]/text()')[0].strip()
    except IndexError:
        profit_growth_value = 'Not available'
    
    # Store all the values in the dictionary
    stock_info["Market_Cap"] = market_cap
    stock_info["Enterprise_Value"] = enterprisevalue
    stock_info["No_of_Shares"] = No_of_shares
    stock_info["P/E_Ratio"] = pe_ratio
    stock_info["P/B_Ratio"] = pb_ratio
    stock_info["Face_Value"] = face_value
    stock_info["Div_Yield"] = div_yield
    stock_info["Book_Value"] = book_value
    stock_info["Cash"] = cash
    stock_info["Debt"] = debt
    stock_info["Promoter_Holding"] = promoter_holding
    stock_info["EPS"] = eps
    stock_info["Sales_Growth"] = sales_growth
    stock_info["ROE"] = roe
    stock_info["ROCE_Value"] = roce_value
    stock_info["Profit_Growth"] = profit_growth_value
    return stock_info
    
def extract_finstar(tree, stock_info):
    try:
        ownership = tree.xpath('//div[@id="mainContent_divOwner"]//span[@class="badge badge-success"]//text()')[0].strip()
    except IndexError:
        ownership = 'Not available'
    
    try:
        valuation = tree.xpath('//div[@id="mainContent_divValuation"]//span[@class="badge badge-success"]//text()')[0].strip()
    except IndexError:
        valuation = 'Not available'
    
    try:
        efficiency = tree.xpath('//div[@id="mainContent_divEff"]//span[@class="badge badge-success"]//text()')[0].strip()
    except IndexError:
        efficiency = 'Not available'
    
    try:
        financials = tree.xpath('//div[@id="mainContent_divFinance"]//span[@class="badge badge-success"]//text()')[0].strip()
    except IndexError:
        financials = 'Not available'
    
    # Store all the values in the dictionary
    stock_info["Ownership"] = ownership
    stock_info["Valuation"] = valuation
    stock_info["Efficiency"] = efficiency
    stock_info["Financials"] = financials
    return stock_info

def extract_sales_growth(tree, stock_info):
    try:
        sales_growth = tree.xpath('//*[@id="mainContent_salesChart"]//@data-chart_values')[0]
        try:
            chart_values = json.loads(sales_growth)
            try:
                Sales_Growth_1st_year = chart_values[0]
            except IndexError:
                Sales_Growth_1st_year = 'Not available'
            try:
                Sales_Growth_2nd_year = chart_values[1]
            except IndexError:
                Sales_Growth_2nd_year = 'Not available'
            try:
                Sales_Growth_3rd_year = chart_values[2]
            except IndexError:
                Sales_Growth_3rd_year = 'Not available'
            try:
                Sales_Growth_4th_year = chart_values[3]
            except IndexError:
                Sales_Growth_4th_year = 'Not available'
            try:
                Sales_Growth_5th_year = chart_values[4]
            except IndexError:
                Sales_Growth_5th_year = 'Not available'
        except json.JSONDecodeError:
            chart_values = []
            Sales_Growth_1st_year = 'Not available'
            Sales_Growth_2nd_year = 'Not available'
            Sales_Growth_3rd_year = 'Not available'
            Sales_Growth_4th_year = 'Not available'
            Sales_Growth_5th_year = 'Not available'
    except IndexError:
        sales_growth = 'Not available'
        chart_values = []
        Sales_Growth_1st_year = 'Not available'
        Sales_Growth_2nd_year = 'Not available'
        Sales_Growth_3rd_year = 'Not available'
        Sales_Growth_4th_year = 'Not available'
        Sales_Growth_5th_year = 'Not available'
    
    stock_info["Sales_Growth_1st_Year"] = Sales_Growth_1st_year
    stock_info["Sales_Growth_2nd_Year"] = Sales_Growth_2nd_year
    stock_info["Sales_Growth_3rd_Year"] = Sales_Growth_3rd_year
    stock_info["Sales_Growth_4th_Year"] = Sales_Growth_4th_year
    stock_info["Sales_Growth_5th_Year"] = Sales_Growth_5th_year
    return stock_info
    
def extract_profit_growth(tree, stock_info):
    try:
        profit_growth = tree.xpath('//*[@id="mainContent_salesChart"]//@data-chart_values')[0]
        try:
            profit_chart_values = json.loads(profit_growth)
            try:
                Profit_Growth_1st_year = profit_chart_values[0]
            except IndexError:
                Profit_Growth_1st_year = 'Not available'
            try:
                Profit_Growth_2nd_year = profit_chart_values[1]
            except IndexError:
                Profit_Growth_2nd_year = 'Not available'
            try:
                Profit_Growth_3rd_year = profit_chart_values[2]
            except IndexError:
                Profit_Growth_3rd_year = 'Not available'
            try:
                Profit_Growth_4th_year = profit_chart_values[3]
            except IndexError:
                Profit_Growth_4th_year = 'Not available'
            try:
                Profit_Growth_5th_year = profit_chart_values[4]
            except IndexError:
                Profit_Growth_5th_year = 'Not available'
        except json.JSONDecodeError:
            profit_chart_values = []
            Profit_Growth_1st_year = 'Not available'
            Profit_Growth_2nd_year = 'Not available'
            Profit_Growth_3rd_year = 'Not available'
            Profit_Growth_4th_year = 'Not available'
            Profit_Growth_5th_year = 'Not available'
    except IndexError:
        profit_growth = 'Not available'
        profit_chart_values = []
        Profit_Growth_1st_year = 'Not available'
        Profit_Growth_2nd_year = 'Not available'
        Profit_Growth_3rd_year = 'Not available'
        Profit_Growth_4th_year = 'Not available'
        Profit_Growth_5th_year = 'Not available'
    stock_info["Profit_Growth_1st_Year"] = Profit_Growth_1st_year
    stock_info["Profit_Growth_2nd_Year"] = Profit_Growth_2nd_year
    stock_info["Profit_Growth_3rd_Year"] = Profit_Growth_3rd_year
    stock_info["Profit_Growth_4th_Year"] = Profit_Growth_4th_year
    stock_info["Profit_Growth_5th_Year"] = Profit_Growth_5th_year
    return stock_info

def extract_roe_chart(tree, stock_info):
    
    try:
        roe_chart = tree.xpath('//*[@id="mainContent_roeChart"]//@data-chart_values')[0]
        try:
            ROE_chart_values = json.loads(roe_chart)
            try:
                ROE_1st_year = ROE_chart_values[0]
            except IndexError:
                ROE_1st_year = 'Not available'
            try:
                ROE_2nd_year = ROE_chart_values[1]
            except IndexError:
                ROE_2nd_year = 'Not available'
            try:
                ROE_3rd_year = ROE_chart_values[2]
            except IndexError:
                ROE_3rd_year = 'Not available'
            try:
                ROE_4th_year = ROE_chart_values[3]
            except IndexError:
                ROE_4th_year = 'Not available'
            try:
                ROE_5th_year = ROE_chart_values[4]
            except IndexError:
                ROE_5th_year = 'Not available'
        except json.JSONDecodeError:
            ROE_chart_values = []
            ROE_1st_year = 'Not available'
            ROE_2nd_year = 'Not available'
            ROE_3rd_year = 'Not available'
            ROE_4th_year = 'Not available'
            ROE_5th_year = 'Not available'
    except IndexError:
        roe_chart = 'Not available'
        ROE_chart_values = []
        ROE_1st_year = 'Not available'
        ROE_2nd_year = 'Not available'
        ROE_3rd_year = 'Not available'
        ROE_4th_year = 'Not available'
        ROE_5th_year = 'Not available'

    stock_info["ROE_1st_Year"] = ROE_1st_year
    stock_info["ROE_2nd_Year"] = ROE_2nd_year
    stock_info["ROE_3rd_Year"] = ROE_3rd_year
    stock_info["ROE_4th_Year"] = ROE_4th_year
    stock_info["ROE_5th_Year"] = ROE_5th_year
    return stock_info    

def extract_roce_chart(tree, stock_info):
    try:
        roce_chart = tree.xpath('//*[@id="mainContent_roceChart"]//@data-chart_values')[0]
        try:
            ROCE_chart_values = json.loads(roce_chart)
            try:
                ROCE_1st_year = ROCE_chart_values[0]
            except IndexError:
                ROCE_1st_year = 'Not available'
            try:
                ROCE_2nd_year = ROCE_chart_values[1]
            except IndexError:
                ROCE_2nd_year = 'Not available'
            try:
                ROCE_3rd_year = ROCE_chart_values[2]
            except IndexError:
                ROCE_3rd_year = 'Not available'
            try:
                ROCE_4th_year = ROCE_chart_values[3]
            except IndexError:
                ROCE_4th_year = 'Not available'
            try:
                ROCE_5th_year = ROCE_chart_values[4]
            except IndexError:
                ROCE_5th_year = 'Not available'
        except json.JSONDecodeError:
            ROCE_chart_values = []
            ROCE_1st_year = 'Not available'
            ROCE_2nd_year = 'Not available'
            ROCE_3rd_year = 'Not available'
            ROCE_4th_year = 'Not available'
            ROCE_5th_year = 'Not available'
    except IndexError:
        roce_chart = 'Not available'
        ROCE_chart_values = []
        ROCE_1st_year = 'Not available'
        ROCE_2nd_year = 'Not available'
        ROCE_3rd_year = 'Not available'
        ROCE_4th_year = 'Not available'
        ROCE_5th_year = 'Not available'

    stock_info["ROCE_1st_Year"] = ROCE_1st_year
    stock_info["ROCE_2nd_Year"] = ROCE_2nd_year
    stock_info["ROCE_3rd_Year"] = ROCE_3rd_year
    stock_info["ROCE_4th_Year"] = ROCE_4th_year
    stock_info["ROCE_5th_Year"] = ROCE_5th_year
    return stock_info

def extract_sales_growth_percent(tree, stock_info):
    try:
        sales_growth_short = tree.xpath('//div[@id="mainContent_divSales"]//span[@class="durationvalue"]//text()')
    except IndexError:
        sales_growth_short = []
    for i in range(3):
        stock_info[f"Sales_Growth_%_{i + 1}th_Year"] = (
            sales_growth_short[i] if i < len(sales_growth_short) else "Not available"
        )

    return stock_info

def extract_profit_growth_percent(tree, stock_info):
    try:
        profit_growth_short = tree.xpath('//div[@id="mainContent_divProfit"]//span[@class="durationvalue"]//text()')
    except IndexError:
        profit_growth_short = []
    for i in range(3):
        stock_info[f"Profit_Growth_%_{i + 1}_Year"] = (
            profit_growth_short[i] if i < len(profit_growth_short) else "Not available"
        )
    return stock_info

def roe_percent_avg(tree, stock_info):
    try:
        roe_short = tree.xpath('//div[@id="mainContent_divROE"]//span[@class="durationvalue"]//text()')
    except IndexError:
        roe_short = []
    for i in range(3):
        stock_info[f"ROE_%_{i + 1}_Year"] = (
            roe_short[i] if i < len(roe_short) else "Not available"
        )
    return stock_info

def roce_percent_avg(tree, stock_info):
    try:
        roce_short = tree.xpath('//div[@id="mainContent_divROCE"]//span[@class="durationvalue"]//text()')
    except IndexError:
        roce_short = []
    for i in range(3):
        stock_info[f"ROCE_%_{i + 1}_Year"] = (
            roce_short[i] if i < len(roce_short) else "Not available"
        )
    return stock_info

def other_ratio(tree, stock_info):
    def extract_value(xpath_query):
        try:
            return tree.xpath(xpath_query)[0].strip()
        except (IndexError, AttributeError):
            return "Not available"
    stock_info["Debt_Equity"] = extract_value('//div[@id="mainContent_divDebtEquity"]//span[@class="Number"]//text()')
    stock_info["Price_to_Cash_Flow"] = extract_value('//div[@id="mainContent_divCash"]//span[@class="Number"]//text()')
    stock_info["Interest_Cover_Ratio"] = extract_value('//div[@id="mainContent_divICR"]//span[@class="Number"]//text()')
    stock_info["CFO_PAT"] = extract_value('//div[@id="mainContent_divCFOPAT"]//span[@class="Number"]//text()')
    return stock_info

def shareholding_pattern(tree, stock_info, url):
    api_headers = constant.api_headers
    api_headers['referer'] = url
    fincode = tree.xpath('//input[@id="mainContent_hffinc"]//@value')[0].strip()
    params = {
        'v': '4.0',
        'fincode': fincode,
    }
    share_holding_response = requests.get('https://ticker.finology.in/GetShares.ashx', params=params, headers=api_headers)
    share_holding_json = json.loads(share_holding_response.text)
    for sh in share_holding_json:
        stock_info[sh['Particulars']] = sh['Data']
    return stock_info

    
    
def extract_data(pagesource, url):
    soup = BeautifulSoup(pagesource, 'html.parser')
    tree = html.fromstring(pagesource)
    stock_info = {}
    stock_info = extract_price_summary(tree, stock_info)
    stock_info = extract_company_essential(tree, stock_info)
    stock_info = extract_finstar(tree, stock_info)
    stock_info = extract_sales_growth(tree, stock_info)
    stock_info = extract_profit_growth(tree, stock_info)
    stock_info = extract_roe_chart(tree, stock_info)
    stock_info = extract_sales_growth_percent(tree, stock_info)
    stock_info = extract_profit_growth_percent(tree, stock_info) 
    stock_info = roe_percent_avg(tree, stock_info)
    stock_info = roce_percent_avg(tree, stock_info)
    stock_info = other_ratio(tree, stock_info)
    stock_info = shareholding_pattern(tree, stock_info, url)
    return stock_info
    
def main(urls):
    # url = 'https://ticker.finology.in/company/RELIANCE',
    stock_list = []
    for url in urls:
        main_url_headers = constant.main_url_headers
        status_code, pagesource = get_req(url,main_url_headers)
        if status_code == 200:
            stock_info = extract_data(pagesource, url)
            stock_list.append(stock_info)
    df = pd.DataFrame(stock_list)
    df_transposed = df.set_index('Company_name').T
    df_transposed.to_excel('test_Output.xlsx')

        
        
if __name__== "__main__":
    urls = ['https://ticker.finology.in/company/RELIANCE',
           'https://ticker.finology.in/company/ITC',
           'https://ticker.finology.in/company/TATAMOTORS',
           'https://ticker.finology.in/company/ZOMATO']
    main(urls)
    

# with open('test.html', 'w+', encoding='utf-8') as f:
#     f.write(response.text)
    

