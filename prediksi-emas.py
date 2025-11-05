# =================================================================
# PREDIKSI JUAL/BELI EMAS MURNI PYTHON (INPUT DATA DARI API)
# Analisis Menggunakan Simple Moving Average (SMA) Bulanan/Harian
# =================================================================

import requests
import time
from datetime import datetime

# --- 1. KONFIGURASI ---
# API untuk mengambil harga historis Gram Gold (GRAMG) dalam IDR dari CoinGecko
# Kita akan ambil data harian untuk 365 hari terakhir (setara 1 tahun)
API_URL = "https://api.coingecko.com/api/v3/coins/gram-gold/market_chart"
CURRENCY = "idr"
DAYS = 365 
WINDOW = 60 # Periode Rata-Rata Bergerak (dalam Hari/Bulan, disesuaikan dengan data API)
# =================================================================

def format_rupiah(angka):
    """Memformat angka menjadi string Rupiah sederhana."""
    if angka is None:
        return "N/A"
    return "{:,.0f}".format(angka).replace(",", "_").replace(".", ",").replace("_", ".")

# --- FUNGSI BARU: MENGAMBIL DATA DARI API ---
def fetch_gold_data_from_api(url, currency, days):
    """Mengambil data historis Gram Gold (GRAMG) terhadap IDR dari API CoinGecko."""
    tanggal_list = []
    harga_list = []
    
    params = {
        'vs_currency': currency,
        'days': days,
        'interval': 'daily' # Mengambil data harian
    }
    
    print(f"Mengambil data {days} hari terakhir dari CoinGecko...")
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Akan memicu error jika status HTTP 4xx atau 5xx
        data = response.json()
        
        # Data harga ada di kolom 'prices'. Format: [timestamp, price]
        if 'prices' in data and data['prices']:
            for timestamp, price in data['prices']:
                # Konversi timestamp (milidetik) menjadi objek datetime
                dt_object = datetime.fromtimestamp(timestamp / 1000)
                
                tanggal_list.append(dt_object.strftime('%Y-%m-%d'))
                # Harga dibulatkan ke bilangan bulat terdekat (sesuai format IDR)
                harga_list.append(int(round(price))) 
                
            return tanggal_list, harga_list
        else:
            print("⚠️ Data 'prices' tidak ditemukan atau kosong dalam respons API.")
            return [], []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Gagal mengambil data dari API CoinGecko. ({e})")
        print("Pastikan koneksi internet Anda stabil.")
        return [], []

def hitung_moving_average(harga_list, window):
    """Menghitung Simple Moving Average (SMA)."""
    ma_list = [None] * len(harga_list)
    
    for i in range(len(harga_list)):
        if i >= window - 1:
            window_harga = harga_list[i - (window - 1) : i + 1]
            rata_rata = sum(window_harga) / window
            ma_list[i] = int(rata_rata)
            
    return ma_list

def analisis_sinyal(harga_terakhir, ma_terakhir, window):
    """Menentukan sinyal Jual, Beli, atau Tahan."""
    
    if ma_terakhir is None:
        return "TAHAN", f"PERHATIAN: Data kurang. Diperlukan minimal {window} data harian untuk menghitung Rata-Rata Bergerak."

    harga_format = format_rupiah(harga_terakhir)
    ma_format = format_rupiah(ma_terakhir)

    if harga_terakhir > ma_terakhir:
        sinyal = "**JUAL** 🔴"
        rekomendasi = f"Harga saat ini (Rp {harga_format}) lebih tinggi dari MA {window} hari (Rp {ma_format}). Sinyal untuk **mengambil untung/menjual**."
    elif harga_terakhir < ma_terakhir:
        sinyal = "**BELI** 🟢"
        rekomendasi = f"Harga saat ini (Rp {harga_format}) lebih rendah dari MA {window} hari (Rp {ma_format}). Sinyal untuk **mengumpulkan/membeli**."
    else:
        sinyal = "**TAHAN** 🟡"
        rekomendasi = f"Harga saat ini (Rp {harga_format}) sama dengan MA {window} hari. Disarankan untuk **menahan posisi**."
        
    return sinyal, rekomendasi

def tampilkan_tabel_detail(tanggal_list, harga_list, ma_list, window):
    """Mencetak 10 baris data historis dan MA terbaru dalam format tabel rapi."""
    
    # Hanya tampilkan 10 baris terakhir agar tidak terlalu panjang
    start_index = max(0, len(tanggal_list) - 10) 
    
    print(f"\nDETAIL 10 DATA HARGA TERAKHIR DAN RATA-RATA BERGERAK ({window} HARI):")
    
    # Header Tabel
    print("-" * 55)
    print("{:<10} {:<18} {}".format("Tanggal", "Harga (Rp)", f"MA {window} Hari (Rp)"))
    print("-" * 55)
    
    # Isi Tabel (10 baris terakhir)
    for t, h, m in zip(tanggal_list[start_index:], harga_list[start_index:], ma_list[start_index:]):
        h_display = format_rupiah(h)
        m_display = format_rupiah(m)
        print("{:<10} {:<18} {}".format(t, h_display, m_display))
    print("-" * 55)


# --- 6. EKSEKUSI PROGRAM UTAMA ---

if __name__ == "__main__":
    
    # 6.1. Memuat Data Otomatis dari API
    tanggal_list, harga_list = fetch_gold_data_from_api(API_URL, CURRENCY, DAYS)

    if not harga_list:
        print("Program dihentikan karena tidak ada data harga yang valid untuk dianalisis.")
    else:
        # 6.2. Perhitungan
        ma_list = hitung_moving_average(harga_list, WINDOW)

        # 6.3. Analisis Data Terakhir
        harga_terakhir = harga_list[-1]
        ma_terakhir = ma_list[-1]
        tanggal_terbaru = tanggal_list[-1]
        
        # Sesuaikan format window untuk output
        window_display = f"{WINDOW} Hari"
        
        sinyal, rekomendasi = analisis_sinyal(harga_terakhir, ma_terakhir, WINDOW)

        # 6.4. Output Utama
        print("\n" + "=" * 55)
        print(f"💰 HASIL ANALISIS JUAL/BELI GRAM GOLD (IDR) ({tanggal_terbaru})")
        print("=" * 55)
        print(f"Harga Emas Terakhir ({tanggal_terbaru}): Rp {format_rupiah(harga_terakhir)}")
        print(f"Rata-Rata Bergerak {window_display} (MA): Rp {format_rupiah(ma_terakhir)}")
        print("-" * 55)
        print(f"SINYAL PREDOMINAN: {sinyal}")
        print(f"REKOMENDASI: {rekomendasi}")
        print("=" * 55)

        # 6.5. Output Detail Tabel
        tampilkan_tabel_detail(tanggal_list, harga_list, ma_list, WINDOW)
