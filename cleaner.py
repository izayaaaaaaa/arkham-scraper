import json
import csv

# Path to the JSON file
file_path = 'c:\\Users\\franc\\Repositories\\arkham-scraper\\network_traffic1.json'
# Path to the output CSV file
csv_file_path = 'c:\\Users\\franc\\Repositories\\arkham-scraper\\output.csv'

# List to hold the filtered data
filtered_data = []

# Open and read the JSON file with UTF-8 encoding
with open(file_path, 'r', encoding='utf-8') as file:
    # Read the file line by line
    for line in file:
        # Check if the line contains the specified text
        if '"text": "{\\"transfers\\"' in line:
            print("Found line with keyword: ", line)
            # Try to find the JSON object starting from the expected position
            try:
                # Extract the JSON substring starting from the first occurrence of '{"transfers"'
                json_start_pos = line.find('{\\"transfers\\')
                if json_start_pos != -1:
                    # Extract the JSON string
                    json_str = line[json_start_pos:-2]  # Adjusted to remove the trailing newline and any other characters after the JSON object
                    print("Extracted JSON string: ", json_str)
                    # Correctly parse the JSON data
                    data = json.loads(json_str)
                    filtered_data.extend(data['transfers'])  # Assuming 'transfers' is the key containing the list of transactions
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

# Write data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=[
        'id', 'transactionHash', 'fromAddress', 'toAddress', 'tokenAddress', 'type', 
        'blockTimestamp', 'blockNumber', 'blockHash', 'tokenName', 'tokenSymbol', 
        'tokenDecimals', 'unitValue', 'tokenId', 'historicalUSD', 'chain'
    ])
    writer.writeheader()
    for item in filtered_data:
        writer.writerow({
            'id': item.get('id', ''),
            'transactionHash': item.get('transactionHash', ''),
            'fromAddress': item.get('fromAddress', {}).get('address', ''),
            'toAddress': item.get('toAddress', {}).get('address', ''),
            'tokenAddress': item.get('tokenAddress', ''),
            'type': item.get('type', ''),
            'blockTimestamp': item.get('blockTimestamp', ''),
            'blockNumber': item.get('blockNumber', ''),
            'blockHash': item.get('blockHash', ''),
            'tokenName': item.get('tokenName', ''),
            'tokenSymbol': item.get('tokenSymbol', ''),
            'tokenDecimals': item.get('tokenDecimals', ''),
            'unitValue': item.get('unitValue', ''),
            'tokenId': item.get('tokenId', ''),
            'historicalUSD': item.get('historicalUSD', ''),
            'chain': item.get('chain', '')
        })

print("Data has been written to CSV.")