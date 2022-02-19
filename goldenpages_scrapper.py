import requests
from bs4 import BeautifulSoup
near= 'County Limerick'
near=near.replace(' ','+')
i_am_looking_for = 'solicitor'
i_am_looking_for = i_am_looking_for.replace(' ','+')

def make_request(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'lxml')
    return soup

def extract_links_form_all_pages():
    links = []
    url = f'https://www.goldenpages.ie/q/business/advanced/where/{near}/what/{i_am_looking_for}/'
    while True:
        soup = make_request(url)
        result_tag = soup.find('div' , id= 'listing_results')
        a_tags = result_tag.find_all('a' ,class_="listing_base_link")
        for a_tag in a_tags:
            link = 'https://www.goldenpages.ie'+a_tag['href']
            links.append(link)
            
        #next page
        pagination_tag = soup.find('ul' ,id='pagination')
        next_page_link =  pagination_tag.find('button' , id = 'btn_pagination_next')
        if(next_page_link==None):
            break
        else:
            url = 'https://www.goldenpages.ie'+next_page_link['data-url']
    
    return links

def extract_data_from_each_link(links):
    i = 1
    for link in links:
        print(link)
        soup = make_request(link)
        try:
            #company name
            h1_tag = soup.find('h1' , class_='company_name')
            company_name = h1_tag.find('span')
            #company address
            company_address = soup.find('p' , class_= 'company_address')
            # other deatils
            div_tag = soup.find('div' , class_='details_contact_other col_item width_2_4')
            li_tags = div_tag.find_all('li')
        
            #print information
            print("Sr No:"+str(i))
            if(company_name == None):
                print("Company Name: Not available")
            else:
                 print("Company Name:"+company_name.text)
                
            if(company_address==None):
                print("Company Address: Not available")
            else:
                print("Company Address: "+company_address.text)
            for li_tag in li_tags:
                if(li_tag.span['class'][0] == 'icon_phone'):
                    print('Phone no: '+ li_tag.text.strip())
                if(li_tag.span['class'][0] == 'icon_email'):
                    print('Email: '+ li_tag.text.strip())
                if(li_tag.span['class'][0] == 'icon_website'):
                     print('Website: '+ li_tag.text.strip())
            print(' ')
        except:
            print("No Data Available")
            print(' ')
        
        i = i +1

        

def main():
    links = extract_links_form_all_pages()
    extract_data_from_each_link(links)

if __name__ == '__main__':
    main()