"""Tout le contenu et la configuration du profil GitHub d'Axel.

Modifie CE fichier (textes, outils, certifs, projets, liens), puis relance :
    python scripts/build.py --readme
"""

# ── Liens (à compléter) ─────────────────────────────────────────────────────
USERNAME = "axeltadjounteu17"
LINKS = {
    "portfolio": "https://axeltadjounteu.vercel.app",
    "linkedin": "https://www.linkedin.com/in/axel-tadjounteu-060502296",
    "email": "mailto:axeltadjounteu@gmail.com",
    "tiktok": "https://www.tiktok.com/@axeltngr17",
}

# ── Logos : clé -> source ───────────────────────────────────────────────────
# ("si", slug)      : Simple Icons (monochrome, recolorié selon le thème)
# ("dev", chemin)   : Devicon (garde ses couleurs d'origine)
LOGOS = {
    "aws": ("dev", "amazonwebservices/amazonwebservices-plain-wordmark.svg"),
    "googlecloud": ("si", "googlecloud"),
    "azure": ("dev", "azure/azure-original.svg"),
    "docker": ("si", "docker"),
    "kubernetes": ("si", "kubernetes"),
    "terraform": ("si", "terraform"),
    "githubactions": ("si", "githubactions"),
    "vercel": ("si", "vercel"),
    "cisco": ("si", "cisco"),
    "wireshark": ("si", "wireshark"),
    "kalilinux": ("si", "kalilinux"),
    "burpsuite": ("si", "burpsuite"),
    "linux": ("si", "linux"),
    "ubuntu": ("si", "ubuntu"),
    "bash": ("si", "gnubash"),
    "owasp": ("si", "owasp"),
    "typescript": ("si", "typescript"),
    "javascript": ("si", "javascript"),
    "python": ("si", "python"),
    "react": ("si", "react"),
    "nextjs": ("si", "nextdotjs"),
    "vite": ("si", "vite"),
    "tailwind": ("si", "tailwindcss"),
    "nodejs": ("dev", "nodejs/nodejs-original.svg"),
    "flutter": ("si", "flutter"),
    "dart": ("si", "dart"),
    "android": ("si", "android"),
    "expo": ("si", "expo"),
    "supabase": ("si", "supabase"),
    "postgresql": ("si", "postgresql"),
    "neon": ("si", "neon"),
    "drizzle": ("si", "drizzle"),
    "upstash": ("si", "upstash"),
    "sentry": ("si", "sentry"),
    "resend": ("si", "resend"),
    "jupyter": ("si", "jupyter"),
    "claude": ("si", "claude"),
    "gemini": ("si", "googlegemini"),
    "notebooklm": ("si", "notebooklm"),
    "figma": ("si", "figma"),
    "canva": ("dev", "canva/canva-original.svg"),
    "notion": ("si", "notion"),
    "vscode": ("dev", "vscode/vscode-original.svg"),
    "github": ("si", "github"),
    "fortinet": ("si", "fortinet"),
    "portswigger": ("si", "portswigger"),
    "tryhackme": ("si", "tryhackme"),
    "datacamp": ("si", "datacamp"),
    "comptia": ("si", "comptia"),
    "linkedin": ("dev", "linkedin/linkedin-plain.svg", "#0A66C2"),
    "tiktok": ("si", "tiktok"),
    "gmail": ("si", "gmail"),
}

