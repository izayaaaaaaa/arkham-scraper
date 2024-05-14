import json
import csv

# Path to the JSON file
json_file_path = 'C:\\Users\\franc\\Repositories\\arkham-scraper\\demo.json'
# Path to the output CSV file
csv_file_path = 'C:\\Users\\franc\\Repositories\\arkham-scraper\\output_clean.csv'

def write_transfers_to_csv(json_file_path, csv_file_path):
    # Open the JSON file and load the data
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        
        # Navigate to the nested 'transfers' data
        entries = data['log']['entries']
        transfers_data = []
        for entry in entries:
            # Check if the response content type is JSON
            if ('response' in entry and 
                'content' in entry['response'] and 
                'mimeType' in entry['response']['content'] and 
                entry['response']['content']['mimeType'] == "application/json; charset=UTF-8" and
                'text' in entry['response']['content']):
                
                content_text = entry['response']['content']['text']
                try:
                    # Parse the JSON data from the text
                    content_data = json.loads(content_text)
                    # Ensure content_data is a dictionary and 'transfers' is a key in it
                    if isinstance(content_data, dict) and 'transfers' in content_data:
                        for transfer in content_data['transfers']:
                            to_address = transfer['toAddress']['address']
                            chain = transfer['chain']
                            entity = transfer['fromAddress']['arkhamEntity']['name']
                            transfers_data.append({
                                'address': to_address,
                                'chain': chain,
                                'entity': entity,
                                'category': 'exchange'
                            })
                except json.JSONDecodeError:
                    continue
    
    # Open the CSV file for writing
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # Create a CSV writer object
        csv_writer = csv.writer(file)
        
        # Check if there are transfers in the data
        if transfers_data:
            # Write the header row
            headers = ['address', 'chain', 'entity', 'category']
            csv_writer.writerow(headers)
            
            # Write data rows
            for transfer in transfers_data:
                csv_writer.writerow([transfer['address'], transfer['chain'], transfer['entity'], transfer['category']])

write_transfers_to_csv(json_file_path, csv_file_path)