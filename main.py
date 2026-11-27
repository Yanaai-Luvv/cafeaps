"""
APLIKASI KASIR KAFE
Projek UAS Algoritma dan Pemrograman (Python)

Masalah dunia nyata:
    Kafe kecil sering mencatat pesanan dan stok secara manual sehingga
    rawan salah hitung, stok tidak terpantau, dan laporan penjualan lambat.

Materi yang dicakup:
    - Percabangan (if/elif/else)       - Perulangan (while, for)
    - List, Tuple, Dictionary          - Fungsi dan parameter
    - Algoritma pencarian (linear & binary search)
    - Algoritma pengurutan (bubble sort & selection sort)
    - Penanganan error (try-except)    - Library standar: datetime
"""

from datetime import datetime

# ======================================================================
# KONSTANTA
# ======================================================================
PAJAK = 0.10            # pajak 10%
DISKON_MINIMAL = 100000  # belanja >= Rp100.000 dapat diskon
DISKON_PERSEN = 0.10     # diskon 10%
STOK_MENIPIS = 5         # peringatan jika stok <= 5

# ======================================================================
# DATA (Dictionary: kode -> data menu)
# ======================================================================
menu = {
    "K01": {"nama": "Espresso",       "kategori": "Kopi",     "harga": 18000, "stok": 30},
    "K02": {"nama": "Cappuccino",     "kategori": "Kopi",     "harga": 25000, "stok": 25},
    "K03": {"nama": "Latte",          "kategori": "Kopi",     "harga": 27000, "stok": 25},
    "K04": {"nama": "Es Kopi Susu",   "kategori": "Kopi",     "harga": 22000, "stok": 40},
    "K05": {"nama": "Teh Tarik",      "kategori": "Non-Kopi", "harga": 15000, "stok": 30},
    "K06": {"nama": "Matcha Latte",   "kategori": "Non-Kopi", "harga": 28000, "stok": 20},
    "K07": {"nama": "Croissant",      "kategori": "Makanan",  "harga": 20000, "stok": 15},
    "K08": {"nama": "Roti Bakar",     "kategori": "Makanan",  "harga": 17000, "stok": 20},
    "K09": {"nama": "Kentang Goreng", "kategori": "Makanan",  "harga": 19000, "stok": 4},
}

# List yang berisi dictionary transaksi
riwayat = []


# ======================================================================
# FUNGSI BANTU
# ======================================================================
def rupiah(angka):
    """Ubah angka menjadi format Rp12.000."""
    return "Rp" + f"{int(angka):,}".replace(",", ".")


def input_angka(pesan, minimal=0):
    """Minta input bilangan bulat, ulangi sampai valid (try-except)."""
    while True:
        try:
            nilai = int(input(pesan))
            if nilai < minimal:
                print(f"  ! Nilai minimal {minimal}.")
            else:
                return nilai
        except ValueError:
            print("  ! Input harus berupa angka bulat.")


def garis(panjang=62, simbol="="):
    print(simbol * panjang)


# ======================================================================
# ALGORITMA PENGURUTAN
# data = list of tuple (kode, dictionary_data); kunci = fungsi pengambil nilai
# ======================================================================
def bubble_sort(data, kunci, naik=True):
    """Bubble sort: bandingkan pasangan bersebelahan, tukar jika salah urutan."""
    hasil = data[:]  # salin agar data asli tidak berubah
    n = len(hasil)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            a, b = kunci(hasil[j]), kunci(hasil[j + 1])
            harus_tukar = a > b if naik else a < b
            if harus_tukar:
                hasil[j], hasil[j + 1] = hasil[j + 1], hasil[j]
    return hasil


def selection_sort(data, kunci, naik=True):
    """Selection sort: pilih nilai terkecil/terbesar lalu tempatkan di depan."""
    hasil = data[:]
    n = len(hasil)
    for i in range(n - 1):
        idx_pilih = i
        for j in range(i + 1, n):
            a, b = kunci(hasil[j]), kunci(hasil[idx_pilih])
            lebih_baik = a < b if naik else a > b
            if lebih_baik:
                idx_pilih = j
        hasil[i], hasil[idx_pilih] = hasil[idx_pilih], hasil[i]
    return hasil


# ======================================================================
# ALGORITMA PENCARIAN
# ======================================================================
def cari_nama(kata):
    """Linear search: periksa menu satu per satu, cocokkan potongan nama."""
    ditemukan = []
    for kode, data in menu.items():
        if kata.lower() in data["nama"].lower():
            ditemukan.append((kode, data))
    return ditemukan


