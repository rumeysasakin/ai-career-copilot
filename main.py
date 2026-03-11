"""AI Kariyer Asistanı — Terminal CLI."""

from core.chain import chain_analiz_et
from core.agent import agent_analiz_et, llm


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def dosyadan_oku(dosya_yolu: str) -> str:
    """Bir metin dosyasını okuyup içeriğini döndürür."""
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return f.read().strip()


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
# ANA PROGRAM
# ============================================================

def main():
    print("=" * 60)
    print("  🔍 AI Kariyer Asistanı — CV & İş İlanı Eşleştirme")
    print("  LangChain + Ollama ile Beceri Analizi")
    print("=" * 60)
    print()

    print("Hangi modu kullanmak istersiniz?")
    print("  1 - Basit Analiz (Chain)")
    print("  2 - Akıllı Analiz (Agent — Hibrit)")
    print()
    print("  Chain: Tek seferde LLM analizi. Hızlı ama deterministik değil.")
    print("  Agent: Tool'larla adım adım analiz. Daha detaylı ve tekrarlanabilir.")
    print()
    mod = input("Seçiminiz (1/2): ").strip()
    print()

    cv_metni = metin_al("ornek_cv.txt", "CV")
    print("-" * 60)
    ilan_metni = metin_al("ornek_ilan.txt", "İş ilanı")

    print("\n" + "=" * 60)
    print("⏳ Analiz ediliyor...")
    print("=" * 60 + "\n")

    if mod == "2":
        print("🤖 Agent modu aktif — Tool çağrıları:\n")
        sonuc = agent_analiz_et(
            cv_metni, ilan_metni,
            log_fn=lambda msg: print(f"  {msg}")
        )
        rapor = sonuc.to_markdown()
    else:
        rapor = chain_analiz_et(cv_metni, ilan_metni)

    print("\n" + "=" * 60)
    print("📊 ANALİZ SONUCU")
    print("=" * 60 + "\n")
    print(rapor)

    # Takip soruları (sadece agent modunda)
    if mod == "2":
        gecmis = [
            {"role": "system", "content": (
                "Sen bir kariyer danışmanısın. Kullanıcının CV'si ve iş ilanı analiz edildi. "
                "Analiz sonuçlarına dayanarak takip sorularına Türkçe, samimi ve somut cevaplar ver. "
                "Gereksiz tekrar yapma, doğrudan soruya odaklan."
            )},
            {"role": "user", "content": f"Analiz sonucum:\n\n{rapor}"},
            {"role": "assistant", "content": "Analiz sonuçlarını inceledim. Sorularınızı bekliyorum."},
        ]

        print("\n" + "-" * 60)
        print("💬 Takip sorusu sorabilirsiniz. Çıkmak için 'q' yazın.\n")
        while True:
            soru = input("Sorunuz: ").strip()
            if soru.lower() in ("q", "quit", "çık", "cik", ""):
                print("Görüşmek üzere! 👋")
                break

            gecmis.append({"role": "user", "content": soru})
            yanit = llm.invoke(gecmis)
            gecmis.append({"role": "assistant", "content": yanit.content})
            print(f"\n{yanit.content}\n")


if __name__ == "__main__":
    main()