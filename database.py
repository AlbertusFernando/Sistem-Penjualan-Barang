import os
import pandas as pd

# Path file
file_path = 'Data_Barang.xlsx'
riwayat_file_path = 'Riwayat_Transaksi.xlsx'
admin_file_path = 'Data_Admin.xlsx'

# Inisialisasi data 
if not os.path.exists(admin_file_path):
    pd.DataFrame(columns=['Username', 'Password']).to_excel(admin_file_path, index=False)
if not os.path.exists(file_path):
    pd.DataFrame(columns=['Nama Barang', 'Harga', 'Stok']).to_excel(file_path, index=False)
if not os.path.exists(riwayat_file_path):
    pd.DataFrame(columns=['Nama Barang', 'Jumlah', 'Total', 'Tanggal']).to_excel(riwayat_file_path, index=False)


# Membaca data 
admin_data = pd.read_excel(admin_file_path)
data = pd.read_excel(file_path)
riwayat_data = pd.read_excel(riwayat_file_path)

# Fungsi untuk menyimpan perubahan data
def update_admin_data():
    admin_data.to_excel(admin_file_path, index=False)
def update_excel():
    data.to_excel(file_path, index=False)
def simpan_riwayat():
    riwayat_data.to_excel(riwayat_file_path, index=False)
    


