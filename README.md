# 💰 Financial Analyzer CLI Suite (Emas & Kripto)

Kumpulan skrip Python ini menyediakan alat analisis teknikal berbasis terminal untuk mengevaluasi sinyal Jual/Beli untuk dua aset utama: **Emas Murni (IDR)** dan beberapa pasangan **Kripto (Binance)** menggunakan strategi *Simple Moving Average (SMA) Crossover*.

---

## 🛠️ Persiapan Awal

### 1. Kebutuhan Software & Library
Skrip ini membutuhkan **Python 3** dan *library* **`requests`** untuk mengambil data *real-time*.

```bash
# Instal Python di Termux
pkg install python 

# Instal library requests
pip install requests
```

### 2. Simpan Kode
Pastikan kedua file (`prediksi-emas.py` dan `prediksi.py`) sudah tersimpan di direktori kerja Termux Anda.

---

## 🪙 Modul 1: Binance SMA Crossover Analyzer (`prediksi.py`)

Modul ini menganalisis beberapa pasangan *spot* kripto dari Binance menggunakan strategi SMA Crossover (Pendek vs Panjang).

### ⚙️ Cara Kerja
* **Data Source**: API Publik Binance (`/api/v3/klines`) dengan interval **1 jam**.
* **Strategi**: Menganalisis persilangan antara SMA Pendek dan SMA Panjang (periode ditentukan pengguna).
* **Daftar Market**: Secara *default* menguji BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT (dapat dikonfigurasi dalam kode).
* **Sinyal**: 1 = Beli (BUY), -1 = Jual (SELL), 0 = Tahan (HOLD).

### 🚀 Cara Menjalankan
1.  Jalankan skrip:
    ```bash
    python prediksi.py
    ```
2.  Pilih konfigurasi sensitivitas SMA dari menu yang tersedia (Scalping, Swing, atau Manual).
3.  Hasil akan ditampilkan per market dalam format tabel yang menunjukkan 12 bar data historis terakhir.

### Contoh Opsi Sensitivitas
```
  [1] Sangat Sensitif (5/10 SMA) 
  [3] Jangka Menengah (20/50 SMA) 
```

---

## 🥇 Modul 2: Emas SMA Analyzer (`prediksi-emas.py`)

Modul ini menganalisis harga Emas Murni dalam Rupiah (IDR) untuk keputusan investasi jangka menengah/panjang.

### ⚙️ Cara Kerja
* **Data Source**: API CoinGecko (Harga Gram Gold/GRAMG vs IDR) untuk **365 hari terakhir**.
* **Strategi**: Membandingkan **Harga Terakhir** dengan **Rata-Rata Bergerak (MA)** dari periode `WINDOW` (default: 60 hari).
* **Sinyal**: Dihasilkan berdasarkan Harga vs MA (JUAL jika Harga > MA; BELI jika Harga < MA).
* **Output**: Menggunakan fungsi format Rupiah (`format_rupiah`) untuk tampilan yang rapi.

### 🚀 Cara Menjalankan
1.  **Konfigurasi**: Anda dapat mengubah periode `WINDOW` (default 60 hari) di awal kode `prediksi-emas.py`.
2.  Jalankan skrip:
    ```bash
    python prediksi-emas.py
    ```
3.  Skrip akan mengambil data, menghitung MA, dan menampilkan sinyal dominan (JUAL/BELI) untuk harga emas terakhir, diikuti oleh detail historis 10 hari terakhir.

---

## ⚠️ Disklaimer

Analisis ini murni berdasarkan indikator teknikal Simple Moving Average dan tidak boleh dianggap sebagai saran investasi keuangan yang mengikat. Selalu lakukan riset Anda sendiri sebelum membuat keputusan trading.

---
## 🤝 Kontribusi

Saran atau ide untuk modul analisis tambahan, perbaikan API, atau penambahan indikator teknikal sangat diapresiasi! Silakan buka **Issues** atau kirimkan **Pull Request**.
