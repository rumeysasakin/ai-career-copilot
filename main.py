from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama


# ============================================================
# 1) LLM TANIMI
# ============================================================
llm = ChatOllama(model="llama3", temperature=0.3)


# ============================================================
# 2) AŞAMA 1 — CHAIN (Basit LLM Workflow)
# ============================================================
# PromptTemplate → LLM → Yanıt (sabit akış, agent yok)

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

analiz_chain = analiz_prompt | llm


# ============================================================
# 3) YARDIMCI FONKSİYONLAR
# ============================================================

def dosyadan_oku(dosya_yolu: str) -> str:
    """Bir metin dosyasını okuyup içeriğini döndürür."""
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return f.read().strip()


def chain_analiz_et(cv_metni: str, ilan_metni: str) -> str:
    """Aşama 1: Basit chain ile analiz."""
    sonuc = analiz_chain.invoke({
        "cv_metni": cv_metni,
        "ilan_metni": ilan_metni
    })
    return sonuc.content


def metin_al(dosya_adi: str, tur: str) -> str:
    """Kullanıcıdan dosya veya elle metin girişi alır."""
    print(f"{tur} metnini nasıl girmek istersiniz?")
    print(f"  1 - Dosyadan oku ({dosya_adi})")
    print(f"  2 - Elle yapıştır")
    secim = input("Seçiminiz (1/2): ").strip()

    if secim == "1":
        metin = dosyadan_oku(dosya_adi)
        print(f"✓ {tur} dosyadan okundu.\n")
        return metin
    else:
        print(f"{tur} metnini yapıştırın (bitirmek için boş satırda 'SON' yazın):")
        satirlar = []
        while True:
            satir = input()
            if satir.strip().upper() == "SON":
                break
            satirlar.append(satir)
        return "\n".join(satirlar)


# ============================================================
# 4) ANA PROGRAM
# ============================================================

def main():
    print("=" * 60)
    print("  🔍 AI Kariyer Asistanı — CV & İş İlanı Eşleştirme")
    print("  LangChain + Ollama ile Beceri Analizi")
    print("=" * 60)
    print()

    # --- Mod seçimi ---
    print("Hangi modu kullanmak istersiniz?")
    print("  1 - Basit Analiz (Chain — Aşama 1)")
    print("  2 - Akıllı Analiz (Agent — Aşama 2)")
    print()
    print("  Chain: Sabit akışta tek seferde analiz yapar.")
    print("  Agent: Tool'ları kullanarak adım adım düşünür, daha detaylı analiz yapar.")
    print()
    mod = input("Seçiminiz (1/2): ").strip()
    print()

    # --- Metin girişi ---
    cv_metni = metin_al("ornek_cv.txt", "CV")
    print("-" * 60)
    ilan_metni = metin_al("ornek_ilan.txt", "İş ilanı")

    print("\n" + "=" * 60)
    print("⏳ Analiz ediliyor... (Bu birkaç saniye sürebilir)")
    print("=" * 60 + "\n")

    # --- Analizi çalıştır ---
    if mod == "2":
        # Aşama 2: Agent modu
        from agent import agent_analiz_et
        print("🤖 Agent modu aktif — Tool çağrılarını aşağıda göreceksiniz:\n")
        sonuc = agent_analiz_et(cv_metni, ilan_metni)
    else:
        # Aşama 1: Chain modu
        sonuc = chain_analiz_et(cv_metni, ilan_metni)

    print("\n" + "=" * 60)
    print("📊 ANALİZ SONUCU")
    print("=" * 60 + "\n")
    print(sonuc)

    # --- Takip sorusu (sadece agent modunda) ---
    if mod == "2":
        from agent import llm

        # Konuşma geçmişini tut — LLM önceki analizi hatırlasın
        gecmis = [
            {"role": "system", "content": (
                "Sen bir kariyer danismanisin. Kullanicinin CV'si ve is ilani analiz edildi. "
                "Analiz sonuclarina dayanarak takip sorularina Turkce, samimi ve somut cevaplar ver. "
                "Gereksiz tekrar yapma, dogrudan soruya odaklan."
            )},
            {"role": "user", "content": (
                f"CV ve is ilani analizimin sonucu:\n\n{sonuc}"
            )},
            {"role": "assistant", "content": (
                "Analiz sonuclarini inceledim. Takip sorularinizi bekliyorum."
            )},
        ]

        print("\n" + "-" * 60)
        print("💬 Agent modunda takip sorusu sorabilirsiniz.")
        print("   Çıkmak için 'q' yazın.\n")
        while True:
            soru = input("Sorunuz: ").strip()
            if soru.lower() in ("q", "quit", "çık", "cik", ""):
                print("Görüşmek üzere! 👋")
                break

            gecmis.append({"role": "user", "content": soru})

            yanit = llm.invoke(gecmis)

            gecmis.append({"role": "assistant", "content": yanit.content})

            print("\n" + yanit.content + "\n")


if __name__ == "__main__":
    main()