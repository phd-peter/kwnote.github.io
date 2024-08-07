# import requests

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=9O3EU71W6YBBFWYA'
# r = requests.get(url)
# data = r.json()

# print(data)


import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=a&apikey=undefined'
r = requests.get(url)
data = r.json()

print(data)