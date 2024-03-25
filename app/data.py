# data.py
import gspread_dataframe as gd
import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def process_data(pedidos_df):
        # Reemplazar '#N/A' por NaN
        pedidos_df.replace('#N/A', np.nan, inplace=True)
        # Eliminar filas con valores NaN
        pedidos_df.dropna(inplace=True)
        # Conversión de tipos de datos
        pedidos_df = pedidos_df.dropna().astype({'codigo_cliente': int, 'codigo_producto': int, 'cantidad': int, 'precio_unitario': int})
        return pedidos_df