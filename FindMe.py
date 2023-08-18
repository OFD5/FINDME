import requests
from bs4 import BeautifulSoup
import os

# Banner
banner = """
  _____ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ ______ 
 |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|
 |  \/  (_)       (_)                  |  __ \               | |                    | | |         | |             
 | \  / |_ ___ ___ _ _ __   __ _ ______| |__) |__  ___  _ __ | | ___ ______ ___ ___ | | | ___  ___| |_ ___  _ __  
 | |\/| | / __/ __| | '_ \ / _` |______|  ___/ _ \/ _ \| '_ \| |/ _ \______/ __/ _ \| | |/ _ \/ __| __/ _ \| '__| 
 | |  | | \__ \__ \ | | | | (_| |      | |  |  __/ (_) | |_) | |  __/     | (_| (_) | | |  __/ (__| || (_) | |    
 |_|  |_|_|___/___/_|_| |_|\__, |      |_|   \___|\___/| .__/|_|\___|      \___\___/|_|_|\___|\___|\__\___/|_|    
                            __/ |                      | |                                                        
  ______ ______ ______ ____|___/____ ______ ______ ____|_|______ ______ ______ ______ ______ ______ ______ ______ 
 |______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|______|
                                                                                                                                                                                                                                 
"""

# Signature
signature = "\nCreated by OFD5, This tool is provided for enhancement of OSINT to find missing people online on the SAPS Website.\n"

def scrape_and_save(user_id):
    url = base_url + str(user_id)
    response = requests.get(url)
    
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        extracted_info = {}
        
        try:
            name = soup.find('h2', align='center').get_text(strip=True)
            extracted_info['Name'] = name
            rows = soup.find_all('tr', class_='active')
            for row in rows:
                cells = row.find_all('td')
                label = cells[0].get_text(strip=True).replace(":", "")
                value = cells[1].get_text(strip=True)
                extracted_info[label] = value
        except Exception as e:
            print(f"Error extracting info for User ID {user_id}: {e}")
            return
        
        # Skip creating HTML file if there's no name or missing information
        if not name or all(value == '' for value in extracted_info.values()):
            print(f"Skipping User ID {user_id} due to missing information.")
            return
        
        # Extract image URLs with absolute paths
        image_urls = []
        for img_tag in soup.find_all('img', src=lambda src: src and 'thumbnail.php?id=' in src):
            img_url = img_tag['src']
            full_img_url = f"https://www.saps.gov.za/crimestop/missing/{img_url}"
            image_urls.append(full_img_url)
        
        # Create an HTML file
        html_filename = f"user_data/user_{user_id}.html"
        
        with open(html_filename, "w") as html_file:
            html_file.write("<html><head><style>")
            html_file.write("body { font-family: Arial, sans-serif; background-color: #f0f0f0; color: #333; }")
            html_file.write("h1 { color: #333; }")
            html_file.write("table { border-collapse: collapse; width: 80%; margin: 20px auto; background-color: #fff; }")
            html_file.write("td { border: 1px solid #ddd; padding: 8px; }")
            html_file.write("img { max-width: 100%; }")
            html_file.write("</style></head><body>")
            
            # Insert banner
            html_file.write("<pre>")
            html_file.write(banner)
            html_file.write("</pre>")
            
            html_file.write(f"<h1>User ID: {user_id}</h1>")
            
            # Generate the HTML table
            html_file.write("<table>")
            for label, value in extracted_info.items():
                html_file.write(f"<tr><td><strong>{label}</strong></td><td>{value}</td></tr>")
            
            # Add image URLs to the table
            for img_url in image_urls:
                html_file.write(f"<tr><td><strong>Image</strong></td><td><img src='{img_url}' alt='User Image'></td></tr>")
            
            html_file.write("</table>")
            
            # Insert signature with color
            html_file.write("<p style='color: blue;'>")
            html_file.write(signature)
            html_file.write("</p>")
            
            html_file.write("</body></html>")
        
        print(f"User ID: {user_id} - HTML file saved as: {html_filename}")
        print("-" * 40)
    else:
        print(f"Failed to retrieve data for User ID: {user_id}")

base_url = "https://www.saps.gov.za/crimestop/missing/detail.php?bid="

# Create a directory to save files
if not os.path.exists("user_data"):
    os.makedirs("user_data")

while True:
    print("1. Scrape user by ID")
    print("2. Scrape all users")
    print("3. Quit")
    choice = input("Enter your choice: ")
    
    if choice == '1':
        user_id = input("Enter User ID: ")
        try:
            user_id = int(user_id)
            scrape_and_save(user_id)
        except ValueError:
            print("Invalid User ID. Please enter a valid integer.")
    elif choice == '2':
        permission = input("Do you want to scrape information for all users? (yes/no): ").lower()
        if permission == 'yes':
            start_id = int(input("Enter the starting User ID: "))
            end_id = int(input("Enter the ending User ID: "))
            
            # Initialize a list to store user data
            all_users_data = []
            
            # Loop through the range of User IDs
            for user_id in range(start_id, end_id + 1):
                 scrape_and_save(user_id)
