# 🔬 IDR — OnlyFans Media-Vault-Downloader (eigenes Vault sichern, möglichst billig)

**Stand:** 2026-06-23 · **Engine:** 🦀 CC Opus 4.8 (inline WebSearch — NotebookLM-MCP war disconnected) · **Scope:** Tools um das **EIGENE** OnlyFans Media-Vault komplett herunterzuladen (Creator-Backup, kein Fremd-Scraping). Ziel: möglichst **billig / OSS / datenschutzsicher**.

> 🧭 **Wichtigste Erkenntnis zuerst:** Es gibt ZWEI verschiedene Tool-Klassen, die oft verwechselt werden:
> - **(A) Creator-eigenes-Vault** — greift auf DEIN hochgeladenes Vault zu (inkl. unveröffentlichte Vault-Listen). Das willst du. → nur wenige Tools (Vault Downloader, Vault Scraper, ofauth-API-DIY).
> - **(B) Fan-Side-Scraper** — lädt Inhalte von Accounts, die DU abonniert hast (veröffentlichte Posts/Medien). Das sind die meisten OSS-GitHub-Tools (OF-Scraper & Co.). Die greifen **NICHT** auf die Vault-API zu.
>
> 👑 **Empfehlung: DIY über die ofauth-API** (Klasse A, gratis, OSS-scriptbar, eigener Key, voller Vault-Zugriff, kein Login-Creds-Abgreifen). Du hast den ofauth-Zugang eh schon (für die Matrix-Bridge).

---

## 1. Feature-Matrix — Top-Kandidaten

**Wertung (100):** Vault-Coverage (eigenes Vault!) 30 · Preis/OSS 25 · Wartung/Aktiv 15 · Sicherheit/Datenschutz 15 · Einfachheit 15

