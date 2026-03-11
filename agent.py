from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import ALL_TOOLS, beceri_cikar, karsilastir, skor_hesapla, oneri_uret


# ============================================================
# 1) LLM TANIMI
# ============================================================
llm = ChatOllama(model="llama3.1", temperature=0.3)


# ============================================================
# 2) SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """Sen kariyer danismani ve CV analiz uzmanisin.
Kullanicinin CV ve is ilani analiz sonuclari sana verilecek.
Bu sonuclari kullanarak Turkce detayli bir rapor yaz.
Takip sorularina da ayni uzmanlikla cevap ver."""


# ============================================================
# 3) AGENT (Takip soruları için)
# ============================================================

agent_executor = create_agent(
    model=llm,
    tools=ALL_TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# 4) ANA ANALİZ FONKSİYONU (Hibrit: Tool'lar + LLM)
# ============================================================
# İlk analiz için tool'ları biz programatik olarak çağırıyoruz.
# Sonuçları LLM'e verip güzel bir Türkçe rapor yazdırıyoruz.
# Bu yaklaşım küçük modellerin tool calling tutarsızlığını ortadan kaldırır.

def agent_analiz_et(cv_metni: str, ilan_metni: str) -> str:
    """Tool'ları sırayla çağırıp sonuçları LLM'e vererek analiz raporu üretir."""
    import re

    # Adım 1: CV'den becerileri çıkar
    print("  [Tool] beceri_cikar(cv) çağrılıyor...")
    cv_beceriler = beceri_cikar.invoke({"metin": cv_metni, "kaynak": "cv"})
    print(f"  → {cv_beceriler}\n")

    # Adım 2: İlandan becerileri çıkar
    print("  [Tool] beceri_cikar(ilan) çağrılıyor...")
    ilan_beceriler = beceri_cikar.invoke({"metin": ilan_metni, "kaynak": "ilan"})
    print(f"  → {ilan_beceriler}\n")

    # Adım 3: Karşılaştır
    cv_skills_str = cv_beceriler.split(": ", 1)[-1] if ": " in cv_beceriler else cv_beceriler
    ilan_skills_str = ilan_beceriler.split(": ", 1)[-1] if ": " in ilan_beceriler else ilan_beceriler

    print("  [Tool] karsilastir çağrılıyor...")
    karsilastirma = karsilastir.invoke({"cv_skills": cv_skills_str, "job_skills": ilan_skills_str})
    print(f"  → {karsilastirma}\n")

    # Adım 4: Skor hesapla
    toplam_match = re.search(r"Toplam aranan: (\d+), Eslesen: (\d+)", karsilastirma)
    if toplam_match:
        toplam = int(toplam_match.group(1))
        eslesen_sayi = int(toplam_match.group(2))
    else:
        toplam, eslesen_sayi = 0, 0

    print("  [Tool] skor_hesapla çağrılıyor...")
    skor = skor_hesapla.invoke({"eslesen": eslesen_sayi, "toplam": toplam})
    print(f"  → {skor}\n")

    # Adım 5: Eksik/eşleşen becerileri parse et
    eksik_match = re.search(r"Eksik beceriler \(\d+\): (.+)", karsilastirma)
    eksik_str = eksik_match.group(1) if eksik_match else "Yok"
    eslesen_match = re.search(r"Eslesen beceriler \(\d+\): (.+)", karsilastirma)
    eslesen_str = eslesen_match.group(1) if eslesen_match else "Yok"

    # Adım 6: Öneri üret (role-specific)
    print("  [Tool] oneri_uret çağrılıyor...")
    oneriler = oneri_uret.invoke({"eksik_beceriler": eksik_str, "mevcut_beceriler": eslesen_str})
    print(f"  → {oneriler[:200]}...\n")

    # Adım 7: LLM'den kişisel değerlendirme al
    print("  [LLM] Kişisel değerlendirme yazılıyor...\n")

    yorum_prompt = f"""Sen kariyer danismanisin. Asagidaki analiz sonuclarina bakarak
kisa ve somut bir degerlendirme yaz (5-8 cumle). Tekrar listeleme yapma.
Kisinin guclu yanlarini, oncelikli ogrenme yolunu ve motivasyon iceren tavsiyeleri yaz.

CV Becerileri: {cv_skills_str}
Eslesen: {eslesen_str}
Eksik: {eksik_str}
Skor: {skor}"""

    yorum = llm.invoke(yorum_prompt)

    # Raporu birleştir
    rapor = f"""## 📋 CV'deki Beceriler
{cv_beceriler}

## 🎯 İlanda Aranan Beceriler
{ilan_beceriler}

## ✅ Eşleşen Beceriler ({eslesen_sayi}/{toplam})
{eslesen_str}

## ❌ Eksik Beceriler
{eksik_str}

## 📊 {skor}

## 🛠️ Somut Öneriler (Beceriye Özel)
{oneriler}

## 💡 Kişisel Değerlendirme
{yorum.content}"""

    return rapor
