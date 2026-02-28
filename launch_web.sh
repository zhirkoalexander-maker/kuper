#!/bin/bash

# 🚀 FPS Tester Web Version Launcher
# Автоматический запуск веб-версии

cd /Users/olekzhyrko/Desktop/fps\ tester

echo "🎮 FPS Tester - Web Version Launcher"
echo "===================================="
echo ""
echo "Выбери способ запуска:"
echo ""
echo "1) Открыть в браузере напрямую (быстро)"
echo "2) Запустить локальный сервер (рекомендуется)"
echo "3) Выход"
echo ""

read -p "Выбери (1-3): " choice

case $choice in
    1)
        echo "Opening index_new.html..."
        open index_new.html
        ;;
    2)
        echo "Starting local server..."
        echo "Server running at: http://localhost:8000"
        echo "Open file: http://localhost:8000/index_new.html"
        echo ""
        echo "Press Ctrl+C to stop server"
        echo ""
        python3 -m http.server 8000
        ;;
    3)
        echo "Bye!"
        ;;
    *)
        echo "Invalid choice"
        ;;
esac