# ── Boîte à outils : catégories de tuiles (label, [(clé_logo, libellé)]) ───
# Retire ce que tu n'utilises pas, ajoute ce que tu veux (voir GUIDE.md).
TOOLBOX = {
    "cloud": {
        "label": {"en": "CLOUD & DEVOPS", "fr": "CLOUD & DEVOPS"},
        "tools": [("aws", "AWS"), ("googlecloud", "Google Cloud"), ("azure", "Azure"),
                  ("docker", "Docker"), ("kubernetes", "Kubernetes"), ("terraform", "Terraform"),
                  ("githubactions", "GitHub Actions"), ("vercel", "Vercel")],
        "chips": {"en": "AWS SERVICES: Lambda · API Gateway · DynamoDB · Cognito · Bedrock",
                  "fr": "SERVICES AWS : Lambda · API Gateway · DynamoDB · Cognito · Bedrock"},
    },
    "security": {
        "label": {"en": "NETWORKS & SECURITY", "fr": "RÉSEAUX & SÉCURITÉ"},
        "tools": [("cisco", "Cisco"), ("wireshark", "Wireshark"), ("kalilinux", "Kali Linux"),
                  ("burpsuite", "Burp Suite"), ("linux", "Linux"), ("ubuntu", "Ubuntu"),
                  ("bash", "Bash"), ("owasp", "OWASP")],
    },
    "dev": {
        "label": {"en": "DEVELOPMENT", "fr": "DÉVELOPPEMENT"},
        "tools": [("typescript", "TypeScript"), ("javascript", "JavaScript"), ("python", "Python"),
                  ("react", "React"), ("nextjs", "Next.js"), ("vite", "Vite"),
                  ("tailwind", "Tailwind CSS"), ("nodejs", "Node.js"),
                  ("flutter", "Flutter"), ("dart", "Dart"), ("android", "Android"), ("expo", "Expo")],
    },
    "data": {
        "label": {"en": "DATA & BACKEND SERVICES", "fr": "DONNÉES & SERVICES BACKEND"},
        "tools": [("supabase", "Supabase"), ("postgresql", "PostgreSQL"), ("neon", "Neon"),
                  ("drizzle", "Drizzle"), ("upstash", "Upstash"), ("sentry", "Sentry"),
                  ("resend", "Resend"), ("jupyter", "Jupyter")],
    },
    "ai": {
        "label": {"en": "AI & PRODUCTIVITY", "fr": "IA & PRODUCTIVITÉ"},
        "tools": [("claude", "Claude"), ("gemini", "Gemini"), ("notebooklm", "NotebookLM"),
                  ("figma", "Figma"), ("canva", "Canva"), ("notion", "Notion"),
                  ("vscode", "VS Code"), ("github", "GitHub")],
    },
    "learning": {
        "label": {"en": "LEARNING PLATFORMS", "fr": "PLATEFORMES D'APPRENTISSAGE"},
        "tools": [("cisco", "Cisco NetAcad"), ("fortinet", "Fortinet NSE"), ("portswigger", "PortSwigger"),
                  ("tryhackme", "TryHackMe"), ("googlecloud", "Skills Boost"), ("datacamp", "DataCamp")],
    },
}

# ── Certifications (status : done | progress | prep | planned) ─────────────
CERTS = [
    {"id": "restart", "logo": "aws", "vendor": "AWS re/Start", "title": {"en": ["Graduate"], "fr": ["Diplômé"]}, "code": {"en": "COHORT CMDOU5", "fr": "COHORTE CMDOU5"}, "status": "done", "done_key": "completed"},
    {"id": "clf", "logo": "aws", "vendor": "AWS CERTIFIED", "title": ["Cloud", "Practitioner"], "code": "CLF-C02", "status": "done", "done_key": "certified"},
    {"id": "saa", "logo": "aws", "vendor": "AWS CERTIFIED", "title": ["Solutions Architect", "Associate"], "code": "SAA-C03", "status": "progress"},
    {"id": "secplus", "logo": "comptia", "vendor": "COMPTIA", "title": ["Security+"], "code": {"en": "12-MONTH ROADMAP", "fr": "PLAN SUR 12 MOIS"}, "status": "planned"},
]
STATUS_TEXT = {
    "completed": {"en": "COMPLETED", "fr": "TERMINÉ"},
    "certified": {"en": "CERTIFIED", "fr": "OBTENUE"},
    "progress": {"en": "IN PROGRESS", "fr": "EN COURS"},
    "prep": {"en": "IN PREP", "fr": "EN PRÉPARATION"},
    "planned": {"en": "PLANNED", "fr": "PRÉVUE"},
}

