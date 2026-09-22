import json
import shutil
import subprocess
from pathlib import Path


# =============================================================
# РЕЗОЛЮЦИЯ OPENCODE CLI
# =============================================================

def opencode_command(args):

    # Приоритет: реальный opencode.exe в PATH.
    exe = shutil.which(
        "opencode.exe"
    )

    if exe:
        return [exe] + list(args)

    # npm-шимы (opencode.cmd / opencode.bat / opencode без расширения)
    # не запускаются напрямую через CreateProcess.
    shim = shutil.which(
        "opencode"
    )

    if shim:

        candidate = (
            Path(shim).parent
            / "node_modules"
            / "opencode-ai"
            / "bin"
            / "opencode.exe"
        )

        if candidate.is_file():
            return [str(candidate)] + list(args)

        if shim.lower().endswith(
            (".cmd", ".bat")
        ):
            return (
                ["cmd.exe", "/c", shim]
                + list(args)
            )

    raise RuntimeError(
        "Не удалось найти исполняемый файл opencode. "
        "Убедитесь, что opencode CLI установлен "
        "и доступен в PATH."
    )


# =============================================================
# PATHS
# =============================================================

# Корень проекта QAI-05_adv1
project_path = Path(__file__).resolve().parent.parent


# =============================================================
# EVALUATOR
# =============================================================

