# Test Model Artifact — Конфигуратор раскроя сэндвич панелей

| Поле | Значение |
|---|---|
| **Producer** | Test Designer (Agent Instruction, skill `test-design`) |
| **Входной артефакт** | `requirement-review.md` (Requirement Review Artifact, validated) |
| **Traceability к Jira** | `jira-tasks.md`: Q0-18 (J-1), Q0-19 (J-2), Q0-20 (J-3), Q0-21 (J-4), Q0-22 (J-5), Q0-23 (J-6), Q0-24 (J-7) |
| **Qase project** | **QT2** — QAI-05 (выбран: единственный проект, соответствующий workspace QAI-05; «qase_test» QT — не подходит) |
| **Дата** | 2026-09-22 |

---

## 0. Структура сьютов Qase (QT2)

| Suite ID | Title |
|---|---|
| 7 | Конфигуратор раскроя сэндвич панелей (root) |
| 8 | Настройки категории (FR-7) |
| 9 | Выбор продукта (FR-1) |
| 10 | Форма ввода (FR-2) |
| 11 | Расчёт площади (FR-3) |
| 12 | Расчёт стоимости (FR-4) |
| 13 | Валидация размеров (FR-6) |
| 14 | Корзина (FR-5) |
| 15 | Risk-based проверки |

Тестовые данные (фиксируются как входные, НЕ как бизнес-поведение):
- продукт: `product_id=52098`, `product_category_id=13551` (из примера тела запроса SR-1);
- габариты листа продукта: 3000 × 1500 (тестовые; совпадение «листа» и атрибутов продукта — открытый вопрос MIS-4);
- настройки категории: `min_width=100`, `min_length=100` (FR-7);
- `cost_one_rub = 250` (тестовое значение; источник — MIS-2/AMB-6, открытый вопрос).

---

## 1. Тест-кейсы

### 1.1 Настройки категории (FR-7) — suite 8

**L-01 / Qase 68** — Переход в категорию: получение настроек конфигуратора min_width=100, min_length=100
- Source Requirement: FR-7, BR-4, VR-4, PF-1, DEP-1 (Jira Q0-18)
- Priority: MEDIUM | Type: positive
- Preconditions: пользователь авторизован; категория сэндвич-панелей с настроенным конфигуратором; min_length=100, min_width=100.
- Steps/Test Intent: перейти в категорию → проверить полученные настройки → проверить применение минимумов в полях формы.
- Expected Result: настройки получены: min_length=100, min_width=100; поля ширины/длины используют минимумы 100.
- Risk Reference: — | Open Questions: — (настройки конкретной категории не тестируются как отдельные значения; FR-7 фиксирует min=100/100)

### 1.2 Выбор продукта (FR-1) — suite 9

**L-02 / Qase 69** — Выбор продукта из списка и отображение габаритов length/width
- Source Requirement: FR-1, PF-2, DEP-4 (Jira Q0-19)
- Priority: MEDIUM | Type: positive
- Preconditions: категория открыта; настройки получены; продукт product_id=52098 (лист 3000×1500).
- Steps/Test Intent: открыть список → выбрать продукт → проверить отображение length/width → проверить использование выбранного продукта в расчёте/валидации.
- Expected Result: продукт выбран; отображаются атрибуты length и width продукта; продукт используется как источник габаритов листа.
- Risk Reference: — | Open Questions: MIS-4 (совпадение «листа» и атрибутов продукта) — тестовое допущение.

### 1.3 Форма ввода (FR-2) — suite 10

**L-03 / Qase 70** — Заполнение полей ширины, длины и количества в форме конфигуратора
- Source Requirement: FR-2, PF-3 (Jira Q0-20)
- Priority: MEDIUM | Type: positive
- Preconditions: выбран продукт; настройки получены.
- Steps/Test Intent: выбрать продукт → ввести width=1200, length=1200, quantity=4 → проверить сохранение значений в форме.
- Expected Result: поля принимают значения; значения сохраняются в состоянии формы.
- Risk Reference: — | Open Questions: поле «маркировка» не проверяется (CON-1) — см. L-04.

