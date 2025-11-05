import requests
import datetime
import sys 

# --- 1. Konfigurasi API dan Data ---
BASE_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "1h"      # Interval waktu: 1 jam
LIMIT = 500          # Jumlah bar data yang diambil (maksimal 1000)

# DAFTAR MARKET YANG AKAN DIANALISIS (Anda bisa menambah/mengurangi di sini)
MARKETS_TO_ANALYZE = [
    "BTCUSDT",
    "ETHUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "DOGEUSDT"
]

# Konfigurasi SMA akan diisi berdasarkan pilihan pengguna
# Daftar Opsi Sensitivitas
SENSITIVITY_OPTIONS = {
    1: {"name": "Sangat Sensitif (Scalping/Tren Cepat)", "pendek": 5, "panjang": 10},
    2: {"name": "Sensitif Sedang (Default)", "pendek": 10, "panjang": 30},
    3: {"name": "Jangka Menengah (Swing Trading)", "pendek": 20, "panjang": 50},
    4: {"name": "Jangka Panjang (Investasi)", "pendek": 50, "panjang": 100},
}

# --- 2. Fungsi Pembantu ---

def convert_time(timestamp_ms):
    """Mengubah timestamp milidetik ke string waktu YYYY-MM-DD HH:MM:SS."""
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def get_binance_data(symbol): # Menerima symbol sebagai argumen
    """Mengambil data klines dari API Binance dan mengembalikan daftar data yang diproses."""
    params = {'symbol': symbol, 'interval': INTERVAL, 'limit': LIMIT}
    
    try:
        print(f"\n--- Mengambil data {symbol} interval {INTERVAL}...")
        
        # Mengabaikan error SSL karena masalah jaringan/sertifikat lokal
        response = requests.get(BASE_URL, params=params, verify=False)
        
        response.raise_for_status() 
        data_klines = response.json()
        
        # Memformat data mentah menjadi dictionary (kamus)
        processed_data = []
        for kline in data_klines:
            processed_data.append({
                'time': convert_time(kline[0]),
                'close': float(kline[4]),
                'sma_pendek': None,
                'sma_panjang': None,
                'signal': 0
            })
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil data dari API: {e}")
        return []

# --- FUNGSI MENDAPATKAN PILIHAN SENSITIVITAS (Tidak Berubah) ---

def get_user_sensitivity():
    """Menyajikan menu pilihan sensitivitas SMA kepada pengguna."""
    print("\n=======================================================")
    print("      PILIH TINGKAT SENSITIVITAS STRATEGI SMA")
    print("=======================================================")
    print("Pilihan:")

    for key, val in SENSITIVITY_OPTIONS.items():
        print(f"  [{key}] {val['name']} ({val['pendek']}/{val['panjang']} SMA)")
    
    # Menambahkan opsi untuk input manual jika pengguna tetap menginginkannya
    print(f"  [M] Input Periode SMA Secara Manual")
    print("  [Q] Keluar Program")
    print("-------------------------------------------------------")

    while True:
        try:
            user_input = input("Masukkan Pilihan Anda (Angka/M/Q): ").strip().upper()

            if user_input == 'Q':
                print("\nProgram dihentikan oleh pengguna.")
                sys.exit(0)
            
            # Opsi Input Manual
            elif user_input == 'M':
                return get_manual_sensitivity_input() # Panggil fungsi input manual
            
            # Opsi Pilihan Menu (Angka)
            elif user_input.isdigit() and int(user_input) in SENSITIVITY_OPTIONS:
                choice = SENSITIVITY_OPTIONS[int(user_input)]
                print(f"✅ Memilih: {choice['name']}")
                return choice['pendek'], choice['panjang']
                
            else:
                print(f"⚠️ Pilihan '{user_input}' tidak valid. Silakan coba lagi.")

        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh pengguna.")
            sys.exit(0)

def get_manual_sensitivity_input():
    """Meminta input periode SMA Pendek dan SMA Panjang secara manual."""
    print("\n--- Mode Input Manual SMA ---")
    
    # Nilai Default Manual
    default_pendek = 10
    default_panjang = 30
    
    while True:
        try:
            # Meminta SMA Pendek
            pendek_input = input(f"Masukkan Periode SMA Pendek (Default: {default_pendek}): ")
            sma_pendek = int(pendek_input) if pendek_input else default_pendek

            # Meminta SMA Panjang
            panjang_input = input(f"Masukkan Periode SMA Panjang (Default: {default_panjang}): ")
            sma_panjang = int(panjang_input) if panjang_input else default_panjang
            
            # Validasi Input
            if sma_pendek <= 0 or sma_panjang <= 0:
                print("⚠️ Error: Periode SMA harus berupa bilangan bulat positif.")
                continue
            
            if sma_pendek >= sma_panjang:
                print("⚠️ Error: SMA Pendek harus lebih kecil dari SMA Panjang.")
                continue

            return sma_pendek, sma_panjang
            
        except ValueError:
            print("⚠️ Error: Input harus berupa angka/bilangan bulat.")
        except KeyboardInterrupt:
            raise # Biarkan KeyboardInterrupt diteruskan

