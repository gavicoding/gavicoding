# Hi, I'm Gabriel Souza (`@gavicoding`) 👋

**IT Automation & Software Engineer | Applied AI & Data Privacy (LGPD/GDPR)**

I design and build resilient production tools across **Python, TypeScript, and C# (.NET)** — turning repetitive IT operations, distributed retail/warehouse bottlenecks, and compliance risks into automated, observable, and secure software.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![C# / .NET 8](https://img.shields.io/badge/.NET_8-512BD4?style=flat-square&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-CC2927?style=flat-square&logo=microsoftsqlserver&logoColor=white)](https://www.microsoft.com/sql-server)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Google Cloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat-square&logo=googlecloud&logoColor=white)](https://cloud.google.com/)

---

## 🔧 What I Build

- **IT Fleet & Operations Automation:** Windows services, remote agents with mutual TLS (mTLS), unattended desktop migrations, and automated sales/sync recovery workflows.
- **Infrastructure Mapping & Observability:** End-to-end service dependency topology maps, read-only database replication monitors, trend-based alerting heuristics, and operational picking/throughput KPIs.
- **Applied AI & Zero-Trust DLP:** Multimodal AI pipelines paired with deterministic & vision-based Data Loss Prevention (LGPD/GDPR PII, tokens, and internal IP guardrails) + GitHub PR API auditing.
- **Native Windows Engineering:** MVVM desktop applications in .NET 8 + WPF and standalone PyInstaller utilities built for non-technical end users and IT support teams.

---

## 🚀 Featured Open-Source Projects

