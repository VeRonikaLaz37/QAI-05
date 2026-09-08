# QAI-05: QA Multi-Agent System

Мультиагентная система автоматизации QA-процесса. Анализирует требования из Confluence, создаёт задачи в Jira и проектирует тестовую модель в Qase.

---

## Архитектура

Система построена на платформе **OpenCode AI** и использует паттерн координатор + специализированные агенты:

| Агент | Тип | Назначение | Инструменты |
|-------|-----|-----------|-------------|
| `qa-orchestrator` | Primary | Координация workflow, Quality Gates, эскалация (HITL) | — |
| `requirement-agent` | Subagent | Систематическое ревью требований из Confluence | Confluence REST API |
| `task-agent` | Subagent | Декомпозиция требований в Jira-задачи | Jira Search / Create |
| `test-agent` | Subagent | Риск-ориентированный тест-дизайн, создание тест-кейсов | Qase Search / Create |

---

## Workflow

```
Confluence (requirements)
        │
        ▼
┌─────────────────────────┐
│  Requirement Analyst    │  Анализ требований, ревью, риски
│  → requirement-review.md│
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Task Designer          │  Декомпозиция в Jira-задачи
│  → jira-tasks.md        │
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Test Designer          │  Тест-дизайн, тест-кейсы в Qase
│  → test-model.md        │
└─────────────────────────┘
```

---

## Технологический стек

| Компонент | Технология |
|-----------|-----------|
| Платформа | OpenCode AI (`@opencode-ai/plugin@1.18.27`) |
| Custom Tools | TypeScript (Confluence REST API v2) |
| VCS | Git |
| Внешние системы | Confluence, Jira, Qase |

---

## Структура проекта

```
QAI-05/
├── AGENTS.md                    # Глобальные правила мультиагентной системы
├── README.md
├── .opencode/
│   ├── agents/                  # Определения агентов
│   │   ├── qa-orchestrator.md   # Координатор (primary)
│   │   ├── requirement-agent.md # QA-аналитик
│   │   ├── task-agent.md        # Архитектор задач
│   │   └── test-agent.md        # Инженер по тест-дизайну
│   ├── skills/                  # Навыки агентов
│   │   ├── requirement-review/  # Ревью требований
│   │   ├── task-design/         # Декомпозиция в Jira
│   │   └── test-design/         # Тест-дизайн для Qase
│   └── tools/                   # Custom Tool-интеграции
│       └── confluence.ts        # Confluence REST API v2
├── artifacts/                   # Промежуточные артефакты workflow
│   ├── requirement-review.md
│   ├── jira-tasks.md
│   └── test-model.md
└── venv/                        # Python virtualenv
```

---

## Конфигурация

### Агенты (`.opencode/agents/`)

Определяют роль, инструкции и ограничения каждого агента. Primary-агент (`qa-orchestrator`) координирует вызов subagent'ов и проверяет результаты.

### Skills (`.opencode/skills/`)

Структурированные инструкции для выполнения特定ных задач:
- **requirement-review** — 15-раздельный анализ требований с паттерном Self-Refine
- **task-design** — декомпозиция требований в Jira-задачи с проверкой дубликатов
- **test-design** — риск-ориентированный тест-дизайн с паттернами Self-Refine и Branching

### Tools (`.opencode/tools/`)

Custom Tool для чтения страниц Confluence:
- **confluence.ts** — GET-запрос к Confluence REST API v2
- Авторизация: Basic Auth (email + API token из env-переменных)

### AGENTS.md

Глобальные правила:
- Запрет на галлюцинации
- Правило 3 попыток (retry)
- Идемпотентность (проверка дубликатов)
- Partial failure (фиксация состояния)
- HITL-эскалация при критических неоднозначностях
- Артефакты в `/artifacts/`

---

## Артефакты

| Файл | Описание | Producer |
|------|----------|----------|
| `requirement-review.md` | Анализ требований: FR, BR, VR, Boundaries, Risks, Open Questions | `requirement-review` |
| `jira-tasks.md` | Аудит Jira-задач: существующие + созданные | `task-design` |
| `test-model.md` | Тест-кейсы в Qase: Positive/Negative/Boundary сценарии | `test-design` |

---

## Быстрый старт

### Прerequisites

- [Node.js](https://nodejs.org/) (для OpenCode plugin)
- OpenCode AI CLI
- Доступ к Confluence, Jira, Qase (credentials в env-переменных)

### Запуск

```bash
# Клонировать репозиторий
git clone <repo-url>
cd QAI-05

# Установить зависимости OpenCode plugin
cd .opencode && npm install && cd ..

# Запустить через OpenCode CLI
opencode "Получи Confluence страницу 884737 и выполни полный QA workflow"
```

### Env-переменные

```
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your-email
CONFLUENCE_API_TOKEN=your-token
```
