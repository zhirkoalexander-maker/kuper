#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Read the file
with open('fps_tester.py', 'r', encoding='utf-8') as f:
    content = f.read()

# All replacements
replacements = [
    # Docstrings
    ('"""Matrix Rain - падающие символы, скорость зависит от мышки"""', '"""Matrix Rain - falling characters, speed depends on mouse"""'),
    ('"""Fractal Tree - рекурсивные фракталы, поворачиваются к мышке"""', '"""Fractal Tree - recursive fractals, rotate towards cursor"""'),
    ('"""Wave Simulation - симуляция волн"""', '"""Wave Simulation - wave simulation"""'),
    ('"""Bouncing Balls - прыгающие шары, притягиваются к мышке"""', '"""Bouncing Balls - bouncing balls, attracted to mouse"""'),
    ('"""Plasma Effect - плазма эффект, реагирует на мышку"""', '"""Plasma Effect - plasma effect, reacts to mouse"""'),
    ('"""Mandelbrot Set - множество Мандельброта, зумируй мышкой"""', '"""Mandelbrot Set - Mandelbrot set, zoom with mouse"""'),
    ('"""Вычисляет значение Мандельброта"""', '"""Calculate Mandelbrot value"""'),
    ('"""Tunnel Effect - 3D тоннель, вращается к мышке"""', '"""Tunnel Effect - 3D tunnel, rotates towards mouse"""'),
    ('"""Starfield - звёздное поле, движется вслед за мышкой"""', '"""Starfield - starfield, follows mouse"""'),
    ('"""Interactive Draw - рисуй и создавай эффекты мышкой"""', '"""Interactive Draw - draw and create effects with mouse"""'),
    ('"""Noise Field - шумовое поле с интерактивностью"""', '"""Noise Field - noise field with interactivity"""'),
    ('"""Particle Attractor - частицы притягиваются к курсору"""', '"""Particle Attractor - particles attracted to cursor"""'),
    
    # Comments
    ('        # Создаем частицы автоматически', '        # Create particles automatically'),
    ('        # Обновляем частицы', '        # Update particles'),
    ('            # Отскок от стен', '            # Bounce off walls'),
    ('            # Удаляем если много или мертвые', '            # Remove if too many or dead'),
    ('            # Двигаются к курсору', '            # Move towards cursor'),
    ('speed_multiplier = 1.0 + (my / WINDOW_HEIGHT) * 2  # Скорость зависит от высоты мышки',
     'speed_multiplier = 1.0 + (my / WINDOW_HEIGHT) * 2  # Speed depends on mouse height'),
    ('        # Конец линии', '        # End of line'),
    ('        # Рекурсия', '        # Recursion'),
    ('        # Вычисляем угол на курсор', '        # Calculate angle to cursor'),
    ('        # Плавное вращение к курсору', '        # Smooth rotation to cursor'),
    ('        # Добавляем возмущение в центр', '        # Add disturbance to center'),
    ('        # Симуляция волн (очень упрощённо)', '        # Wave simulation (very simplified)'),
    ('        # Правая кнопка мышки = отталкивание', '        # Right mouse button = repulsion'),
    ('            # Притяжение/отталкивание к мышке', '            # Attraction/repulsion to mouse'),
    ('            # Трение', '            # Friction'),
    ('                # Расстояние до мышки', '                # Distance to mouse'),
    ('                # Плазма формула с влиянием мышки', '                # Plasma formula with mouse influence'),
    ('        # Зум к позиции мышки', '        # Zoom to mouse position'),
    ('        # Смещение в центр мышки', '        # Offset to mouse center'),
    ('                # Преобразуем экранные координаты в комплексные', '                # Transform screen coordinates to complex'),
    ('        # Вращение в зависимости от мышки', '        # Rotation depends on mouse'),
    ('            # Размер кольца в зависимости от глубины', '            # Ring size depends on depth'),
    ('            # Цвет меняется в зависимости от вращения', '            # Color changes with rotation'),
    ('        # Плавное движение к мышке', '        # Smooth movement to mouse'),
    ('            # Перспективная проекция', '            # Perspective projection'),
    ('        # График CPU', '        # CPU graph'),
    ('        # График RAM', '        # RAM graph'),
    ('        # Информация', '        # Information'),
    ('        # Обновляем точки рисования', '        # Update drawing points'),
    ('if pygame.mouse.get_pressed()[0]:  # Левая кнопка', 'if pygame.mouse.get_pressed()[0]:  # Left button'),
    ('            # Создаем частицы вокруг курсора', '            # Create particles around cursor'),
    ('            # Ограничиваем размер', '            # Limit size'),
    ('        # Рисуем линию из точек', '        # Draw line from points'),
    ('        # Рисуем частицы', '        # Draw particles'),
    ('        # Клик мышкой создает возмущение', '        # Mouse click creates disturbance'),
    ('        # Обновляем возмущения', '        # Update disturbances'),
    ('        # Фоновый шум', '        # Background noise'),
    ('                # Перлин-подобный шум (упрощенный)', '                # Perlin-like noise (simplified)'),
    ('                # Проверяем возмущения', '                # Check disturbances'),
    ('        # Рисуем волны возмущений', '        # Draw disturbance waves'),
    ('            # Вектор к курсору', '            # Vector to cursor'),
    ('            # Сила притяжения', '            # Attraction force'),
    ('        # Курсор как большая точка', '        # Cursor as big point'),
    ('# МЕНЮ И РЕЗУЛЬТАТЫ', '# MENUS AND RESULTS'),
    ('# ГЛАВНОЕ МЕНЮ', '# MAIN MENU'),
    ('"""Главное меню - выбор между FPS, System тестами и Настройками"""',
     '"""Main menu - choose between FPS, System tests and Settings"""'),
    ('    # Анимация фона', '    # Background animation'),
    ('        # Обновляем частицы фона', '        # Update background particles'),
    ('        # Рисуем фон с частицами', '        # Draw background with particles'),
    ('        # Заголовок с эффектом', '        # Title with effect'),
    ('        # Добавляем свечение', '        # Add glow'),
    ('"""Меню выбора FPS режима"""', '"""Menu to select FPS mode"""'),
    ('"""Меню выбора System тестов"""', '"""Menu to select System tests"""'),
    ('# МЕНЮ НАСТРОЕК', '# SETTINGS MENU'),
    ('"""Экран приветствия с информацией"""', '"""Welcome screen with information"""'),
    ('        # Анимация появления текста', '        # Text appearing animation'),
    ('        # Рисуем звезды в фоне', '        # Draw stars in background'),
    ('        # Заголовок', '        # Title'),
    ('        # Пульсирующее приглашение', '        # Pulsing invitation'),
    ('"""Меню для настройки отображения характеристик"""',
     '"""Menu for configuring display settings"""'),
    ('"""Меню выбора режима"""', '"""Menu to select mode"""'),
    ('# СИСТЕМА РЕКОМЕНДАЦИЙ', '# RECOMMENDATION SYSTEM'),
    ('"""Запустить выбранный режим"""', '"""Run selected mode"""'),
    ('    # Создаем режим', '    # Create mode'),
    ('                # Управление', '                # Controls'),
    ('                # Обновляем режим', '                # Update mode'),
    ('                # Получаем FPS', '                # Get FPS'),
    ('                # Рисуем', '                # Render/Draw'),
    ('clock.tick()  # Без ограничений', 'clock.tick()  # Unlimited FPS'),
    ('        # Показываем результаты (даже если был краш)', '        # Show results (even if crash occurred)'),
    ('# ГЛАВНЫЙ ЦИКЛ', '# MAIN LOOP'),
    ('# Показываем экран приветствия', '# Show welcome screen'),
    ('    # Главное меню', '    # Main menu'),
    ('    # Выбор режима в зависимости от категории', '    # Select mode based on category'),
]

# Apply all replacements
for russian, english in replacements:
    content = content.replace(russian, english)

# Write back
with open('fps_tester.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ Applied {len(replacements)} translations successfully!")
