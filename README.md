# 🖥️ InfraWatch

**Outil de monitoring et d'audit d'infrastructure léger, en Python.**
Conçu dans le cadre d'une formation en **infrastructure digitale** pour apprendre
à surveiller l'état d'un parc : CPU, mémoire, disque, réseau et services.

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Licence](https://img.shields.io/badge/licence-MIT-green)
![CI](https://github.com/TON_UTILISATEUR/infra-watch/actions/workflows/ci.yml/badge.svg)

---

## ✨ Fonctionnalités

- 📊 **Snapshot système** : CPU, RAM, disque, connexions réseau actives
- 🩺 **Vérification de services** (`systemctl is-active`, ex. `ssh`, `nginx`)
- 🚦 **Seuils d'alerte** configurables : `ok` → `warning` → `critical`
- 📄 **Rapport HTML** autonome (un seul fichier, aucune dépendance web)
- 🧩 **Sortie JSON** pour intégration à un SIEM ou un outil de supervision
- ✅ **Code testé** avec `pytest` + intégration continue GitHub Actions

## 🚀 Installation

```bash
git clone https://github.com/TON_UTILISATEUR/infra-watch.git
cd infra-watch
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 🛠️ Utilisation

```bash
# Rapport JSON sur stdout
python -m infra_watch

# Avec vérification de services et de plusieurs disques
python -m infra_watch --services ssh nginx --disks / /var --format html -o rapport.html

# Code de retour : 0 = tout va bien, 2 = métrique critique (pratique pour cron/CI)
```

Exemple de sortie JSON :

```json
{
  "hostname": "serveur-prod-01",
  "metrics": [
    {"name": "cpu_usage", "value": 12.4, "unit": "%", "status": "ok"},
    {"name": "memory_usage", "value": 83.1, "unit": "%", "status": "warning"},
    {"name": "service[nginx]", "value": 1.0, "unit": "bool", "status": "ok"}
  ]
}
```

## 🧪 Tests

```bash
pytest -v
```

## 🗺️ Roadmap

- [ ] Export Prometheus / métriques exposées sur `/metrics`
- [ ] Alertes par e-mail ou webhook (Slack / Discord)
- [ ] Mode daemon avec historique (SQLite)
- [ ] Dockerfile officiel

## 🧑‍💻 Auteur

Projet réalisé paron ADAM ELMANAOUAI (@thereal4dam)— stagiaire en infrastructure digitale.
Retours et suggestions bienvenus via les *issues* !

## 📄 Licence

Distribué sous licence MIT. Voir [LICENSE](LICENSE).
"# infra-watch" 
