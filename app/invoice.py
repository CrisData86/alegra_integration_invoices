# invoice.py
import requests

class InvoiceProcessor:
    @staticmethod
    def process_invoices(pedidos_df):
        invoice_data_void = []
        for codigo_cliente in pedidos_df['codigo_cliente'].unique():
            # Lógica de procesamiento de facturas aquí
            # ...
            
            df = pedidos_df[pedidos_df['codigo_cliente'] == codigo_cliente]
            items = []
            for _, row in df.iterrows():
                id_item = str(row['codigo_producto'])
                quantity = row['cantidad']
                url = f"https://api.alegra.com/api/v1/items/{id_item}"
                headers = {
                    "accept": "application/json",
                    "authorization": "Basic bWVyY2Fkb2Fncmljb2xhZGVsYXNpZXJyYTNAZ21haWwuY29tOjI0MTFmYTQ3NzUyMjRjYTkyNWNk"
                }
                response_item = requests.get(url, headers=headers).json()
                item = {
                    "id": int(response_item['id']),
                    "quantity": int(row['cantidad']),
                    "price": int(response_item['price'][0]['price'])
                }
                items.append(item)

            payload = {
                "status": "open",
                "paymentForm": "CASH",
                "paymentMethod": "CASH",
                "client": {"id": int(df['codigo_cliente'].iloc[0])},
                "date": df['fecha_creacion'].iloc[0],
                "dueDate": df['fecha_creacion'].iloc[0],
                "items": items
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": "Basic bWVyY2Fkb2Fncmljb2xhZGVsYXNpZXJyYTNAZ21haWwuY29tOjI0MTFmYTQ3NzUyMjRjYTkyNWNk"
            }
            response = requests.post("https://api.alegra.com/api/v1/invoices", json=payload, headers=headers)
            response_json = response.json()
            
            invoice_data_to_add = [
                response_json['numberTemplate']['prefix'] + response_json['numberTemplate']['number'],
                response_json['id'],
                response_json['date'],
                response_json['client']['name'],
                response_json['client']['identification'],
                response_json['total']
            ]
            invoice_data_void.append(invoice_data_to_add)
           

        return invoice_data_void