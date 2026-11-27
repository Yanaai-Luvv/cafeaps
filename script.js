/* APLIKASI KASIR KAFE - versi web (padanan dari kasir_kafe.py)
   Materi: percabangan, perulangan, array/objek, fungsi,
   linear & binary search, bubble & selection sort. */

// ===== KONSTANTA =====
const PAJAK = 0.10, DISKON_MIN = 100000, DISKON = 0.10, STOK_TIPIS = 5;

// ===== DATA (objek: kode -> data menu) =====
const menu = {
  K01: { nama: "Espresso",       kategori: "Kopi",     harga: 18000, stok: 30 },
  K02: { nama: "Cappuccino",     kategori: "Kopi",     harga: 25000, stok: 25 },
  K03: { nama: "Latte",          kategori: "Kopi",     harga: 27000, stok: 25 },
  K04: { nama: "Es Kopi Susu",   kategori: "Kopi",     harga: 22000, stok: 40 },
  K05: { nama: "Teh Tarik",      kategori: "Non-Kopi", harga: 15000, stok: 30 },
  K06: { nama: "Matcha Latte",   kategori: "Non-Kopi", harga: 28000, stok: 20 },
  K07: { nama: "Croissant",      kategori: "Makanan",  harga: 20000, stok: 15 },
  K08: { nama: "Roti Bakar",     kategori: "Makanan",  harga: 17000, stok: 20 },
  K09: { nama: "Kentang Goreng", kategori: "Makanan",  harga: 19000, stok: 4 }
};
let riwayat = [];    // array transaksi
let keranjang = [];  // array {kode, nama, jumlah, harga}
let tampil = null;   // hasil cari/urut yang sedang ditampilkan

