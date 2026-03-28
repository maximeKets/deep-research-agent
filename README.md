<div align="center">

# 🔍 Deep Research Agent : Analyse Concurrentielle

**Un système multi-agents autonome conçu pour réaliser une analyse de marché complète sur n'importe quelle entreprise et d'envoyer un rapport détaillé par email.**

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![OpenAI Agents SDK](https://img.shields.io/badge/OpenAI_Agents_SDK-0.13%2B-412991?logo=openai&logoColor=white)](https://openai.github.io/openai-agents-python/)
[![Gradio](https://img.shields.io/badge/Gradio-6.10%2B-orange?logo=gradio&logoColor=white)](https://www.gradio.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![uv](https://img.shields.io/badge/Packaged_with-uv-7C3AED)](https://github.com/astral-sh/uv)

</div>

---

## 📖 Overview

**Deep Research Agent** est un pipeline autonome de recherche spécialisé dans l'**Analyse Concurrentielle**, basé sur le **OpenAI Agents SDK**. Vous saisissez simplement le nom d'une entreprise (ex: Tesla, OpenAI), et le système :

1. 🗓️ **Planifie** une stratégie de recherche ciblée (concurrents, parts de marché, actus)
2. 🌐 **Recherche** sur le web avec des appels asynchrones parallèles
3. ✍️ **Rédige** un rapport Markdown structuré avec les données chiffrées
4. 📧 **Envoie** le rapport formaté en HTML directement dans votre boîte de réception via Mailtrap

Le système intègre  **une interface en temps réel**, une **authentification Hugging Face OAuth**, un **suivi des quotas d'utilisation**, et est protégé par des **guardrails**.

---

## ✨ Key Features

- **Spécialisation métier** : Prompts calibrés pour la veille concurrentielle.
- **Authentification & Quotas** : Intégration de `gr.LoginButton()` (HF OAuth) et limitation à 3 requêtes par utilisateur pour maîtriser les coûts.
- **Logs en Temps Réel** : Suivi de l'activité des agents et de l'exécution des outils en direct sur l'interface Gradio grâce au streaming asynchrone (`Runner.run_streamed`).
- **Orchestration Multi-Agents** (`Agent`, `Runner`, `handoffs`) et exécution asynchrone (`asyncio`).
- **Input Guardrail** : Bloque les attaques par injection de prompt ou les requêtes hors sujet.
- **Email End-to-End** : Envoi automatisé du rapport via SMTP.

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                       Gradio UI                             │
│       (gradio_ui.py + usage_tracker.py + HF OAuth)          │
└────────────────────────┬────────────────────────────────────┘
                         │ Nom de l'entreprise
                         ▼
              ┌──────────────────────┐
              │   Input Guardrail    │  ← Bloque requêtes malveillantes
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Research Manager   │  ← Orchestrateur central (gpt-4o-mini)
              │ (deep_research_....py)│
              └──┬───────────────┬───┘
                 │               │
        ┌────────▼───┐   ┌───────▼──────┐
        │  Planner   │   │ Search Agent │ × N (async)
        │   Agent    │   │  WebSearch   │
        └────────────┘   └──────┬───────┘
                                │ Résumés de recherche
                         ┌──────▼───────┐
                         │ Writer Agent │  → Rapport final Markdown
                         └──────┬───────┘
                                │ Handoff
                         ┌──────▼───────┐
                         │ Email Agent  │  → Envoi SMTP (Mailtrap)
                         └──────────────┘
```

### Rôle des Agents

| Agent | Fichier | Rôle |
|---|---|---|
| **Research Manager** | `deep_research_manager.py` | Orchestrateur central — lance la planification, la recherche, délègue la rédaction. |
| **Planner Agent** | `planner_agent.py` | Décompose le nom de l'entreprise en requêtes ciblées (parts de marché, concurrents). |
| **Search Agent** | `search_agent.py` | Recherche sur le web et résume les résultats trouvés. |
| **Writer Agent** | `writer_agent.py` | Synthétise les données techniques en un rapport concurrentiel Markdown. |
| **Email Agent** | `email_agent.py` | Convertit le rapport en HTML et l'envoie. |

---

## 🚀 Getting Started

### Prérequis

- Python **3.12+**
- [`uv`](https://github.com/astral-sh/uv)
- Profil **Hugging Face** (pour l'authentification OAuth locale/en ligne)
- Clé **OpenAI API**
- Compte **[Mailtrap](https://mailtrap.io/)** (plan gratuit)

### Installation & Lancement

1. **Cloner le repo**
```bash
git clone https://github.com/maximeKets/deep-research-agent.git
cd deep-research-agent
```

2. **Installer les dépendances**
```bash
uv sync
```

3. **Variables d'environnement** (`.env`)
```env
OPENAI_API_KEY=sk-...
MAILTRAP_USERNAME=votre_username
MAILTRAP_PASSWORD=votre_password
```

4. **Lancer l'application**
```bash
uv run python gradio_ui.py
```
> *L'interface web Gradio s'ouvrira (ou vous donnera un lien local). Connectez-vous avec votre profil Hugging Face pour tester l'architecture limitant les abus (3 recherches max).*

---

## 📂 Structure du Projet

```text
deep-research-agent/
├── gradio_ui.py            # Entry point: Interface Gradio, Logs temps-réel, Auth HF
├── deep_research_manager.py# Orchestrateur (Manager Agent)
├── usage_tracker.py        # Suivi local des limites utilisateurs (rate limiting)
├── planner_agent.py        # Agent planificateur
├── search_agent.py         # Agent de recherche internet
├── writer_agent.py         # Agent de synthèse/rédaction
├── email_agent.py          # Agent d'envoi d'email
├── guardrails_config.json  # Configuration des limites d'input (sécurité)
├── pyproject.toml          # Dépendances (uv)
└── usage_db.json           # Fichier généré localement stockant les quotas
```

---

<div align="center">
  Made with ❤️ and lots of async/await
</div>
