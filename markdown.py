# Markdown Text #

markdown_text_page_1_section_1 = '''
There was an anomalous increase in booking mismatches between 17 May to 31 May. 
This was due to backend issues leading to the loss of precision in stored address coordinates. 
This issue has been resolved. Since 31 May, the daily mismatch rate has been reduced to 
an average of approximately 10% a day (which is close to the approximately 9.07% daily mismatch rate 
before the backend issues occured).'''

markdown_text_page_1_section_2_1 = '''
Most of the mismatches that occured after 31 May are due to the feature of our app, instead of a bug. 
As seen from the map visualization, our app is programmed to offer passengers a waypoint (from our database) 
that is located closest to their requested waypoint. 
Thus, for instance, a passenger may request to be booked from Blk 408. However, their requested coordinate may be closer 
to the waypoint for Blk 409. In this case, our app will allocate the passenger Blk 409 instead of Blk 408.'''

markdown_text_page_1_section_2_2 = '''
Additionally, as seen from the histogram, the plot for requested-offered is more 
right skewed than the plot for requested-onemap. Most of the offered location are within 10m of the 
requested location. In contrast, there is a wider spread of distance deviation (beyond 10m) between the 
requested location and the onemap returned location (proxy for user's actual intended location). Evident from the map 
visualization and the histogram plot, the prevailing mismatches are due to features on our app created to 
provide users with a closer location to their requested waypoint.'''

markdown_text_page_1_section_2_3 = '''
Since the prevailing mismatches are due to a feature and not a bug, a complete elimination of all mismatches will
require changes to our app's feature(s) as well as our booking flow.'''

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

markdown_text_page_2_section_2 = '''
Download the files used for analysis here. 
Bookings CSV contains data of all bookings made from 1 May to 19 July.
Addresses CSV contains data of all user's saved addresses from 1 May to 19 July
'''