// ===== FUNGSI BANTU =====
const $ = id => document.getElementById(id);
const rp = n => "Rp" + Math.round(n).toLocaleString("id-ID");
const esc = s => String(s).replace(/[&<>"']/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const tukar = (a, i, j) => { const t = a[i]; a[i] = a[j]; a[j] = t; };

// ===== ALGORITMA PENGURUTAN (data = array [kode, data]) =====
function bubbleSort(data, kunci, naik) {
  const h = data.slice();
  for (let i = 0; i < h.length - 1; i++) {
    for (let j = 0; j < h.length - 1 - i; j++) {
      const a = kunci(h[j]), b = kunci(h[j + 1]);
      if (naik ? a > b : a < b) tukar(h, j, j + 1);
    }
  }
  return h;
}
function selectionSort(data, kunci, naik) {
  const h = data.slice();
  for (let i = 0; i < h.length - 1; i++) {
    let p = i;
    for (let j = i + 1; j < h.length; j++) {
      const a = kunci(h[j]), b = kunci(h[p]);
      if (naik ? a < b : a > b) p = j;
    }
    tukar(h, i, p);
  }
  return h;
}

// ===== ALGORITMA PENCARIAN =====
function cariNama(kata) {            // linear search
  const hasil = [];
  for (const [kode, d] of Object.entries(menu)) {
    if (d.nama.toLowerCase().includes(kata.toLowerCase())) hasil.push([kode, d]);
  }
  return hasil;
}
function cariKode(kode) {            // binary search
  const d = Object.keys(menu).sort();
  let l = 0, r = d.length - 1;
  while (l <= r) {
    const m = Math.floor((l + r) / 2);
    if (d[m] === kode) return d[m];
    if (d[m] < kode) l = m + 1; else r = m - 1;
  }
  return null;
}

// ===== MENU: TAMPIL, CARI, URUT =====
function renderMenu() {
  const daftar = tampil || Object.entries(menu);
  $("tbMenu").innerHTML = daftar.length === 0
    ? "<tr><td colspan='5'>Tidak ada data.</td></tr>"
    : daftar.map(([k, d]) => `<tr><td>${k}</td><td>${esc(d.nama)}</td><td>${esc(d.kategori)}</td>
        <td>${rp(d.harga)}</td><td class="${d.stok <= STOK_TIPIS ? "tipis" : ""}">${d.stok}</td></tr>`).join("");
}
function aksiCari() {
  const kata = $("kataCari").value.trim();
  if (kata === "") { tampil = null; return renderMenu(); }
  if ($("modeCari").value === "nama") tampil = cariNama(kata);
  else { const k = cariKode(kata.toUpperCase()); tampil = k ? [[k, menu[k]]] : []; }
  renderMenu();
}
function aksiUrut() {
  const kr = $("kriteria").value, naik = $("arah").value === "naik";
  const kunci = kr === "nama" ? it => it[1].nama.toLowerCase() : it => it[1][kr];
  const data = Object.entries(menu);
  tampil = $("algo").value === "bubble" ? bubbleSort(data, kunci, naik) : selectionSort(data, kunci, naik);
  renderMenu();
}

// ===== TRANSAKSI =====
function renderPilihan() {
  $("pilihMenu").innerHTML = Object.entries(menu).map(([k, d]) =>
    `<option value="${k}">${k} - ${esc(d.nama)} (${rp(d.harga)}, stok ${d.stok})</option>`).join("");
}
function hitung() {
  let subtotal = 0;
  for (const it of keranjang) subtotal += it.jumlah * it.harga;
  const diskon = subtotal >= DISKON_MIN ? subtotal * DISKON : 0;
  const pajak = (subtotal - diskon) * PAJAK;
  return { subtotal, diskon, pajak, total: subtotal - diskon + pajak };
}
function tambahKeranjang() {
  const kode = $("pilihMenu").value, jml = parseInt($("jumlah").value);
  if (!cariKode(kode)) return alert("Kode menu tidak ditemukan.");
  if (isNaN(jml) || jml < 1) return alert("Jumlah harus angka bulat minimal 1.");
  const ada = keranjang.find(it => it.kode === kode);
  const sudah = ada ? ada.jumlah : 0;
  if (sudah + jml > menu[kode].stok)
    return alert(`Stok tidak cukup (tersedia ${menu[kode].stok}, di keranjang ${sudah}).`);
  if (ada) ada.jumlah += jml;
  else keranjang.push({ kode, nama: menu[kode].nama, jumlah: jml, harga: menu[kode].harga });
  renderKeranjang();
}
function hapusItem(i) { keranjang.splice(i, 1); renderKeranjang(); }
function renderKeranjang() {
  $("tbKeranjang").innerHTML = keranjang.length === 0
    ? "<tr><td colspan='5'>Keranjang kosong.</td></tr>"
    : keranjang.map((it, i) => `<tr><td>${esc(it.nama)}</td><td>${it.jumlah}</td><td>${rp(it.harga)}</td>
        <td>${rp(it.jumlah * it.harga)}</td><td><button class="merah" onclick="hapusItem(${i})">x</button></td></tr>`).join("");
  const h = hitung();
  $("ringkasan").innerHTML = `Subtotal: ${rp(h.subtotal)}<br>` +
    (h.diskon > 0 ? `Diskon 10%: -${rp(h.diskon)}<br>` : "") +
    `Pajak 10%: ${rp(h.pajak)}<br><b>TOTAL: ${rp(h.total)}</b>`;
}
function prosesBayar() {
  if (keranjang.length === 0) return alert("Keranjang masih kosong.");
  const h = hitung(), total = Math.round(h.total), bayar = parseInt($("bayar").value);
  if (isNaN(bayar) || bayar <= 0) return alert("Masukkan uang yang dibayar.");
  if (bayar < total) return alert(`Uang kurang ${rp(total - bayar)}.`);

  for (const it of keranjang) menu[it.kode].stok -= it.jumlah;   // kurangi stok
  const trx = {
    id: "TRX" + String(riwayat.length + 1).padStart(3, "0"),
    waktu: new Date().toLocaleString("id-ID"),
    pelanggan: $("pelanggan").value.trim() || "Umum",
    item: keranjang.map(it => [it.nama, it.jumlah, it.harga]),
    ...h, total, bayar, kembalian: bayar - total
  };
  riwayat.push(trx);
  cetakStruk(trx);
  keranjang = []; $("bayar").value = ""; $("pelanggan").value = "";
  refresh();
}
function cetakStruk(t) {
  const garis = "=".repeat(44);
  let s = `${garis}\n            STRUK KAFE\n${garis}\n` +
          `No      : ${t.id}\nWaktu   : ${t.waktu}\nNama    : ${t.pelanggan}\n${"-".repeat(44)}\n`;
  for (const [nama, jml, harga] of t.item)
    s += `${nama.padEnd(16)}${String(jml).padStart(3)} x ${rp(harga).padStart(10)}${rp(jml * harga).padStart(11)}\n`;
  s += `${"-".repeat(44)}\n`;
  s += `${"Subtotal".padEnd(30)}${rp(t.subtotal).padStart(14)}\n`;
  if (t.diskon > 0) s += `${"Diskon 10%".padEnd(30)}${("-" + rp(t.diskon)).padStart(14)}\n`;
  s += `${"Pajak 10%".padEnd(30)}${rp(t.pajak).padStart(14)}\n`;
  s += `${"TOTAL".padEnd(30)}${rp(t.total).padStart(14)}\n`;
  s += `${"Bayar".padEnd(30)}${rp(t.bayar).padStart(14)}\n`;
  s += `${"Kembalian".padEnd(30)}${rp(t.kembalian).padStart(14)}\n${garis}\n    Terima kasih, selamat menikmati!\n`;
  $("struk").textContent = s;
  $("struk").hidden = false;
}

// ===== KELOLA MENU =====
function kodeBaru() {
  let n = 1;
  while (menu["K" + String(n).padStart(2, "0")]) n++;
  return "K" + String(n).padStart(2, "0");
}
function tambahMenu() {
  const nama = $("nNama").value.trim(), kategori = $("nKategori").value.trim() || "Lainnya";
  const harga = parseInt($("nHarga").value), stok = parseInt($("nStok").value);
  if (nama === "") return alert("Nama tidak boleh kosong.");
  if (isNaN(harga) || harga < 1) return alert("Harga harus angka minimal 1.");
  if (isNaN(stok) || stok < 0) return alert("Stok harus angka minimal 0.");
  menu[kodeBaru()] = { nama, kategori, harga, stok };
  ["nNama", "nKategori", "nHarga", "nStok"].forEach(id => $(id).value = "");
  refresh();
}
function ubahHarga(k) {
  const h = parseInt(prompt("Harga baru untuk " + menu[k].nama + ":"));
  if (isNaN(h) || h < 1) return alert("Harga tidak valid.");
  menu[k].harga = h; refresh();
}
function tambahStok(k) {
  const s = parseInt(prompt("Jumlah stok ditambah untuk " + menu[k].nama + ":"));
  if (isNaN(s) || s < 1) return alert("Jumlah tidak valid.");
  menu[k].stok += s; refresh();
}
function hapusMenu(k) {
  if (confirm("Hapus " + menu[k].nama + "?")) {
    delete menu[k];
    keranjang = keranjang.filter(it => it.kode !== k);
    refresh();
  }
}
function renderKelola() {
  $("tbKelola").innerHTML = Object.entries(menu).map(([k, d]) => `<tr><td>${k}</td><td>${esc(d.nama)}</td>
    <td>${rp(d.harga)}</td><td>${d.stok}</td><td>
    <button onclick="ubahHarga('${k}')">Harga</button>
    <button onclick="tambahStok('${k}')">+Stok</button>
    <button class="merah" onclick="hapusMenu('${k}')">Hapus</button></td></tr>`).join("");
}

// ===== RIWAYAT & LAPORAN =====
function renderRiwayat() {
  $("tbRiwayat").innerHTML = riwayat.length === 0
    ? "<tr><td colspan='4'>Belum ada transaksi.</td></tr>"
    : riwayat.map(t => `<tr><td>${t.id}</td><td>${t.waktu}</td><td>${esc(t.pelanggan)}</td><td>${rp(t.total)}</td></tr>`).join("");
}
function renderLaporan() {
  let html = "";
  if (riwayat.length === 0) html += "<p>Belum ada transaksi.</p>";
  else {
    let pendapatan = 0;
    const terjual = {};                       // objek: nama -> jumlah porsi
    for (const t of riwayat) {
      pendapatan += t.total;
      for (const [nama, jml] of t.item) terjual[nama] = (terjual[nama] || 0) + jml;
    }
    const urut = selectionSort(Object.entries(terjual), it => it[1], false);
    html += `<p>Jumlah transaksi: <b>${riwayat.length}</b><br>Total pendapatan: <b>${rp(pendapatan)}</b><br>
      Rata-rata/transaksi: <b>${rp(pendapatan / riwayat.length)}</b></p><h3>Menu terlaris</h3><ol>` +
      urut.map(([n, j]) => `<li>${esc(n)} - ${j} porsi</li>`).join("") + "</ol>";
  }
  const tipis = Object.entries(menu).filter(([, d]) => d.stok <= STOK_TIPIS);
  html += `<h3>Stok menipis (&le; ${STOK_TIPIS})</h3>` + (tipis.length === 0 ? "<p>Semua stok aman.</p>"
    : "<ul>" + tipis.map(([k, d]) => `<li class="tipis">${k} ${esc(d.nama)} (sisa ${d.stok})</li>`).join("") + "</ul>");
  $("isiLaporan").innerHTML = html;
}

// ===== PROGRAM UTAMA =====
function refresh() {
  renderMenu(); renderPilihan(); renderKeranjang();
  renderKelola(); renderRiwayat(); renderLaporan();
}
document.querySelectorAll("nav button").forEach(btn => {
  btn.onclick = () => {
    document.querySelectorAll("nav button, .tab").forEach(e => e.classList.remove("aktif"));
    btn.classList.add("aktif");
    $(btn.dataset.tab).classList.add("aktif");
  };
});
refresh();