# --- 3. Fungsi Utama Analisis (Tidak Berubah) ---

def analyze_and_generate_signal(data, SMA_PENDEK, SMA_PANJANG):
    """Menghitung SMA dan menghasilkan sinyal trading."""
    
    # 3.1. Hitung SMA secara manual
    for i in range(len(data)):
        # Hitung SMA Pendek
        if i >= SMA_PENDEK - 1:
            window_pendek = [data[j]['close'] for j in range(i - SMA_PENDEK + 1, i + 1)]
            data[i]['sma_pendek'] = sum(window_pendek) / SMA_PENDEK

        # Hitung SMA Panjang
        if i >= SMA_PANJANG - 1:
            window_panjang = [data[j]['close'] for j in range(i - SMA_PANJANG + 1, i + 1)]
            data[i]['sma_panjang'] = sum(window_panjang) / SMA_PANJANG

    # 3.2. Generate Sinyal (SMA Crossover)
    for i in range(SMA_PANJANG, len(data)):
        current_pendek = data[i]['sma_pendek']
        current_panjang = data[i]['sma_panjang']
        
        prev_pendek = data[i-1]['sma_pendek']
        prev_panjang = data[i-1]['sma_panjang']
        
        # Sinyal Beli (1): SMA Pendek memotong ke atas SMA Panjang
        if current_pendek > current_panjang and prev_pendek <= prev_panjang:
            data[i]['signal'] = 1  # BUY
        
        # Sinyal Jual (-1): SMA Pendek memotong ke bawah SMA Panjang
        elif current_pendek < current_panjang and prev_pendek >= prev_panjang:
            data[i]['signal'] = -1 # SELL
        
        else:
            data[i]['signal'] = 0 # HOLD

    # Hapus data awal yang tidak memiliki SMA
    return data[SMA_PANJANG - 1:]

# --- 4. Eksekusi Program (MODIFIKASI UTAMA) ---

if __name__ == "__main__":
    
    # 1. Mendapatkan konfigurasi SMA dari pengguna melalui menu (Dipilih sekali)
    SMA_P, SMA_PJ = get_user_sensitivity()
    
    print("\n=======================================================")
    print(f"    MEMULAI ANALISIS UNTUK SEMUA MARKET ({SMA_P}/{SMA_PJ} SMA)")
    print("=======================================================")
    
    # 2. Lakukan perulangan untuk setiap market yang ada
    for SELECTED_SYMBOL in MARKETS_TO_ANALYZE:

        # A. Ambil data untuk market saat ini
        raw_data = get_binance_data(SELECTED_SYMBOL)
        
        if raw_data:
            # B. Analisis data menggunakan konfigurasi pengguna
            analyzed_data = analyze_and_generate_signal(raw_data, SMA_P, SMA_PJ)
            
            # C. Menampilkan hasil analisis (5 baris terakhir)
            print("\n---------------------------------------------------------------")
            print(f"🔍 HASIL {SELECTED_SYMBOL} ({SMA_P}/{SMA_PJ} SMA, 5 Baris Terakhir):") 
            print("---------------------------------------------------------------")
            
            print(f"| {'Waktu':<19} | {'Close':<8} | {'SMA P.':<8} | {'SMA Pj.':<8} | {'Sinyal':<6} |")
            print("---------------------------------------------------------------")
            
            # Menampilkan data 5 baris terakhir (ubah [-5:] jika ingin lebih banyak)
            for row in analyzed_data[-12:]:
                sma_pendek_val = row['sma_pendek'] if row['sma_pendek'] is not None else 0.0
                sma_panjang_val = row['sma_panjang'] if row['sma_panjang'] is not None else 0.0
                
                # Pembulatan ke 1 angka desimal (1f) dan lebar 8
                print(f"| {row['time']:<19} | {row['close']:<8.1f} | {sma_pendek_val:<8.1f} | {sma_panjang_val:<8.1f} | {row['signal']:<6} |")

            print("---------------------------------------------------------------")

        else:
            print(f"⚠️ Melewati {SELECTED_SYMBOL} karena gagal mengambil data.")


    print("\n✅ Proses Analisis Semua Market Selesai.")
    print("Keterangan Sinyal: 1 = Beli (BUY), -1 = Jual (SELL), 0 = Tahan (HOLD)")
