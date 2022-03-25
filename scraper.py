from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import re
import json 
import datetime
from deep_translator import GoogleTranslator
from forex_python.converter import CurrencyRates

def convert_try_to_usd(price):
    c = CurrencyRates()
    tryTOusd = format(c.convert('TRY','USD',price),'.2f')
    return tryTOusd

def translate_text(text):
    translated = GoogleTranslator(source='tr', target='ar').translate(text=text)
    return translated
def id_from_url(url):
        # extract product id from a given url string
        pattern = r"(?<=-p-).[0-9]+"
        ID = re.search(pattern, url).group(0)
        return int(ID)

def json_site(url):
    r = requests.get(url)
    return json.loads(r.text)

def get_group_id(url):
    site_json = json_site(url)
    productGroupId = site_json['result']['productGroupId']
    return productGroupId

def title_description(url):
    site_json = json_site(url)
    title = site_json['result']['nameWithProductCode']
    title = translate_text(title)
    descriptions = site_json['result']['contentDescriptions']
    desc = ''
    for description in descriptions:
        d_text = description['description']
        try:
            d_text = d_text.replace('Trendyol', 'مولنا أونلاين')
        except :
            d_text = d_text
        try:
            d_text = d_text.replace(' TRENDYOL', 'مولنا أونلاين')
        except:
                d_text = d_text
            
        desc += '<p>' + translate_text(d_text) + '</p>' + '\n'
    return title,desc

def get_all_productURL(group_link, product_id):
    site_json = json_site(group_link)
    id_list = []
    if len(site_json['result']['slicingAttributes'])>0:
        attributes = site_json['result']['slicingAttributes'][0]['attributes']
    
        for content in attributes:
            # r = "https://www.trendyol.com"
            url_site = content['contents'][0]['url']
            id_product = id_from_url(url_site)
            id_list.append(id_product)
    else:
        
        id_list.append(product_id)
    
    return id_list

def get_data(id_list, productGroupId, base_url, list):
    for product_id in id_list:
        try:
            link = base_url.format(productId=product_id)
            site_json = json_site(link)
            color = site_json['result']['color']
            allVariants = site_json['result']['allVariants']
            variants = []           
            for val in allVariants:
                if len(allVariants) == 1 and val['value'] == '':
                    # Oversized Duvet Cover
                    try:
                        SKU = str(product_id) + '-' + '1' + '-' + color
                    except:
                        SKU = str(product_id) + '-' + '1' + '-' + 'None'
                    Var_inv_No = 7
                    variant = site_json['result']['attributes'][0]['value']
                    variants.append(('الأبعاد',variant['name'],Var_inv_No))
                else:
                    # Dress ....
                    try:
                        SKU = str(product_id) + '-' + val['value'] + '-' + color
                    except:
                        SKU = str(product_id) + '-' + val['value'] + '-' + 'None'
                    if val['inStock']:
                        Var_inv_No = 7
                    else:
                        Var_inv_No = 0   
                    variants.append(('المقاس',val['value'],Var_inv_No)) 
                        
            price = site_json['result']['price']
            
            originalPrice_value = price['originalPrice']['value']    
            compared_price = convert_try_to_usd(originalPrice_value)
            discountedPrice_value = price['discountedPrice']['value']
            sell_price = convert_try_to_usd(discountedPrice_value)
            # print(originalPrice_value, discountedPrice_value)
            # print(compared_price, sell_price)
            category = site_json['result']['category']['name']
            category = translate_text(category)
            try:
                vendor_satici = site_json['result']['brand']['name']
            except:
                vendor_satici = ''
            # print(vendor_satici)
            images = site_json['result']['images']
            image_url = "https://cdn.dsmcdn.com"
            try:
                try:
                    imag01 = image_url + images[0]
                except:
                    imag01 = ""

                try:
                    imag02 =  image_url + images[1]
                except:
                    imag02 = ""
                
                try:
                    imag03 =  image_url + images[2]
                except:
                    imag03 = ""
                try:
                    imag04 =  image_url + images[3]
                except:
                    imag04 = ""
                try:
                    imag05 =  image_url + images[4]
                except:
                    imag05 = ""
                try:
                    imag06 =  image_url + images[5]
                except:
                    imag06 = ""
            except:
                print('Error in images list')
            for v in variants:
                d = {}
                d['SKU'] = SKU
                d['Name'] = title
                d['Description'] = desc
                d['option1_name'] = v[0]  
                d['option1_value'] = v[1]
                d['option2_name'] = None
                d['option2_value'] = None
                d['cost_price'] = '10'
                d['Var_inv_No'] = v[2]
                d['weight'] = '1.5'
                d['compared_price'] = compared_price
                d['sell_price'] = sell_price
                d['tags'] = category
                d['vendor_satici'] = vendor_satici
                d['image 1'] = imag01
                d['image 2'] = imag02
                d['image 3'] = imag03
                d['image 4'] = imag04
                d['image 5'] = imag05
                d['image 6'] = imag06
                d['Original_link'] = link
                d['Original_Price_TRY'] = originalPrice_value
                list.append(d)
        except:
            pass

if __name__ == '__main__':
    
    time_now = datetime.datetime.now()
    base_url = "https://public.trendyol.com/discovery-web-productgw-service/api/productDetail/{productId}?storefrontId=1&culture=tr-TR&linearVariants=true"
    group_url = "https://public.trendyol.com/discovery-web-websfxproductgroups-santral/api/v1/product-groups/{productGroupId}"
    list = []
    with open('link.txt', 'r') as lines:
        for line in lines:
            try:
                link = line.strip()
                product_id = id_from_url(link)
                base_link = base_url.format(productId=product_id)
                # Get the title and description of all common product
                title,desc = title_description(base_link)
                productGroupId = get_group_id(base_link)
                group_link = group_url.format(productGroupId = productGroupId)
                id_list = get_all_productURL(group_link, product_id)
                get_data(id_list, productGroupId, base_url, list)
         
                # break
            except:
                pass
        
        pd.DataFrame(list).to_csv('Data.csv')
        lines.close()
    print(datetime.datetime.now() - time_now)

