import os
import pandas as pd
from tkinter import *
from tkinter import messagebox, Canvas
from datetime import datetime
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from database import *

# Fungsi validasi login
def validate_login():
    username = username_var.get().strip()  # Menghilangkan spasi yang tidak terlihat
    password = password_var.get().strip()  # Menghilangkan spasi yang tidak terlihat

    if username in admin_data['Username'].values:
        # Mengkonversi password yang diambil menjadi string
        stored_password = str(admin_data.loc[admin_data['Username'] == username, 'Password'].values[0]).strip()
        if password == stored_password:
            messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
            setup_main_menu()  # Menyiapkan menu utama
            show_frame(main_menu)  # Menampilkan menu utama setelah login berhasil
        else:
            messagebox.showerror("Login Gagal", "Password salah!")
    else:
        messagebox.showerror("Login Gagal", "Username tidak ditemukan!")

# Fungsi untuk menampilkan login frame
def show_login():
    show_frame(login_frame)  # Menampilkan frame login
    for widget in login_frame.winfo_children():
        widget.destroy()  # Menghapus widget yang sudah ada

# Frame Sign Up
def show_sign_up():
    def register_admin():
        username = username_var.get()
        password = password_var.get()
        if username in admin_data['Username'].values:
            messagebox.showerror("Sign Up Gagal", "Username sudah terdaftar!")
            return
        admin_data.loc[len(admin_data)] = [username, password]
        update_admin_data()
        messagebox.showinfo("Sign Up Berhasil", "Akun admin berhasil dibuat!")
        show_frame(login_frame)

    show_frame(sign_up_frame)
    for widget in sign_up_frame.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk background
    canvas = Canvas(sign_up_frame, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("window.png")
        image = image.resize((1600, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(image)  # Ganti path dengan lokasi file gambar Anda
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return

    # Menambahkan elemen UI di atas Canvas
    Sign_Up_text = canvas.create_text(770, 180, text="Sign Up Admin", font=("Bubble Bobble", 50, "bold"), fill="black")
    username_label = canvas.create_text(770, 280, text="Username:", font=("Arial", 14), fill="black")
    password_label = canvas.create_text(770, 370, text="Password:", font=("Arial", 14), fill="black")
    Entry(sign_up_frame, textvariable=username_var, font=("Arial", 14)).place(relx=0.5, rely=0.40, anchor="center")
    Entry(sign_up_frame, textvariable=password_var,font=("Arial", 14), show="*").place(relx=0.5, rely=0.51, anchor="center")
    Button(sign_up_frame, text="Register", command=register_admin, bg="#4CAF50", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.58, anchor="center")
    Button(sign_up_frame, text="Kembali", command=lambda: show_frame(login_frame), bg="#f44336", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.64, anchor="center")

# Fungsi tambah barang
def tambah_barang():
    def simpan_barang():
        
        nama, harga, stok = nama_var.get(), harga_var.get(), stok_var.get()
        if not nama or not harga.isdigit() or not stok.isdigit():
            messagebox.showerror("Error", "Input tidak valid!")
            return
        if nama in data['Nama Barang'].values:
            messagebox.showerror("Error", "Barang sudah ada!")
            return
        data.loc[len(data)] = [nama, int(harga), int(stok)]
        update_excel()
        messagebox.showinfo("Sukses", f"Barang '{nama}' berhasil ditambahkan!")
        nama_var.set("")
        harga_var.set("")
        stok_var.set("")

    show_frame(barang_menu)
    for widget in barang_menu.winfo_children():
        widget.destroy()
        
    # Membuat Canvas untuk background
    canvas = Canvas(barang_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("fitur.jpg")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return

    tambah_barang_text = canvas.create_text(770, 180, text="Tambah Barang", font=("Bubble Bobble", 50, "bold"), fill="black")
    nama_var, harga_var, stok_var = StringVar(), StringVar(), StringVar()

    nama_barang_label = canvas.create_text(770, 260, text="Nama Barang:", font=("Arial", 14), fill="black")
    Entry(barang_menu, textvariable=nama_var, font=("Arial", 14)).place(relx=0.5, rely=0.37, anchor="center")
    harga_label = canvas.create_text(770, 332, text="Harga:", font=("Arial", 14), fill="black")
    Entry(barang_menu, textvariable=harga_var, font=("Arial", 14)).place(relx=0.5, rely=0.46, anchor="center")
    stok_label = canvas.create_text(770, 405, text="Stok:", font=("Arial", 14), fill="black")
    Entry(barang_menu, textvariable=stok_var, font=("Arial", 14)).place(relx=0.5, rely=0.545, anchor="center")
    Button(barang_menu, text="Simpan", command=simpan_barang, bg="#4CAF50", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.6, anchor="center")
    Button(barang_menu, text="Kembali", command=lambda: show_frame(main_menu), font=("Arial", 11), bg="#CC0000", fg="white").place(relx=0.5, rely=0.65, anchor="center")

# Fungsi daftar barang
def daftar_barang():
    show_frame(daftar_menu)
    for widget in daftar_menu.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk background
    canvas = Canvas(daftar_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("fitur.jpg")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return
    
    # Judul
    tambah_barang_text = canvas.create_text(770, 120, text="Daftar Barang", font=("Bubble Bobble", 50, "bold"), fill="black")

    # Treeview untuk tabel
    columns = ("Nama Barang", "Harga", "Stok")
    tree = ttk.Treeview(daftar_menu, columns=columns, show="headings", height=20)
    tree.place(relx=0.5, rely=0.5, anchor="center")

    # Menambahkan heading untuk setiap kolom
    tree.heading("Nama Barang", text="Nama Barang")
    tree.heading("Harga", text="Harga")
    tree.heading("Stok", text="Stok")

    # Menentukan lebar kolom
    tree.column("Nama Barang", width=200, anchor="w")
    tree.column("Harga", width=100, anchor="center")
    tree.column("Stok", width=100, anchor="center")

    # Menambahkan data ke tabel
    for _, row in data.iterrows():
        tree.insert("", "end", values=(row['Nama Barang'], row['Harga'], row['Stok']))

    # Tombol kembali
    Button(daftar_menu, text="Kembali", command=lambda: show_frame(main_menu), bg="#CC0000", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.82, anchor="center")

# Fungsi menambah stok barang
def tambah_stok():
    def simpan_stok():
        nama = selected_item_var.get()
        jumlah = stok_var.get()
        if not jumlah.isdigit():
            messagebox.showerror("Error", "Masukkan jumlah stok yang valid!")
            return
        jumlah = int(jumlah)
        if nama == "Pilih Barang":
            messagebox.showerror("Error", "Pilih barang yang ingin ditambah stok!")
            return
        data.loc[data['Nama Barang'] == nama, 'Stok'] += jumlah
        update_excel()
        messagebox.showinfo("Sukses", f"Stok barang '{nama}' berhasil ditambah sebanyak {jumlah}!")
        stok_var.set("")
        selected_item_var.set("Pilih Barang")

    show_frame(tambah_stok_menu)  # Menampilkan frame tambah stok
    for widget in tambah_stok_menu.winfo_children():
        widget.destroy()
        
    # Membuat Canvas untuk background
    canvas = Canvas(tambah_stok_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("fitur.jpg")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return
    
    tambah_barang_text = canvas.create_text(770, 210, text="Tambah Stok Barang", font=("Bubble Bobble", 40, "bold"), fill="black")
    selected_item_var, stok_var = StringVar(value="Pilih Barang"), StringVar()

    OptionMenu(tambah_stok_menu, selected_item_var, *data['Nama Barang']).place(relx=0.5, rely=0.38, anchor="center")
    Entry(tambah_stok_menu, textvariable=stok_var, font=("Arial", 14)).place(relx=0.5, rely=0.43, anchor="center")
    Button(tambah_stok_menu, text="Simpan", command=simpan_stok, bg="#4CAF50", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.48, anchor="center")
    Button(tambah_stok_menu, text="Kembali", command=lambda: show_frame(main_menu), bg="#CC0000", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.53, anchor="center")  # Tombol Kembali berfungsi dengan baik

# Fungsi transaksi
def transaksi_penjualan():
    def simpan_transaksi():
        nonlocal transaksi
        if not transaksi:
            messagebox.showerror("Error", "Belum ada barang dalam transaksi!")
            return
        
        # Penanganan nomor transaksi
        if not riwayat_data.empty:
            no_transaksi = riwayat_data['No Transaksi'].max() + 1
        else:
            no_transaksi = 1
        
        waktu_transaksi = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        total_transaksi = 0  # Inisialisasi total transaksi

        # Menambahkan barang-barang dalam transaksi
        for item in transaksi:
            nama, jumlah, harga = item['Nama Barang'], item['Jumlah'], item['Harga']
            total = jumlah * harga
            total_transaksi += total  # Menambahkan total per item ke total transaksi
            data.loc[data['Nama Barang'] == nama, 'Stok'] -= jumlah  # Update stok
            # Menambahkan transaksi baru ke riwayat, dengan No Transaksi yang sama
            riwayat_data.loc[len(riwayat_data)] = [no_transaksi, nama, jumlah, total, waktu_transaksi]
        
        # Pastikan untuk menyimpan data ke Excel setelah transaksi selesai
        update_excel()
        simpan_riwayat()
        
        # Menampilkan total transaksi setelah proses
        messagebox.showinfo("Sukses", f"Transaksi berhasil disimpan!\nTotal Transaksi: Rp{total_transaksi:,.0f}")
        
        transaksi.clear()  # Reset transaksi
        reset_form()  # Reset form transaksi

    def add_item():
        nama, jumlah = selected_item_var.get(), jumlah_var.get()
        if not nama or not jumlah.isdigit():
            messagebox.showerror("Error", "Pilih barang dan masukkan jumlah!")
            return
        jumlah = int(jumlah)
        stok = data.loc[data['Nama Barang'] == nama, 'Stok'].values[0]
        if jumlah > stok:
            messagebox.showerror("Error", "Stok tidak mencukupi!")
            return
        harga = data.loc[data['Nama Barang'] == nama, 'Harga'].values[0]
        transaksi.append({"Nama Barang": nama, "Jumlah": jumlah, "Harga": harga})
        update_listbox()  # Update tampilan listbox
        update_total_label()  # Update total transaksi
        jumlah_var.set("")  # Reset input jumlah

    def update_listbox():
        listbox.delete(0, END)
        for item in transaksi:
            total_item = item['Jumlah'] * item['Harga']
            listbox.insert(END, f"{item['Nama Barang']} - {item['Jumlah']} x {item['Harga']} = Rp{total_item:,.0f}")

    def update_total_label():
        total_transaksi = sum(item['Jumlah'] * item['Harga'] for item in transaksi)
        total_label.config(text=f"Total Transaksi: Rp{total_transaksi:,.0f}")  # Update total label

    def reset_form():
        transaksi.clear()
        listbox.delete(0, END)
        jumlah_var.set("")
        selected_item_var.set("Pilih Barang")
        update_total_label()  # Reset total label saat form direset

    transaksi = []  # Inisialisasi list transaksi
    show_frame(transaksi_menu)  # Menampilkan frame transaksi
    for widget in transaksi_menu.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk background
    canvas = Canvas(transaksi_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("fitur.jpg")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return
    
    # Judul dan elemen input
    transaksi_text = canvas.create_text(770, 80, text="Transaksi Penjualan", font=("Bubble Bobble", 50, "bold"), fill="black")
    selected_item_var, jumlah_var = StringVar(value="Pilih Barang"), StringVar()

    # Dropdown untuk memilih barang
    OptionMenu(transaksi_menu, selected_item_var, *data['Nama Barang']).place(relx=0.5, rely=0.215, anchor="center")
    # Input untuk jumlah barang
    Entry(transaksi_menu, textvariable=jumlah_var).place(relx=0.5, rely=0.25, anchor="center")
    # Tombol untuk menambah barang ke transaksi
    Button(transaksi_menu, text="Tambah", command=add_item).place(relx=0.5, rely=0.29, anchor="center")

    # Listbox untuk menampilkan barang dalam transaksi
    listbox = Listbox(transaksi_menu, width=50, height=15)
    listbox.place(relx=0.5, rely=0.47, anchor="center")

    # Label untuk menampilkan total transaksi
    total_label = Label(transaksi_menu, text="Total Transaksi: Rp0", font=("Arial", 12, "bold"))
    total_label.place(relx=0.5, rely=0.65, anchor="center")

    # Tombol untuk memproses transaksi
    Button(transaksi_menu, text="Proses Transaksi", command=simpan_transaksi, font=("Arial", 12), bg="#4CAF50", fg="white").place(relx=0.5, rely=0.70, anchor="center")
    
    # Tombol reset
    Button(transaksi_menu, text="Reset", command=reset_form, font=("Arial", 12), bg="#4CAF50", fg="white").place(relx=0.5, rely=0.75, anchor="center")

    # Tombol kembali ke menu utama
    Button(transaksi_menu, text="Kembali", command=lambda: show_frame(main_menu), font=("Arial", 12), bg="#CC0000", fg="white").place(relx=0.5, rely=0.80, anchor="center")

# Fungsi riwayat
def riwayat_transaksi():
    show_frame(riwayat_menu)
    for widget in riwayat_menu.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk background
    canvas = Canvas(riwayat_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("fitur.jpg")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return
    
    # Judul
    riwayat_text = canvas.create_text(770, 80, text="Riwayat Transaksi", font=("Bubble Bobble", 50, "bold"), fill="black")

    # Treeview untuk tabel
    columns = ("No Transaksi", "Nama Barang", "Jumlah", "Total", "Tanggal")
    tree = ttk.Treeview(riwayat_menu, columns=columns, show="headings", height=20)
    tree.place(relx=0.5, rely=0.45, anchor="center")

    # Menambahkan heading untuk setiap kolom
    tree.heading("No Transaksi", text="No Transaksi")
    tree.heading("Nama Barang", text="Nama Barang")
    tree.heading("Jumlah", text="Jumlah")
    tree.heading("Total", text="Total (Rp)")
    tree.heading("Tanggal", text="Tanggal")

    # Menentukan lebar kolom
    tree.column("No Transaksi", width=100, anchor="center")
    tree.column("Nama Barang", width=200, anchor="w")
    tree.column("Jumlah", width=100, anchor="center")
    tree.column("Total", width=150, anchor="center")
    tree.column("Tanggal", width=150, anchor="center")

    # Menambahkan data per transaksi ke tabel
    for _, row in riwayat_data.iterrows():
        tree.insert("", "end", values=(row['No Transaksi'], row['Nama Barang'], row['Jumlah'], f"Rp{row['Total']:,.0f}", row['Tanggal']))

    # Tombol kembali
    Button(riwayat_menu, text="Kembali", command=lambda: show_frame(main_menu), bg="#CC0000", fg="white", font=("Arial", 11)).place(relx=0.5, rely=0.755, anchor="center")

# Fungsi untuk keluar dan menutup aplikasi
def keluar():
    jawab = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin keluar?")
    if jawab:  
        root.destroy() 

# Inisialisasi aplikasi
root = Tk() 
root.title("Sistem Penjualan Barang")
root.geometry("1920x1080")

# Variabel global untuk input
username_var = StringVar()
password_var = StringVar()
nama_var = StringVar()
harga_var = StringVar()
stok_var = StringVar()
selected_item_var = StringVar(value="Pilih Barang")
jumlah_var = StringVar()

# Fungsi untuk menampilkan frame
def show_frame(frame):
    # Menyembunyikan semua frame terlebih dahulu
    for f in [login_frame, sign_up_frame, main_menu, barang_menu, daftar_menu, transaksi_menu, riwayat_menu, tambah_stok_menu]:
        f.pack_forget()
    frame.pack(fill="both", expand=True)  # Menampilkan frame yang dipilih

# Setup Frame (login, sign up, dll.)
login_frame = Frame(root)
sign_up_frame = Frame(root)
main_menu = Frame(root)
barang_menu = Frame(root)
daftar_menu = Frame(root)
transaksi_menu = Frame(root)
riwayat_menu = Frame(root)
tambah_stok_menu = Frame(root)

# Fungsi untuk menampilkan frame login
def show_login():
    show_frame(login_frame)
    for widget in login_frame.winfo_children():
        widget.destroy()
    
    # Membuat canvas untuk background
    canvas = Canvas(login_frame, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    # Memuat gambar background
    try:
        image = Image.open("login.png")
        resized_image = image.resize((1600, 800))  # Ubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.bg_image = bg_image  # Menyimpan referensi gambar agar tidak hilang
        canvas_image = canvas.create_image(0, 0, image=bg_image, anchor="nw")

        # Mengatur ulang ukuran kanvas saat jendela berubah ukuran
        def resize_canvas(event):
            canvas.config(width=event.width, height=event.height)
            canvas.itemconfig(canvas_image, image=bg_image)  # Pastikan gambar mengikuti ukuran kanvas

        root.bind("<Configure>", resize_canvas)

    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return
    
    # Menambahkan widget login di atas canvas
    Entry(login_frame, textvariable=username_var,font=("Arial", 14)).place(relx=0.55, rely=0.47, anchor="center") 
    Entry(login_frame, textvariable=password_var, font=("Arial", 14), show="*").place(relx=0.55, rely=0.54, anchor="center")
    Button(login_frame, text="Login", command=validate_login, bg="#00CC00", fg="white", font=("Arial", 14), width=10, cursor="hand2").place(relx=0.5, rely=0.62, anchor="center")
    Button(login_frame, text="Sign Up", command=show_sign_up, fg="blue", font=("Arial", 10, "underline"), cursor="hand2").place(relx=0.5, rely=0.68, anchor="center")
    login_text = canvas.create_text(770, 290, text="Login Admin", font=("Bubble Bobble", 50, "bold"), fill="black")
    username_label = canvas.create_text(630, 370, text="Username:", font=("Arial", 14), fill="black")
    password_label = canvas.create_text(630, 430, text="Password:", font=("Arial", 14), fill="black")
  
# Frame Menu Utama
def setup_main_menu():
    # Menghancurkan widget yang ada sebelumnya
    for widget in main_menu.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk background
    canvas = Canvas(main_menu, width=root.winfo_width(), height=root.winfo_height())
    canvas.pack(fill="both", expand=True)

    try:
        image = Image.open("menu_utama.png")
        resized_image = image.resize((1560, 800))  # Mengubah ukuran gambar
        bg_image = ImageTk.PhotoImage(resized_image)  # Konversi ke format Tkinter
        canvas.create_image(0, 0, image=bg_image, anchor="nw")
        canvas.image = bg_image  # Simpan referensi gambar agar tidak hilang
    except Exception as e:
        messagebox.showerror("Error", f"Tidak dapat memuat background: {e}")
        return

    # Menambahkan elemen UI di atas canvas
    Menu_text = canvas.create_text(770, 190, text="Toko Pena Ceria", font=("Coffee Spark", 50, "bold"), fill="black")

    Button(main_menu, text="Tambah Barang", command=tambah_barang,fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.35, anchor="center")
    Button(main_menu, text="Daftar Barang", command=daftar_barang, fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.43, anchor="center")
    Button(main_menu, text="Transaksi Penjualan", command=transaksi_penjualan, fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.51, anchor="center")
    Button(main_menu, text="Riwayat Transaksi", command=riwayat_transaksi, fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.59, anchor="center")
    Button(main_menu, text="Tambah Stok", command=tambah_stok, fg="black", font=("Arial", 16)).place(relx=0.5, rely=0.67, anchor="center")
    Button(main_menu, text="Keluar", command=keluar, bg="#CC0000", fg="white", font=("Arial", 16)).place(relx=0.5, rely=0.75, anchor="center")

# Menampilkan login frame pertama kali
show_login()

# Mainloop untuk menjalankan aplikasi
root.mainloop()