**L-04 / Qase 71** — Ввод маркировки: обязательность, формат и передача в корзину (**BLOCKED**)
- Source Requirement: FR-2, AMB-2, CON-1, MIS-3 (Jira Q0-20)
- Priority: MEDIUM | Type: не определён (blocked) | Status в Qase: Draft
- Preconditions: выбран продукт; форма открыта.
- Steps/Test Intent: заполнить размеры → ввести маркировку → добавить в корзину → проверить тело запроса.
- Expected Result: **НЕ ОПРЕДЕЛЕНО — REQUIRES_HUMAN_DECISION.** FR-2 требует поле «маркировка», но в подтверждённом примере тела запроса поля маркировки нет (CON-1); формат и обязательность не определены (AMB-2, MIS-3, OQ-3).
- Risk Reference: — | Open Questions/Blocker: CON-1, AMB-2, MIS-3, OQ-3.

### 1.4 Расчёт площади (FR-3) — suite 11

**L-05 / Qase 72** — Автоматический расчёт площади: площадь = ширина × длина
- Source Requirement: FR-3, BR-1, PF-3, DEP-2 (Jira Q0-21)
- Priority: HIGH | Type: positive
- Preconditions: выбран продукт; width=1200, length=1200, quantity=4.
- Steps/Test Intent: ввести размеры → проверить автоматическую площадь.
- Expected Result: площадь = 1200 × 1200 = 1 440 000 (в единицах ввода²); ручной ввод площади невозможен (BR-1).
- Risk Reference: — | Open Questions: AMB-1/OQ-1 (единицы измерения; отображаемые единицы не утверждаются).

**L-06 / Qase 73** — Граница минимума: расчёт площади при размерах 100×100
- Source Requirement: FR-3, BR-4 (граница min) (Jira Q0-21)
- Priority: HIGH | Type: boundary
- Preconditions: продукт с листом не менее 100×100.
- Steps/Test Intent: ввести width=100, length=100 → проверить площадь.
- Expected Result: площадь = 100 × 100 = 10 000 (ед.²), рассчитана автоматически; ошибок нет.
- Risk Reference: — | Open Questions: — (граничное значение из FR-7)

### 1.5 Расчёт стоимости (FR-4) — suite 12

**L-07 / Qase 74** — Автоматический расчёт стоимости: стоимость = площадь × cost_one_rub
- Source Requirement: FR-4, BR-2, PF-4, DEP-3 (Jira Q0-22)
- Priority: HIGH | Type: positive
- Preconditions: площадь рассчитана; бэкенд возвращает cost_one_rub=250 (тестовое значение; источник — MIS-2/AMB-6, не проверяется).
- Steps/Test Intent: ввести width=1200, length=1200 → проверить стоимость.
- Expected Result: стоимость = площадь × cost_one_rub = 1,44 × 250 = 360 (при допущении единиц мм (AMB-1) и трактовки cost_one_rub за м² (AMB-6)); формула соответствует BR-2.
- Risk Reference: — | Open Questions: AMB-1, AMB-6, MIS-2, OQ-2 (влияют на числовое ожидание; само поведение — подтверждённая формула).

### 1.6 Валидация размеров (FR-6) — suite 13

**L-08 / Qase 77** — Валидные размеры (прямая ориентация) — валидация пройдена
- Source Requirement: FR-6, BR-3, VR-3, PF-5 (Jira Q0-23)
- Priority: HIGH | Type: positive
- Preconditions: продукт/лист 3000×1500; min=100/100.
- Steps/Test Intent: ввести width=1200, length=1200 (1200 ≤ 3000, 1200 ≤ 1500) → фронт → бэк.
- Expected Result: фронт и бэк принимают размеры; ошибок нет.
- Risk Reference: — | Open Questions: MIS-7 (тексты ошибок) — проверяется факт прохождения.