# ── Projets (status : company | live | design | pitched | hack) ────────────
PROJECTS = [
    {"key": "atnyx", "status": "company",
     "title": "Atnyx",
     "desc": {"en": "IT services company I founded in Douala: cybersecurity, cloud, web and mobile development, IT support.",
              "fr": "Entreprise de services IT que j'ai fondée à Douala : cybersécurité, cloud, développement web et mobile, support IT."},
     "tags": {"en": ["Cybersecurity", "Cloud", "Web & Mobile", "IT Support"], "fr": ["Cybersécurité", "Cloud", "Web & Mobile", "Support IT"]}},
    {"key": "nkul", "status": "design",
     "title": "NKUL",
     "desc": {"en": "Cybersecurity and cloud audit platform for African SMEs. Brand identity and full product specification done.",
              "fr": "Plateforme d'audit cybersécurité et cloud pour les PME africaines. Identité de marque et cahier des charges produit terminés."},
     "tags": {"en": ["Security", "Cloud", "SaaS"], "fr": ["Sécurité", "Cloud", "SaaS"]}},
    {"key": "ecocamer", "status": "pitched",
     "title": "EcoCamer",
     "desc": {"en": "Civic-tech app to report urban waste by geolocation, with an SMS/USSD fallback. Pitched at the MTN YaMo Pitch S4 regional auditions.",
              "fr": "Application civic-tech de signalement des déchets urbains par géolocalisation, avec repli SMS/USSD. Pitchée aux auditions régionales MTN YaMo Pitch S4."},
     "tags": ["Civic-tech", "SMS/USSD", "Africa's Talking"]},
    {"key": "branchline", "status": "design",
     "title": "Branchline",
     "desc": {"en": "GitHub management dashboard SaaS. Frontend and backend specifications written, brand identity chosen.",
              "fr": "SaaS de gestion GitHub sous forme de tableau de bord. Spécifications frontend et backend rédigées, identité de marque choisie."},
     "tags": ["Next.js 15", "Drizzle", "Neon", "Auth.js"]},
    {"key": "fansquad", "status": "hack",
     "title": "Fan Squad",
     "desc": {"en": "Real-time multiplayer second-screen app for Bundesliga fans, built for the AWS World Sports Innovation Cup 2026.",
              "fr": "Application second écran multijoueur en temps réel pour les fans de Bundesliga, conçue pour l'AWS World Sports Innovation Cup 2026."},
     "tags": ["Expo", "WebSocket", "Lambda", "Bedrock"]},
    {"key": "portfolio", "status": "live",
     "title": "Portfolio",
     "desc": {"en": "My personal site: React, Vite and Tailwind, animated with Framer Motion, multilingual, with a contact form.",
              "fr": "Mon site personnel : React, Vite et Tailwind, animé avec Framer Motion, multilingue, avec formulaire de contact."},
     "tags": ["React", "Vite", "Tailwind 4", "i18n"]},
]
PROJECT_STATUS = {
    "company": {"en": "COMPANY", "fr": "ENTREPRISE"},
    "live": {"en": "LIVE", "fr": "EN LIGNE"},
    "design": {"en": "IN DESIGN", "fr": "EN CONCEPTION"},
    "pitched": {"en": "PITCHED", "fr": "PITCHÉ"},
    "hack": {"en": "HACKATHON", "fr": "HACKATHON"},
}

# ── Services Atnyx ──────────────────────────────────────────────────────────
SERVICES = [
    ("shield", {"en": "Cybersecurity", "fr": "Cybersécurité"}),
    ("cloud", {"en": "Cloud", "fr": "Cloud"}),
    ("code", {"en": "Web & Mobile", "fr": "Web & Mobile"}),
    ("lifebuoy", {"en": "IT Support", "fr": "Support IT"}),
]

# ── Bannière ────────────────────────────────────────────────────────────────
BANNER = {
    "pill": {"en": "FOUNDER @ ATNYX · DOUALA, CM", "fr": "FONDATEUR @ ATNYX · DOUALA, CM"},
    "tagline": {"en": "Cybersecurity · Cloud · Software development", "fr": "Cybersécurité · Cloud · Développement"},
    "line1": {"en": "Networks & Telecom (Security) · Université de Douala", "fr": "Réseaux & Télécoms (Sécurité) · Université de Douala"},
    "line2": {"en": "AWS re/Start alumnus · AWS Cloud Practitioner", "fr": "Alumnus AWS re/Start · AWS Cloud Practitioner"},
    "term": [
        ("whoami", {"en": "axel: cloud & security", "fr": "axel : cloud & sécurité"}),
        ("status", {"en": "founder @ atnyx", "fr": "fondateur @ atnyx"}),
        ("studying", {"en": "AWS SAA-C03", "fr": "AWS SAA-C03"}),
        ("location", {"en": "Douala, Cameroon", "fr": "Douala, Cameroun"}),
    ],
}