| # | Tool · Link | Klasse | Typ | Lizenz | Preis | Eigenes-Vault? | Datenschutz | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | **ofauth-API DIY** · [docs.ofauth.com](https://ofauth.com) (Vault+Lists-Endpoints) | **A** | API/Script | OSS (dein Code) | **gratis** (ofauth-Key, evtl. API-Kosten) | ✅ voll (Vault-Listen-API) | 🟢 eigener Key, lokal | **92** 👑 |
| 2 | **Vault Downloader** · [vaultdownloader.com](https://vaultdownloader.com) · [Chrome](https://chrome-stats.com/d/mhnaomjciifmgkgdelefbghmlhijfina) · [OFX](https://ofx.gumroad.com/l/vaultdownloader) | **A** | Chrome-Ext | Closed | bezahlt (Free-Trial = nur Preview, DL gesperrt); Abo „1 Monat" | ✅ ja (Vault-Listen, nach Datum, Ordner je Liste/Typ) | 🟠 läuft im eigenen Browser, aber Closed | **74** |
| 3 | **OnlyFans Vault Scraper** · [vaultscraper.com](https://vaultscraper.com) | **A** | Web-Service | Closed | bezahlt (Preis nicht öffentlich) | ✅ ja (Bulk-Vault-Export) | 🔴 Web-Service will Login → Creds-Risiko | **55** |
| 4 | **OnlyMonster Vault Mgmt** · [docs.onlymonster.ai](https://docs.onlymonster.ai/members-features/vault-management) | **A** | Creator-Suite | Closed | bezahlt (Suite-Abo) | ✅ ja (Teil der Suite) | 🟠 Suite | **52** |
| 5 | **OF-Scraper (datawhores)** · [github.com/datawhores/OF-Scraper](https://github.com/datawhores/OF-Scraper) · [PyPI ofscraper](https://pypi.org/project/ofscraper/) | **B** | CLI (Python) | OSS | **gratis** | 🟠 nur veröffentlichte Posts deines Accounts, NICHT Vault-API | 🟢 lokal, eigener Login | **70** (für Klasse B) |
| 6 | **ofdl/ofdl** · [github.com/ofdl/ofdl](https://github.com/ofdl/ofdl) | **B** | CLI (self-contained, Aria2/Stash) | OSS | gratis | 🟠 Fan-Side | 🟢 lokal | 66 |
| 7 | **Fansly-OF-Downloader** · [github.com/Frangus90/Fansly-OF-Downloader](https://github.com/Frangus90/Fansly-OF-Downloader) | **B** | GUI+CLI dual-platform | OSS | gratis | 🟠 Fan-Side (dedup/inkrementell) | 🟢 lokal | 64 |
| 8 | **onlyfans-scraper** · [github.com/TrendingTechnology/onlyfans-scraper](https://github.com/TrendingTechnology/onlyfans-scraper) | **B** | CLI | OSS | gratis | 🟠 Fan-Side (älter) | 🟢 lokal | 58 |
| 9 | **OFDL GUI (Hashirama)** · [github.com/Hashirama/OFDL](https://github.com/Hashirama/OFDL) | **B** | GUI (PyQt5) | OSS | gratis | 🟠 Fan-Side | 🟢 lokal | 55 |
| 10 | **mediadown/Onlyfans-Downloader** · [github.com/mediadown/Onlyfans-Downloader](https://github.com/mediadown/Onlyfans-Downloader) | **B** | Chrome | OSS-ish | gratis | 🟠 Post-Content | 🟠 Ext | 48 |
| — | locoloader.com | B | Web | Closed | freemium | ❌ Einzel-Post, kein Vault | 🔴 Web | 30 (raus) |

> ⭐-Stars nicht zuverlässig live abrufbar (kein API-Call gemacht) — Links zum Selbst-Prüfen angegeben, keine erfundenen Zahlen.

---

## 2. 👑 Gewinner + Begründung

**👑 #1 — DIY über die ofauth-API (Score 92).** Billigster + sicherster Weg für DEIN eigenes Vault:
- **Echter Vault-Zugriff** (die ofauth-API hat Vault+Lists-Endpoints — genau die unveröffentlichten Vault-Medien, die Fan-Scraper NICHT sehen).
- **Gratis/OSS** — du scriptest es selbst (ein kleines Python/Node-Script: Vault-Listen paginieren → Media-URLs → herunterladen), **eigener API-Key**, **kein Closed-Service der deine OF-Login-Creds abgreift**.
- Du hast den ofauth-Zugang **schon** (für die `ofauth-matrix-bridge`) → quasi 0 Zusatzkosten.

**🥈 Wenn du KEIN Script willst → Vault Downloader (Chrome-Ext, Score 74):** das einzige fertige Tool, das gezielt das **Creator-Vault** abdeckt (nach Datum, Ordner je Liste/Typ). Aber **closed + bezahlt** (Free-Trial lädt nicht runter, nur Preview) + Closed-Source = Vertrauens-/Datenschutz-Abwägung.

**Finger weg / Vorsicht:** reine **Web-Services** (vaultscraper.com etc.), die deinen OnlyFans-**Login** verlangen → 🔴 Creds-Risiko/Account-Ban-Gefahr. Die **OSS-Fan-Scraper** (OF-Scraper & Co.) sind super, aber **fürs eigene VAULT das falsche Werkzeug** (sie laden veröffentlichte Posts, nicht die Vault-API).

---

## 3. ⚠️ Risiko-Box (Pflicht)
- Nur fürs **EIGENE** Vault/Backup gedacht (deine hochgeladenen Inhalte). Fremd-Scraping = rechtlich/ToS heikel.
- **OnlyFans-ToS:** automatisiertes Scraping kann gegen die ToS verstoßen → im Zweifel Account-Risiko. ofauth-API ist die „offiziellere" Schicht (genutzt von Bridges), trotzdem inoffiziell.
- **Datenschutz:** OSS + lokal (DIY/ofauth) >> Closed-Web-Service (der deine Login-Daten sieht). Niemals OF-Passwort in einen fremden Web-Dienst eingeben.

> 🤖 Manager-IDR · WebSearch-verifiziert (Links oben) · keine erfundenen Tools/Stars · NotebookLM-MCP war offline → reine Web-Recherche.
