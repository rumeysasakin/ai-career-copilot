"""
Chain modu — PromptTemplate + LCEL ile tek seferde LLM analizi.

Tüm analiz tek bir LLM çağrısında yapılır. Hızlı ama deterministik değil.
"""

import os

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

OLLAMA_BASE_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

llm = ChatOllama(model="llama3", temperature=0.3, base_url=OLLAMA_BASE_URL)

ANALIZ_PROMPT = PromptTemplate(
    input_variables=["cv_metni", "ilan_metni"],
    template="""Sen bir kariyer danışmanısın. CV metni ve iş ilanı metni verilecek.

Görevlerin:
1. CV'deki becerileri çıkar
2. İlandaki aranan becerileri çıkar
3. Eşleşen becerileri bul
4. Eksik becerileri bul
5. Somut öneriler ver
6. Uyum skoru hesapla

Yanıtını şu formatta ver:

## 📋 CV'deki Beceriler
- (madde madde)

## 🎯 İlanda Aranan Beceriler
- (madde madde)

## ✅ Eşleşen Beceriler
- (madde madde)

## ❌ Eksik Beceriler
- (madde madde)

## 🛠️ Öneriler
- (somut, kısa öneriler)

## 📊 Uyum Skoru
- Yüzde olarak tahmini skor ve kısa açıklama.

---
CV METNİ:
{cv_metni}

---
İŞ İLANI METNİ:
{ilan_metni}
""",
)

analiz_chain = ANALIZ_PROMPT | llm


def chain_analiz_et(cv_metni: str, ilan_metni: str) -> str:
    """Chain modu ile tek seferde analiz. Markdown string döndürür."""
    sonuc = analiz_chain.invoke({"cv_metni": cv_metni, "ilan_metni": ilan_metni})
    return sonuc.content
