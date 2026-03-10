from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import ALL_TOOLS


# ============================================================
# 1) LLM TANIMI
# ============================================================
# Tool calling için llama3.1 kullanıyoruz.
# llama3 tool calling desteklemez, llama3.1 destekler.
# temperature=0.3 → tutarlı ve odaklı analizler için düşük tuttuk.
llm = ChatOllama(model="llama3.1", temperature=0.3)


# ============================================================
# 2) AGENT PROMPT'U (System Prompt)
# ============================================================
# create_agent, system_prompt parametresi alır.
# Agent'a kim olduğunu, ne yapması gerektiğini ve hangi tool'ları
# nasıl kullanacağını söylüyoruz.

SYSTEM_PROMPT = """Sen kariyer danismani ve CV analiz uzmanisin.

Gorev: CV ile is ilani arasindaki beceri uyumunu analiz et.

Adimlar:
1. beceri_cikar tool'u ile CV'den becerileri cikar (kaynak='cv')
2. beceri_cikar tool'u ile ilandan becerileri cikar (kaynak='ilan')
3. karsilastir tool'u ile eslesen ve eksik becerileri bul
4. skor_hesapla tool'u ile uyum skorunu hesapla
5. oneri_uret tool'u ile kariyer onerileri olustur

Sonucta kullaniciya Turkce detayli bir rapor sun. Raporda su bolumler olmali:
- CV'deki Beceriler
- Ilanda Aranan Beceriler
- Eslesen Beceriler
- Eksik Beceriler
- Kariyer Onerileri
- Uyum Skoru"""


# ============================================================
# 3) AGENT OLUŞTURMA
# ============================================================
# create_agent:
#   LangChain 1.x'in yeni agent API'si. LangGraph tabanlı çalışır.
#   Model'e tool'ları bağlar. Model hangi tool'u ne zaman çağıracağına
#   kendisi karar verir (ReAct döngüsü: Düşün → Çağır → Gözlemle).
#
# Döndürdüğü nesne bir CompiledStateGraph:
#   - invoke() ile çalıştırılır
#   - messages listesi alır ve döndürür

agent_executor = create_agent(
    model=llm,
    tools=ALL_TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


# ============================================================
# 4) ÇALIŞTIRMA FONKSİYONU
# ============================================================

def agent_analiz_et(cv_metni: str, ilan_metni: str) -> str:
    """Agent'ı çalıştırıp CV-ilan analizini döndürür."""
    kullanici_mesaji = f"""Aşağıdaki CV ve iş ilanını analiz et:

CV:
{cv_metni}

İŞ İLANI:
{ilan_metni}"""

    result = agent_executor.invoke({
        "messages": [{"role": "user", "content": kullanici_mesaji}]
    })

    # Son AI mesajını döndür
    son_mesaj = result["messages"][-1]
    return son_mesaj.content
