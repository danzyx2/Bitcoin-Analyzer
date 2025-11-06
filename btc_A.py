import requests
import datetime
import sys 
import warnings # Digunakan untuk mengabaikan peringatan SSL
import math     # Digunakan untuk fungsi math.fabs (nilai absolut)

# --- 1. KONSTANTA WARNA ANSI ---
class Colors:
    """Kelas untuk memegang kode warna ANSI."""
    RESET = '\033[0m'
    HIJAU = '\033[92m'  # Hijau Terang (Sinyal Beli, Harga Naik)
    MERAH = '\033[91m'  # Merah Terang (Sinyal Jual, Harga Turun)
    KUNING = '\033[93m' # Kuning Terang 
    BIRU = '\033[94m'   # Biru Terang (Garis Batas)
    CYAN = '\033[96m'   # Cyan Teran (Sinyal Hold)
    BOLD = '\033[1m'    # Tebal
# --- AKHIR KONSTANTA WARNA ---

# --- 2. KONFIGURASI API DAN DATA ---
BASE_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "1h"      # Interval waktu: 1 jam
LIMIT = 500          # Jumlah bar data yang diambil (maksimal 1000)

# DAFTAR MARKET YANG AKAN DIANALISIS
MARKETS_TO_ANALYZE = [
    "BTCUSDT",
    # "ETHUSDT", 
]

# Daftar Opsi Sensitivitas MA (Diubah untuk fokus pada MACD/RSI)
SENSITIVITY_OPTIONS = {
    1: {"name": "MACD-RSI Standar", "macd_fast": 12, "macd_slow": 26, "macd_signal": 9, "rsi_len": 14},
    2: {"name": "MACD Cepat", "macd_fast": 8, "macd_slow": 17, "macd_signal": 9, "rsi_len": 9},
    3: {"name": "Input Manual", "macd_fast": 12, "macd_slow": 26, "macd_signal": 9, "rsi_len": 14},
}

# Periode default
DEFAULT_MACD_FAST = 12
DEFAULT_MACD_SLOW = 26
DEFAULT_MACD_SIGNAL = 9
DEFAULT_RSI_LEN = 14

# --- 3. FUNGSI PEMBANTU DASAR ---

def convert_time(timestamp_ms):
    """Mengubah timestamp milidetik ke string waktu YYYY-MM-DD HH:MM:SS."""
    return datetime.datetime.fromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')

def get_binance_data(symbol): 
    """Mengambil data klines dari API Binance."""
    params = {'symbol': symbol, 'interval': INTERVAL, 'limit': LIMIT}
    
    # Abaikan InsecureRequestWarning dari 'verify=False'
    warnings.filterwarnings("ignore") 
    
    try:
        print(f"\n--- Mengambil data {symbol} interval {INTERVAL}...")
        
        # Mengabaikan verifikasi SSL karena masalah jaringan/sertifikat lokal
        response = requests.get(BASE_URL, params=params, verify=False)
        response.raise_for_status() 
        data_klines = response.json()
        
        # Memformat data mentah
        processed_data = []
        for kline in data_klines:
            processed_data.append({
                'time': convert_time(kline[0]),
                'close': float(kline[4]),
                'macd_line': None,
                'macd_signal_line': None,
                'macd_hist': None,
                'rsi': None,
                'signal': 0
            })
        return processed_data
    except requests.exceptions.RequestException as e:
        print(f"❌ Error saat mengambil data dari API: {e}")
        return []

def get_user_sensitivity():
    """Menyajikan menu pilihan sensitivitas MACD/RSI kepada pengguna."""
    print("\n" + Colors.BOLD + "=======================================================")
    print("      PILIH TINGKAT SENSITIVITAS STRATEGI MACD-RSI")
    print("=======================================================" + Colors.RESET)
    print("Pilihan:")

    for key, val in SENSITIVITY_OPTIONS.items():
        if key != 3:
            print(f"  [{Colors.BOLD}{key}{Colors.RESET}] {val['name']} (MACD: {val['macd_fast']}/{val['macd_slow']}/{val['macd_signal']}, RSI: {val['rsi_len']})")
    
    print(f"  [{Colors.BOLD}3{Colors.RESET}] Input Periode Secara Manual (MACD/RSI)")
    print(f"  [{Colors.BOLD}Q{Colors.RESET}] Keluar Program")
    print("-------------------------------------------------------")

    while True:
        try:
            user_input = input("Masukkan Pilihan Anda (Angka/Q): ").strip().upper()

            if user_input == 'Q':
                print("\nProgram dihentikan oleh pengguna.")
                sys.exit(0)
            
            elif user_input.isdigit():
                choice_key = int(user_input)
                
                if choice_key in SENSITIVITY_OPTIONS:
                    choice = SENSITIVITY_OPTIONS[choice_key]
                    if choice_key == 3:
                        return get_manual_sensitivity_input() 
                        
                    print(f"✅ Memilih: {choice['name']}")
                    return choice['macd_fast'], choice['macd_slow'], choice['macd_signal'], choice['rsi_len']
                
                else:
                    print(f"⚠️ Pilihan '{user_input}' tidak valid. Silakan coba lagi.")
            
            else:
                print(f"⚠️ Pilihan '{user_input}' tidak valid. Silakan coba lagi.")

        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh pengguna.")
            sys.exit(0)