# ── En-têtes de section : (id, titre, légende) ─────────────────────────────
SECTIONS = [
    ("about", {"en": "About", "fr": "À propos"}, {"en": "who I am", "fr": "qui je suis"}),
    ("approach", {"en": "How I build", "fr": "Ma façon de construire"}, {"en": "principles I stick to", "fr": "mes principes"}),
    ("now", {"en": "Now", "fr": "En ce moment"}, {"en": "learning and building", "fr": "j'apprends, je construis"}),
    ("atnyx", {"en": "Atnyx", "fr": "Atnyx"}, {"en": "the company I founded", "fr": "l'entreprise que j'ai fondée"}),
    ("projects", {"en": "Projects", "fr": "Projets"}, {"en": "built, pitched, in design", "fr": "réalisés, pitchés, en conception"}),
    ("toolbox", {"en": "Toolbox", "fr": "Boîte à outils"}, {"en": "what I use and explore", "fr": "ce que j'utilise et explore"}),
    ("labs", {"en": "Labs", "fr": "Labs"}, {"en": "hands-on practice", "fr": "pratique concrète"}),
    ("certs", {"en": "Certifications", "fr": "Certifications"}, {"en": "earned, in progress, planned", "fr": "obtenues, en cours, prévues"}),
    ("achievements", {"en": "Achievements", "fr": "Réalisations"}, {"en": "milestones so far", "fr": "les étapes franchies"}),
    ("activity", {"en": "Activity", "fr": "Activité"}, {"en": "live from the GitHub API", "fr": "données en direct de l'API GitHub"}),
    ("content", {"en": "Writing & content", "fr": "Écrits & contenu"}, {"en": "sharing what I learn", "fr": "je partage ce que j'apprends"}),
    ("contact", {"en": "Contact", "fr": "Contact"}, {"en": "let's work together", "fr": "travaillons ensemble"}),
]

# ── Aperçus sociaux de dépôts (PNG 1280x640) ───────────────────────────────
REPOS = [
    {"name": "portfolio", "sub": {"en": "Personal site, multilingual", "fr": "Site personnel multilingue"}, "tags": ["React", "Vite", "Tailwind", "Framer Motion"]},
    {"name": "cloud-labs", "sub": {"en": "AWS and Google Cloud hands-on labs", "fr": "Labs pratiques AWS et Google Cloud"}, "tags": ["AWS", "Google Cloud", "CLI", "IaC"]},
    {"name": "network-security-labs", "sub": {"en": "Packet Tracer labs and security exercises", "fr": "Labs Packet Tracer et exercices de sécurité"}, "tags": ["Cisco", "VLAN", "ACL", "VPN"]},
    {"name": "certification-notes", "sub": {"en": "Study notes: AWS SAA-C03 and Security+", "fr": "Notes de révision : AWS SAA-C03 et Security+"}, "tags": ["AWS", "CompTIA", "Cloud"]},
    {"name": "nkul", "sub": {"en": "Security and cloud audit for African SMEs", "fr": "Audit sécurité et cloud pour PME africaines"}, "tags": ["Security", "Cloud", "SaaS"]},
    {"name": "ecocamer", "sub": {"en": "Urban waste reporting, SMS/USSD ready", "fr": "Signalement des déchets urbains, compatible SMS/USSD"}, "tags": ["Civic-tech", "Geolocation", "USSD"]},
    {"name": "branchline", "sub": {"en": "GitHub management dashboard", "fr": "Tableau de bord de gestion GitHub"}, "tags": ["Next.js", "Drizzle", "Neon"]},
    {"name": "atnyx-platform", "sub": {"en": "Multi-branch IT services website", "fr": "Site multi-branches de services IT"}, "tags": ["Next.js", "Atnyx"]},
]


# ── Liens cliquables (optionnels) ───────────────────────────────────────────
# Certifications : preuve Credly / Google Cloud. Clés = id de CERTS (restart, clf, saa, secplus).
CERT_PROOF = {
    # "clf": "https://www.credly.com/badges/XXXXXXXX",
}
# Projets : dépôt public ou site en ligne. Clés = key de PROJECTS.
PROJECT_LINKS = {
    "portfolio": "https://axeltadjounteu.vercel.app",
    # "nkul": "https://github.com/axeltadjounteu17/nkul",
}

# ── Rubrique « How I build » (principes, à adapter à ta façon de travailler) ─
PRINCIPLES = [
    ("shield", {"en": "Secure by default", "fr": "Sécurisé par défaut"},
     {"en": "Security is designed in from the first line, not patched on at the end.",
      "fr": "La sécurité est pensée dès la première ligne, pas ajoutée à la fin."}),
    ("wifi", {"en": "Built for the field", "fr": "Pensé pour le terrain"},
     {"en": "Offline-first and lightweight, because networks and devices are not always fast.",
      "fr": "Hors ligne d'abord et léger, car les réseaux et les appareils ne sont pas toujours rapides."}),
    ("check", {"en": "Tested and readable", "fr": "Testé et lisible"},
     {"en": "Tests, clear names and short functions keep the code easy to maintain.",
      "fr": "Des tests, des noms clairs et des fonctions courtes gardent le code maintenable."}),
    ("compass", {"en": "Stack on purpose", "fr": "Stack choisie"},
     {"en": "I pick tools for the constraints of the project, not for the hype.",
      "fr": "Je choisis les outils selon les contraintes du projet, pas selon la mode."}),
]