def evaluate_response(eval_case, agent_response):

    # ---------------------------------------------------------
    # INPUT EVAL CASE
    # ---------------------------------------------------------

    eval_input = eval_case["input"]

    page_id = eval_input.get(
        "confluence_page_id"
    )

    source = "confluence" if page_id else "inline"


    # ---------------------------------------------------------
    # ОПИСАНИЕ ИСТОЧНИКА
    # ---------------------------------------------------------

    requirements = eval_input.get(
        "requirements"
    )

    if source == "confluence":

        input_description = (
            f"Требования находятся в Confluence. "
            f"pageId={page_id}."
        )

    elif requirements:

        input_description = requirements

    else:

        input_description = str(eval_input)


    negative_constraints = eval_case.get(
        "negative_constraints",
        []
    )


    # =========================================================
    # PROMPT ДЛЯ LLM-AS-A-JUDGE
    # =========================================================

    judge_prompt = f"""
Ты — независимый Evaluator результатов AI QA Agent.

Твоя задача — оценить фактический ответ агента
относительно заданного Eval Case.


ПРАВИЛА ОЦЕНКИ:

1. Оценивай смысл ответа, а не точное совпадение формулировок.

2. Не добавляй собственные требования.

3. Каждое Expected Property оцени отдельно.

4. Каждое Forbidden Behavior оцени отдельно.

5. Expected Property считается выполненным,
если ответ агента явно или семантически подтверждает
требуемое поведение.

6. Forbidden Behavior считается нарушенным только тогда,
когда агент действительно совершил запрещённое действие.

7. Итоговый статус PASS возможен только если:
- выполнены ВСЕ Expected Properties;
- не нарушено НИ ОДНО Forbidden Behavior.

8. Если хотя бы одно Expected Property не выполнено,
итоговый статус должен быть FAIL.

9. Если хотя бы одно Forbidden Behavior нарушено,
итоговый статус должен быть FAIL.


EVAL CASE ID:

{eval_case["id"]}


INPUT SOURCE:

{source}


INPUT:

{input_description}


EXPECTED PROPERTIES:

{json.dumps(
    eval_case["expected_properties"],
    ensure_ascii=False,
    indent=2
)}


FORBIDDEN BEHAVIOR:

{json.dumps(
    negative_constraints,
    ensure_ascii=False,
    indent=2
)}


ACTUAL AGENT RESPONSE:

{agent_response}


Верни ТОЛЬКО валидный JSON следующей структуры:

{{
  "eval_case_id": "{eval_case["id"]}",
  "expected_properties": [
    {{
      "property": "текст проверяемого Expected Property",
      "passed": true,
      "reason": "краткое объяснение решения"
    }}
  ],
  "forbidden_behavior": [
    {{
      "rule": "текст проверяемого Forbidden Behavior",
      "violated": false,
      "reason": "краткое объяснение решения"
    }}
  ],
  "status": "PASS",
  "score": 1.0
}}


ПРАВИЛА SCORE:

1.0 — PASS.
0.0 — FAIL.


ВАЖНО:

Не используй Markdown.
Не используй ```json.
Не используй ```.
Не добавляй пояснения до JSON.
Не добавляй пояснения после JSON.
Ответ должен содержать только один JSON-объект.
"""


    # =========================================================
    # ЗАПУСК EVALUATOR
    # =========================================================

    process = subprocess.Popen(
        opencode_command(
            [
                "run",
                "--format",
                "json",
                "--dir",
                str(project_path),
                judge_prompt
            ]
        ),
        cwd=project_path,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        bufsize=1
    )


    # Здесь собираем текстовый ответ Evaluator.
    text_parts = []


    print("Evaluator запущен...")


    # =========================================================
    # ЧТЕНИЕ JSON EVENTS
    # =========================================================

    if process.stdout:

        for line in process.stdout:

            line = line.strip()

            if not line:
                continue

            try:

                event = json.loads(line)

                event_type = event.get("type")

                print(
                    "EVALUATOR EVENT:",
                    event_type,
                    flush=True
                )


                # Забираем только текстовые события.
                if event_type == "text":

                    part = event.get("part", {})

                    text = part.get("text")

                    if text:
                        text_parts.append(text)


            except json.JSONDecodeError:

                print(
                    "Не удалось разобрать событие Evaluator",
                    flush=True
                )


    # =========================================================
    # ЗАВЕРШЕНИЕ EVALUATOR
    # =========================================================

    return_code = process.wait()


    print(
        "EVALUATOR RETURN CODE:",
        return_code
    )


    # ---------------------------------------------------------
    # ПРОВЕРКА RETURN CODE
    # ---------------------------------------------------------

    if return_code != 0:

        stderr = ""

        if process.stderr:
            stderr = process.stderr.read()

        raise RuntimeError(
            f"Evaluator завершился с ошибкой. "
            f"Return code: {return_code}. "
            f"STDERR: {stderr}"
        )


    # =========================================================
    # СБОРКА ОТВЕТА
    # =========================================================

    judge_response = "\n".join(
        text_parts
    ).strip()


    if not judge_response:

        raise RuntimeError(
            "Evaluator не вернул текстовый ответ."
        )


    # =========================================================
    # УДАЛЕНИЕ MARKDOWN CODE BLOCK
    # =========================================================

    # На случай, если модель всё-таки вернула:
    #
    # ```json
    # {...}
    # ```

    if judge_response.startswith("```json"):

        judge_response = judge_response[7:]

    elif judge_response.startswith("```"):

        judge_response = judge_response[3:]


    if judge_response.endswith("```"):

        judge_response = judge_response[:-3]


    judge_response = judge_response.strip()


    # =========================================================
    # JSON PARSING
    # =========================================================

    try:

        evaluation_result = json.loads(
            judge_response
        )

    except json.JSONDecodeError as error:

        print()
        print(
            "Не удалось разобрать ответ "
            "Evaluator как JSON."
        )

        print()
        print("Фактический ответ Evaluator:")

        print(judge_response)

        raise RuntimeError(
            "Evaluator вернул невалидный JSON."
        ) from error


    # =========================================================
    # ПРОВЕРКА СТРУКТУРЫ
    # =========================================================

    required_fields = [
        "eval_case_id",
        "expected_properties",
        "forbidden_behavior",
        "status",
        "score"
    ]


    for field in required_fields:

        if field not in evaluation_result:

            raise RuntimeError(
                f"В ответе Evaluator отсутствует "
                f"обязательное поле: {field}"
            )


    # =========================================================
    # RETURN
    # =========================================================

    return evaluation_result