def get_manual_sensitivity_input():
    """Meminta input periode MACD dan RSI secara manual."""
    print("\n--- Mode Input Manual MACD/RSI ---")
    
    while True:
        try:
            # Input MACD
            fast_input = input(f"Masukkan Periode EMA MACD Cepat (Default: {DEFAULT_MACD_FAST}): ")
            macd_fast = int(fast_input) if fast_input else DEFAULT_MACD_FAST

            slow_input = input(f"Masukkan Periode EMA MACD Lambat (Default: {DEFAULT_MACD_SLOW}): ")
            macd_slow = int(slow_input) if slow_input else DEFAULT_MACD_SLOW
            
            signal_input = input(f"Masukkan Periode EMA MACD Sinyal (Default: {DEFAULT_MACD_SIGNAL}): ")
            macd_signal = int(signal_input) if signal_input else DEFAULT_MACD_SIGNAL
            
            # Input RSI
            rsi_input = input(f"Masukkan Periode RSI (Default: {DEFAULT_RSI_LEN}): ")
            rsi_len = int(rsi_input) if rsi_input else DEFAULT_RSI_LEN
            
            # Validasi
            if macd_fast <= 0 or macd_slow <= 0 or macd_signal <= 0 or rsi_len <= 0:
                print("⚠️ Error: Periode harus berupa bilangan bulat positif.")
                continue
            
            if macd_fast >= macd_slow:
                print("⚠️ Error: EMA Cepat harus lebih kecil dari EMA Lambat.")
                continue

            return macd_fast, macd_slow, macd_signal, rsi_len
            
        except ValueError:
            print("⚠️ Error: Input harus berupa angka/bilangan bulat.")
        except KeyboardInterrupt:
            raise 

# --- 4. FUNGSI PERHITUNGAN TEKNIKAL MANUAL ---

def calculate_ema(data, length, close_key='close', ema_key=None):
    """
    Menghitung Exponential Moving Average (EMA) secara manual.
    Diperbaiki agar dinamis menemukan titik awal data non-None.
    """
    if length <= 0 or not ema_key:
        return

    # 1. Tentukan titik awal (first_valid_index)
    first_valid_index = -1
    for i in range(len(data)):
        if data[i].get(close_key) is not None:
            first_valid_index = i
            break
            
    # Jika tidak ada data yang valid untuk dihitung, keluar
    if first_valid_index == -1:
        return

    # 2. Tentukan indeks baris di mana EMA pertama kali dihitung (initial_ema_index)
    # Kita butuh 'length' data points yang valid setelah first_valid_index
    initial_ema_index = first_valid_index + length - 1
    
    # Periksa apakah total data yang tersisa cukup untuk menghitung EMA awal
    if initial_ema_index >= len(data):
        return

    # 3. Hitung Multiplier (K)
    multiplier = 2 / (length + 1)
    
    # 4. Hitung SMA awal (hanya untuk mengisi nilai awal EMA)
    # Menjumlahkan data dari first_valid_index hingga initial_ema_index
    sma_sum = sum(data[i][close_key] for i in range(first_valid_index, initial_ema_index + 1))
    
    # Set nilai EMA pertama
    data[initial_ema_index][ema_key] = sma_sum / length

    # 5. Hitung EMA untuk data selanjutnya
    for i in range(initial_ema_index + 1, len(data)):
        current_close = data[i][close_key]
        previous_ema = data[i-1][ema_key]
        
        if current_close is None or previous_ema is None:
             continue
        
        current_ema = (current_close * multiplier) + (previous_ema * (1 - multiplier))
        data[i][ema_key] = current_ema