def cari_kode(kode):
    """Binary search pada daftar kode yang sudah terurut. Return kode / None."""
    daftar = sorted(menu.keys())
    kiri, kanan = 0, len(daftar) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if daftar[tengah] == kode:
            return daftar[tengah]
        elif daftar[tengah] < kode:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return None


# ======================================================================
# TAMPILAN MENU
# ======================================================================
def tampilkan_menu(daftar=None):
    """Cetak tabel menu. daftar = list of tuple (kode, data)."""
    if daftar is None:
        daftar = list(menu.items())
    if len(daftar) == 0:
        print("  (tidak ada data)")
        return
    garis()
    print(f"{'Kode':<6}{'Nama':<18}{'Kategori':<11}{'Harga':>11}{'Stok':>7}")
    garis(62, "-")
    for kode, d in daftar:
        peringatan = " !" if d["stok"] <= STOK_MENIPIS else ""
        print(f"{kode:<6}{d['nama']:<18}{d['kategori']:<11}"
              f"{rupiah(d['harga']):>11}{d['stok']:>7}{peringatan}")
    garis()


def menu_cari():
    print("\n--- CARI MENU ---")
    print("1. Cari berdasarkan nama (linear search)")
    print("2. Cari berdasarkan kode (binary search)")
    pilih = input("Pilih: ").strip()
    if pilih == "1":
        kata = input("Masukkan nama/sebagian nama: ").strip()
        tampilkan_menu(cari_nama(kata))
    elif pilih == "2":
        kode = input("Masukkan kode (contoh K01): ").strip().upper()
        hasil = cari_kode(kode)
        if hasil:
            tampilkan_menu([(hasil, menu[hasil])])
        else:
            print("  Kode tidak ditemukan.")
    else:
        print("  Pilihan tidak valid.")


def menu_urutkan():
    print("\n--- URUTKAN MENU ---")
    print("Kriteria : 1. Harga  2. Nama  3. Stok")
    kriteria = input("Pilih kriteria: ").strip()
    print("Algoritma: 1. Bubble sort  2. Selection sort")
    algo = input("Pilih algoritma: ").strip()
    arah = input("Urutan (1 = naik, 2 = turun): ").strip()

    if kriteria == "1":
        kunci = lambda item: item[1]["harga"]
    elif kriteria == "2":
        kunci = lambda item: item[1]["nama"].lower()
    elif kriteria == "3":
        kunci = lambda item: item[1]["stok"]
    else:
        print("  Kriteria tidak valid.")
        return
    if algo not in ("1", "2") or arah not in ("1", "2"):
        print("  Pilihan tidak valid.")
        return

    naik = (arah == "1")
    data = list(menu.items())
    if algo == "1":
        hasil = bubble_sort(data, kunci, naik)
    else:
        hasil = selection_sort(data, kunci, naik)
    tampilkan_menu(hasil)


# ======================================================================
# TRANSAKSI
# ======================================================================
def jumlah_di_keranjang(keranjang, kode):
    """Hitung jumlah suatu kode yang sudah ada di keranjang."""
    for item in keranjang:
        if item[0] == kode:
            return item[2]
    return 0


def tambah_ke_keranjang(keranjang, kode, jumlah):
    """Keranjang = list of tuple (kode, nama, jumlah, harga). Tuple tidak bisa
    diubah, jadi item lama diganti tuple baru bila kode sudah ada."""
    for i in range(len(keranjang)):
        if keranjang[i][0] == kode:
            k, nama, jml, harga = keranjang[i]
            keranjang[i] = (k, nama, jml + jumlah, harga)
            return
    keranjang.append((kode, menu[kode]["nama"], jumlah, menu[kode]["harga"]))


def hitung_total(keranjang):
    """Return (subtotal, diskon, pajak, total)."""
    subtotal = 0
    for _, _, jumlah, harga in keranjang:
        subtotal += jumlah * harga
    diskon = subtotal * DISKON_PERSEN if subtotal >= DISKON_MINIMAL else 0
    pajak = (subtotal - diskon) * PAJAK
    total = subtotal - diskon + pajak
    return subtotal, diskon, pajak, total


