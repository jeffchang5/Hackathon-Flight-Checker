### All the configuration needed for the application

config = {
    # Necessary to use Google services
    "spreadsheet_id": "",
    "qpx_api_key": "",

    # Write dates in YYYY-MM-DD e.g. "2017-05-13"
    "date_start": "2017-09-16",
    "date_end": "2017-09-24",

    # Write times in HH:MM e.g. "13:00"
    "time_arrival_latest_time": "15:00",
    "time_departure_earliest_time": "15:00",

    # The format is in IATA airport. Choose your nearest international airport
    "destination": "DTW",

    # The format is the ISO code for your country
    "country_code": "US",

    # The name of your sheets on your Google Sheets
    "sheet_names": ["Domestic", "International"]

}
