import csv
import json

with open("city.list.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

# 1. Определить количество городов в файле.
def get_count_cities(lst: list[dict]) -> int:
    return len(lst)
print(get_count_cities(data)) # 209579

# 2. Создать словарь, где ключ — это код страны, а значение — количество городов.
def get_dict_count_cities_by_countries(lst: list) -> list:
   return list(map(lambda x: {x : len(list(filter(lambda y: y["country"] == x, lst)))}, set(map(lambda x: x["country"], lst))))
print(get_dict_count_cities_by_countries(data))

# 3. Подсчитать количество городов в северном полушарии и в южном.
def get_count_cities_poles(lst: list[dict]) -> dict:
    north = 0
    south = 0
    for n in range(len(lst)):
        if lst[n]["coord"]["lon"] > 0:
            north += 1
        elif lst[n]["coord"]["lon"] < 0:
            south += 1
    return {"north": north, "south": south}
print(get_count_cities_poles(data)) # {'north': 141445, 'south': 68113}

# 4. Перевести в CSV файл данные по городам (координаты представить в виде строки значений через запятую).
def json_to_csv(lst: list[dict], filename: str) -> None:
     for n in range(len(lst)):
         lst[n] = lst[n].copy() # чтобы не менялись элементы исходного списка data
         lst[n]["coord"] = f"{lst[n]["coord"]["lon"]}, {lst[n]["coord"]["lat"]}"
     with open(filename, "w", encoding="utf-8") as csv_file:
         writer = csv.DictWriter(csv_file, delimiter=",", lineterminator="\r", fieldnames=lst[0].keys())
         writer.writeheader()
         writer.writerows(lst)
json_to_csv(data.copy(), "city.csv")

# 5. Создать другой JSON файл, в который сохранить только города одной выбранной страны.
def get_cities_by_country(lst: list[dict], country_name: str) -> list[dict]:
    return list(filter(lambda x: x["country"] == country_name, lst))
print(get_cities_by_country(data, "RU"))

# 6. Для каждой страны создать свой файл JSON с данными городов. Лучше создать отдельную папку в PyCharm, и указать путь к новому файлу с этой папкой.
path = "Cities"
countries = set(map(lambda x: x["country"], data))
for country in countries:
    with open(f"{path}/{country}.json", "w", encoding="utf-8") as json_file:
        json_file.write(get_cities_by_country(data, country).__str__())

# 7. Необходимо сформировать geojson файл с координатами городов для одной страны. Формат geojson используется для хранения и обмена географическими данными в виде JSON.
def get_geojson(lst: list[dict], country_name: str) :
    cities = list(filter(lambda x: x["country"] == country_name, lst))
    return (
        f'{{"type": "FeatureCollection", "features": {
        list(map(lambda x: {
            "type": "Feature",
            "id": x["id"], 
            "geometry": {
                "type": "Point", 
                "coordinates": [x["coord"]["lon"], x["coord"]["lat"]],
            }, 
            "properties": {
                "iconCaption": x["name"], 
                "marker-color": "#b51eff",
            },
        }, cities)).__str__().replace("'", '"')
        }}}'
    )

with open("LR.geojson", "w", encoding="utf-8") as json_file:
    json_file.write(get_geojson(data, "LR"))