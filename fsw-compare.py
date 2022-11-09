import requests

headers = {
    "User-Agent": "FSW/OSRS Opt-out tool (personal) SaltySaltySalt#1337"
}
time_range = "1h"
base_url = "https://prices.runescape.wiki/api/v1"
osrs_avgs = requests.get(f"{base_url}/osrs/{time_range}", headers=headers).json()['data']
fsw_avgs = requests.get(f"{base_url}/fsw/{time_range}", headers=headers).json()['data']

good_items = []
failures = 0

def get_profit(line):
    return line['profit']

for item in osrs_avgs:
    osrs_prices = osrs_avgs[item]
    if item in fsw_avgs:
        fsw_prices = fsw_avgs[item]
        try:
            osrs_avg_price = (osrs_prices['avgHighPrice'] + osrs_prices['avgLowPrice'])/2
            fsw_avg_price = (fsw_prices['avgHighPrice'] + fsw_prices['avgLowPrice'])/2
        except:
            #print(f'Item {item} doesn\'t have a price in fsw data yet :(')
            continue
    else:
        #print(f'Item {item} doesn\'t exist in fsw data yet :(')
        failures += 1
        continue

    if (osrs_avg_price > fsw_avg_price):
        perc_increase = (osrs_avg_price/fsw_avg_price)*100
        good_items.append({'id':item,'profit':perc_increase})

print(f"{len(good_items)} potential items. {failures} don't yet exist in FSW data.")


sorted_list = sorted(good_items, key=get_profit)

print("LOWEST PROFIT")
for x in sorted_list[0:5]:
    print(f"Item: {x['id']} Profit margin: {round(x['profit'])}%")
print("HIGHEST PROFIT")
for y in sorted_list[-5:]:
    print(f"Item: {y['id']} Profit margin: {round(y['profit'])}%")