# routes.py

from flask import render_template, jsonify, Blueprint
from app.auth import GoogleSheetAuth
from app.data import DataProcessor
from app.invoice import InvoiceProcessor

app_bp = Blueprint('app', __name__)

@app_bp.route('/')
def index():
    return render_template('index.html')

@app_bp.route('/process_invoice', methods=['GET'])
def process_invoice():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    json_parameters = {...}  # tus credenciales aquí

    auth = GoogleSheetAuth(json_parameters, scope)
    myclient = auth.authenticate()

    sh1 = myclient.open_by_url('https://docs.google.com/spreadsheets/d/1aEwSfTggDd_k6C2pKUspOqzGlfnteR1WoqRusfU/edit#gid=0')
    pedidos = sh1.worksheet('pedidos')
    pedidos_df = pd.DataFrame(pedidos.get_all_records())

    pedidos_df = DataProcessor.process_data(pedidos_df)
    invoice_data_void = InvoiceProcessor.process_invoices(pedidos_df)

    view_2 = sh1.worksheet('facturas')

    existing_data = view_2.get_all_values()

    if existing_data:
        existing_data_df = pd.DataFrame(existing_data[1:], columns=existing_data[0])
        combined_data_df = pd.concat([existing_data_df, invoice_data_df])
    else:
        combined_data_df = invoice_data_df

    gd.set_with_dataframe(view_2, combined_data_df.astype(str), resize=True)

    return jsonify({'message': 'Invoices processed successfully.'})
