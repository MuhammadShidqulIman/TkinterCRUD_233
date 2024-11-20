import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    # Koneksi ke database SQLite (akan membuat file jika belum ada)
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Membuat tabel `nilai_siswa` jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()   # Menutup koneksi

# Fungsi untuk mengambil semua data dari tabel `nilai_siswa`
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query
    conn.close()  # Menutup koneksi
    return rows

# Fungsi untuk menyimpan data baru ke tabel `nilai_siswa`
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menyisipkan data
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data berdasarkan `id`
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))  # Memperbarui data
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data berdasarkan `id`
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Inggris tertinggi
    else:
        return "Tidak Diketahui"  # Nilai sama atau kondisi lainnya

# Fungsi untuk menambahkan data baru
def submit():
    try:
        # Mengambil nilai dari input pengguna
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")  # Validasi nama

        # Menghitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Simpan ke database

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Kosongkan input
        populate_table()  # Perbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")  # Menangani input invalid

# Fungsi untuk memperbarui data yang dipilih
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")  # Validasi data yang dipilih

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")  # Validasi nama

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Hitung prediksi
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Perbarui database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")  # Validasi data yang dipilih

        record_id = int(selected_record_id.get())
        delete_database(record_id)  # Hapus dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan semua input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk memperbarui tabel dengan data terbaru
def populate_table():
    for row in tree.get_children():
        tree.delete(row)  # Hapus semua baris di tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)  # Tambahkan data baru ke tabel

# Fungsi untuk mengisi input dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Ambil item yang dipilih
        selected_row = tree.item(selected_item)['values']  # Ambil nilai baris

        selected_record_id.set(selected_row[0])  # Set ID record yang dipilih
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Elemen GUI
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)  # Event untuk memilih data

populate_table()  # Isi tabel dengan data awal

root.mainloop()  


