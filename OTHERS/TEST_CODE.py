```python
import requests
# Replace with your HubSpot private app API key
HUBSPOT_API_KEY = "YOUR_HUBSPOT_API_KEY"
# Replace with the contact ID and association details
CONTACT_ID = "CONTACT_ID" #VID
ASSOCIATION_TYPE = "company"  # Replace with "deal", "ticket", or "engagement" as needed
ASSOCIATED_OBJECT_ID = "ASSOCIATED_OBJECT_ID"  # Replace with the ID of the associated object
# HubSpot API endpoint to create contact associations
endpoint = f"https://api.hubapi.com/crm/v3/objects/contacts/{CONTACT_ID}/associations/{ASSOCIATION_TYPE}/{ASSOCIATED_OBJECT_ID}"
# Request headers including the API key
headers = {
    "Authorization": f"Bearer {HUBSPOT_API_KEY}"
}
# Make the API call to create the contact association
response = requests.put(endpoint, headers=headers)
# Check the response status
if response.status_code == 200:
    print("Contact association created successfully.")
else:
    print("Failed to create contact association. Status code:", response.status_code)
```
