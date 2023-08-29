from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API setup
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('google_sheets_credentials.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Your Spreadsheet Name')
worksheet = spreadsheet.get_worksheet(0)  # Assuming the data is in the first worksheet

# ... Other Flask app setup ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_book = request.form['selected-book']
        address = request.form['address']
        
        # Update Google Sheets (Assuming your spreadsheet has columns "Title" and "Quantity")
        book_info = worksheet.find(selected_book)
        row = book_info.row
        column = worksheet.find('Quantity').col
        quantity = int(worksheet.cell(row, column).value)
        
        if quantity > 0:
            worksheet.update_cell(row, column, quantity - 1)
            # Send email notifications (You need to implement this)
            
            return render_template('thank_you.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
