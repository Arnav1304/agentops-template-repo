import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_google_sheets():
    # Define the scope
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # Add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('credential.json', scope)

    # Authorize the clientsheet
    client = gspread.authorize(creds)

    try:
        # Try to open a test spreadsheet (you'll need to create this)
        sheet = client.open('BBQ Nation Chatbot Logs').sheet1
        print("Successfully connected to Google Sheets!")
        return True
    except Exception as e:
        print(f"Error connecting to Google Sheets: {str(e)}")
        return False

if __name__ == "__main__":
    test_google_sheets() 