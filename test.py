from requests import get, post
from lxml import html

url = 'https://youla.ru/moskva/nedvijimost/kommercheskaya-nedvijimost/arienda-pomieshchieniie-svobodnogho-naznachieniia-0-m2-5d3f064f686bc4d286431696'

html_ = get(url)
page = html.fromstring(html_.text)
print(page.xpath('//div[@class="itemDesc"]/a[2]/@href'))
print(html_.text.find('sc-kSFxNF bMqDsV'))
print(html_.text)
# print(type(''))