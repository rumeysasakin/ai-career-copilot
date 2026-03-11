"""
Beceri çıkarma ve normalizasyon motoru.

- KNOWN_SKILLS: Tanınan teknik beceri listesi (standart formlar)
- SKILL_ALIASES: Eş anlamlı/farklı yazım → standart form eşlemesi
- normalize_skill(): Tek beceri adını standart forma dönüştürür
- extract_skills(): Metinden bilinen becerileri çıkarır
"""


# ============================================================
# BECERİ VERİTABANI (Standart formlar, küçük harf)
# ============================================================

KNOWN_SKILLS = [
    # Programlama Dilleri
    "python", "javascript", "typescript", "java", "c#", "c++", "go", "rust", "ruby",
    # Web Temelleri
    "html", "css", "sql",
    # Backend Frameworks
    "django", "flask", "fastapi", "spring", "express", ".net", "node.js",
    # Frontend Frameworks
    "react", "vue", "angular", "next.js",
    # Veritabanları
    "postgresql", "mysql", "sqlite", "mongodb", "redis", "elasticsearch",
    # DevOps & Altyapı
    "docker", "kubernetes", "jenkins", "github actions", "ci/cd",
    "git", "linux", "aws", "azure", "gcp",
    # API & Mimari
    "rest api", "graphql", "grpc", "microservices",
    # Mesaj Kuyrukları & Async
    "celery", "rabbitmq", "kafka",
    # Test
    "pytest", "selenium", "jest",
    # AI / ML
    "machine learning", "deep learning", "nlp", "langchain",
    # Veri & BI
    "power bi", "tableau", "nosql",
    # Proje Yönetimi
    "agile", "scrum", "jira",
]


# ============================================================
# EŞ ANLAMLI / FARKLI YAZIM → STANDART FORM
# ============================================================

SKILL_ALIASES = {
    # API varyantları
    "restful api": "rest api",
    "rest": "rest api",
    "restful": "rest api",
    # CI/CD varyantları
    "ci cd": "ci/cd",
    "ci-cd": "ci/cd",
    "cicd": "ci/cd",
    # JS/TS kısaltmaları
    "js": "javascript",
    "ts": "typescript",
    # Python kısaltması
    "py": "python",
    # Veritabanı varyantları
    "postgres": "postgresql",
    "psql": "postgresql",
    "mongo": "mongodb",
    # DevOps kısaltmaları
    "k8s": "kubernetes",
    "gh actions": "github actions",
    "github action": "github actions",
    # Framework varyantları
    "node": "node.js",
    "nodejs": "node.js",
    "nextjs": "next.js",
    "expressjs": "express",
    "vue.js": "vue",
    "vuejs": "vue",
    "react.js": "react",
    "reactjs": "react",
    # C varyantları
    "c sharp": "c#",
    "csharp": "c#",
    "cpp": "c++",
    # HTML/CSS varyantları
    "html5": "html",
    "css3": "css",
    "html/css": "html",
    # BI varyantları
    "powerbi": "power bi",
    "power_bi": "power bi",
    # ML kısaltmaları
    "ml": "machine learning",
    "dl": "deep learning",
    # Mikroservis
    "mikroservis": "microservices",
    "micro services": "microservices",
}


def normalize_skill(skill: str) -> str:
    """Beceri adını standart forma dönüştürür.

    Önce alias tablosunda arar, bulursa standart formu döndürür.
    Bulamazsa lowercase/strip halini döndürür.
    """
    cleaned = skill.strip().lower()
    return SKILL_ALIASES.get(cleaned, cleaned)


def extract_skills(metin: str) -> list[str]:
    """Metinden bilinen teknik becerileri çıkarır.

    1. KNOWN_SKILLS listesinden doğrudan eşleşenler bulunur
    2. SKILL_ALIASES üzerinden normalize edilen eşleşmeler eklenir
    3. Tekrarlar kaldırılır, alfabetik sıralı liste döndürülür
    """
    metin_lower = metin.lower()
    bulunan = set()

    for skill in KNOWN_SKILLS:
        if skill in metin_lower:
            bulunan.add(skill)

    for alias, standart in SKILL_ALIASES.items():
        if alias in metin_lower and standart in KNOWN_SKILLS:
            bulunan.add(standart)

    return sorted(bulunan)
