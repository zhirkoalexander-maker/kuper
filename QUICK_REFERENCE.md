# 🎯 QUICK REFERENCE - System Detection

## Вопрос
> "Как оно системные проверяет настрой и на сайте и в питоне?"

## Краткий ответ

### Python ✅
```
psutil → читает реально → CPU%, RAM%, Disk → показывает правду
```

### Web (без сервера) ❌
```
Math.random() → случайное → любые числа → неправда
```

### Web (с сервером) ✅
```
fetch() → psutil на сервере → реально → показывает правду
```

---

## 🚀 Быстрый старт

### Python (просто)
```bash
python3 fps_tester.py
```
✅ Готово, работает с реальными метриками

### Web (с сервером)
```bash
# Terminal 1
python3 backend_server.py

# Terminal 2
python3 -m http.server 8000

# Browser
http://localhost:8000
```
✅ Готово, работает с реальными метриками

---

## 📊 Где что читает метрики

| Что | Python | Web (сервер) | Web (без) |
|----|--------|------|---------|
| CPU | psutil | psutil | random |
| RAM | psutil | psutil | random |
| Disk | psutil | psutil | random |
| Точность | 100% | 100% | 0% |

---

## 🔧 Файлы для Web версии

1. **backend_server.py** - Flask сервер
   - Читает CPU, RAM, Disk через psutil
   - Отправляет JSON через API

2. **system_metrics_api.js** - JavaScript helper
   - fetch'ит от backend'а
   - Fallback на simulation если нет сервера

---

## 📚 Читай документацию

1. **SYSTEM_DETECTION_ANSWER.md** ← Полный ответ на вопрос
2. **SYSTEM_DETECTION_SETUP.md** ← Как запустить
3. **SYSTEM_DETECTION_EXPLANATION.md** ← Технические детали

---

## ✅ Проверка

### Python работает?
```bash
python3 -c "import psutil; print(psutil.cpu_percent())"
# Должно показать: 42.3 (или другое реальное число)
```

### Backend работает?
```bash
curl http://localhost:5000/api/system-metrics
# Должно показать: {"cpu_percent": 42.3, "ram_percent": 65.1, ...}
```

### JavaScript подключен?
```javascript
// В Console браузера (F12)
fetch('http://localhost:5000/api/system-metrics').then(r => r.json()).then(console.log)
// Должно показать: {cpu_percent: 42.3, ram_percent: 65.1, ...}
```

---

## 🎉 Итог

- Python ✅ Использует psutil → реально
- Web ✅ Использует backend → реально
- Обе ✅ Показывают правду о компьютере

**Вот так и проверяет! 🚀**
