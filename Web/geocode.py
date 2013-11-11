from pygeocoder import Geocoder
from geopy import geocoders

results = Geocoder.geocode("San Francisco, CA")

# print(results[0]) # prints written location
# print(results.count) # number of results
# print(results[0].coordinates) # need this to add to map - latlng
# print(results[0].country) # prints country
# print(results[0].postal_code) # zipcode

# address validation
# print Geocoder.geocode("683 sutter st, sf, ca").valid_address

# result = Geocoder.geocode("683 sutter st, sf, ca")
# result.valid_address
# print(result)

address = "683 Sutter St"
city = "SF"
state = "CA"
zipcode = "94108"
full_address = address + city + state + zipcode
print full_address

# result = Geocoder.geocode(full_address)
# print result
# print result.coordinates

g = geocoders.GoogleV3()
address = g.geocode(full_address)
print address[0]
print address[1]