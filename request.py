import requests
import json
import csv
from datetime import datetime

def get_ticketmaster_events():
    # API endpoint and parameters
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    api_key = "o54GFCryCbhRkAlv0vc6qEFcK7HEDTCJ"
    
    # Query parameters
    params = {
        'size': 200,  # Increased to 300 events
        'apikey': api_key,
        'startDateTime': '2025-01-07T03:00:00Z',
        'sort': 'date,asc',
        'keyword': 'Toronto Maple Leafs'
    }
    
    try:
        # Make the GET request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        # Parse the JSON response
        data = response.json()
        
        # Store the response in a file for later use
        with open('ticketmaster_response_maple.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        # Print total events found
        if '_embedded' in data and 'events' in data['_embedded']:
            print(f"Total events found: {len(data['_embedded']['events'])}")
            
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

def process_events_to_csv():
    # Read the stored JSON file
    with open('ticketmaster_response_maple.json', 'r') as f:
        data = json.load(f)
    
    # Create a list to store event information
    event_info = []
    skipped_events = []
    
    # Extract events from the response
    if '_embedded' in data and 'events' in data['_embedded']:
        events = data['_embedded']['events']
        for event in events:
            try:
                event_id = event['id']
                
                # Verify this is a Toronto Raptors event
                if 'name' in event and 'Toronto Maple Leafs' in event['name']:
                    # Parse the datetime and create decoded ID
                    date_time = datetime.strptime(event['dates']['start']['dateTime'], '%Y-%m-%dT%H:%M:%SZ')
                    decoded_id = f"L{date_time.strftime('%y%m%d')}"
                    event_info.append([event_id, decoded_id, event['name'], event['dates']['start']['dateTime']])
                else:
                    skipped_events.append(event['name'])
            except KeyError as e:
                print(f"Error processing event: Missing key {e}")
                continue
            except Exception as e:
                print(f"Unexpected error processing event: {e}")
                continue
    
    # Write to CSV file with more information for verification
    with open('event_ids_maple.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['EventID', 'DecodedID', 'EventName', 'DateTime'])  # Extended header
        writer.writerows(event_info)
    
    # Print summary
    print(f"Processed {len(event_info)} events successfully")
    if skipped_events:
        print(f"Skipped {len(skipped_events)} non-Toronto Maple Leafs events")
    
    return event_info

if __name__ == "__main__":
    events_data = get_ticketmaster_events()
    if events_data:
        print("Data successfully retrieved and stored in ticketmaster_response_maple.json")
        event_info = process_events_to_csv()
        print("Event IDs have been processed and saved to event_ids_maple.csv")