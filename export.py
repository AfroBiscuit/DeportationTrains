"""Create GeoJSON export of public DeportationTrains Google Sheets data."""
import json
import requests


MAP_ENGINE_URL = (
    'https://spreadsheets.google.com/feeds/list/'
    '1PdSBY70PJal_xMjLy_igDddDwgbGQC_URlIJelAHKXE/3/public/full?alt=json'
)
PEOPLE_URL = (
    'https://spreadsheets.google.com/feeds/list/'
    '1PdSBY70PJal_xMjLy_igDddDwgbGQC_URlIJelAHKXE/2/public/full?alt=json'
)


def offset_date(day: str, month: str, year: str, offset: int) -> str:
    """Constructs a valid ISO 8601 date string from day, month and year
    values. If a provided day or month value is empty space (.e.g ' ') or
    falsy (e.g. ''), defaults to the middle value for that given period. The
    year value is offset to work around pre-1970 date issues in
    Leaflet.TimeDimension.

    Args:
        day: Day of the month (DD, e.g., 03).
        month: Month of the year (MM, e.g., 11).
        year: Any year (YYYY, e.g., 1901).
        offset: A postive number of years to offset the year by (e.g., 52).
    Returns:
        Valid date string as per ISO 8601 (YYYY-MM-DD, e.g., 1901-11-03).
    """
    time = [
        str(int(year) + offset),
        month.strip() or '06',
        day.strip() or '15'
    ]
    return '-'.join(time)


def date_certainty(day: str, month: str, year: str) -> str:
    """Determine if a date should be considered exact or not."""
    if day and month and year:
        return 'Exact'
    else:
        return 'Estimated'


def generate_deportee_feature_collection(deportee_map_data, deportee_properties_data):
    """Return a GeoJSON feature collection for a given individual."""
    deportee = {
        'features': generate_deportee_features(deportee_map_data),
        'properties': generate_deportee_properties(deportee_properties_data),
        'type': 'FeatureCollection'
    }
    return deportee


def valid_lat_long(row):
    return row['gsx$long']['$t'].strip() and row['gsx$lat']['$t'].strip()


def generate_deportee_features(deportee_map_data):
    features = [
        generate_feature(row) for row in deportee_map_data if valid_lat_long(row)
    ]
    return features


def generate_feature(row):
    """
    Generates a geojson feature from row data provided by a google spreadsheets
    json export.

    Input: Row from google sheets in json
    Output: geojson feature object

    Notes: Alternative method to look into is looping over keys beginning with 'gsx$',
    but this doesn't seem necessary given the low number of keys and low likelyhood
    of big schema changes.
    """

    datecertainty = row['gsx$datecertainty']['$t'] or date_certainty(
        row['gsx$startday']['$t'],
        row['gsx$startmonth']['$t'],
        row['gsx$startyear']['$t']
    )

    time = offset_date(
        row['gsx$startday']['$t'],
        row['gsx$startmonth']['$t'],
        row['gsx$startyear']['$t'],
        100
    )

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [float(row['gsx$long']['$t']), float(row['gsx$lat']['$t'])]
        },
        "properties": {
            "name": row['gsx$name']['$t'],
            "status": row['gsx$status']['$t'],
            "event": row['gsx$event']['$t'],
            "startyear": row['gsx$startyear']['$t'],
            "time": time,
            "endyear": row['gsx$endyear']['$t'],
            "startmonth": row['gsx$startmonth']['$t'],
            "endmonth": row['gsx$endmonth']['$t'],
            "startday": row['gsx$startday']['$t'],
            "endday": row['gsx$endday']['$t'],
            "datecertainty": datecertainty,
            "place": row['gsx$place']['$t'],
            "city": row['gsx$city']['$t'],
            "state": row['gsx$state']['$t'],
            "country": row['gsx$country']['$t'],
            "notes": row['gsx$notes']['$t'],
            "trainidentifier": row['gsx$trainidentifier']['$t']
        },
        "id": row['gsx$uniquepersonidentifier']['$t']
    }
    return feature


def generate_deportee_properties(deportee_properties_data):
    properties = {}
    for value in deportee_properties_data[0]:
        if 'gsx$' in value:
            value_name = value[4:]
            properties[value_name] = deportee_properties_data[0][value]['$t']
    return properties


def export_output(output):
    with open('static/data.geojson', 'w') as export_file:
        json.dump(output, export_file, sort_keys=True, indent=4)


def main():
    """Main execution body."""
    map_data = requests.get(MAP_ENGINE_URL).json()['feed']['entry']
    properties_data = requests.get(PEOPLE_URL).json()['feed']['entry']

    deportees = list(set([x['gsx$name']['$t'] for x in properties_data]))
    trains = list(set([x['gsx$trainid']['$t'] for x in properties_data]))
    ethnicities = list(set([x['gsx$ethnicity']['$t'] for x in properties_data]))

    output = {
        "filters": {
            "trains": trains,
            "deportees": deportees,
            'ethnicities': ethnicities
        },
        "geojson": {}
    }

    for deportee in deportees:
        deportee_map_data = [row for row in map_data if row['gsx$name']['$t'] == deportee]
        deportee_properties_data = [row for row in properties_data if row['gsx$name']['$t'] == deportee]

        if deportee_map_data:  # What to do if name but no data?
            output['geojson'][deportee] = generate_deportee_feature_collection(
                deportee_map_data,
                deportee_properties_data
            )

    export_output(output)


if __name__ == "__main__":
    main()
