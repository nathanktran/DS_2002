This API returns the current time and UTC offset for a given capital city.  
The base URL is: http://34.42.54.251:5050/api/time  
All requests must include a valid token. The token in this example is ilikehamburgers6144  
If a valid token is not given, there will be a 401 Unauthorized error.  
  
Example request:  
http://34.42.54.251:5050/api/time?city=Tokyo&token=ilikehamburgers6144  
  
Example response:  
{  
  "city": "Tokyo",  
  "current_time": "2025-04-21 22:15:30",  
  "utc_offset": "+0900"  
}  
  
If a city is missing or an invalid city is given, there will be an error.  
  
List of cities:  
Washington  
London  
Tokyo  
Paris  
Canberra  
Ottawa  
Brasília  
New Delhi  
