import re
from langchain_core.tools import tool


# ============================================================
# TOOL'LAR (Agent'ın Kullanabileceği Araçlar)
# ============================================================
# Her tool bir Python fonksiyonu. @tool dekoratörü ile LangChain'e
# "bu fonksiyonu agent çağırabilir" diyoruz.
# Docstring önemli → Agent, tool'u NE ZAMAN çağıracağına docstring'e bakarak karar verir.

# Bilinen teknik beceri anahtar kelimeleri (küçük harf)
KNOWN_SKILLS = [
    "python", "javascript", "typescript", "java", "c#", "c++", "go", "rust", "ruby",
    "html", "css", "html/css", "sql", "nosql", "graphql",
    "django", "flask", "fastapi", "react", "vue", "angular", "next.js", "node.js",
    "spring", "express", ".net",
    "postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
    "docker", "kubernetes", "jenkins", "github actions", "ci/cd", "ci cd",
    "git", "github", "gitlab", "vs code",
    "rest api", "restful api", "grpc", "microservices", "mikroservis",
    "celery", "rabbitmq", "kafka",
    "pytest", "unittest", "jest", "selenium",
    "linux", "aws", "azure", "gcp",
    "machine learning", "deep learning", "nlp", "langchain",
    "agile", "scrum", "jira",
]


def _extract_skills(metin: str) -> list[str]:
    """Metinden bilinen teknik becerileri çıkarır."""
    metin_lower = metin.lower()
    bulunan = []

    # Bilinen beceri listesinden eşleşenleri bul
    for skill in KNOWN_SKILLS:
        if skill in metin_lower:
            bulunan.append(skill)

    # Tekrarları kaldır, sıralı döndür
    seen = set()
    sonuc = []
    for b in bulunan:
        if b not in seen:
            seen.add(b)
            sonuc.append(b)
    return sonuc


@tool
def beceri_cikar(metin: str, kaynak: str) -> str:
    """Bir CV veya is ilani metninden teknik becerileri cikarir ve liste olarak dondurur.
    kaynak parametresi 'cv' veya 'ilan' olmali.

    Args:
        metin: Analiz edilecek metin icerigi
        kaynak: 'cv' veya 'ilan'
    """
    beceriler = _extract_skills(metin)
    if not beceriler:
        return f"[{kaynak.upper()}] metninde bilinen bir beceri bulunamadi."

    beceri_listesi = ", ".join(beceriler)
    return f"[{kaynak.upper()}] Bulunan beceriler ({len(beceriler)}): {beceri_listesi}"


def _normalize_set(beceri_str: str) -> set:
    """Virgülle ayrılmış beceri stringini normalize set'e çevirir."""
    parcalar = re.split(r'[,\n\-•]', beceri_str)
    return set(
        b.strip().lower()
        for b in parcalar
        if b.strip() and len(b.strip()) > 1
    )


@tool
def karsilastir(cv_skills: str, job_skills: str) -> str:
    """CV becerileri ile is ilani becerilerini karsilastirir, eslesen ve eksik becerileri bulur.

    Args:
        cv_skills: CV'den cikarilan becerilerin virgullu listesi
        job_skills: Is ilanindan cikarilan becerilerin virgullu listesi
    """
    cv_set = _normalize_set(cv_skills)
    job_set = _normalize_set(job_skills)

    # Kısmi eşleştirme
    eslesen = set()
    for cv_b in cv_set:
        for job_b in job_set:
            if cv_b in job_b or job_b in cv_b:
                eslesen.add(job_b)
            elif len(cv_b) > 2 and len(job_b) > 2:
                cv_words = set(cv_b.split())
                job_words = set(job_b.split())
                ortak = cv_words & job_words
                if ortak and any(len(w) > 2 for w in ortak):
                    eslesen.add(job_b)

    eksik = job_set - eslesen

    return (
        f"Eslesen beceriler ({len(eslesen)}): {', '.join(sorted(eslesen)) if eslesen else 'Yok'}\n"
        f"Eksik beceriler ({len(eksik)}): {', '.join(sorted(eksik)) if eksik else 'Yok'}\n"
        f"Toplam aranan: {len(job_set)}, Eslesen: {len(eslesen)}"
    )


@tool
def skor_hesapla(eslesen: int, toplam: int) -> str:
    """Uyum skorunu hesaplar. eslesen / toplam * 100 formulu ile yuzde verir.

    Args:
        eslesen: Eslesen beceri sayisi
        toplam: Toplam aranan beceri sayisi
    """
    if toplam == 0:
        return "Skor hesaplanamadi — toplam 0."

    skor = round((eslesen / toplam) * 100)

    if skor >= 80:
        yorum = "Mukemmel uyum! Bu ilana guvenle basvurabilirsiniz."
    elif skor >= 60:
        yorum = "Iyi uyum. Birkac eksik beceriyi hizlica kapatabilirsiniz."
    elif skor >= 40:
        yorum = "Orta uyum. Eksik becerilere odaklanmaniz gerekiyor."
    else:
        yorum = "Dusuk uyum. Bu ilan icin ciddi hazirlik gerekebilir."

    return f"Uyum Skoru: %{skor} — {yorum}"


@tool
def oneri_uret(eksik_beceriler: str, mevcut_beceriler: str) -> str:
    """Eksik becerilere gore somut kariyer onerileri uretir.

    Args:
        eksik_beceriler: Virgullu eksik beceri listesi
        mevcut_beceriler: Virgullu mevcut beceri listesi
    """
    eksik_list = [b.strip() for b in eksik_beceriler.split(",") if b.strip()]
    mevcut_list = [b.strip() for b in mevcut_beceriler.split(",") if b.strip()]

    oneriler = []
    for beceri in eksik_list:
        oneriler.append(f"- {beceri}: Online kurs veya dokumantasyon ile ogrenin.")

    if not oneriler:
        oneriler.append("- Tum beceriler mevcut, pratik projelerle pekistirin.")

    return (
        f"Mevcut beceriler ({len(mevcut_list)}): {', '.join(mevcut_list)}\n"
        f"Eksik beceriler ({len(eksik_list)}): {', '.join(eksik_list)}\n\n"
        f"Oneriler:\n" + "\n".join(oneriler)
    )


# Tool listesi — Agent'a verilecek
ALL_TOOLS = [beceri_cikar, karsilastir, skor_hesapla, oneri_uret]
