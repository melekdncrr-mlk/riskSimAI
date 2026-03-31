import streamlit as st
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(
    page_title="RiskSim AI",
    page_icon="📈",
    layout="wide"
)

# --- MODERN UI CSS ---
st.markdown("""
<style>
/* Gradient Buton */
div.stButton > button {
    background: linear-gradient(90deg, #1E88E5 0%, #00E676 100%);
    color: white !important;
    border: none;
    padding: 14px 28px;
    font-size: 18px;
    font-weight: 700;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #00E676 0%, #1E88E5 100%);
    box-shadow: 0 6px 20px rgba(0,0,0,0.5);
    transform: translateY(-2px);
}
/* Metrik Değerleri (Kartlar) */
div[data-testid="stMetricValue"] {
    font-size: 28px;
    color: #00E676;
    font-weight: 700;
}
div[data-testid="stMetricLabel"] {
    font-size: 16px;
    color: #B0BEC5;
    font-weight: 500;
}
/* Başlık */
h1 {
    font-weight: 800 !important;
    background: -webkit-linear-gradient(45deg, #1E88E5, #00E676);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

def run_monte_carlo(initial_investment, duration_years, stock_pct, bond_pct, crypto_pct, risk_tolerance):
    """
    Geometrik Brownian Hareketi (GBM) ile Monte Carlo Simülasyonu çalıştırır.
    """
    # 1. Beklenen Getiri (mu) ve Volatilite (sigma) Varsayımları (Yıllık)
    assets = {
        'Stock': {'mu': 0.12, 'sigma': 0.20},
        'Bond': {'mu': 0.06, 'sigma': 0.05},
        'Crypto': {'mu': 0.25, 'sigma': 0.60}
    }
    
    # Ağırlıklar
    w_stock = stock_pct / 100.0
    w_bond = bond_pct / 100.0
    w_crypto = crypto_pct / 100.0
    
    # Portföy Beklenen Getirisi (Ağırlıklı Ortalama)
    mu_port = (w_stock * assets['Stock']['mu'] + 
               w_bond * assets['Bond']['mu'] + 
               w_crypto * assets['Crypto']['mu'])
    
    # Portföy Volatilitesi 
    var_port = ((w_stock * assets['Stock']['sigma'])**2 + 
                (w_bond * assets['Bond']['sigma'])**2 + 
                (w_crypto * assets['Crypto']['sigma'])**2)
    sigma_port = np.sqrt(var_port)
    
    # 2. Risk Toleransına Göre Ayarlama Modeli
    if risk_tolerance == "Düşük (Low)":
        mu_port *= 0.90
        sigma_port *= 0.80 
    elif risk_tolerance == "Yüksek (High)":
        mu_port *= 1.15
        sigma_port *= 1.30 

    # 3. Monte Carlo Simülasyonu Başlangıcı
    n_simulations = 10000
    dt = 1 # 1 Yıllık adımlar
    
    paths = np.zeros((duration_years + 1, n_simulations))
    paths[0] = initial_investment
    
    # GBM Hesaplaması
    for t in range(1, duration_years + 1):
        Z = np.random.standard_normal(n_simulations)
        drift = (mu_port - (sigma_port**2) / 2) * dt
        shock = sigma_port * np.sqrt(dt) * Z
        
        growth = np.exp(drift + shock)
        paths[t] = paths[t-1] * growth
        
    final_wealths = paths[-1]
    
    return paths, final_wealths, mu_port, sigma_port

def main():
    st.title("RiskSim AI 📈")
    
    # Sidebar: Kullanıcı Formu
    st.sidebar.header("Kullanıcı Parametreleri")
    
    age = st.sidebar.number_input("Yaşınız", min_value=18, max_value=100, value=25, step=1)
    
    risk_tolerance = st.sidebar.selectbox(
        "Risk Toleransı", 
        ["Düşük (Low)", "Orta (Medium)", "Yüksek (High)"], 
        index=1
    )
    
    initial_investment = st.sidebar.number_input(
        "Başlangıç Yatırım Miktarı (TL)", 
        min_value=1000, 
        max_value=10000000, 
        value=50000, 
        step=5000
    )
    
    investment_duration_years = st.sidebar.slider(
        "Yatırım Süresi (Yıl)", 
        min_value=1, 
        max_value=40, 
        value=5, 
        step=1
    )
    
    # Portföy Dağılımı
    st.sidebar.header("Portföy Dağılımı (%)")
    
    stock_pct = st.sidebar.number_input("Hisse Senedi (%)", min_value=0, max_value=100, value=60)
    bond_pct = st.sidebar.number_input("Tahvil (%)", min_value=0, max_value=100, value=30)
    crypto_pct = st.sidebar.number_input("Kripto Para (%)", min_value=0, max_value=100, value=10)
    
    total_pct = stock_pct + bond_pct + crypto_pct
    
    if total_pct != 100:
        st.sidebar.error(f"⚠️ Portföy toplamı tam %100 olmalıdır! (Şu an: %{total_pct})")
        st.stop()
    else:
        st.sidebar.success("Portföy geçerli.")

    # Simülasyon Butonu
    st.sidebar.markdown("---")
    simulation_button = st.sidebar.button("Simülasyonu Başlat 🚀", use_container_width=True)

    if simulation_button:
        with st.spinner("Simülasyon çalıştırılıyor (10.000 iterasyon)..."):
            paths, final_wealths, mu_port, sigma_port = run_monte_carlo(
                initial_investment, investment_duration_years, stock_pct, bond_pct, crypto_pct, risk_tolerance
            )
            
            avg_wealth = np.mean(final_wealths)
            p5 = np.percentile(final_wealths, 5)
            p10 = np.percentile(final_wealths, 10)
            p50 = np.percentile(final_wealths, 50)
            p90 = np.percentile(final_wealths, 90)
            
            var_95 = max(0, initial_investment - p5)
            loss_probability = np.mean(final_wealths < initial_investment) * 100
            
            with st.container():
                st.subheader("📊 Simülasyon Sonuçları")
                
                st.info(f'''
                💡 **Yatırım Özeti ({investment_duration_years} Yıllık Değerlendirme):**
                - Bu yatırımla {investment_duration_years} yılın sonunda paranızın başlangıç değerinin ({(initial_investment):,.0f} ₺) altına düşme (zarar etme) olasılığı yaklaşık **%{loss_probability:.1f}**'dir.
                - Ortalama beklenen nihai servetiniz **{avg_wealth:,.0f} ₺** seviyesindedir.
                - Riske Maruz Değer (VaR %95): En kötü %5'lik senaryoda yaşayabileceğiniz potansiyel kayıp yaklaşık **{var_95:,.0f} ₺**'dir.
                - Portföyünüzün yıllık beklenen getirisi **%{mu_port*100:.1f}**, volatilitesi (risk) ise **%{sigma_port*100:.1f}** olarak hesaplanmıştır.
                ''')
                
                st.markdown("#### Temel İstatistiksel Değerler")
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Ortalama Final Servet", f"{avg_wealth:,.0f} ₺")
                col2.metric("Kötü Senaryo (%10)", f"{p10:,.0f} ₺")
                col3.metric("Medyan Senaryo (%50)", f"{p50:,.0f} ₺")
                col4.metric("İyi Senaryo (%90)", f"{p90:,.0f} ₺")
                
                st.markdown("---")
                
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(
                    x=final_wealths,
                    nbinsx=100,
                    name='Frekans',
                    marker_color='#1E88E5',
                    opacity=0.85
                ))
                
                fig_hist.add_vline(x=initial_investment, line_dash="dash", line_color="#FF5252", 
                                   annotation_text="Başlangıç", annotation_position="top left")
                fig_hist.add_vline(x=p50, line_dash="dash", line_color="#00E676", 
                                   annotation_text="Medyan", annotation_position="top right")
                
                fig_hist.update_layout(
                    template="plotly_dark",
                    title="Nihai Servet Dağılımı (Histogram)",
                    xaxis_title="Final Servet (TL)",
                    yaxis_title="Frekans",
                    bargap=0.05,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    title_font=dict(size=20, color="#FAFAFA"),
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                
                st.plotly_chart(fig_hist, use_container_width=True)
                
                st.markdown("---")
                
                sampled_paths = paths[:, :100]
                df_paths = pd.DataFrame(sampled_paths, index=range(0, investment_duration_years + 1))
                
                fig_paths = px.line(
                    df_paths, 
                    labels={'index': 'Yıl', 'value': 'Servet (TL)', 'variable': 'Senaryo'}
                )
                fig_paths.update_traces(line=dict(color="#1E88E5", width=1), opacity=0.15)
                fig_paths.update_layout(
                    template="plotly_dark",
                    title="Örnek 100 Gelecek Senaryosu",
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    title_font=dict(size=20, color="#FAFAFA"),
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                fig_paths.add_hline(y=initial_investment, line_dash="dash", line_color="#FF5252", annotation_text="Başlangıç Sınırı")
                
                st.plotly_chart(fig_paths, use_container_width=True)

if __name__ == "__main__":
    main()
