# Email Accounts Monitor for CRM Close

Система мониторинга состояния email-аккаунтов в CRM Close с автоматической генерацией отчетов в Google Sheets.

## Структура проекта

```
EmailAccountsReport/
├── main.py                          # Точка входа приложения
├── config.py                        # Конфигурация приложения
├── emailaccs_monitor.py             # Основной класс мониторинга
├── report_generator.py              # Генератор отчетов
├── requirements.txt                 # Зависимости Python
├── logs.log                         # Файл логов (автосоздание)
│
├── tools/                           # Вспомогательные модули
│   ├── close.py                     # API клиент для CRM Close
│   ├── sheets.py                    # Работа с Google Sheets API
│   ├── telegram_notifier.py         # Отправка уведомлений в Telegram
│   ├── env_loader.py                # Загрузка переменных окружения
│   ├── logger.py                    # Настройка системы логирования
│   ├── utilities.py                 # Вспомогательные функции
│   ├── color_prints.py              # Цветной вывод в консоль
│   └── __init__.py                  # Пакет tools
│
└── secrets/                         # Секреты и конфигурация
    ├── .env                         # Переменные окружения
    └── service_account.json         # Сервисный аккаунт Google
```

## Описание модулей

### Основные модули

- **main.py** - Главный скрипт запуска приложения
- **config.py** - Централизованная конфигурация всех параметров
- **emailaccs_monitor.py** - Класс `EmailAccountsMonitor` для управления процессом мониторинга
- **report_generator.py** - Генерация структурированных отчетов из данных API

### Вспомогательные модули (tools/)

- **close.py** - Функции для работы с Close.com API (`get_email_accounts`, `get_users`)
- **sheets.py** - Интеграция с Google Sheets API (`write_spread_sheet`)
- **telegram_notifier.py** - Отправка уведомлений в Telegram о критических событиях
- **env_loader.py** - Загрузка переменных окружения из `.env` файла
- **logger.py** - Настройка системы логирования
- **utilities.py** - Вспомогательные функции (даты, строки и т.д.)
- **color_prints.py** - Утилиты для цветного вывода в консоль

## Настройка окружения

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Настройка секретов

Создайте папку `secrets` и добавьте файлы:

**secrets/.env:**
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
CLOSE_API_KEY=your_close_api_key
```

**secrets/service_account.json:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  ...
}
```

### 3. Конфигурация

Основные настройки редактируются в `config.py`:

```python
class Config:
    SPREAD_NAME = "Close Email Accounts v2.0"      # Название Google таблицы
    OUT_SHEET_NAME = "emailaccts_api_report"       # Название листа
    UPDATE_INTERVAL = 300                          # Интервал обновления (сек)
    TELEGRAM_ENABLED = True                        # Включить уведомления
```

## Запуск приложения

```bash
python main.py
```

## Функциональность

### 📊 Мониторинг аккаунтов
- Автоматический сбор данных о email-аккаунтах каждые 5 минут
- Отслеживание статусов отправки и получения почты
- Обнаружение ошибок подключения

### 📈 Отчетность
- Автоматическая генерация отчетов в Google Sheets
- Детальная информация по каждому аккаунту
- История изменений и последнего использования

### 🔔 Уведомления
- Telegram уведомления о критических ошибках
- Уведомления об успешном перезапуске
- Мониторинг состояния системы

### ⚡ Надежность
- Автоматический перезапуск при сбоях
- Подробное логирование всех операций
- Обработка ошибок API

## Переменные окружения

| Переменная | Описание | Обязательная |
|------------|-----------|--------------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота | Да |
| `TELEGRAM_CHAT_ID` | ID чата для уведомлений | Да |
| `CLOSE_API_KEY` | API ключ Close.com | Да |

## Логирование

Приложение ведет детальные логи в:
- Файл `logs.log`
- Консоль с цветным выводом
- Telegram уведомления для критических событий

## Безопасность

- Секреты хранятся в отдельной папке `secrets/`
- Файлы `.env` и `service_account.json` добавлены в `.gitignore`
- Используется безопасная загрузка конфигурации