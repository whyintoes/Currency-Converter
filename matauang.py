import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Konversi Mata Uang Sederhana",
    page_icon="💱",
    layout="centered"
)

# CSS kustom
st.markdown("""
<style>
    .result-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1.5rem;
        margin-top: 1rem;
        text-align: center;
    }
    .highlight {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
    }
    .footer {
        text-align: center;
        margin-top: 2rem;
        color: #7f8c8d;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Data mata uang terkini (Juli 2024)
CURRENCY_DATA = {
    "USD": {"Nama": "Dolar AS", "Rate": {"EUR": 0.93, "GBP": 0.79, "JPY": 161.5, "IDR": 16250, "SGD": 1.36}},
    "EUR": {"Nama": "Euro", "Rate": {"USD": 1.08, "IDR": 17500}},
    "GBP": {"Nama": "Pound Sterling", "Rate": {"USD": 1.27, "IDR": 20600}},
    "IDR": {"Nama": "Rupiah", "Rate": {"USD": 0.000062}},
    "JPY": {"Nama": "Yen Jepang", "Rate": {"USD": 0.0062, "IDR": 100.5}},
    "SGD": {"Nama": "Dolar Singapura", "Rate": {"USD": 0.74, "IDR": 11900}}
}

def convert_currency(amount, from_curr, to_curr):
    if from_curr == to_curr:
        return amount
    
    try:
        # Cek rate langsung
        if to_curr in CURRENCY_DATA[from_curr]["Rate"]:
            return amount * CURRENCY_DATA[from_curr]["Rate"][to_curr]
        
        # Konversi melalui USD jika tidak ada rate langsung
        if "USD" in CURRENCY_DATA[from_curr]["Rate"] and to_curr in CURRENCY_DATA["USD"]["Rate"]:
            usd_amount = amount * CURRENCY_DATA[from_curr]["Rate"]["USD"]
            return usd_amount * CURRENCY_DATA["USD"]["Rate"][to_curr]
        
        return None
    except KeyError:
        return None

# Tampilan aplikasi
st.title("💱 Konversi Mata Uang")

col1, col2 = st.columns(2)
with col1:
    amount = st.number_input("Jumlah", min_value=0.01, value=1.0, step=0.01)
with col2:
    from_currency = st.selectbox("Dari", list(CURRENCY_DATA.keys()), format_func=lambda x: f"{x} - {CURRENCY_DATA[x]['Nama']}")

to_currency = st.selectbox("Ke", list(CURRENCY_DATA.keys()), format_func=lambda x: f"{x} - {CURRENCY_DATA[x]['Nama']}")

if st.button("Konversi", type="primary"):
    result = convert_currency(amount, from_currency, to_currency)
    
    if result is not None:
        if to_currency == "IDR":
            result_str = f"Rp {result:,.0f}".replace(",", ".")
        else:
            result_str = f"{result:,.2f} {to_currency}"
        
        st.markdown(f"""
        <div class="result-box">
            <p>{amount} {from_currency} =</p>
            <p class="highlight">{result_str}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tampilkan kurs dasar
        rate = convert_currency(1, from_currency, to_currency)
        st.caption(f"Kurs 1 {from_currency} = {rate:,.4f} {to_currency}")
    else:
        st.error("Konversi tidak tersedia untuk pasangan mata uang ini")

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>Kurs terkini per Juli 2024</p>
    <p>Terakhir diperbarui: {datetime.now().strftime('%d %B %Y')}</p>
</div>
""", unsafe_allow_html=True)