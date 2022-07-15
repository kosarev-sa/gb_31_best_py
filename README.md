# gb_31_best_py
GB 3.1 dev BestPy group job search training project

# Autotests

Запуск автотестов из директории проекта - `python -m pytest -v -m all tests/`

Прогон по меткам:
`python -m pytest -v -m 'all and urls and not negative' tests/`

## Allure
Запуск с формированием allure отчета
`python -m pytest --alluredir=allure_reports -v -m all tests/` где allure_reports - имя для временной папки с отчетами

Запуск сервера allure для просмотра результатов тестов 
`allure serve allure_reports/`
