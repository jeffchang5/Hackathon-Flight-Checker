# Hackathon Flight Checker

Given a column of airports in Google Sheets, this will look at the lowest price for each flight from a specific location and record it in Google Sheet.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

* Python 3.x
* Follow this [link](https://console.developers.google.com/start/api?) to create a new project and enable Google QPX Express API and copy the API key into the `config.py` file.
* An `client_secret.json` file for the Google Sheets API. 
	* 	 Go to [this wizard](https://console.developers.google.com/start/api?id=sheets.googleapis.com) and create an application.
	* 	 On the **Add credentials** to your project page, click the **Cancel** button.
	* 	 At the top of the page, select the **OAuth consent screen** tab. Select an **Email address**, enter a **Product name** if not already set, and click the **Save** button.
	* 	 Select the **Credentials** tab, click the **Create credentials** button and select **OAuth client ID**.
	* 	 Select the application type **Other**, enter whatever you want as the name, and click the **Create** button.
	* 	 Click **OK** to dismiss the resulting dialog.
	* 	 Click the  **Download JSON** button to the right of the client ID.
	* 	 Move this file to the root of the project and rename it `client_secret.json`.
* 	 This application follows a specific structure for writing to a Google Spreadsheet. Copy this [Google Sheet](https://docs.google.com/a/umich.edu/spreadsheets/d/1PUOzcKsndwybYyNek_cGk1ttwslFw66Gxu_iojYfWCo/edit?usp=sharing) to get started. Make sure to enter the Airport IATA Code as this will read that code from the B column. By default, this will write to the C and D columns the price and the IATA code for that airline. Feel free to suggest more cities in the Google Sheet.




### Installing

Install the packages for this application. In terminal, at the root of the project, enter

```bash
pip install -r requirements.txt
```
or

```bash
pip3 install -r requirements.txt
```



Write the `config.py` file at the root of the project with the structure.

The `spreadsheet_id` is an unique identifier for the Google Sheet. For example, the bolded portion of the following url would be the spreadsheet ID.
> https://docs.google.com/spreadsheets/d/**1PUOzcKsndwybYyNek_cGk1ttwslFw66Gxu_iojYfWCo**



```python
config = {
    # Necessary to use Google services
    "spreadsheet_id": "Spreadsheet ID",
    # 
    "google_api_key": "API_KEY",

    # Write dates in YYYY-MM-DD e.g. "2017-05-13"
    "date_start": "2017-01-01",
    "date_end": "2017-01-01",

    # Write times in HH:MM e.g. "13:00"
    "time_arrival_latest_time": "12:00",
    "time_departure_earliest_time": "12:00",

    # The format is in a standard IATA code for an airport. Choose your nearest international airport. This is the destination. 
    "destination": "DTW",

    # The format is the ISO code for your country
    "country_code": "US",

    # The name of your sheets on your Google Sheets
    "sheet_names": ["Domestic", "International"]

}
```

## Running
Run `python3 main.py` or `python main.py`!
## Notes
* QPX Express has a free quota of 50 requests per day.
* You must be authorized to read/write to the Google Sheet for this to work. 
* The QPX Express API does not support American Airlines or Delta. Keep this in mind.
* If American Airlines or Delta are the only primary airlines flying, this will write a message to your Sheet.

## Contributing

If you have any features you want to add. Fork and pull request!


## Authors

* **Jeffrey Chang** - [GitHub](https://github.com/jeffchang5) 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