# ── Rubrique « Achievements » : médailles rondes (icône, titre, sous-titre) ─
ACHIEVEMENTS = [
    ("cap", {"en": ["AWS re/Start"], "fr": ["AWS re/Start"]}, {"en": "Alumnus · CMDOU5", "fr": "Alumnus · CMDOU5"}),
    ("award", {"en": ["Cloud", "Practitioner"], "fr": ["Cloud", "Practitioner"]}, {"en": "AWS · CLF-C02", "fr": "AWS · CLF-C02"}),
    ("building", {"en": ["Founder"], "fr": ["Fondateur"]}, {"en": "Atnyx · Douala", "fr": "Atnyx · Douala"}),
    ("mic", {"en": ["MTN YaMo", "Pitch"], "fr": ["MTN YaMo", "Pitch"]}, {"en": "Season 4 · Douala", "fr": "Saison 4 · Douala"}),
    ("trophy", {"en": ["AWS Sports", "Cup"], "fr": ["AWS Sports", "Cup"]}, {"en": "Hackathon 2026", "fr": "Hackathon 2026"}),
    ("layers", {"en": ["No-Code", "training"], "fr": ["Formation", "No-Code"]}, {"en": "Orange Digital Center", "fr": "Orange Digital Center"}),
]

# ── Rubrique « Writing & content » : cartes de chaînes ─────────────────────
# Pour ajouter Medium, Dev.to, AWS Builder Center… : ajoute le logo dans LOGOS
# (extract_logos.py), une entrée ici, et son lien dans LINKS.
CHANNELS = [
    {"key": "tiktok", "name": "TikTok",
     "desc": {"en": "Short videos on cybersecurity and development, explained in plain language.",
              "fr": "Vidéos courtes sur la cybersécurité et le développement, expliquées simplement."},
     "cta": {"en": "Watch", "fr": "Voir"}},
    {"key": "linkedin", "name": "LinkedIn",
     "desc": {"en": "Posts on cloud, security and AI: what I learn, build and ship.",
              "fr": "Posts sur le cloud, la sécurité et l'IA : ce que j'apprends, construis et livre."},
     "cta": {"en": "Read", "fr": "Lire"}},
]

# ── Rubrique « Activity » (textes du tableau de bord) ──────────────────────
ACTIVITY_TEXT = {
    "contrib": {"en": "CONTRIBUTIONS · LAST YEAR", "fr": "CONTRIBUTIONS · 12 MOIS"},
    "commits": {"en": "COMMITS", "fr": "COMMITS"},
    "prs": {"en": "PULL REQUESTS", "fr": "PULL REQUESTS"},
    "streak": {"en": "CURRENT STREAK · DAYS", "fr": "SÉRIE EN COURS · JOURS"},
    "heat": {"en": "CONTRIBUTION GRAPH", "fr": "GRAPHIQUE DE CONTRIBUTIONS"},
    "langs": {"en": "TOP LANGUAGES", "fr": "LANGAGES PRINCIPAUX"},
    "mix": {"en": "ACTIVITY MIX", "fr": "RÉPARTITION DE L'ACTIVITÉ"},
    "less": {"en": "Less", "fr": "Moins"}, "more": {"en": "More", "fr": "Plus"},
    "mix_rows": {"en": ["Commits", "Pull requests", "Issues", "Code review"], "fr": ["Commits", "Pull requests", "Issues", "Revue de code"]},
    "waiting": {"en": "Waiting for the first sync. Run the “Refresh activity” workflow in the Actions tab.",
                "fr": "En attente de la première synchronisation. Lance le workflow « Refresh activity » dans l'onglet Actions."},
    "updated": {"en": "updated", "fr": "mis à jour le"},
    "days": ["Mon", "Wed", "Fri"], "days_fr": ["Lun", "Mer", "Ven"],
    "months": {"en": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
               "fr": ["Janv", "Févr", "Mars", "Avr", "Mai", "Juin", "Juil", "Août", "Sept", "Oct", "Nov", "Déc"]},
}
