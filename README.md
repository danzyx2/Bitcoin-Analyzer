# 🚀 Financial Analyzer CLI Suite (3 Modul) - Analisis Mendalam

Kumpulan skrip Python berbasis terminal ini menyediakan tiga modul analisis teknikal berbeda untuk pengambilan keputusan investasi/trading:

1. **Kripto MACD-RSI Analyzer** (Analisis Lanjut)
2. **Emas SMA Analyzer** (Analisis Investasi Jangka Menengah)
3. **Kripto SMA Crossover Analyzer** (Analisis Dasar)

Semua modul menggunakan data *real-time* dari API publik (Binance & CoinGecko).

---

## 📚 Pengertian Indikator Utama

### 1. Simple Moving Average (SMA)
SMA adalah indikator berbasis tren yang menghitung **harga rata-rata aset selama periode waktu tertentu** (misalnya, 20 hari, 50 jam). SMA berfungsi sebagai garis *support* dan *resistance* yang dinamis. Dalam strategi *Crossover*, sinyal muncul ketika:
* **BUY**: SMA Pendek (Sensitif) memotong di atas SMA Panjang (Lambat).
* **SELL**: SMA Pendek memotong di bawah SMA Panjang.

### 2. Relative Strength Index (RSI)
RSI adalah **indikator momentum** yang mengukur kecepatan dan perubahan pergerakan harga. Nilainya berkisar antara 0 hingga 100. Fungsi utamanya:
* **Area *Overbought*** (Jenuh Beli): RSI di atas 70. Menandakan aset mungkin akan segera turun.
* **Area *Oversold*** (Jenuh Jual): RSI di bawah 30. Menandakan aset mungkin akan segera naik.

### 3. Moving Average Convergence Divergence (MACD)
MACD adalah indikator momentum berbasis EMA (Exponential Moving Average) yang menunjukkan hubungan antara dua harga rata-rata aset. MACD terdiri dari tiga bagian:
* **MACD Line**: Perbedaan antara EMA Cepat dan EMA Lambat.
* **Signal Line**: EMA dari MACD Line itu sendiri.
* **MACD Histogram**: Perbedaan antara MACD Line dan Signal Line (menunjukkan momentum).
Sinyal **BUY/SELL** terjadi saat **MACD Line melintasi Signal Line**.

---

## 🪙 Modul 1: Kripto MACD-RSI Analyzer (`btc_A.py`)

Modul ini menggabungkan sinyal tren (MACD) dan sinyal momentum (RSI) untuk filter yang lebih ketat.

### 💡 Fitur-Fitur Utama
* **Sinyal Terfilter**: Sinyal BUY (MACD Crossover UP) **dibatalkan** jika RSI sudah berada di zona *Overbought* (>70). Sinyal SELL (MACD Crossover DOWN) **dibatalkan** jika RSI sudah berada di zona *Oversold* (<30).
* **Indikator Manual**: Semua indikator (EMA, MACD, RSI) dihitung secara manual dalam skrip, tidak bergantung pada *library* pihak ketiga seperti `pandas`.
* **Visualisasi Warna**: Menggunakan warna ANSI untuk menyorot Harga, MACD Histogram (positif/negatif), RSI (overbought/oversold), dan Sinyal BUY/SELL/HOLD.

### 🚀 Cara Menjalankan
```bash
python prediksi.py
```
---

## 🥇 Modul 2: Emas SMA Analyzer (API-Driven) (`prediksi-emas.py`)

Modul ini fokus pada keputusan investasi jangka panjang Emas Murni (IDR).

### 💡 Fitur-Fitur Utama
* **Data *Real-time***: Mengambil harga harian Gram Gold (GRAMG) terhadap IDR selama 365 hari terakhir dari API **CoinGecko**.
* **Strategi Investasi**: Menggunakan perbandingan Harga saat ini vs MA Jangka Panjang (default 60 Hari) untuk menentukan apakah harga di bawah (BUY) atau di atas (JUAL) nilai wajarnya.
* **Output Lokal**: Format harga otomatis ke konvensi Rupiah (`Rp 1.000.000`) agar mudah dibaca.

### 🚀 Cara Menjalankan
```bash
python prediksi-emas.py
```

---

## 📉 Modul 3: Kripto SMA Crossover Analyzer (prediksi.py)

Ini adalah modul kripto yang lebih sederhana, ideal untuk pemula, hanya menggunakan strategi SMA Crossover.

### 💡 Fitur-Fitur Utama
* **Simplicity**: Hanya membutuhkan input dua periode SMA (Pendek dan Panjang).
* **Pilihan Sensitivitas**: Menyediakan opsi prasetel (Scalping, Swing, Investasi) untuk periode SMA, memudahkan pengguna memilih gaya trading.
* **Multi-Market**: Dapat menganalisis daftar market yang dikonfigurasi dalam kode dalam satu sesi.

### 🚀 Cara Menjalankan
```bash
python prediksi.py
```
> **Catatan**: Pastikan skrip `prediksi.py` Anda menggunakan kode versi SMA Crossover untuk menjalankan modul ini.

---

## 🚨 Troubleshooting (Error Koneksi API)

Jika Anda menemui *error* saat skrip mencoba mengambil data dari API Binance atau CoinGecko, terutama *Timeout* atau *SSL Error*, ini mungkin disebabkan oleh pembatasan jaringan (termasuk firewall atau pembatasan geografis).

### Solusi: Gunakan VPN
Untuk mengatasi masalah ini, **disarankan untuk menjalankan skrip menggunakan layanan VPN**.
* **Tujuan VPN**: VPN dapat mengalihkan koneksi Anda melalui server di lokasi yang tidak memiliki pembatasan akses ke API publik Binance/CoinGecko.
* **Contoh Error**: Anda mungkin melihat `requests.exceptions.ConnectionError` atau `SSLError`.

---

## 🤝 Kontribusi

Ide, saran, atau laporan *bug* sangat kami hargai. Silakan buka **Issues** atau kirimkan **Pull Request**.
