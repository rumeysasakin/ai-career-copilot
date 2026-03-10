from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


# ============================================================
# 1) LLM TANIMI
# ============================================================
# Ollama üzerinden yerel çalışan LLM modelimizi tanımlıyoruz.
# temperature=0.3 → daha tutarlı ve odaklı cevaplar için düşük tuttuk.
llm = ChatOllama(model="llama3", temperature=0.3)


# ============================================================
# 2) PROMPT ŞABLONLARI
# ============================================================

# --- Adım 1: CV ve iş ilanından beceri çıkarma + karşılaştırma ---
analiz_prompt = PromptTemplate(
    input_variables=["cv_metni", "ilan_metni"],
    template="""Sen bir kariyer danışmanısın. Sana bir CV metni ve bir iş ilanı metni vereceğim.

Görevlerin:
1. CV'deki becerileri ve deneyimleri çıkar
2. İş ilanındaki aranan becerileri ve gereksinimleri çıkar
3. Eşleşen becerileri bul (CV'de olan VE ilanda aranan)
4. Eksik becerileri bul (İlanda aranan AMA CV'de olmayan)
5. Kısa ve somut öneriler ver (eksikleri nasıl kapatabilir?)

Yanıtını aşağıdaki formatta ver:

## 📋 CV'deki Beceriler
- (madde madde listele)

## 🎯 İlanda Aranan Beceriler
- (madde madde listele)

## ✅ Eşleşen Beceriler
- (madde madde listele)

## ❌ Eksik Beceriler
- (madde madde listele)

## 💡 Öneriler
- (somut, kısa öneriler ver)

## 📊 Uyum Skoru
- Yüzde olarak tahmini bir uyum skoru ver ve kısaca açıkla.

---
CV METNİ:
{cv_metni}

---
İŞ İLANI METNİ:
{ilan_metni}
"""
)

# --- Chain oluşturma (LCEL - LangChain Expression Language) ---
# PromptTemplate → LLM → Yanıt
# Bu "pipe" (|) operatörü LangChain'in LCEL özelliğidir.
# Veriyi soldan sağa adım adım geçirir: önce prompt oluşturulur, sonra LLM'e gönderilir.
analiz_chain = analiz_prompt | llm


# ============================================================
# 3) YARDIMCI FONKSİYONLAR
# ============================================================

def dosyadan_oku(dosya_yolu: str) -> str:
    """Bir metin dosyasını okuyup içeriğini döndürür."""
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return f.read().strip()


def cv_analiz_et(cv_metni: str, ilan_metni: str) -> str:
    """CV ve iş ilanını karşılaştırıp analiz sonucunu döndürür."""
    sonuc = analiz_chain.invoke({
        "cv_metni": cv_metni,
        "ilan_metni": ilan_metni
    })
    return sonuc.content


# ============================================================
# 4) ANA PROGRAM
# ============================================================

def main():
    print("=" * 60)
    print("  🔍 CV - İş İlanı Eşleştirme Sistemi")
    print("  LangChain + Ollama ile Beceri Analizi")
    print("=" * 60)
    print()

    # Kullanıcıya seçenek sun: dosyadan mı okusun, elle mi girsin?
    print("CV metnini nasıl girmek istersiniz?")
    print("  1 - Dosyadan oku (ornek_cv.txt)")
    print("  2 - Elle yapıştır")
    secim_cv = input("Seçiminiz (1/2): ").strip()

    if secim_cv == "1":
        cv_metni = dosyadan_oku("ornek_cv.txt")
        print("✓ CV dosyadan okundu.\n")
    else:
        print("CV metnini yapıştırın (bitirmek için boş satırda 'SON' yazın):")
        satirlar = []
        while True:
            satir = input()
            if satir.strip().upper() == "SON":
                break
            satirlar.append(satir)
        cv_metni = "\n".join(satirlar)

    print("-" * 60)

    print("İş ilanı metnini nasıl girmek istersiniz?")
    print("  1 - Dosyadan oku (ornek_ilan.txt)")
    print("  2 - Elle yapıştır")
    secim_ilan = input("Seçiminiz (1/2): ").strip()

    if secim_ilan == "1":
        ilan_metni = dosyadan_oku("ornek_ilan.txt")
        print("✓ İş ilanı dosyadan okundu.\n")
    else:
        print("İş ilanı metnini yapıştırın (bitirmek için boş satırda 'SON' yazın):")
        satirlar = []
        while True:
            satir = input()
            if satir.strip().upper() == "SON":
                break
            satirlar.append(satir)
        ilan_metni = "\n".join(satirlar)

    print("\n" + "=" * 60)
    print("⏳ Analiz ediliyor... (Bu birkaç saniye sürebilir)")
    print("=" * 60 + "\n")

    # Chain'i çalıştır
    sonuc = cv_analiz_et(cv_metni, ilan_metni)
    print(sonuc)


if __name__ == "__main__":
    main()