**L-09 / Qase 78** — Изделие вписывается в лист только с поворотом — валидация пройдена
- Source Requirement: FR-6, BR-3, VR-3 (поворот), RK-4 (Jira Q0-23)
- Priority: HIGH | Type: positive
- Preconditions: продукт/лист 3000×1500.
- Steps/Test Intent: ввести width=1000, length=2800 (прямая не помещается: 2800 > 1500; повёрнутая помещается: 2800 ≤ 3000, 1000 ≤ 1500) → фронт → бэк.
- Expected Result: фронт и бэк принимают — изделие вписывается с учётом поворота (подтверждено BR-3/VR-3: допустимы обе ориентации).
- Risk Reference: RK-4 | Open Questions: AMB-3/OQ-4 (кто управляет поворотом — пользователь/система; в сценарии не утверждается, проверяется только подтверждённая допустимость обоих вариантов).

**L-10 / Qase 79** — Ширина меньше минимума (99 < min_width 100) — ошибка на фронте и бэке
- Source Requirement: FR-6, VR-1, NF-1, BR-4 (Jira Q0-23)
- Priority: HIGH | Type: negative
- Preconditions: min_width=100.
- Steps/Test Intent: ввести width=99, length=1200 → попытка добавить/запрос.
- Expected Result: фронт — ошибка валидации; бэк отклоняет; в корзину не добавляется (DEP-5).
- Risk Reference: — | Open Questions: MIS-7 (конкретный текст ошибки не утверждается).

**L-11 / Qase 80** — Длина меньше минимума (99 < min_length 100) — ошибка на фронте и бэке
- Source Requirement: FR-6, VR-2, NF-2, BR-4 (Jira Q0-23)
- Priority: HIGH | Type: negative
- Preconditions: min_length=100.
- Steps/Test Intent: ввести width=1200, length=99 → попытка добавить/запрос.
- Expected Result: фронт — ошибка валидации; бэк отклоняет; в корзину не добавляется.

**L-12 / Qase 81** — Изделие не помещается на лист ни в одной ориентации — ошибка валидации
- Source Requirement: FR-6, VR-3, NF-3, BR-3 (Jira Q0-23)
- Priority: HIGH | Type: negative
- Preconditions: продукт/лист 3000×1500.
- Steps/Test Intent: ввести width=1600, length=1600 (1600 > 1500 в обоих вариантах) → попытка добавить.
- Expected Result: фронт — ошибка; бэк отклоняет; в корзину не добавляется.

**L-13 / Qase 82** — Граница минимума: ровно min_width=100 и min_length=100 — валидация пройдена
- Source Requirement: FR-6, BR-4, VR-1, VR-2 (граница min=100) (Jira Q0-23)
- Priority: HIGH | Type: boundary
- Preconditions: продукт/лист 3000×1500; min=100/100.
- Steps/Test Intent: ввести width=100, length=100 → фронт → бэк.
- Expected Result: ошибок нет; бэк принимает; добавление возможно.

**L-14 / Qase 83** — Граница листа: размеры ровно равны габаритам листа с поворотом — валидация пройдена
- Source Requirement: FR-6, VR-3, BR-3 (граница == лист) (Jira Q0-23)
- Priority: MEDIUM | Type: boundary
- Preconditions: продукт/лист 3000×1500.
- Steps/Test Intent: ввести width=1500, length=3000 (3000 ≤ 3000, 1500 ≤ 1500 — точное равенство).
- Expected Result: фронт и бэк принимают (граничное равенство допустимо).

**L-15 / Qase 84** — Граница листа: размер на 1 ед. больше габаритов листа — ошибка валидации
- Source Requirement: FR-6, VR-3, BR-3 (граница: 1 ед. сверх листа) (Jira Q0-23)
- Priority: MEDIUM | Type: boundary/negative
- Preconditions: продукт/лист 3000×1500.
- Steps/Test Intent: ввести width=1501, length=3000 (1501 > 1500 в обоих вариантах).
- Expected Result: фронт — ошибка; бэк отклоняет; в корзину не добавляется.