def calculate_rsi(data, length, close_key='close', rsi_key='rsi'):
    """Menghitung Relative Strength Index (RSI) secara manual."""
    if length <= 0:
        return

    # Inisialisasi kolom Gain, Loss, AG, AL
    for row in data:
        row['gain'] = 0.0
        row['loss'] = 0.0
        row['avg_gain'] = None
        row['avg_loss'] = None

    # 1. Hitung Gain dan Loss
    for i in range(1, len(data)):
        change = data[i][close_key] - data[i-1][close_key]
        data[i]['gain'] = max(0, change)
        data[i]['loss'] = max(0, -change)

    # 2. Hitung Average Gain (AG) dan Average Loss (AL) - Wilders Smoothing
    if len(data) > length:
        # Hitung AG/AL awal (SMA dari length pertama, dimulai dari index 1)
        initial_gain = sum(data[i]['gain'] for i in range(1, length + 1)) / length
        initial_loss = sum(data[i]['loss'] for i in range(1, length + 1)) / length
        
        # Set nilai awal untuk indeks 'length'
        data[length]['avg_gain'] = initial_gain
        data[length]['avg_loss'] = initial_loss
        
        # Hitung AG/AL selanjutnya
        for i in range(length + 1, len(data)):
            # Rumus Wilders Smoothing: New AG = ((Prev AG * (length - 1)) + Current Gain) / length
            prev_ag = data[i-1]['avg_gain']
            prev_al = data[i-1]['avg_loss']
            
            current_ag = (prev_ag * (length - 1) + data[i]['gain']) / length
            current_al = (prev_al * (length - 1) + data[i]['loss']) / length
            
            data[i]['avg_gain'] = current_ag
            data[i]['avg_loss'] = current_al

            # 3. Hitung Relative Strength (RS) dan RSI
            if current_al == 0:
                rs = 100 
            else:
                rs = current_ag / current_al
            
            data[i][rsi_key] = 100 - (100 / (1 + rs))

    # Bersihkan kolom bantu
    for row in data:
        if 'gain' in row: del row['gain']
        if 'loss' in row: del row['loss']
        if 'avg_gain' in row: del row['avg_gain']
        if 'avg_loss' in row: del row['avg_loss']

# --- 5. FUNGSI UTAMA ANALISIS DAN SINYAL ---

def analyze_and_generate_signal(data, MACD_FAST, MACD_SLOW, MACD_SIGNAL, RSI_LEN):
    """Menghitung EMA, MACD, RSI, dan menghasilkan sinyal trading (MACD Crossover + RSI Konfirmasi)."""
    
    data_length = len(data)
    
    # 1. Hitung EMA Fast (12)
    calculate_ema(data, MACD_FAST, ema_key='ema_fast')
    
    # 2. Hitung EMA Slow (26)
    calculate_ema(data, MACD_SLOW, ema_key='ema_slow')
    
    # 3. Hitung MACD Line (MACD Line = EMA Fast - EMA Slow)
    for i in range(data_length):
        if data[i].get('ema_fast') is not None and data[i].get('ema_slow') is not None:
            data[i]['macd_line'] = data[i]['ema_fast'] - data[i]['ema_slow']
        
    # 4. Hitung MACD Signal Line (EMA 9 dari MACD Line)
    calculate_ema(data, MACD_SIGNAL, close_key='macd_line', ema_key='macd_signal_line')
    
    # 5. Hitung MACD Histogram (Histogram = MACD Line - Signal Line)
    for i in range(data_length):
        if data[i].get('macd_line') is not None and data[i].get('macd_signal_line') is not None:
            data[i]['macd_hist'] = data[i]['macd_line'] - data[i]['macd_signal_line']
            
    # 6. Hitung RSI
    calculate_rsi(data, RSI_LEN, rsi_key='rsi')

    # 7. Generate Sinyal (MACD Crossover Dikonfirmasi oleh RSI)
    # Start index: Gunakan MAX periode untuk memastikan semua indikator terhitung
    max_period = MACD_SLOW + MACD_SIGNAL + 2 
    
    for i in range(max_period, data_length):
        
        current_macd = data[i].get('macd_line')
        current_signal = data[i].get('macd_signal_line')
        prev_macd = data[i-1].get('macd_line')
        prev_signal = data[i-1].get('macd_signal_line')
        current_rsi = data[i].get('rsi') # Ambil nilai RSI
        
        # Pastikan semua indikator sudah terhitung
        if (current_macd is not None and current_signal is not None and 
            prev_macd is not None and prev_signal is not None and 
            current_rsi is not None):
            
            # 1. Cek Sinyal Beli (MACD Crossover UP)
            if current_macd > current_signal and prev_macd <= prev_signal:
                
                # Konfirmasi RSI: Sinyal BUY hanya valid jika RSI < 70 (tidak Overbought)
                if current_rsi < 70:
                    data[i]['signal'] = 1  # BUY Dikonfirmasi
                else:
                    data[i]['signal'] = 0  # HOLD (Sinyal BUY ditolak karena RSI terlalu tinggi)
            
            # 2. Cek Sinyal Jual (MACD Crossover DOWN)
            elif current_macd < current_signal and prev_macd >= prev_signal:
                
                # Konfirmasi RSI: Sinyal SELL hanya valid jika RSI > 30 (tidak Oversold)
                if current_rsi > 30:
                    data[i]['signal'] = -1 # SELL Dikonfirmasi
                else:
                    data[i]['signal'] = 0 # HOLD (Sinyal SELL ditolak karena RSI terlalu rendah)
            
            else:
                data[i]['signal'] = 0 # HOLD (Tidak ada Crossover)
        
        else:
             data[i]['signal'] = 0 # HOLD (Data indikator belum lengkap)


    # Hapus data awal yang tidak memiliki semua indikator
    return data[max_period - 1:]

