import json
import requests
import urllib.request
from lxml import html
from collections import OrderedDict
import argparse

def parse(source, destination, date):
    for i in range(1):
        try:
            url = 'https://www.expedia.com/Flights-Search?trip=oneway&leg1=from:{0},to:{1},departure:{2}TANYT&passengers=adults:1,children:0,seniors:0,infantinlap:Y&options=cabinclass:economy&mode=search&origref=www.expedia.com'.format(source,destination,date)
            print(url)
            headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
            response = requests.get(url, headers = headers, verify = False)
            parser = html.fromstring(response.text)
            json_data_xpath = parser.xpath('//script[@id="cachedResultsJson"]/text()')
            raw_json = json.loads(json_data_xpath[0] if json_data_xpath else '')
            flight_data = json.loads(raw_json["content"])

            flight_infor = OrderedDict()
            lists = []
            # with open('flight-data.json','w') as file:
            #     json.dump(flight_data, file)
            for i in flight_data['legs'].keys():
                total_distance = flight_data['legs'][i].get('formattedDistance','')
                exact_price =  flight_data['legs'][i].get('price',{}).get('totalPriceAsDecimal','')
                departure_location_airport = flight_data['legs'][i].get('departureLocation',{}).get('longName','')
                departure_location_city = flight_data['legs'][i].get('departureLocation',{}).get('airportCity','')
                departure_location_airport_code = flight_data['legs'][i].get('departureLocation',{}).get('airportCode','')

                arrival_location_airport = flight_data['legs'][i].get('arrivalLocation',{}).get('longName','')
                arrival_location_airport_code = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCode','')
                arrival_location_airport_city = flight_data['legs'][i].get('arrivalLocation',{}).get('airportCity','')
                airline_name = flight_data['legs'][i].get('carrierSummary',{}).get('airlineName','')

                no_of_stops = flight_data['legs'][i].get('stops','')
                flight_duration = flight_data['legs'][i].get('duration',{})
                flight_hour = flight_duration.get('hours','')
                flight_minutes = flight_duration.get('minutes','')
                flight_days = flight_duration.get('numOfDays','')

                if no_of_stops == 0:
                    stop = 'Nonstop'
                else:
                    stop = str(no_of_stops) + 'Stop'

                total_flight_duration = '{0} days {1} hours {2} minutes'.format(flight_days, flight_hour, flight_minutes)
                departure = departure_location_airport + ', ' + departure_location_city
                arrival = arrival_location_airport + ', ' + arrival_location_airport_city
                carrier = flight_data['legs'][i].get('timeline',[])[0].get('carrier',{})
                plane = carrier.get('plane','')
                plane_code = carrier.get('planeCode','')
                formatted_price = '{0:.2f}'.format(exact_price)
                
                if not airline_name:
                    airline_name = carrier.get('operatedBy','')

                timings = []
                for timeline in flight_data['legs'][i].get('timeline',{}):
                    if 'departureAirport' in timeline.keys():
                        departure_airport = timeline['departureAirport'].get('longName','')
                        departure_time = timeline['departureTime'].get('time','')
                        arrival_airport = timeline['arrivalAirport'].get('longName','')
                        arrival_time = timeline['arrivalTime'].get('time','')
                        flight_timing = {
                            'departure_airport':departure_airport,
                            'departure_time':departure_time,
                            'arrival_airport':arrival_airport,
                            'arrival_time':arrival_time,
                        }
                        timings.append(flight_timing)

                flight_infor =  {
                    'stops':stop,
                    'ticket price':formatted_price,
                    'departure':departure,
                    'arrival':arrival,
                    'flight_duration':flight_duration,
                    'airline':airline_name,
                    'plane':plane,
                    'plane_code':plane_code
                }
                lists.append(flight_infor)
                sortedlist = sorted(lists, key=lambda k:k['ticket price'], reverse=False)
                print('test...' + str(i))
                return sortedlist
        except ValueError:
            print('Retrying...')

    return {'error':'failed to process the page.'}

if __name__ == '__main__':
    argparse = argparse.ArgumentParser()
    argparse.add_argument('source', help = 'Source airport code')
    argparse.add_argument('destination', help = 'Destination airport code')
    argparse.add_argument('date', help = 'MM/DD/YYYY')

    args = argparse.parse_args()
    source = args.source
    destination = args.destination
    date = args.date

    print('Fetching flight details')
    scrape_data = parse(source, destination, date)
    print('Writing data to out put file')
    with open('%s-%s-flight-result.json'%(source,destination),'w') as fp:
        json.dump(scrape_data,fp,indent=4)