### 1.7 Корзина (FR-5) — suite 14

**L-16 / Qase 85** — Добавление в корзину валидного изделия: параметры сохраняются
- Source Requirement: FR-5, PF-5, DEP-5 (Jira Q0-24)
- Priority: MEDIUM | Type: positive
- Preconditions: product_id=52098, product_category_id=13551; width=1200, length=1200, quantity=4; валидация пройдена.
- Steps/Test Intent: «Добавить в корзину» → проверить состав сохраняемых параметров.
- Expected Result: запрос успешен; сохранены configurator=sandwich_m2, product_id=52098, product_category_id=13551, quantity=4, width=1200, length=1200 (подтверждённый пример тела запроса).
- Risk Reference: — | Open Questions: маркировка отсутствует в подтверждённом примере (CON-1) — см. L-04.

**L-17 / Qase 86** — Добавление в корзину с невалидными размерами отклоняется, параметры не сохраняются
- Source Requirement: FR-5, NF-4, DEP-5, FR-6 (Jira Q0-24, Q0-23)
- Priority: MEDIUM | Type: negative
- Preconditions: width=50, length=1200 (width < min_width 100).
- Steps/Test Intent: попытка добавления (при пропуске фронта или прямым запросом) → проверка корзины.
- Expected Result: запрос отклонён (бэк-валидация); параметры не сохраняются.

### 1.8 Risk-based проверки — suite 15

**L-18 / Qase 75** — [Risk] Округление и точность расчёта при дробной площади/стоимости
- Source Requirement: FR-4, BR-2 | Risk: RK-2 (Jira Q0-22)
- Priority: HIGH | Type: risk-based
- Preconditions: cost_one_rub=250 (тест.); продукт выбран.
- Steps/Test Intent: ввести width=1150, length=1150 → площадь 1,3225 м² → проверить стоимость → проверить отображение.
- Expected Result: стоимость = 1,3225 × 250 = 330,625 — точное произведение без потери точности (BR-2). Правила округления/отображения не определены (MIS-6/OQ-8) — проверка отображения REQUIRES_HUMAN_DECISION, в тесте не утверждается.
- Risk Reference: RK-2 | Open Questions: MIS-6, OQ-8.

**L-19 / Qase 76** — [Risk] Трактовка cost_one_rub: за м² изделия vs за м² листа (**BLOCKED**)
- Source Requirement: FR-4 | Risk: RK-3 (Jira Q0-22)
- Priority: HIGH | Type: risk-based | Status в Qase: Draft
- Preconditions: требуется определённый источник и назначение cost_one_rub.
- Steps/Test Intent: сравнить расчёт при трактовке «за м² изделия» vs «за м² листа»; определить источник значения.
- Expected Result: **НЕ ОПРЕДЕЛЕНО — REQUIRES_HUMAN_DECISION.** Источник и назначение cost_one_rub не описаны (MIS-2, AMB-6, OQ-2).
- Risk Reference: RK-3 | Open Questions/Blocker: MIS-2, AMB-6, OQ-2.

**L-20 / Qase 87** — [Risk] Прямой API-запрос в корзину с невалидными данными в обход фронта: бэк обязан отклонить
- Source Requirement: FR-6, FR-5 | Risk: RK-1 (Jira Q0-23, Q0-24)
- Priority: HIGH | Type: risk-based
- Preconditions: доступен API бэкенда; запрос width=50, length=1200.
- Steps/Test Intent: отправить прямой API-запрос (минуя фронт) → проверить корзину.
- Expected Result: бэкенд отклоняет (валидация и на бэке — FR-6, VR-1); параметры не сохраняются.
- Risk Reference: RK-1 | Open Questions: — (поведение подтверждено FR-6).

