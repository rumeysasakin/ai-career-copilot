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
    """Eksik becerilere gore somut ve kisisellestirilmis kariyer onerileri uretir.

    Args:
        eksik_beceriler: Virgullu eksik beceri listesi
        mevcut_beceriler: Virgullu mevcut beceri listesi
    """
    eksik_list = [b.strip().lower() for b in eksik_beceriler.split(",") if b.strip()]
    mevcut_list = [b.strip().lower() for b in mevcut_beceriler.split(",") if b.strip()]

    # Beceriye özel somut öneri haritası
    ONERI_HARITASI = {
        "docker": "Mevcut projelerinizden birini Dockerfile ile konteynerize edin. "
                  "docker-compose ile multi-service bir ortam kurun (ornegin Django + PostgreSQL + Redis).",
        "kubernetes": "Minikube ile yerel bir K8s cluster kurun. "
                      "Docker'la olusturdugunuz imaji K8s pod'una deploy edin. kubectl komutlarini ogrenin.",
        "fastapi": "Basit bir REST API projesi olusturun (ornegin todo-app). "
                   "FastAPI'nin otomatik Swagger dokumanini kesfet. async endpoint yazmayı deneyin.",
        "ci/cd": "GitHub Actions ile mevcut bir projenize otomatik test + lint pipeline'i ekleyin. "
                 "push'ta pytest calistiran bir .github/workflows/test.yml olusturun.",
        "ci cd": "GitHub Actions ile mevcut bir projenize otomatik test pipeline'i ekleyin.",
        "jenkins": "Jenkins'i Docker ile yerel kurun. Basit bir freestyle job olusturup "
                   "GitHub reponuzu build ettirin. Pipeline as Code (Jenkinsfile) yazmayı deneyin.",
        "redis": "Mevcut Django/Flask projenize cache ekleyin (django-redis veya flask-caching). "
                 "Redis CLI ile temel komutlari deneyin: SET, GET, EXPIRE, LPUSH.",
        "celery": "Django projenize Celery + Redis entegrasyonu yapin. "
                  "Uzun suren bir islemi (ornegin email gonderimi) asenkron task'a cevirin.",
        "rabbitmq": "RabbitMQ'yu Docker ile kurun. Basit bir producer-consumer ornegi yazin. "
                    "Celery ile RabbitMQ broker olarak entegre edin.",
        "pytest": "Mevcut projenizdeki en onemli 3 fonksiyon icin unit test yazin. "
                  "pytest-cov ile coverage raporunu olusturun. %80 coverage hedefleyin.",
        "mikroservis": "Monolitik bir projenizi iki ayri servise bölun (ornegin auth + api). "
                       "Servisler arasi iletisimi REST veya message queue ile kurun.",
        "microservices": "Mevcut projenizi iki bagimsiz servise ayirin. Docker Compose ile orkestre edin.",
        "postgresql": "PostgreSQL'de index, JOIN ve EXPLAIN ANALYZE komutlarini deneyin. "
                      "Django ORM sorgularinin SQL karsiliklarini inceleyin.",
        "mysql": "MySQL Workbench ile sorgulama pratiği yapin. "
                 "PostgreSQL biliyorsaniz farklilikları (syntax, JSON desteği) ogrenin.",
        "aws": "AWS Free Tier ile EC2 instance baslatip bir Flask/Django uygulamasi deploy edin. "
               "S3, RDS ve Lambda'yi kesfet.",
        "azure": "Azure App Service ile bir Python web uygulamasi deploy edin. Azure Portal'i kesfet.",
        "gcp": "Google Cloud Run ile konteyner deploy edin. BigQuery ile veri analizi deneyin.",
        "react": "Basit bir frontend projesi olusturun (portfolio sitesi). Props, state ve useEffect ogrenin.",
        "vue": "Vue CLI ile proje olusturup component yapisi ve reactivity ogrenin.",
        "angular": "Angular CLI ile proje olusturup component, service ve routing ogrenin.",
        "machine learning": "scikit-learn ile basit bir siniflandirma projesi yapin (ornegin iris dataset). "
                            "Kaggle'da beginner yarismalarına katılın.",
        "deep learning": "PyTorch veya TensorFlow ile basit bir sinir agi egitimi yapin. "
                         "MNIST el yazisi tanima projesinden baslayin.",
        "nlp": "Hugging Face transformers kutuphanesiyle sentiment analizi yapin. "
               "Kendi verinizle fine-tuning deneyin.",
        "langchain": "Bu projeyi referans alin! LangChain dokumantasyonundaki quickstart'i tamamlayin. "
                     "RAG (Retrieval Augmented Generation) ornegi yapin.",
        "graphql": "Strawberry veya Graphene ile bir GraphQL API olusturup REST ile kiyaslayin.",
        "kafka": "Docker ile Kafka cluster kurun. Python confluent-kafka ile producer-consumer yazin.",
        "elasticsearch": "Docker ile Elasticsearch kurun. Python elasticsearch client ile index olusturup arama yapin.",
        "selenium": "Selenium ile bir web sitesini otomatik test eden script yazin. Page Object Pattern ogrenin.",
        "power bi": "Ornek bir veri seti ile dashboard olusturun. DAX formulleri ve iliski modelleme ogrenin.",
        "tableau": "Tableau Public ile ucretsiz dashboard olusturup yayinlayin.",
        "jira": "Kendi projeniz icin Jira'da board olusturun. Sprint planlama ve backlog yonetimi pratiği yapin.",
        "agile": "Scrum Guide'i okuyun. Kendi projelerinizde 1 haftalik sprint dönguleri uygulayın.",
        "scrum": "Scrum Guide'i okuyun. Daily standup, sprint review ve retrospective kavramlarini pratikte deneyin.",
        "git": "Git branch stratejileri (Git Flow, trunk-based) ogrenin. "
               "Interactive rebase ve cherry-pick komutlarini deneyin.",
        "linux": "WSL veya bir VM ile Linux komut satirini gunluk isinizde kullanin. "
                 "Bash scripting ile dosya islemlerini otomatize edin.",
        "rest api": "OpenAPI/Swagger spec yazmayi ogrenin. Postman ile API testleri yapin.",
        "restful api": "OpenAPI/Swagger spec yazmayi ogrenin. Postman ile API testleri yapin.",
        "sql": "LeetCode veya HackerRank'te SQL sorulari cozun. Window functions ve CTE'leri ogrenin.",
        "nosql": "MongoDB Atlas free tier ile dokuman tabanlı veritabani deneyin. CRUD islemleri yapin.",
        "mongodb": "MongoDB Atlas free tier ile bir koleksiyon olusturun. Aggregation pipeline ogrenin.",
    }

    oneriler = []
    for beceri in eksik_list:
        beceri_lower = beceri.lower()
        if beceri_lower in ONERI_HARITASI:
            oneriler.append(f"- **{beceri}**: {ONERI_HARITASI[beceri_lower]}")
        else:
            # Bilinmeyen beceri için genel ama yine de somut öneri
            oneriler.append(
                f"- **{beceri}**: Resmi dokumantasyonu okuyun, YouTube'da crash course izleyin "
                f"ve kucuk bir pratik proje yapin."
            )

    if not oneriler:
        oneriler.append("- Tum beceriler mevcut! Pratik projelerle pekistirin ve portfoyunuze ekleyin.")

    return (
        f"Mevcut beceriler ({len(mevcut_list)}): {', '.join(mevcut_list)}\n"
        f"Eksik beceriler ({len(eksik_list)}): {', '.join(eksik_list)}\n\n"
        f"Somut Oneriler:\n" + "\n".join(oneriler)
    )


# Tool listesi — Agent'a verilecek
ALL_TOOLS = [beceri_cikar, karsilastir, skor_hesapla, oneri_uret]