def cetak_struk(trx):
    garis()
    print(f"{'STRUK KAFE':^62}")
    garis()
    print(f"No. Transaksi : {trx['id']}")
    print(f"Waktu         : {trx['waktu']}")
    print(f"Kasir/Pelanggan: {trx['pelanggan']}")
    garis(62, "-")
    for nama, jumlah, harga in trx["item"]:
        print(f"{nama:<20}{jumlah:>3} x {rupiah(harga):>10}{rupiah(jumlah * harga):>14}")
    garis(62, "-")
    print(f"{'Subtotal':<40}{rupiah(trx['subtotal']):>22}")
    if trx["diskon"] > 0:
        print(f"{'Diskon 10%':<40}{'-' + rupiah(trx['diskon']):>22}")
    print(f"{'Pajak 10%':<40}{rupiah(trx['pajak']):>22}")
    print(f"{'TOTAL':<40}{rupiah(trx['total']):>22}")
    print(f"{'Bayar':<40}{rupiah(trx['bayar']):>22}")
    print(f"{'Kembalian':<40}{rupiah(trx['kembalian']):>22}")
    garis()
    print(f"{'Terima kasih, selamat menikmati!':^62}")
    garis()


def transaksi():
    print("\n--- TRANSAKSI BARU ---")
    pelanggan = input("Nama pelanggan (Enter = Umum): ").strip() or "Umum"
    keranjang = []  # list of tuple

    while True:
        print()
        tampilkan_menu()
        print("Ketik kode menu untuk memesan | 'selesai' = bayar | 'batal' = batalkan")
        kode = input("Kode: ").strip().upper()

        if kode == "SELESAI":
            if len(keranjang) == 0:
                print("  Keranjang masih kosong.")
                continue
            break
        elif kode == "BATAL":
            print("  Transaksi dibatalkan.")
            return

        if cari_kode(kode) is None:          # binary search
            print("  ! Kode menu tidak ditemukan.")
            continue

        jumlah = input_angka(f"Jumlah {menu[kode]['nama']}: ", minimal=1)
        sudah = jumlah_di_keranjang(keranjang, kode)
        if sudah + jumlah > menu[kode]["stok"]:
            print(f"  ! Stok tidak cukup (tersedia {menu[kode]['stok']}, "
                  f"di keranjang {sudah}).")
            continue

        tambah_ke_keranjang(keranjang, kode, jumlah)
        print(f"  + {jumlah} {menu[kode]['nama']} ditambahkan.")

    # Ringkasan pesanan
    subtotal, diskon, pajak, total = hitung_total(keranjang)
    print("\n--- RINGKASAN PESANAN ---")
    for _, nama, jumlah, harga in keranjang:
        print(f"  {nama:<18}{jumlah:>3} x {rupiah(harga):>10} = {rupiah(jumlah * harga):>10}")
    print(f"  Subtotal : {rupiah(subtotal)}")
    if diskon > 0:
        print(f"  Diskon   : -{rupiah(diskon)}  (belanja >= {rupiah(DISKON_MINIMAL)})")
    print(f"  Pajak    : {rupiah(pajak)}")
    print(f"  TOTAL    : {rupiah(total)}")

    # Pembayaran (ulang sampai uang cukup, atau 0 untuk batal)
    while True:
        bayar = input_angka("Uang dibayar (0 = batal): ", minimal=0)
        if bayar == 0:
            print("  Transaksi dibatalkan.")
            return
        if bayar >= round(total):
            break
        print(f"  ! Uang kurang {rupiah(round(total) - bayar)}.")

    # Kurangi stok
    for kode, _, jumlah, _ in keranjang:
        menu[kode]["stok"] -= jumlah

    # Simpan ke riwayat
    trx = {
        "id": f"TRX{len(riwayat) + 1:03d}",
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "pelanggan": pelanggan,
        "item": [(nama, jumlah, harga) for _, nama, jumlah, harga in keranjang],
        "subtotal": subtotal,
        "diskon": diskon,
        "pajak": pajak,
        "total": round(total),
        "bayar": bayar,
        "kembalian": bayar - round(total),
    }
    riwayat.append(trx)
    print()
    cetak_struk(trx)


# ======================================================================
# KELOLA MENU (tambah, ubah harga, tambah stok, hapus)
# ======================================================================
def kode_baru():
    nomor = 1
    while f"K{nomor:02d}" in menu:
        nomor += 1
    return f"K{nomor:02d}"


