from langchain_core.tools import tool


# ============================================================
# TOOL'LAR (Agent'ın Kullanabileceği Araçlar)
# ============================================================
# Her tool bir Python fonksiyonu. @tool dekoratörü ile LangChain'e
# "bu fonksiyonu agent çağırabilir" diyoruz.
# Docstring önemli → Agent, tool'u NE ZAMAN çağıracağına docstring'e bakarak karar verir.


@tool
def beceri_cikar(metin: str, kaynak: str) -> str:
    """Bir CV veya is ilani metninden teknik ve kisisel becerileri cikarir.
    kaynak parametresi 'cv' veya 'ilan' olmali.

    Args:
        metin: Analiz edilecek metin icerigi
        kaynak: 'cv' veya 'ilan'
    """
    return f"[{kaynak.upper()}] metninden beceriler cikarildi."


@tool
def karsilastir(cv_skills: str, job_skills: str) -> str:
    """CV becerileri ile is ilani becerilerini karsilastirir, eslesen ve eksik becerileri bulur.

    Args:
        cv_skills: CV'den cikarilan becerilerin virgullu listesi
        job_skills: Is ilanindan cikarilan becerilerin virgullu listesi
    """
    # Becerileri normalize et: küçük harf, boşlukları temizle
    def normalize(beceri_str: str) -> set:
        # Virgül, satır sonu veya tire ile ayır
        import re
        parcalar = re.split(r'[,\n\-•]', beceri_str)
        return set(
            b.strip().lower()
            for b in parcalar
            if b.strip() and len(b.strip()) > 1
        )

    cv_set = normalize(cv_skills)
    job_set = normalize(job_skills)

    # Kısmi eşleştirme: "python" hem "python programlama" hem "python" ile eşleşir
    eslesen = set()
    for cv_b in cv_set:
        for job_b in job_set:
            # Tam eşleşme veya kısmi eşleşme (en az 3 karakter)
            if cv_b in job_b or job_b in cv_b:
                eslesen.add(job_b)
            # Kelime bazlı eşleşme: ortak kelimeler varsa eşleştir
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
    return (
        f"Mevcut: {mevcut_beceriler}\n"
        f"Eksik: {eksik_beceriler}\n"
        "Bu bilgilere gore kisiye ozel oneriler uretildi."
    )


# Tool listesi — Agent'a verilecek
ALL_TOOLS = [beceri_cikar, karsilastir, skor_hesapla, oneri_uret]
