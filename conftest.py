"""Настройки pytest для учебного репозитория.

1. Тест, упавший с NotImplementedError, считается не проваленным, а «ещё не решённым»
   (skipped). Поэтому на ветке main с заготовками CI зелёный, а твой прогресс виден
   по числу пройденных тестов.
2. В конце прогона печатается таблица прогресса по разделам.
"""

from collections import defaultdict

import pytest

SECTIONS = {
    "test_data_structures.py": "Структуры данных",
    "test_algorithms_arrays.py": "Алгоритмы: паттерны 1-5",
    "test_algorithms_structures.py": "Алгоритмы: паттерны 6-11",
    "test_python_core.py": "Python core",
    "test_ml_basics.py": "ML с нуля",
}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if call.excinfo is not None and call.excinfo.errisinstance(NotImplementedError):
        report.outcome = "skipped"
        report.longrepr = (str(item.path), item.location[1] or 0, "ещё не решено")


def pytest_terminal_summary(terminalreporter):
    solved: dict[str, int] = defaultdict(int)
    total: dict[str, int] = defaultdict(int)
    for status in ("passed", "failed", "skipped"):
        for report in terminalreporter.stats.get(status, []):
            if report.when != "call" and status != "skipped":
                continue
            section = SECTIONS.get(report.nodeid.split("::")[0].split("/")[-1])
            if section is None:
                continue
            total[section] += 1
            solved[section] += status == "passed"
    if not total:
        return
    terminalreporter.section("Прогресс")
    for section in SECTIONS.values():
        if total[section]:
            done, all_ = solved[section], total[section]
            bar = "#" * round(20 * done / all_) + "-" * (20 - round(20 * done / all_))
            terminalreporter.write_line(f"{section:<28} [{bar}] {done:>3}/{all_}")