**L-21 / Qase 88** — [Risk] Согласованность валидации фронта и бэка при повороте изделия
- Source Requirement: FR-6, BR-3, VR-3 | Risk: RK-1, RK-4 (Jira Q0-23)
- Priority: HIGH | Type: risk-based
- Preconditions: лист 3000×1500; доступны фронт и API.
- Steps/Test Intent: сравнить результаты фронта и бэка для (1000,2800) — принимается; для (1600,1600) — отклоняется.
- Expected Result: результаты фронта и бэка совпадают в обоих случаях; расхождений нет.
- Risk Reference: RK-1, RK-4 | Open Questions: AMB-3 не влияет на проверку согласованности.

**L-22 / Qase 89** — [Risk] Количество (quantity): граничные и недопустимые значения (**BLOCKED**)
- Source Requirement: FR-2 | Risk: RK-5 (Jira Q0-20, Q0-24)
- Priority: MEDIUM | Type: risk-based | Status в Qase: Draft
- Preconditions: форма открыта; размеры валидны.
- Steps/Test Intent: quantity = 0; −1; дробное (2,5); очень большое.
- Expected Result: **НЕ ОПРЕДЕЛЕНО — REQUIRES_HUMAN_DECISION.** Диапазон quantity не задан (MIS-5, OQ-5): целое/дробное, max, допустимость 0/отрицательных.
- Risk Reference: RK-5 | Open Questions/Blocker: MIS-5, OQ-5.

---

## 2. Метрики покрытия

### FR (функциональные требования) — 7/7 = 100%

| ID | Покрытие (Qase ID) |
|---|---|
| FR-1 | 69 |
| FR-2 | 70, 71 (BLOCKED), 89 (BLOCKED) |
| FR-3 | 72, 73 |
| FR-4 | 74, 75, 76 (BLOCKED) |
| FR-5 | 85, 86, 87 |
| FR-6 | 77, 78, 79, 80, 81, 82, 83, 84, 87, 88 |
| FR-7 | 68 |

Непокрытых FR нет. Примечание: FR-2 покрыт по части «ввод полей» (70); часть «маркировка» (71) и «диапазон quantity» (89) — BLOCKED (не скрыты).

### BR (бизнес-правила) — 4/4 = 100%

| ID | Покрытие (Qase ID) |
|---|---|
| BR-1 | 72, 73 |
| BR-2 | 74, 75 |
| BR-3 | 77, 78, 81, 83, 84, 88 |
| BR-4 | 68, 79, 80, 82 |

### VR (правила валидации) — 4/4 = 100%

| ID | Покрытие (Qase ID) |
|---|---|
| VR-1 | 79, 82 |
| VR-2 | 80, 82 |
| VR-3 | 77, 78, 81, 83, 84, 88 |
| VR-4 | 68 |

### Риски (RK) — покрытие

| Риск | Покрытие (Qase ID) | Статус |
|---|---|---|
| RK-1 (расхождение фронт/бэк) | 87, 88 | покрыт |
| RK-2 (округление денежных сумм) | 75 | покрыт (частично: отображение REQUIRES_HUMAN_DECISION) |
| RK-3 (источник cost_one_rub) | 76 | BLOCKED/REQUIRES_HUMAN_DECISION |
| RK-4 (трактовка поворота) | 78, 88 | покрыт (в рамках подтверждённого BR-3/VR-3) |
| RK-5 (непокрытые границы quantity) | 89 | BLOCKED/REQUIRES_HUMAN_DECISION |
| RK-6 (отсутствие AC) | — | Процессный риск: не отображается в исполняемый тест; эскалирован в Open Questions (OQ-9), тест-кейс не применим |

### Границы (Boundary)

| Граница | Qase ID |
|---|---|
| min_width = 100 / min_length = 100 (ровно и минус 1) | 73, 82, 79, 80 |
| Вписывание == габариты листа (с поворотом) | 83 |
| 1 ед. сверх листа | 84 |
| Обе ориентации (прямая и повёрнутая) | 77, 78, 81 |

