# 📈 Binance SMA Crossover Analyzer CLI

Skrip Python ini berfungsi sebagai alat analisis teknikal berbasis terminal yang mengambil data *real-time* dari API Binance (spot market) dan menerapkan strategi *Simple Moving Average (SMA) Crossover* untuk menghasilkan sinyal *Buy* atau *Sell*.

Ideal digunakan untuk menganalisis cepat beberapa aset kripto tanpa perlu membuka platform trading.

---

## 💡 Fitur Utama

* **Multi-Market Analysis** 📊
    Menganalisis beberapa market (default: BTCUSDT, ETHUSDT, SOLUSDT, XRPUSDT, DOGEUSDT) secara otomatis dalam satu sesi.
* **SMA Crossover Strategy** 📉
    Menggunakan persilangan antara SMA Pendek dan SMA Panjang untuk menghasilkan sinyal trading (1 = BUY, -1 = SELL, 0 = HOLD).
* **Pilihan Sensitivitas Dinamis** ⚙️
    Menyediakan menu interaktif untuk memilih konfigurasi SMA yang sudah ditentukan (**Scalping, Swing Trading, Investasi**) atau menginput periode SMA secara manual.
* **Data *Real-time*** 🔗
    Mengambil 500 bar data historis terbaru (1 jam per baris) dari API publik Binance.
* **Output Terminal Jelas** 🎯
    Menampilkan hasil analisis (Waktu, Harga Tutup, Nilai SMA) dalam format tabel yang mudah dibaca untuk 12 bar data terakhir.

---

## 🛠️ Persiapan Awal

### 1. Kebutuhan Software
Skrip ini membutuhkan **Python 3** dan *library* **`requests`**.

```bash
# Perbarui Termux dan instal Python
pkg install python 

# Instal library requests untuk mengambil data API
pip install requests
```

### 2. Konfigurasi File
Anda dapat mengedit daftar **`MARKETS_TO_ANALYZE`** dalam file Python untuk mengubah aset kripto yang akan diuji.

```python
MARKETS_TO_ANALYZE = [
    "BTCUSDT",
    "ETHUSDT",
    # Tambahkan market lain di sini...
]
```

---

## 🚀 Cara Menggunakan

1.  **Jalankan Skrip dari Terminal:**
    ```bash
    python prediksi.py
    ```

2.  **Pilih Sensitivitas Strategi:**
    Anda akan disajikan menu untuk memilih periode SMA (misalnya 10/30) yang sesuai dengan gaya trading Anda (Sensitif, Jangka Panjang, atau Manual).

3.  **Lihat Hasil Analisis:**
    Skrip akan mengambil data, menghitung SMA, dan menampilkan tabel hasil untuk setiap market yang dikonfigurasi.

### Interpretasi Sinyal

| Sinyal | Keterangan |
| :----: | :---------- |
| **1** | **BUY** (SMA Pendek memotong ke atas SMA Panjang) |
| **-1** | **SELL** (SMA Pendek memotong ke bawah SMA Panjang) |
| **0** | **HOLD** (Tidak ada persilangan yang terjadi) |

### Contoh Opsi Sensitivitas
```
  [1] Sangat Sensitif (Scalping/Tren Cepat) (5/10 SMA)
  [2] Sensitif Sedang (Default) (10/30 SMA)
  [3] Jangka Menengah (Swing Trading) (20/50 SMA)
  [4] Jangka Panjang (Investasi) (50/100 SMA)
```

---

## 🤝 Kontribusi

Saran untuk menambahkan indikator teknikal lain (seperti RSI, MACD) atau *endpoint* API baru sangat diapresiasi! Silakan buka **Issues** atau kirimkan **Pull Request**.
