# FPS Tester - System Detection Setup Guide

## 🎯 Как система проверяет параметры

### Python версия ✅ (Desktop)
```
fps_tester.py использует psutil для реальных метрик:
- CPU% → psutil.cpu_percent()
- RAM% → psutil.virtual_memory().percent
- Disk → psutil.disk_usage('/')
- Fallback: Math simulation если psutil не установлен
```

### JavaScript версия (Web)
```
Браузер НЕ может читать системные метрики (security restriction)
Два варианта:

1️⃣  БЕЗ СЕРВЕРА (текущее):
   - Использует Math.random() - только симуляция
   - Показывает случайные числа, не реальные метрики
   
2️⃣  С СЕРВЕРОМ (рекомендуется):
   - Запрашивает метрики у backend сервера
   - Backend читает с помощью psutil
   - Показывает РЕАЛЬНЫЕ метрики
```

---

## 🚀 Быстрый Старт

### Вариант 1: Только Python (просто, без веб)

```bash
cd "/Users/olekzhyrko/Desktop/fps tester"
python3 fps_tester.py
```

**Результат:** 
- ✅ Все тесты работают с реальными метриками
- ✅ System tests показывают CPU%, RAM%, Disk
- ✅ Полностью локально, без интернета

---

### Вариант 2: Python + Web с Backend Server (полный функционал)

#### Шаг 1: Установить зависимости

```bash
cd "/Users/olekzhyrko/Desktop/fps tester"

# Установить Flask для бэкенда
pip install flask flask-cors

# Проверить psutil
pip install psutil
```

#### Шаг 2: Запустить Backend Server (в одном терминале)

```bash
cd "/Users/olekzhyrko/Desktop/fps tester"
python3 backend_server.py
```

**Вывод:**
```
🎮 FPS Tester Backend Server
==================================================
psutil: ✓ Available
==================================================
Starting server on http://localhost:5000
Available endpoints:
  GET /api/health
  GET /api/system-metrics
  GET /api/system-metrics-history
  GET /api/system-info
==================================================
```

#### Шаг 3: Открыть веб-приложение (в браузере)

```
http://localhost:8000
```

(Или запустить простой HTTP сервер для index.html)

```bash
# В отдельном терминале
cd "/Users/olekzhyrko/Desktop/fps tester"
python3 -m http.server 8000
```

**Результат:**
- ✅ JavaScript подключается к backend серверу
- ✅ System tests показывают РЕАЛЬНЫЕ метрики (не simulation)
- ✅ Одинаковые результаты как в Python версии
- ✅ Графики обновляются в реальном времени

---

## 📡 Как работает система обнаружения

### Когда запускается System Test (CPU Test):

#### Python версия:
```
1. CPUTest.update() вызывается каждый frame
2. Проверяет: if HAS_PSUTIL:
3. Да → psutil.cpu_percent() → реальное значение
4. Нет → simulation с Math.sin()
5. Сохраняет в self.cpu_history
6. Отображает на экране
```

#### JavaScript версия (с бэкендом):
```
1. CPUTest.update() вызывается каждый frame
2. Вызывает: await getSystemMetrics()
3. getSystemMetrics() проверяет: if BACKEND_AVAILABLE:
4. Да → fetch('/api/system-metrics') → psutil на сервере → реальное
5. Нет → simulateSystemMetrics() → Math.random() → simulation
6. Отображает на canvas
```

---

## 🔍 Проверка что работает

### Проверка Python версии

```bash
# Запустить Python
python3

# Проверить psutil
>>> import psutil
>>> psutil.cpu_percent(interval=0.1)
42.3  # ← реальное значение вашей системы
>>> psutil.virtual_memory().percent
65.1  # ← реальное значение вашей системы
```

### Проверка Backend Server

```bash
# В отдельном терминале, когда сервер запущен:
curl http://localhost:5000/api/system-metrics

# Результат (реальные данные):
{
  "cpu_percent": 42.3,
  "ram_percent": 65.1,
  "disk_percent": 78.5,
  "has_psutil": true,
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Проверка JavaScript подключения

Откройте Console в браузере (F12) и запустите:

```javascript
// Проверить подключение к backend
await fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(d => console.log('Backend:', d))

// Проверить метрики
await fetch('http://localhost:5000/api/system-metrics')
  .then(r => r.json())
  .then(d => console.log('Metrics:', d))