# --- 6. EKSEKUSI PROGRAM UTAMA (DENGAN PEWARNAAN) ---

if __name__ == "__main__":
    
    # 1. Mendapatkan konfigurasi indikator dari pengguna
    MACD_F, MACD_S, MACD_SIG, RSI_L = get_user_sensitivity()
    
    print("\n" + Colors.BOLD + "=======================================================")
    print(f"    MEMULAI ANALISIS UNTUK SEMUA MARKET (MACD: {MACD_F}/{MACD_S}/{MACD_SIG}, RSI: {RSI_L})")
    print("=======================================================" + Colors.RESET)
    
    # 2. Lakukan perulangan untuk setiap market yang ada
    for SELECTED_SYMBOL in MARKETS_TO_ANALYZE:

        raw_data = get_binance_data(SELECTED_SYMBOL)
        
        if raw_data:
            # Panggil fungsi analisis baru
            analyzed_data = analyze_and_generate_signal(raw_data, MACD_F, MACD_S, MACD_SIG, RSI_L)
            
            previous_close = None
            
            # C. Menampilkan hasil analisis
            print("\n" + Colors.BOLD + Colors.BIRU + "------------------------------------------------------------------------------------------------" + Colors.RESET)
            print(f"🔍 HASIL {SELECTED_SYMBOL} (MACD/RSI, {len(analyzed_data)} Baris Terakhir):") 
            print("------------------------------------------------------------------------------------------------" + Colors.RESET)
            
            # Header baru
            print(f"| {'Waktu':<19} | {'Close':<14} | {'MACD Hist.':<12} | {'RSI':<5} | {Colors.BOLD + 'Sinyal (MACD)':<13} |" + Colors.RESET)
            print(Colors.BIRU + "------------------------------------------------------------------------------------------------" + Colors.RESET)
            
            # Hanya menampilkan semua baris yang teranalisis
            for row in analyzed_data: 
                
                # 1. PEWARNAAN SINYAL
                signal_val = row['signal']
                if signal_val == 1:
                    signal_color = Colors.BOLD + Colors.HIJAU + "BUY"
                elif signal_val == -1:
                    signal_color = Colors.BOLD + Colors.MERAH + "SELL"
                else:
                    signal_color = Colors.CYAN + "HOLD"
                
                # 2. PEWARNAAN HARGA CLOSE
                current_close = row['close']
                close_color = ""
                
                if previous_close is not None:
                    if current_close > previous_close:
                        close_color = Colors.BOLD + Colors.HIJAU
                    elif current_close < previous_close:
                        close_color = Colors.BOLD + Colors.MERAH
                    else:
                        close_color = Colors.RESET
                
                previous_close = current_close

                # 3. PEWARNAAN MACD HISTOGRAM (Positif/Negatif)
                macd_hist_val = row['macd_hist'] if row['macd_hist'] is not None else 0.0
                if macd_hist_val > 0:
                    macd_hist_color = Colors.HIJAU
                elif macd_hist_val < 0:
                    macd_hist_color = Colors.MERAH
                else:
                    macd_hist_color = Colors.RESET

                # 4. PEWARNAAN RSI (Overbought/Oversold)
                rsi_val = row['rsi'] if row['rsi'] is not None else 0.0
                if rsi_val >= 70:
                    rsi_color = Colors.BOLD + Colors.MERAH
                elif rsi_val <= 30:
                    rsi_color = Colors.BOLD + Colors.HIJAU
                else:
                    rsi_color = Colors.RESET
                
                # Pembulatan dan Format Pencetakan
                print(f"| {row['time']:<19} | {close_color}{current_close:<14.1f}{Colors.RESET} | {macd_hist_color}{macd_hist_val:<12.3f}{Colors.RESET} | {rsi_color}{rsi_val:<5.0f}{Colors.RESET} | {signal_color:<13}{Colors.RESET} |")

            print(Colors.BIRU + "------------------------------------------------------------------------------------------------" + Colors.RESET)

        else:
            print(f"⚠️ Melewati {SELECTED_SYMBOL} karena gagal mengambil data.")


    print("\n" + Colors.BOLD + "✅ Proses Analisis Semua Market Selesai." + Colors.RESET)
    print("Sinyal Utama: MACD Crossover. RSI digunakan sebagai filter/konfirmasi (RSI < 70 untuk BUY, RSI > 30 untuk SELL).")
