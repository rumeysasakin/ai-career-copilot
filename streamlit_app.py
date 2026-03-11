"""AI Kariyer Asistanı — Streamlit Web Arayüzü."""

import streamlit as st

st.set_page_config(
    page_title="AI Kariyer Asistanı",
    page_icon="🔍",
    layout="wide",
)

# --- Başlık ---
st.title("🔍 AI Kariyer Asistanı")
st.caption(
    "CV'nizi bir iş ilanıyla karşılaştırın — eşleşen becerileri, eksikleri "
    "ve somut kariyer önerilerini görün. Tamamen yerel çalışır (Ollama + LangChain)."
)
st.divider()


# --- Örnek verileri yükle ---
@st.cache_data
def _load_sample(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


ORNEK_CV = _load_sample("ornek_cv.txt")
ORNEK_ILAN = _load_sample("ornek_ilan.txt")


# --- Girdiler ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 CV Metni")
    cv_metni = st.text_area(
        "CV metnini buraya yapıştırın:",
        value=ORNEK_CV,
        height=300,
        key="cv_input",
    )

with col2:
    st.subheader("📋 İş İlanı Metni")
    ilan_metni = st.text_area(
        "İş ilanı metnini buraya yapıştırın:",
        value=ORNEK_ILAN,
        height=300,
        key="ilan_input",
    )


# --- Mod seçimi ve buton ---
st.divider()
col_mod, col_btn = st.columns([3, 1])

with col_mod:
    mod = st.radio(
        "Analiz Modu",
        options=["agent", "chain"],
        format_func=lambda x: (
            "🤖 Agent — Detaylı Hibrit Analiz (deterministik + LLM)"
            if x == "agent"
            else "⚡ Chain — Hızlı LLM Analizi (tek çağrı)"
        ),
        horizontal=True,
    )

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    analiz_btn = st.button("🔍 Analiz Et", type="primary", use_container_width=True)


# --- Analiz ---
if analiz_btn:
    if not cv_metni.strip():
        st.error("⚠️ CV metni boş olamaz.")
    elif not ilan_metni.strip():
        st.error("⚠️ İş ilanı metni boş olamaz.")
    else:
        try:
            if mod == "agent":
                from core.agent import agent_analiz_et

                with st.status("🔧 Agent pipeline çalışıyor...", expanded=True) as status:
                    def streamlit_log(msg: str):
                        st.text(msg)

                    sonuc = agent_analiz_et(cv_metni, ilan_metni, log_fn=streamlit_log)
                    status.update(label="✅ Analiz tamamlandı!", state="complete")

                st.divider()
                st.subheader("📊 Analiz Sonucu")

                # Metrikler
                m1, m2, m3 = st.columns(3)
                skor_pct = round((sonuc.eslesen_sayi / sonuc.toplam) * 100) if sonuc.toplam > 0 else 0
                eksik_count = len([e for e in sonuc.eksik.split(",") if e.strip() and e.strip() != "Yok"])

                m1.metric("Eşleşen Beceri", f"{sonuc.eslesen_sayi} / {sonuc.toplam}")
                m2.metric("Uyum Skoru", f"%{skor_pct}")
                m3.metric("Eksik Beceri", str(eksik_count))

                # Sekmeler
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["✅ Eşleşen", "❌ Eksik", "🛠️ Öneriler", "💡 Değerlendirme"]
                )

                with tab1:
                    st.markdown(f"**CV Becerileri:** {sonuc.cv_beceriler}")
                    st.markdown(f"**İlan Becerileri:** {sonuc.ilan_beceriler}")
                    st.divider()
                    if sonuc.eslesen and sonuc.eslesen != "Yok":
                        for b in sonuc.eslesen.split(","):
                            st.markdown(f"- ✅ {b.strip()}")
                    else:
                        st.info("Eşleşen beceri bulunamadı.")

                with tab2:
                    if sonuc.eksik and sonuc.eksik != "Yok":
                        for b in sonuc.eksik.split(","):
                            st.markdown(f"- ❌ {b.strip()}")
                    else:
                        st.success("Tüm beceriler mevcut!")

                with tab3:
                    st.markdown(sonuc.oneriler)

                with tab4:
                    st.markdown(sonuc.degerlendirme)

            else:
                from core.chain import chain_analiz_et

                with st.spinner("⏳ Chain analizi yapılıyor..."):
                    rapor = chain_analiz_et(cv_metni, ilan_metni)

                st.divider()
                st.subheader("📊 Analiz Sonucu")
                st.markdown(rapor)

        except Exception as e:
            error_msg = str(e)
            st.error(f"❌ Analiz sırasında hata oluştu: {error_msg}")
            st.info(
                "💡 **Kontrol edin:**\n\n"
                "1. Ollama çalışıyor mu? → `ollama serve`\n"
                "2. Modeller indirildi mi? → `ollama pull llama3` ve `ollama pull llama3.1`\n"
                "3. Ollama varsayılan portta mı? → `http://localhost:11434`"
            )


# --- Footer ---
st.divider()
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.85em;'>"
    "AI Kariyer Asistanı · LangChain + Ollama · "
    "<a href='https://github.com/rumeysasakin/ai-career-copilot'>GitHub</a>"
    "</div>",
    unsafe_allow_html=True,
)