| Project | Stack | Description |
| :--- | :--- | :--- |
| **[pii-screenshot-guard](https://github.com/gavicoding/pii-screenshot-guard)** ([Docs](https://gavicoding.github.io/pii-screenshot-guard/)) | Python · CLI · GitHub API · OCR/Vision · Docker | Zero-Trust DLP scanner, redactor & GitHub PR diff auditor catching LGPD/GDPR PII (mod-11 CPF/CNPJ, Luhn cards), API secrets, and RFC 1918 internal IPs in logs, PRs, and screenshots. |
| **[queue-health-watchdog](https://github.com/gavicoding/queue-health-watchdog)** | TypeScript · Node.js · Docker | Read-only replication & job queue monitor with snapshot trend heuristics (distinguishing active `HIGH_LOAD` from `STALLED` queues), cooldown alert throttling, webhooks, and a live status dashboard. |
| **[OtimizaPC](https://github.com/gavicoding/OtimizaPC)** | C# · .NET 8 · WPF (MVVM) | Dark-mode Windows system optimizer with System Restore Points, multi-profile cleanup, content-hash duplicate finder, 90-day orphan residue detection, S.M.A.R.T. health, and instant disk space analysis. |
| **[Thunderbird-Outlook](https://github.com/gavicoding/Thunderbird-Outlook)** | Python · COM · SQLite · vCard 3.0 | Bidirectional Windows email & address-book migrator preserving folder trees, original received dates (`MSGFLAG_UNSENT` / MAPI), senders, attachments, and long file paths (`\\?\`). |

---

## 🗺️ Visual Architecture Highlights (Sanitized)

### Distributed Infrastructure Topology, Fleet Control & ERP Sync Observability

```mermaid
flowchart LR
    subgraph EDGE["Distributed Stores & Warehouse Ops"]
        POS["POS / Store Servers\n(100+ Endpoints)"]
        WH["Warehouse Picking &\nFulfillment Ops"]
        DVR["Store DVRs / NVRs"]
    end

    subgraph OBSERVE["Control Plane, Topology & Watchdogs"]
        AGENT["Windows Fleet Agent\n(WebSockets + mTLS)"]
        TOPO["Infrastructure & Service\nTopology Map"]
        WATCH["Read-Only ERP Replication\n& Sales Retransmission Watchdog"]
        KPI["Picking Performance &\nThroughput Analytics"]
    end

    subgraph ACTION["Automated Actions & Alerts"]
        ALERTS["Proactive Alerts\n(Email / Webhook / Recovery)"]
        ITSM["ITSM Ticket\nOrchestration"]
    end

    POS <-->|"mTLS Heartbeat & Commands"| AGENT
    POS -->|"Queue Snapshots (Read-Only)"| WATCH
    WH -->|"Stage & Separation Telemetry"| KPI
    AGENT --> TOPO
    WATCH --> TOPO
    DVR -->|"Evidence Sync"| ITSM
    WATCH -->|"STALLED / Bottleneck"| ALERTS
    TOPO -->|"Root-Cause Isolation"| ITSM
```

### Applied AI & Zero-Trust DLP Pipeline

```mermaid
flowchart LR
    IN["Voice Notes / Logs /\nPR Diffs / Screenshots"] --> GATE["Zero-Trust DLP Gate\n(Mod-11 + Luhn + Secret Regex + Vision)"]
    GATE -->|"Sensitive Data Found"| MASK["Block / Redact\n& Masked Alert"]
    GATE -->|"Verified Clean"| AI["AI Orchestration\n(Gemini / Vertex AI)"]
    AI --> OUT["Structured Outputs /\nAutomated Publishing"]
```

---

## 🏗️ Selected Private Production Architectures (Sanitized Case Studies)

> Many of my daily production systems run in private corporate environments and remain strictly private. Below are architectural summaries of systems I engineered end-to-end:

### 1. Infrastructure & Service Dependency Topology Map
- **Challenge:** Distributed retail environments often struggle during outages because teams cannot quickly see how stores, departments, hosts, and background services depend on each other.
- **Architecture:** Built a unified **infrastructure & service topology map** linking distributed store locations, operational sectors, host nodes, and running services — enabling rapid fault correlation, dependency visualization, and root-cause isolation.

### 2. Automated Sales Retransmission & Sync Recovery
- **Challenge:** Intermittent store connectivity and validation errors caused recurring bottlenecks in sales retransmission between POS/store databases and the central ERP.
- **Architecture:** Engineered an automated detection and **sales retransmission pipeline** that identifies stalled batches, pinpoints failing records early, executes safe recovery/retransmission workflows, and dispatches proactive alerts before manual escalation.

### 3. Warehouse Picking & Operational Performance Analytics
- **Challenge:** Lack of granular operational metrics made it difficult to measure order separation (picking) throughput, queue delays, and sector efficiency.
- **Architecture:** Built performance tracking and bottleneck analytics around warehouse separation/picking stages, surfacing actionable KPIs to support faster fulfillment and data-driven operational adjustments.

### 4. Multi-Store Windows Fleet Management Agent (`100+ Endpoints`)
- **Challenge:** Standardize monitoring, diagnostics, and controlled remote actions across hundreds of distributed retail workstations, POS terminals, and store servers.
- **Architecture:** Windows service agent (`NSSM` / `LocalSystem`) communicating over persistent **WebSockets secured with mTLS** to a **FastAPI + PostgreSQL** central control plane, featuring heartbeat telemetry, remote commands, self-updates, watchdogs, and anti-tamper protections.

### 5. Read-Only ERP Replication Watchdog
- **Challenge:** Detect stuck HQ ↔ Store database replication queues early without ever writing to production ERP tables or flooding IT support with false alarms during peak hours.
- **Architecture:** **TypeScript + Prisma** polling worker capturing periodic snapshots of SQL Server replication tables (`read-only`), distinguishing `HIGH_LOAD` from `STALLED` via trend heuristics, with throttled alerting.

### 6. ITSM + CCTV Evidence Automation Pipeline
- **Challenge:** Eliminate manual ticket triage and manual camera footage retrieval across dozens of distributed store NVRs/DVRs.
- **Architecture:** **Python** orchestrator integrating ITSM ticketing APIs with heterogeneous DVR/NVR HTTP APIs & fallback automation, complete with retry queues for intermittent store connectivity and automated ticket updates.

### 7. AI Workflow Copilot with Vision DLP Gate
- **Challenge:** Turn raw voice notes, RSS feeds, and screenshots into structured technical posts safely without risking credential or internal infrastructure exposure.
- **Architecture:** Async **Python** service deployed via **Docker / Cloud Run**, integrating Gemini/Vertex AI, PostgreSQL, OAuth 2.0 publishing, and an automated Vision DLP audit layer that blocks screenshots containing leaked tokens, emails, or internal IPs.

---

## 🌎 Collaboration & Availability

- **Working Style:** Remote · Async-first · Clear technical writing in **English** and **Portuguese**
- **Focus Areas:** IT Automation, Backend/Platform Engineering (Python / TypeScript), Windows Tooling (.NET / Python), Applied AI & Privacy Engineering (LGPD/GDPR)
- **GitHub:** [@gavicoding](https://github.com/gavicoding)

---

<details>
<summary>🇧🇷 Resumo em Português (Clique para expandir)</summary>

### Gabriel Souza (`@gavicoding`) — Engenharia de Software, Automação de TI & IA Aplicada

Desenvolvo sistemas de produção e ferramentas de automação com foco em **Python, TypeScript e C# (.NET)** — resolvendo gargalos reais de operação de TI, infraestrutura distribuída, observabilidade e segurança/privacidade de dados (LGPD/GDPR).

- **Projetos Open-Source em Destaque:**
  - [`pii-screenshot-guard`](https://github.com/gavicoding/pii-screenshot-guard) ([Documentação](https://gavicoding.github.io/pii-screenshot-guard/)): Scanner, redator e auditor de PRs via API do GitHub com foco em Zero-Trust DLP (LGPD/GDPR, CPF/CNPJ com dígito verificador, cartões Luhn, chaves de API, IPs internos e OCR/Vision).
  - [`queue-health-watchdog`](https://github.com/gavicoding/queue-health-watchdog): Monitor somente leitura de filas/replicação em TypeScript com heurística de tendência (diferencia `HIGH_LOAD` de `STALLED`), throttling de alertas, webhooks e dashboard ao vivo.
  - [`OtimizaPC`](https://github.com/gavicoding/OtimizaPC): Otimizador nativo para Windows em .NET 8 + WPF (MVVM), com pontos de restauração, limpeza multi-usuário, busca de duplicados por hash e análise instantânea de disco.
  - [`Thunderbird-Outlook`](https://github.com/gavicoding/Thunderbird-Outlook): Migrador bidirecional de e-mails e contatos entre Thunderbird e Outlook Clássico preservando datas originais, remetentes e caminhos longos no Windows.

- **Experiência em Arquiteturas Corporativas (Casos Sanitizados):**
  - **Mapa de Topologia de Infraestrutura & Serviços:** mapeamento conectando lojas, setores, servidores e serviços ativos para detecção rápida de falhas e isolamento de causa raiz.
  - **Automação de Retransmissão de Vendas:** detecção proativa de gargalos de transmissão entre lojas/PDVs e ERP central com fluxos automáticos de recuperação e alertas.
  - **Analytics de Performance na Separação (Picking):** visibilidade operacional de etapas, filas e indicadores de produtividade logística.
  - **Agente de Gerenciamento de Frota Windows (`100+ máquinas`):** serviço Windows via WebSockets com mTLS, painel FastAPI + PostgreSQL e watchdogs.
  - **Monitor Somente Leitura de Replicação SQL Server:** heurística anti-falso-positivo e alertas com cooldown.
  - **Orquestrador ITSM + CFTV:** automação de coleta de evidências em DVRs/NVRs com fila de retentativas e atualização automática de chamados.
  - **Copiloto Assíncrono de Conteúdo com Vision DLP:** pipeline Docker/Cloud Run com auditoria visual automática antes da publicação.

</details>