```

---

## 🎯 Разница между режимами

| Режим | Source | Accuracy | Real-time | Notes |
|-------|--------|----------|-----------|-------|
| **Python (psutil)** | psutil library | ✅ 100% | ✅ Yes | Истинные метрики |
| **Python (simulation)** | Math.sin() | ❌ 0% | ✅ Yes | Только если нет psutil |
| **JavaScript (backend)** | psutil via API | ✅ 100% | ✅ Yes | Требует сервер |
| **JavaScript (simulation)** | Math.random() | ❌ 0% | ✅ Yes | Без сервера |

---

## 📊 Что показывает каждый тест

### CPU Test
```
Backend: cpuPercent = psutil.cpu_percent()
↓
Показывает: "CPU: 42.3%" ← РЕАЛЬНОЕ значение
```

### RAM Test
```
Backend: ramPercent = psutil.virtual_memory().percent
↓
Показывает: "RAM: 65.1%" ← РЕАЛЬНОЕ значение
         "Using: 1024 MB of 1536 MB" ← РЕАЛЬНЫЕ значения
```

### Disk I/O Test
```
Backend: diskUsage = psutil.disk_usage('/')
↓
Показывает: "Disk: 78.5%" ← РЕАЛЬНОЕ значение
         "Free: 50.2 GB" ← РЕАЛЬНОЕ значение
```

### System Monitor
```
Backend: CPU история + RAM история
↓
Показывает: Графики в реальном времени ← РЕАЛЬНЫЕ данные
         "Status: Good" ← На основе реальных метрик
```

---

## 🔧 Архитектура системы

```
┌─────────────────────────────────────────────────────┐
│              FPS Tester v2.0                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────┐       ┌──────────────────┐  │
│  │  Python App      │       │  Web Browser     │  │
│  │  fps_tester.py   │       │  index.html      │  │
│  │                  │       │  fps_tester.js   │  │
│  │  ✓ CPU: psutil   │       │                  │  │
│  │  ✓ RAM: psutil   │       │ ⚠ Needs server   │  │
│  │  ✓ Disk: psutil  │       │                  │  │
│  └────────┬─────────┘       └────────┬─────────┘  │
│           │                         │             │
│           │ (local only)            │ (fetch API) │
│           │                         │             │
│  ┌────────▼─────────────────────────▼──────────┐  │
│  │  Backend Server (backend_server.py)        │  │
│  │  Flask + psutil                            │  │
│  │  Endpoints:                                │  │
│  │    /api/health                            │  │
│  │    /api/system-metrics                    │  │
│  │    /api/system-metrics-history            │  │
│  │    /api/system-info                       │  │
│  └────────────────────────────────────────────┘  │
│           │                                      │
│           └──→ psutil (реальные метрики)        │
│                                                  │
└─────────────────────────────────────────────────────┘
```

---

## 📝 Файлы системы

### Python версия
- `fps_tester.py` - основное приложение с psutil
- Встроен System Monitor с настоящими метриками

### Web версия (требует сервер)
- `index.html` - UI
- `fps_tester.js` - тесты (обновить для fetch API)
- `system_metrics_api.js` - новый файл для подключения к backend
- `backend_server.py` - новый файл, Flask сервер

---

## ✅ Проверочный список

### Python версия
- [ ] `pip install psutil` выполнен
- [ ] `python3 fps_tester.py` запускается
- [ ] System tests показывают реальные CPU%
- [ ] System tests показывают реальные RAM%
- [ ] Рекомендации генерируются корректно

### Web версия (с сервером)
- [ ] `pip install flask flask-cors` выполнен
- [ ] `python3 backend_server.py` запускается
- [ ] `curl http://localhost:5000/api/health` работает
- [ ] `curl http://localhost:5000/api/system-metrics` возвращает реальные данные
- [ ] `python3 -m http.server 8000` запускается для веб-части
- [ ] JavaScript может fetch'ить метрики от backend
- [ ] System tests в браузере показывают реальные метрики

---

## 🚀 Production Deploy

Для развертывания на веб-сервере:

```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 backend_server:app

# Or use systemd service file for auto-restart
# Or use Docker for containerized deployment
```

---

## 🎉 Результат

**Python:** ✅ Реальные метрики через psutil
**Web:** ✅ Реальные метрики через backend API

Обе версии показывают:
- ✅ Истинное использование CPU
- ✅ Истинное использование RAM  
- ✅ Истинное использование Disk
- ✅ Правильные рекомендации

**Вот так вот всё работает правильно! 🎯**