def kelola_menu():
    while True:
        print("\n--- KELOLA MENU ---")
        print("1. Tambah menu baru")
        print("2. Ubah harga")
        print("3. Tambah stok")
        print("4. Hapus menu")
        print("0. Kembali")
        pilih = input("Pilih: ").strip()

        if pilih == "1":
            nama = input("Nama menu: ").strip()
            if nama == "":
                print("  ! Nama tidak boleh kosong.")
                continue
            kategori = input("Kategori (Kopi/Non-Kopi/Makanan): ").strip() or "Lainnya"
            harga = input_angka("Harga: ", minimal=1)
            stok = input_angka("Stok awal: ", minimal=0)
            kode = kode_baru()
            menu[kode] = {"nama": nama, "kategori": kategori, "harga": harga, "stok": stok}
            print(f"  Menu {nama} ditambahkan dengan kode {kode}.")

        elif pilih in ("2", "3", "4"):
            tampilkan_menu()
            kode = input("Kode menu: ").strip().upper()
            if cari_kode(kode) is None:
                print("  ! Kode tidak ditemukan.")
                continue
            if pilih == "2":
                menu[kode]["harga"] = input_angka("Harga baru: ", minimal=1)
                print("  Harga diperbarui.")
            elif pilih == "3":
                menu[kode]["stok"] += input_angka("Jumlah stok ditambah: ", minimal=1)
                print("  Stok diperbarui.")
            else:
                yakin = input(f"Hapus {menu[kode]['nama']}? (y/n): ").strip().lower()
                if yakin == "y":
                    del menu[kode]
                    print("  Menu dihapus.")

        elif pilih == "0":
            break
        else:
            print("  Pilihan tidak valid.")


# ======================================================================
# RIWAYAT & LAPORAN
# ======================================================================
def lihat_riwayat():
    print("\n--- RIWAYAT TRANSAKSI ---")
    if len(riwayat) == 0:
        print("  Belum ada transaksi.")
        return
    garis()
    print(f"{'ID':<8}{'Waktu':<21}{'Pelanggan':<16}{'Total':>14}")
    garis(62, "-")
    for trx in riwayat:
        print(f"{trx['id']:<8}{trx['waktu']:<21}{trx['pelanggan']:<16}{rupiah(trx['total']):>14}")
    garis()


def laporan():
    print("\n--- LAPORAN PENJUALAN ---")
    if len(riwayat) == 0:
        print("  Belum ada transaksi.")
    else:
        pendapatan = 0
        terjual = {}  # dictionary: nama menu -> total porsi terjual
        for trx in riwayat:
            pendapatan += trx["total"]
            for nama, jumlah, _ in trx["item"]:
                terjual[nama] = terjual.get(nama, 0) + jumlah

        print(f"Jumlah transaksi : {len(riwayat)}")
        print(f"Total pendapatan : {rupiah(pendapatan)}")
        print(f"Rata-rata/trx    : {rupiah(pendapatan / len(riwayat))}")

        # Urutkan menu terlaris (selection sort, turun)
        daftar = list(terjual.items())  # list of tuple (nama, jumlah)
        daftar = selection_sort(daftar, lambda x: x[1], naik=False)
        print("\nMenu terlaris:")
        for urutan, (nama, jumlah) in enumerate(daftar, start=1):
            print(f"  {urutan}. {nama:<18}{jumlah} porsi")

    # Peringatan stok menipis
    print("\nStok menipis (<= " + str(STOK_MENIPIS) + "):")
    ada = False
    for kode, d in menu.items():
        if d["stok"] <= STOK_MENIPIS:
            print(f"  - {kode} {d['nama']} (sisa {d['stok']})")
            ada = True
    if not ada:
        print("  Semua stok aman.")


# ======================================================================
# PROGRAM UTAMA
# ======================================================================
def main():
    print("=" * 62)
    print(f"{'SELAMAT DATANG DI APLIKASI KASIR KAFE':^62}")
    print("=" * 62)

    while True:
        print("\n========== MENU UTAMA ==========")
        print("1. Lihat daftar menu")
        print("2. Cari menu")
        print("3. Urutkan menu")
        print("4. Transaksi baru")
        print("5. Kelola menu & stok")
        print("6. Riwayat transaksi")
        print("7. Laporan penjualan")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            tampilkan_menu()
        elif pilih == "2":
            menu_cari()
        elif pilih == "3":
            menu_urutkan()
        elif pilih == "4":
            transaksi()
        elif pilih == "5":
            kelola_menu()
        elif pilih == "6":
            lihat_riwayat()
        elif pilih == "7":
            laporan()
        elif pilih == "0":
            print("Terima kasih. Program selesai.")
            break
        else:
            print("  ! Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()
