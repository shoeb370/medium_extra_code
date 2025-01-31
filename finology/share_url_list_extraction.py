import requests
import csv
import ticket_constant as constant
from bs4 import BeautifulSoup
from lxml import html

headers = constant.pagination_headers


def get_req(url, headers):
    response = requests.get(url, headers=headers)
    return response.status_code, response.text


def get_stock_url(tree):
    raw_url = tree.xpath('//a[@class="btn btn-sm btn-primary ml-0 col-4"]//@href')
    url_list = ['https://ticker.finology.in' + url for url in raw_url]
    return url_list


def next_page_url(tree):
    try:
        return tree.xpath('//a[@id="mainContent_lnkNext"]//@href')[0]
    except IndexError:
        return None


def extract_data(start_url, headers, output_file):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Stock URL"])  # Header row
        
        url = start_url
        while url:
            response_status_code, page_source = get_req(url, headers)
            if response_status_code != 200:
                break
            
            soup = BeautifulSoup(page_source, 'html.parser')
            tree = html.fromstring(page_source)
            url_bucket = get_stock_url(tree)
            
            for stock_url in url_bucket:
                writer.writerow([stock_url])
            
            next_url_suffix = next_page_url(tree)
            if next_url_suffix:
                url = next_url_suffix
            else:
                break


if __name__ == "__main__":
    start_url = 'https://ticker.finology.in/company?page=1'
    output_file = 'stock_urls_list.csv'
    extract_data(start_url, headers, output_file)
    print(f"Stock URLs have been saved to {output_file}")
