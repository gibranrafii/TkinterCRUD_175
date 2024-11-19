
# Mengimpor modul sqlite3 untuk berinteraksi dengan database SQLite
import sqlite3

# Mengimpor kelas dan fungsi tertentu dari modul tkinter untuk membuat elemen GUI
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk
# Fungsi untuk membuat database dan tabel
def create_database():
    # Membuka koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Menjalankan perintah SQL untuk membuat tabel 'nilai_siswa' jika belum ada
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
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

def fetch_data():
    # Membuka koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Menjalankan perintah SQL untuk mengambil semua data dari tabel 'nilai_siswa'
    cursor.execute("SELECT * FROM nilai_siswa")
    
    # Mengambil semua baris hasil query dan menyimpannya dalam variabel 'rows'
    rows = cursor.fetchall()
    
    # Menutup koneksi ke database
    conn.close()
    
    # Mengembalikan hasil query sebagai output dari fungsi
    return rows

def save_to_database(nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Menjalankan perintah SQL untuk memasukkan data baru ke dalam tabel 'nilai_siswa'
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Menjalankan perintah SQL untuk memperbarui data pada tabel 'nilai_siswa' berdasarkan 'id'
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

def delete_database(record_id):
    # Membuka koneksi ke database SQLite bernama 'nilai_siswa.db'
    conn = sqlite3.connect('nilai_siswa.db')
    
    # Membuat objek cursor untuk mengeksekusi perintah SQL
    cursor = conn.cursor()
    
    # Menjalankan perintah SQL untuk menghapus data dari tabel 'nilai_siswa' berdasarkan 'id'
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    
    # Menyimpan perubahan ke database
    conn.commit()
    
    # Menutup koneksi ke database
    conn.close()

def calculate_prediction(biologi, fisika, inggris):
    # Fungsi untuk mengambil prediksi fakultas berdasarkan nilai biologi, fisika, dan inggris
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"
def submit():
    # Fungsi untuk menyimpan data ke dalam database 'nilai_siswa.db'
    try:
        nama = nama_var.get()  # Mengambil nilai dari variabel nama_var
        biologi = int(biologi_var.get())  # Mengambil nilai dari variabel biologi_var
        fisika = int(fisika_var.get())  # Mengambil nilai dari variabel fisika_var
        inggris = int(inggris_var.get())  # Mengambil nilai dari variabel inggris_var

        if not nama:  # Jika nama kosong, maka akanjarkan exception
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Mengambil prediksi fakultas berdasarkan nilai biologi, fisika, dan inggris
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Mengirimkan perintah SQL untuk menyimpan data baru ke dalam tabel 'nilai_siswa'

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  # Mengirimkan pesan sukses
        clear_inputs()  # Mengosongkan isi input field
        populate_table()  # Mengosongkan data dari tabel 'nilai_siswa' ke tabel
    except ValueError as e:  # Jika terjadi kesalahan input, maka akanjarkan exception
        messagebox.showerror("Error", f"Input tidak valid: {e}")

def update():
    # Fungsi untuk mengubah data dalam database 'nilai_siswa.db'
    try:
        if not selected_record_id.get():  # Jika tidak ada data yang dipilih, maka akanjarkan exception
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())  # Mengambil nilai dari variabel selected_record_id
        nama = nama_var.get()  # Mengambil nilai dari variabel nama_var
        biologi = int(biologi_var.get())  # Mengambil nilai dari variabel biologi_var
        fisika = int(fisika_var.get())  # Mengambil nilai dari variabel fisika_var
        inggris = int(inggris_var.get())  # Mengambil nilai dari variabel inggris_var

        if not nama:  # Jika nama kosong, maka akanjarkan exception
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)  # Mengambil prediksi fakultas berdasarkan nilai biologi, fisika, dan inggris
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Mengirimkan perintah SQL untuk memperbarui data dalam tabel 'nilai_siswa'

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")  # Mengirimkan pesan sukses
        clear_inputs()  # Mengosongkan isi input field
        populate_table()  # Mengosongkan data dari tabel 'nilai_siswa' ke tabel
    except ValueError as e:  # Jika terjadi kesalahan input, maka akanjarkan exception
        messagebox.showerror("Error", f"Kesalahan: {e}")
def delete():
    # Fungsi untuk menghapus data dalam database 'nilai_siswa.db'
    try:
        if not selected_record_id.get():  # Jika tidak ada data yang dipilih, maka akanjarkan exception
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil nilai dari variabel selected_record_id
        delete_database(record_id)  # Mengirimkan perintah SQL untuk menghapus data dari tabel 'nilai_siswa' berdasarkan 'id'
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")  # Mengirimkan pesan sukses
        clear_inputs()  # Mengosongkan isi input field
        populate_table()  # Mengosongkan data dari tabel 'nilai_siswa' ke tabel
    except ValueError as e:  # Jika terjadi kesalahan input, maka akanjarkan exception
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    # Fungsi untuk mengosongkan isi input field
    nama_var.set("")  # Mengosongkan nilai dari variabel nama_var
    biologi_var.set("")  # Mengosongkan nilai dari variabel biologi_var
    fisika_var.set("")  # Mengosongkan nilai dari variabel fisika_var
    inggris_var.set("")  # Mengosongkan nilai dari variabel inggris_var
    selected_record_id.set("")  # Mengosongkan data dari tabel 'nilai_siswa' ke variabel selected_record_id

def populate_table():
    # Fungsi untuk menampilkan data dalam tabel
    for row in tree.get_children():  # Mengosongkan semua baris yang ada di tabel
        tree.delete(row)  # Menghapus semua baris yang ada di tabel
    for row in fetch_data():  # Mengambil semua data dari tabel 'nilai_siswa'
        tree.insert('', 'end', values=row)  # Menambahkan baris baru ke tabel dengan nilai yang sama dengan nilai dalam variabel 'row'

# Fungsi yang dipanggil ketika user memilih baris data di tabel
def fill_inputs_from_table(event):
    try:
        # Mengambil baris yang dipilih oleh user
        selected_item = tree.selection()[0]
        # Mengambil nilai-nilai pada baris yang dipilih
        selected_row = tree.item(selected_item)['values']

        # Mengisi nilai-nilai pada variabel-variabel tkinter dengan nilai-nilai pada baris yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        # Jika user belum memilih baris data, maka akan muncul pesan error
        messagebox.showerror("Error", "Pilih data yang valid!")
# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

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

tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

populate_table()

root.mainloop()