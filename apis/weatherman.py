def currentWeather(city='Provo', state='UT'):
    """
    get the current weather for the given city, state
    @param city: String, the city name
    @param state: String, 2 letter state abbreviation (UT)
    @return weather: Dict with status, temp rain (mm), and cloud %
    """
    import requests
    import json

    # send the request and get the data
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=%s,%s' % (city, state))
    data = json.loads(r.text)
    weather = {
        'status': '',
        'temp': '',
    }

    weather['status'] = data['weather'][0]['main']
    weather['temp'] = int((data['main']['temp'] - 273.15)*1.8000 + 32) # convert Kelvin to F

    return weather
