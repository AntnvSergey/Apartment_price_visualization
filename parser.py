from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import time
import folium
import pandas as pd
from pandas import DataFrame


class CaptchaError(Exception):
    pass


# headers for get requests
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://cian.ru",
        "Connection": "keep-alive",
        "Cache-Control": 'no-cache',
    }

# List of St. Petersburg districts and their index
list_of_spb_district = {"Admiralteysky": 150, "Kirovsky": 146, "Kyrortniy": 141,
                        "Petrodvoretsovy": 137, "Vasileostrovky": 149, "Kolpinsky": 145,
                        "Moscow": 140, "Primorksky": 136, "Vyborg": 148,
                        "Krasnogvardeisky": 144, "Nevsky": 139, "Pushkinsky": 135,
                        "Kalininsky": 147, "Krasnoselsky": 143, "Frunze": 134,
                        "Petrogradsky": 138, "Central": 133, "Kronstadt": 142}

# List of Moscow districts and their index
list_of_moscow_district = {"Novomoskovsky": 325, "Northwestern": 1, "Northern": 5,
                           "Northeastern": 6, "Troitsky": 326, "West": 11, "Central": 2,
                           "Eastern": 7, "Zelenogradsky": 151, "Southwestern": 2,
                           "South": 9, "Southeastern": 8}

# List of Ekaterinburg districts and their index
list_of_ekb_district = {"VerkhIsetsky": 286, "Kirovsky": 289, "Oktyabrsky": 290,
                        "Chkalovsky": 291, "Zheleznodorozhnyy": 287, "Leninsky": 292,
                        "Ordzhonikidzevsky": 288}


city_district = {"St.Petersburg": list_of_spb_district,
                 "Moscow": list_of_moscow_district,
                 "Ekaterinburg": list_of_ekb_district}


def get_url(city, index, count):
    """Return url for a specific city"""

    city_url = {"St.Petersburg": f'https://spb.cian.ru/cat.php?deal_type=sale\
&district%5B0%5D={index}&engine_version=2&offer_type=flat&p={count}\
&region=2&room1=1&room2=1&room3=1',
                "Moscow": f'https://www.cian.ru/cat.php?deal_type=sale\
&district%5B0%5D={index}&engine_version=2&offer_type=flat&p={count}\
&region=1&room1=1&room2=1&room3=1',
                "Ekaterinburg": f'https://ekb.cian.ru/cat.php?deal_type=sale\
&district%5B0%5D={index}&engine_version=2&offer_type=flat&p={count}\
&region=4743&room1=1&room2=1&room3=1'}
    return city_url[city]


def get_average(data):
    """Sorts the list and returns the average value"""
    if len(data) == 0:
        print("Most likely captcha appeared on the page, try to run the program\
after some time or change ip address")
        raise Captcha_Error
    else:
        data.sort()
        index = len(data) // 2
        return data[index]


def get_pages(city):
    """Save pages for all city district"""
    district_list = {}
    session = requests.Session()

    for district, index in city_district[city].items():
        page_list = []

        for count in range(1, 4):
            time.sleep(5)
            page = session.get(get_url(city, index, count), headers=HEADERS)
            page_list.append(page)
        district_list[district] = page_list

    return district_list


def get_info(page_list):
    """Find and return information like average total price, price per meter and area
     for all city district"""
    total_price_list = []
    price_per_meter_list = []
    area_list = []

    for district, value in page_list.items():
        pages_total_price = []
        pages_price_per_meter = []
        pages_area = []

        for page in value:
            soup = BeautifulSoup(page.text, 'html.parser')
            content = soup.findAll("div", {"class": "c6e8ba5398--price_flex_container--2kbcb"})

            for result in content:
                info = result.text.replace('₽/м²', '')
                price = info.replace(' ', '').split('₽')
                price = list(map(int, price))
                price.append(round(price[0] / price[1], 1))
                pages_total_price.append(price[0])
                pages_price_per_meter.append(price[1])
                pages_area.append(price[2])

        total_price_list.append(get_average(pages_total_price))
        price_per_meter_list.append(get_average(pages_price_per_meter))
        area_list.append(get_average(pages_area))

    return total_price_list, price_per_meter_list, area_list


def plot_histogram(x, y, x_label, y_label, title):
    """Plot histogram"""
    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title(title)
    plt.xlabel(x_label)
    plt.xticks(rotation=90)
    plt.ylabel(y_label)
    plt.grid()
    plt.show()
    fig.savefig(title+"/"+y_label)


def save_info(filename, districts, tot_price, price_meter, areas):
    """Save information about city in a csv file to build a map"""
    data = {'district': districts,
            'total_price': tot_price,
            'price_per_meter': price_meter,
            'area': areas
            }
    df = DataFrame(data, columns=['district', 'total_price', 'price_per_meter', 'area'])
    df.to_csv(f'{filename}.csv', index=None, header=True)


def show_map(city):
    """Build a city map. You can see map in html file"""

    city_coordinates = {
        'St.Petersburg': (59.934551, 30.332822),
        'Moscow': (55.753518, 37.622558),
        'Ekaterinburg': (56.835566, 60.612731)
    }
    map = folium.Map(location=city_coordinates[city], zoom_start=12)
    state_geo = city+'.geojson'
    state_data = pd.read_csv(city+".csv")

    folium.Choropleth(
        geo_data=state_geo,
        name='choropleth',
        data=state_data,
        columns=['district', 'price_per_meter'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Price per meter'
    ).add_to(map)
    map.save(city+'.html')


city = input()

district_list = get_pages(city)
total_price, price_per_meter, area = get_info(district_list)

save_info(city, list(city_district[city].keys()), total_price, price_per_meter, area)
plot_histogram(city_district[city].keys(), total_price, "district", "total_price", city)
plot_histogram(city_district[city].keys(), area, "district", "area", city)

show_map(city)
