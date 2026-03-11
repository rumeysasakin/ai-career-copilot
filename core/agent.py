"""
Hibrit Agent modu — programatik tool çağrıları + LLM değerlendirme.

Tool'lar sırayla çağrılır, sonuçlar yapısal bir AnalizSonucu'na toplanır.
LLM yalnızca kişisel değerlendirme yazmak için kullanılır.
Bu yaklaşım küçük modellerin tool calling tutarsızlığını ortadan kaldırır.
"""

import os
import re
from dataclasses import dataclass

from langchain_ollama import ChatOllama

from .tools import beceri_cikar, karsilastir, skor_hesapla, oneri_uret

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(model="llama3.1", temperature=0.3, base_url=OLLAMA_BASE_URL)


@dataclass
class AnalizSonucu:
    """Analiz çıktısını yapısal olarak tutan veri sınıfı."""

    cv_beceriler: str = ""
    ilan_beceriler: str = ""
    eslesen: str = ""
    eksik: str = ""
    eslesen_sayi: int = 0
    toplam: int = 0
    skor: str = ""
    oneriler: str = ""
    degerlendirme: str = ""

    def to_markdown(self) -> str:
        return (
            f"## 📋 CV'deki Beceriler\n{self.cv_beceriler}\n\n"
            f"## 🎯 İlanda Aranan Beceriler\n{self.ilan_beceriler}\n\n"
            f"## ✅ Eşleşen Beceriler ({self.eslesen_sayi}/{self.toplam})\n{self.eslesen}\n\n"
            f"## ❌ Eksik Beceriler\n{self.eksik}\n\n"
            f"## 📊 {self.skor}\n\n"
            f"## 🛠️ Somut Öneriler (Beceriye Özel)\n{self.oneriler}\n\n"
            f"## 💡 Kişisel Değerlendirme\n{self.degerlendirme}"
        )


def agent_analiz_et(cv_metni: str, ilan_metni: str, log_fn=None) -> AnalizSonucu:
    """Tool'ları sırayla çağırıp yapısal analiz sonucu üretir.

    Args:
        cv_metni: CV metni
        ilan_metni: İş ilanı metni
        log_fn: Opsiyonel log fonksiyonu (terminal print veya Streamlit callback)

    Returns:
        AnalizSonucu dataclass
    """

    def log(msg: str):
        if log_fn:
            log_fn(msg)

    sonuc = AnalizSonucu()

    # 1. CV becerileri
    log("🔧 beceri_cikar(cv) çağrılıyor...")
    sonuc.cv_beceriler = beceri_cikar.invoke({"metin": cv_metni, "kaynak": "cv"})
    log(f"  → {sonuc.cv_beceriler}")

    # 2. İlan becerileri
    log("🔧 beceri_cikar(ilan) çağrılıyor...")
    sonuc.ilan_beceriler = beceri_cikar.invoke({"metin": ilan_metni, "kaynak": "ilan"})
    log(f"  → {sonuc.ilan_beceriler}")

    # 3. Karşılaştırma
    cv_skills_str = sonuc.cv_beceriler.split(": ", 1)[-1] if ": " in sonuc.cv_beceriler else sonuc.cv_beceriler
    ilan_skills_str = sonuc.ilan_beceriler.split(": ", 1)[-1] if ": " in sonuc.ilan_beceriler else sonuc.ilan_beceriler

    log("🔧 karsilastir çağrılıyor...")
    karsilastirma = karsilastir.invoke({"cv_skills": cv_skills_str, "job_skills": ilan_skills_str})
    log(f"  → {karsilastirma}")

    # Parse
    toplam_match = re.search(r"Toplam aranan: (\d+), Eslesen: (\d+)", karsilastirma)
    if toplam_match:
        sonuc.toplam = int(toplam_match.group(1))
        sonuc.eslesen_sayi = int(toplam_match.group(2))

    eksik_match = re.search(r"Eksik beceriler \(\d+\): (.+)", karsilastirma)
    sonuc.eksik = eksik_match.group(1) if eksik_match else "Yok"

    eslesen_match = re.search(r"Eslesen beceriler \(\d+\): (.+)", karsilastirma)
    sonuc.eslesen = eslesen_match.group(1) if eslesen_match else "Yok"

    # 4. Skor
    log("🔧 skor_hesapla çağrılıyor...")
    sonuc.skor = skor_hesapla.invoke({"eslesen": sonuc.eslesen_sayi, "toplam": sonuc.toplam})
    log(f"  → {sonuc.skor}")

    # 5. Öneriler
    log("🔧 oneri_uret çağrılıyor...")
    sonuc.oneriler = oneri_uret.invoke({"eksik_beceriler": sonuc.eksik, "mevcut_beceriler": sonuc.eslesen})
    log(f"  → Öneriler üretildi ({len(sonuc.eksik.split(','))} beceri için)")

    # 6. LLM kişisel değerlendirme
    log("🤖 Kişisel değerlendirme yazılıyor...")
    yorum_prompt = (
        "Sen kariyer danışmanısın. Aşağıdaki analiz sonuçlarına bakarak "
        "kısa ve somut bir değerlendirme yaz (5-8 cümle). Tekrar listeleme yapma. "
        "Kişinin güçlü yanlarını, öncelikli öğrenme yolunu ve motivasyon içeren tavsiyeleri yaz.\n\n"
        f"CV Becerileri: {cv_skills_str}\n"
        f"Eşleşen: {sonuc.eslesen}\n"
        f"Eksik: {sonuc.eksik}\n"
        f"Skor: {sonuc.skor}"
    )
    yorum = llm.invoke(yorum_prompt)
    sonuc.degerlendirme = yorum.content

    return sonuc
