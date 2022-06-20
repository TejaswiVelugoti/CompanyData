import requests
from lxml import html
import re
import json
import csv

data_urls = []
company_data = []
sitemap_url = "https://clutch.co/sitemap.xml"
response = requests.get(sitemap_url)
tree = html.fromstring(response.content)
profile_urls = tree.xpath("//loc//text()[contains(., 'profile')]")
for p in profile_urls:
    prof_resp = requests.get(p)
    prof_tree = html.fromstring(prof_resp.content)
    data_urls.extend(prof_tree.xpath("//loc//text()[contains(., 'profile')]"))

for d in data_urls:
    data_response = requests.get(d)
    data_tree = html.fromstring(data_response.content)
    company = re.sub("\s+",'',"".join(data_tree.xpath("//h1[@class='header-company--title']//text()")))
    website = re.sub("\s+",'',"".join(data_tree.xpath("//h1//a[@class='website-link__item']/@href")))
    location = re.sub("\s+",'',"".join(data_tree.xpath("//span[@class='location-name']//text()")))
    contact = re.sub("\s+",'',"".join(data_tree.xpath("//a[@class='contact phone_icon']//text()")))
    rating = re.sub("\s+",'',"".join(data_tree.xpath("//section[@id='summary_section']//span[@itemprop='ratingValue']//text()")))
    review_count = re.sub("\s+",'',"".join(data_tree.xpath("//section[@id='summary_section']//span[@itemprop='reviewCount']//text()")))
    hourly_rate = re.sub("\s+",'',"".join(data_tree.xpath("//section[@id='summary_section']//div[@data-content='<i>Avg. hourly rate</i>']//span/text()")))
    min_project_size = re.sub("\s+",'',"".join(data_tree.xpath("//section[@id='summary_section']//div[@data-content='<i>Min. project size</i>']//span/text()")))
    employee_size = re.sub("\s+",'',"".join(data_tree.xpath("//section[@id='summary_section']//div[@data-content='<i>Employees</i>']//span/text()")))
    
    company_data.append({'company':company, 'website':website, 'location':location, 'contact':contact, 'rating':rating, 'review_count':review_count, 'hourly_rate':hourly_rate, 'min_project_size':min_project_size, 'employee_size':employee_size})

dump_jsondata = json.dumps(company_data)
jsondata = json.loads(dump_jsondata)

data_file = open('companies.csv', 'w')

csv_writer = csv.writer(data_file)
 
count = 0
for data in jsondata:
    if count == 0:
        header = data.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(data.values())
data_file.close()
