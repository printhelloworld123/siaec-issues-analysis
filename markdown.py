# Markdown Text #

markdown_text_page_1_section_1_1 = '''
There was an anomalous increase in booking mismatches between 17 May to 31 May. 
This was due to backend issues leading to the loss of precision in stored address coordinates. 
This issue has been resolved. Since 31 May, the daily mismatch rate has been reduced to 
an average of approximately 10% a day (which is close to the approximately 9.07% daily mismatch rate 
before the backend issues occured).
'''

markdown_text_page_1_section_2_1 = '''
Most of the mismatches that occured after 31 May are due to the feature of our app, instead of a bug. 
As seen from the map visualization, our app is programmed to offer passengers a waypoint (from our database) 
that is located closest to their requested waypoint. 
Thus, for instance, a passenger may request to be booked from Blk 408. However, their requested coordinate may be closer 
to the waypoint for Blk 409. In this case, our app will allocate the passenger Blk 409 instead of Blk 408.
'''

markdown_text_page_1_section_2_2 = '''
Additionally, as seen from the histogram, most of the offered locations are within 10m of the 
requested locations. In contrast, there is a wider spread of distance deviation (beyond 10m) between the 
requested location and the onemap location (proxy for user's actual intended location).
'''

markdown_text_page_1_section_2_3 = '''
Evident from the map and the histogram plot, most of the prevailing mismatches are not caused by
unresolved bugs. Rather, they are due to features on our app created to provide users with a
waypoint closest to their requested waypoint (which may nor may not take reference to the same building as
user's requested waypoint).
'''

markdown_text_page_2_section_1_1 = '''
1) Collate a list of all pickup and drop-off home addresses 
'''
markdown_text_page_2_section_1_2 = '''
2) Based on user's requested_name for the waypoints, clean up the name into a format that can be taken in by 
OneMap's API (infer user intention)
'''

markdown_text_page_2_section_1_3 = '''
3) Pass the cleaned_name into OneMap's search API to extract the onemap_address (and onemap_lat and onemap_lon)
'''

markdown_text_page_2_section_1_4 = '''
3) Extract the postal codes from onemap_address and offer_location
'''

markdown_text_page_2_section_1_5 = '''
4) Compare the onemap_postal and offer_postal to ascertain the match
'''

markdown_text_page_2_section_2_1 = '''
Download the files used for analysis here. 
Bookings CSV contains data of all bookings made from 1 May to 19 July.
Addresses CSV contains data of all user's saved addresses from 1 May to 19 July
'''
