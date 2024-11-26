import pandas as pd
import os
from datetime import datetime
from tkinter import Tk, Label, Button, Entry, Toplevel, messagebox, StringVar, Listbox, END, OptionMenu, Canvas, PhotoImage

# Path ke file Excel
file_path = 'd:\projecta\Data_Barang.xlsx'
riwayat_file_path = 'd:\projecta\Riwayat_Transaksi.xlsx'
admin_file_path = 'd:\projecta\Data_Admin.xlsx'

# Membaca data admin dari file Excel
if os.path.exists(admin_file_path):
    admin_data = pd.read_excel(admin_file_path)
    admin_credentials = {str(k).strip(): str(v).strip() for k, v in zip(admin_data['Username'].astype(str), admin_data['Password'].astype(str))}
else:
    admin_data = pd.DataFrame(columns=['Username', 'Password'])
    admin_data.to_excel(admin_file_path, index=False)
    admin_credentials = {}

# Membuat file barang dan riwayat 
if not os.path.exists(file_path):
    pd.DataFrame(columns=['Nama Barang', 'Harga', 'Stok']).to_excel(file_path, index=False)
if not os.path.exists(riwayat_file_path):
    pd.DataFrame(columns=['Nama Barang', 'Jumlah', 'Total', 'Tanggal']).to_excel(riwayat_file_path, index=False)

# Membaca data barang dan riwayat
data = pd.read_excel(file_path)
riwayat_data = pd.read_excel(riwayat_file_path)

# Fungsi untuk menyimpan data barang ke file Excel
def update_excel():
    data.to_excel(file_path, index=False)

# Fungsi untuk menyimpan riwayat transaksi ke file Excel
def simpan_riwayat():
    riwayat_data.to_excel(riwayat_file_path, index=False)

# Fungsi untuk menampilkan riwayat transaksi
def tampilkan_riwayat():
    window = Toplevel()
    window.title("Riwayat Transaksi")

    Label(window, text="Riwayat Transaksi", font=("Arial", 16, "bold")).pack(pady=10)

    listbox = Listbox(window, font=("Arial", 12), width=80, height=20)
    listbox.pack(pady=10)

    for i, row in riwayat_data.iterrows():
        # Menampilkan hanya Nama Barang, Jumlah, dan Total
        listbox.insert(END, f"{row['Nama Barang']} - Jumlah: {row['Jumlah']} - Total: {row['Total']}")

    Button(window, text="Tutup", command=window.destroy, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=10)

# Fungsi untuk keluar dari aplikasi
def keluar(window, even=None):
    confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
    if confirm:
        window.quit()

# Fungsi untuk menampilkan daftar barang
def tampilkan_barang():
    def load_barang():
        listbox.delete(0, END)
        for i, row in data.iterrows():
            listbox.insert(END, f"{row['Nama Barang']} - Harga: {row['Harga']} - Stok: {row['Stok']}")

    window = Toplevel()
    window.title("Daftar Barang")
    Label(window, text="Daftar Barang", font=("Arial", 16, "bold")).pack(pady=10)

    listbox = Listbox(window, font=("Arial", 12), width=50)
    listbox.pack(pady=10)
    load_barang()

    Button(window, text="Tutup", command=window.destroy, bg="#f44336", fg="white", font=("Arial", 12)).pack(pady=10)

