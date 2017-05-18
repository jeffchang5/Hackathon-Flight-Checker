from __future__ import print_function

import os
import re

import grequests
import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from config import config

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flaRgs = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
QPX_API_URL = 'https://www.googleapis.com/qpxExpress/v1/trips/search'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Hackathon Flights'


class HackathonFlight:
    def __init__(self, config):
        self.QPX_EXPRESS_KEY = config["qpx_api_key"]
        self.SPREADSHEET_ID = config["spreadsheet_id"]
        self.COUNTRY_CODE = config["country_code"]

    def create_discovery_service(self):

        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('.')
        credential_dir = os.path.join(home_dir, 'credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'google-sheets-credentials.json')

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        http = credentials.authorize(httplib2.Http())
        self.credentials = credentials
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                        'version=v4')
        self.service = discovery.build('sheets', 'v4', http=http,
                                       discoveryServiceUrl=discoveryUrl)
    def read_from_spreadsheet(self):
        http = self.credentials.authorize(httplib2.Http())
        rangeName = self.sheet_name + '!B2:B'
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.SPREADSHEET_ID, range=rangeName).execute()
        values = result.get('values', [])
        if (values):
            print('Fetched cities from Google Sheets!')
            self.VALUES = []
            for item in values:
                if not item:
                    self.VALUES.append('')
                else:
                    self.VALUES.append(item[0])
        else:
            print('Can\'t read data from spreadsheets.')

    def write_to_spreadsheet(self):
        rangeName = self.sheet_name + '!C2'
        body = {
            'values': self.flight_data
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=rangeName,
            body=body,
            valueInputOption="USER_ENTERED").execute()
        print("Spreadsheet %s is updated!" % self.sheet_name)

    def _getFlightCosts(self, x):

        prices = []
        body = \
            {
                "request": {
                    "solutions": "5",
                    "saleCountry": config["country_code"],
                    "ticketingCountry": config["country_code"],
                    "passengers": {
                        "adultCount": 1
                    },
                    "slice": [
                        {
                            "origin": x,
                            "destination": config["destination"],
                            "date": config["date_start"],
                            "permittedDepartureTime": {
                                "latestTime": "15:00"
                            }
                        },
                        {
                            "origin": config["destination"],
                            "destination": x,
                            "date": config["date_end"],
                            "permittedDepartureTime": {
                                "earliestTime": "15:00"
                            }
                        }
                    ],
                }
            }
        return body

    def _mapAirportToRequestBody(self, x):

        if (re.match("^[A-Z]{3}$", x)):
            return self._getFlightCosts(x)
        else:
            return ['', '']

    def get_flight_data(self):
        print("Getting flight costs for %s!" % self.sheet_name)
        self.flight_data = []
        url = '%s?key=%s' % (QPX_API_URL, self.QPX_EXPRESS_KEY)
        self.json_request_body = list(map(self._mapAirportToRequestBody, self.VALUES[0:2]))
        rs = (grequests.post(url=url, json=body) for body in self.json_request_body)
        response = grequests.map(rs)
        for res in response:

            res = res.json()
            if 'tripOption' not in res["trips"]:
                print("1. The primary airline is American Airlines or Delta")
                print("2. The airline code is incorrect")
                self.flight_data.append(["Couldn't find cost", "Couldn't find airline"])

            else:
                self.flight_data.append([
                    res["trips"]["tripOption"][0]["saleTotal"][3:],
                    res["trips"]["tripOption"][0]["slice"][0]["segment"][0]["flight"]["carrier"]
                ])

    def run(self):
        self.create_discovery_service()
        for i in config["sheet_names"]:
            self.sheet_name = i
            self.read_from_spreadsheet()
            self.get_flight_data()
            self.write_to_spreadsheet()
        print("Finished!")


if __name__ == '__main__':
    flights = HackathonFlight(config=config)
    flights.run()