### Quality Gates
- ✅ Для каждого критического требования есть positive и negative сценарии (исключения зафиксированы: FR-1, FR-7 — негативный сценарий не формализуем из подтверждённого текста, поведение не выдумывалось).
- ✅ Риски из Requirement Review покрыты отдельными risk-based кейсами или явно заблокированы.
- ✅ Шаги и ожидаемые результаты однозначны для готовых кейсов.
- ✅ Покрытие FR/BR/VR = 100% (BLOCKED-сценарии зафиксированы, не скрыты).
- ✅ Artifact сохранён в `/artifacts/test-model.md`.

---

## 3. BLOCKED / REQUIRES_HUMAN_DECISION

| Qase ID | Title | Причина |
|---|---|---|
| 71 (L-04) | Ввод маркировки: обязательность, формат и передача в корзину | CON-1 (FR-2 vs пример тела запроса без маркировки), AMB-2, MIS-3, OQ-3. Ожидаемый результат не определим без решения PO. Статус Qase: Draft, тег blocked/requires_human_decision. |
| 76 (L-19) | [Risk] Трактовка cost_one_rub | MIS-2, AMB-6, OQ-2: источник и назначение cost_one_rub не описаны. Ожидаемое значение стоимости зависит от трактовки. Статус Qase: Draft, тег blocked/requires_human_decision. |
| 89 (L-22) | [Risk] Количество (quantity): граничные и недопустимые значения | MIS-5, OQ-5: диапазон quantity не задан (целое/дробное, max, 0/отрицательные). Статус Qase: Draft, тег blocked/requires_human_decision. |

Дополнительные открытые вопросы, НЕ блокирующие исполнение, но влияющие на числовые ожидания: AMB-1/OQ-1 (единицы измерения), AMB-4 (момент валидации), MIS-4 (габариты листа), MIS-6/OQ-8 (округление и валюта), MIS-7 (тексты/коды ошибок). Заложены как допущения в описаниях соответствующих кейсов.

---

## 4. Аудит-лог (Audit Log)

| Время | Этап | Инструмент | Действие | Артефакт / ID | Причина |
|---|---|---|---|---|---|
| 2026-09-22 | 1 | read | Прочитан Requirement Review Artifact | artifacts/requirement-review.md | Входной контекст |
| 2026-09-22 | 1 | read | Прочитан Jira Tasks Artifact | artifacts/jira-tasks.md | Traceability Q0-18…Q0-24 |
| 2026-09-22 | 1 | skill | Загружен skill `test-design` | SKILL.md | Методология проектирования |
| 2026-09-22 | 2 | qase_api GET /v1/project | Получены проекты Qase | QT (qase_test), QT2 (QAI-05) | Выбор проекта: выбран QT2 (совпадает с workspace QAI-05) |
| 2026-09-22 | 2 | qase_project_context | Контекст проекта QT2 | 0 suites, 0 cases | Структура проекта пуста → создать сьюты |
| 2026-09-22 | 2 | qql_help + qase_api system_field | Определены enum-значения | priority/status/type/behavior | Корректные значения полей |
| 2026-09-22 | 3 | qase_suite_upsert | Созданы сьюты | root=7; дети 8..15 | Структура тестовой модели |
| 2026-09-22 | 4 | qql_search | Поиск существующих кейсов | 0 результатов | Идемпотентность: дубликатов нет |
| 2026-09-22 | 5 | qase_case_bulk_create | Создано 22 тест-кейса | IDs 68–89 (пачка ≤ 100) | Создание тестовой модели |
| 2026-09-22 | 6 | qase_get | Верификация кейса 68 | id=68, status=0, priority=2, suite=8 | Подтверждение создания |
| 2026-09-22 | 6 | qase_api GET /v1/case/QT2 | Верификация всех кейсов | total=22, ids 68–89 | Фактическое состояние (QQL отставал по индексации — не использовался как основание) |
| 2026-09-22 | 7 | write | Записан Test Model Artifact | artifacts/test-model.md | Выход этапа |

Паузы между запросами Qase ≥ 200 мс. Временных ошибок и повторов не было; создание прошло с первого вызова.