# Fungsi untuk menambah barang baru
def tambah_barang():
    def simpan_barang():
        nama = nama_var.get()
        harga = harga_var.get()
        stok = stok_var.get()
        if nama in data['Nama Barang'].values:
            messagebox.showerror("Error", "Barang sudah ada!")
            return
        if not nama or not harga or not stok:
            messagebox.showerror("Error", "Semua kolom harus diisi!")
            return
        data.loc[len(data)] = [nama, int(harga), int(stok)]
        update_excel()
        messagebox.showinfo("Sukses", f"Barang '{nama}' berhasil ditambahkan!")
        tambah_window.destroy()

    tambah_window = Toplevel()
    tambah_window.title("Tambah Barang Baru")

    Label(tambah_window, text="Nama Barang:", font=("Arial", 12)).pack(pady=5)
    nama_var = StringVar()
    Entry(tambah_window, textvariable=nama_var, font=("Arial", 12)).pack(pady=5)

    Label(tambah_window, text="Harga:", font=("Arial", 12)).pack(pady=5)
    harga_var = StringVar()
    Entry(tambah_window, textvariable=harga_var, font=("Arial", 12)).pack(pady=5)

    Label(tambah_window, text="Stok:", font=("Arial", 12)).pack(pady=5)
    stok_var = StringVar()
    Entry(tambah_window, textvariable=stok_var, font=("Arial", 12)).pack(pady=5)

    Button(tambah_window, text="Simpan", command=simpan_barang, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# Fungsi untuk transaksi penjualan
def transaksi_penjualan():
    def simpan_transaksi():
        total_all = 0
        for item in transaksi:
            nama = item['Nama Barang']
            jumlah = item['Jumlah']
            harga = item['Harga']
            total = harga * jumlah
            total_all += total
            data.loc[data['Nama Barang'] == nama, 'Stok'] -= jumlah
            riwayat_data.loc[len(riwayat_data)] = [nama, jumlah, total, datetime.now()]
        simpan_riwayat()
        update_excel()
        messagebox.showinfo("Sukses", f"Transaksi berhasil dilakukan! Total: {total_all}")
        transaksi_window.destroy()

    def add_item_to_transaction():
        selected_item = selected_item_var.get()
        jumlah = jumlah_var.get()
        if not jumlah or selected_item == "Pilih Barang":
            messagebox.showerror("Error", "Pilih barang dan jumlah!")
            return
        if selected_item not in data['Nama Barang'].values:
            messagebox.showerror("Error", "Barang tidak ditemukan!")
            return
        harga = data.loc[data['Nama Barang'] == selected_item, 'Harga'].values[0]
        stok = data.loc[data['Nama Barang'] == selected_item, 'Stok'].values[0]
        if int(jumlah) > stok:
            messagebox.showerror("Error", "Jumlah melebihi stok tersedia!")
            return
        transaksi.append({"Nama Barang": selected_item, "Jumlah": int(jumlah), "Harga": harga})
        update_transaction_display()
        jumlah_var.set("")  # Clear jumlah input

    def update_transaction_display():
        listbox.delete(0, END)
        total_all = 0
        for item in transaksi:
            listbox.insert(END, f"{item['Nama Barang']} - Jumlah: {item['Jumlah']} - Harga: {item['Harga']} - Total: {item['Jumlah'] * item['Harga']}")
            total_all += item['Jumlah'] * item['Harga']
        total_label.config(text=f"Total: {total_all}")

    transaksi = []

    transaksi_window = Toplevel()
    transaksi_window.title("Transaksi Penjualan")

    Label(transaksi_window, text="Pilih Barang:", font=("Arial", 12)).pack(pady=5)
    selected_item_var = StringVar()
    selected_item_var.set("Pilih Barang")
    item_choices = list(data['Nama Barang'])
    item_dropdown = OptionMenu(transaksi_window, selected_item_var, *item_choices)
    item_dropdown.pack(pady=5)

    Label(transaksi_window, text="Jumlah:", font=("Arial", 12)).pack(pady=5)
    jumlah_var = StringVar()
    Entry(transaksi_window, textvariable=jumlah_var, font=("Arial", 12)).pack(pady=5)

    Button(transaksi_window, text="Tambah ke Transaksi", command=add_item_to_transaction, font=("Arial", 12)).pack(pady=10)

    listbox = Listbox(transaksi_window, font=("Arial", 12), width=50)
    listbox.pack(pady=10)

    total_label = Label(transaksi_window, text="Total: 0", font=("Arial", 12, "bold"))
    total_label.pack(pady=10)

    Button(transaksi_window, text="Proses Transaksi", command=simpan_transaksi, font=("Arial", 12)).pack(pady=10)

# Fungsi untuk menambah stok barang
def tambah_stok():
    def simpan_stok():
        nama = nama_var.get()
        stok = stok_var.get()
        if nama not in data['Nama Barang'].values:
            messagebox.showerror("Error", "Barang tidak ditemukan!")
            return
        if not stok.isdigit() or int(stok) <= 0:
            messagebox.showerror("Error", "Stok harus berupa angka positif!")
            return
        data.loc[data['Nama Barang'] == nama, 'Stok'] += int(stok)
        update_excel()
        messagebox.showinfo("Sukses", f"Stok untuk '{nama}' berhasil ditambahkan!")
        tambah_stok_window.destroy()

    tambah_stok_window = Toplevel()
    tambah_stok_window.title("Tambah Stok Barang")

    Label(tambah_stok_window, text="Nama Barang:", font=("Arial", 12)).pack(pady=5)
    nama_var = StringVar()
    Entry(tambah_stok_window, textvariable=nama_var, font=("Arial", 12)).pack(pady=5)

    Label(tambah_stok_window, text="Jumlah Stok:", font=("Arial", 12)).pack(pady=5)
    stok_var = StringVar()
    Entry(tambah_stok_window, textvariable=stok_var, font=("Arial", 12)).pack(pady=5)

    Button(tambah_stok_window, text="Simpan", command=simpan_stok, bg="#4CAF50", fg="white", font=("Arial", 12)).pack(pady=10)

# Fungsi utama menu setelah login

def menu_utama():
    window = Tk()
    window.title("Menu Utama")
    window.geometry("600x400")

    # Memuat background
    try:
        bg_image = PhotoImage(file="d:\\projecta\\background 2.png")
        canvas = Canvas(window, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return

    # Elemen di atas Canvas
    canvas.create_text(300, 50, text="Sistem Penjualan Barang", font=("Comic Sans MS", 18, "bold"), fill="white")

    tambah_barang_button = Button(window, text="Tambah Barang", command=tambah_barang, font=("Arial", 10))
    canvas.create_window(300, 120, window=tambah_barang_button, width=150)

    tambah_stok_button = Button(window, text="Tambah Stok", command=tambah_stok, font=("Arial", 10))
    canvas.create_window(300, 170, window=tambah_stok_button, width=150)

    transaksi_button = Button(window, text="Transaksi Penjualan", command=transaksi_penjualan, font=("Arial", 10))
    canvas.create_window(300, 220, window=transaksi_button, width=150)

    daftar_barang_button = Button(window, text="Daftar Barang", command=tampilkan_barang, font=("Arial", 10))
    canvas.create_window(300, 270, window=daftar_barang_button, width=150)

    riwayat_button = Button(window, text="Riwayat Transaksi", command=tampilkan_riwayat, font=("Arial", 10))
    canvas.create_window(300, 320, window=riwayat_button, width=150)

    keluar_button = Button(window, text="Keluar", command=lambda: keluar(window), bg="#CC0000", fg="white", font=("Arial", 10))
    canvas.create_window(300, 370, window=keluar_button, width=150)

    window.mainloop()


# Fungsi login
def login():
    def check_login():
        username = username_var.get()
        password = password_var.get()
        if username in admin_credentials and admin_credentials[username] == password:
            messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
            main_window.destroy()
            menu_utama()  # Setelah login berhasil, buka menu utama
        else:
            messagebox.showerror("Error", "Username atau password salah!")

    main_window = Tk()
    main_window.title("Login Admin")
    main_window.geometry("600x400")  # Ukuran window login

    # Memuat background
    try:
        bg_image = PhotoImage(file="d:\\projecta\\background 1.png")  
        canvas = Canvas(main_window, width=600, height=400)
        canvas.pack(fill="both", expand=True)
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return

    # Form login
    canvas.create_text(300, 80, text="Login Admin", font=("Arial", 24, "bold"), fill="black")
    canvas.create_text(180, 150, text="Username:", font=("Arial", 14), fill="Black")
    username_var = StringVar()
    username_entry = Entry(main_window, textvariable=username_var, font=("brial", 14))
    canvas.create_window(400, 150, window=username_entry, width=200)

    canvas.create_text(180, 200, text="Password:", font=("Arial", 14), fill="black")
    password_var = StringVar()
    password_entry = Entry(main_window, textvariable=password_var, font=("Arial", 14), show="*")
    canvas.create_window(400, 200, window=password_entry, width=200)

    login_button = Button(main_window, text="Login", command=check_login, bg="#00CC00", fg="white", font=("Arial", 14))
    canvas.create_window(300, 300, window=login_button, width=100)

    main_window.mainloop()

# Panggil fungsi login saat program dimulai
login()

# Fungsi untuk keluar dari aplikasi
def keluar(event=None):
    confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
    if confirm:
        event.widget.quit()
