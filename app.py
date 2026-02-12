from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
import threading
import time
import requests
import uuid
import os

app = Flask(__name__)
CORS(app)  # Включаем CORS для всех доменов

def keep_awake():
    """Держит API активным на Render"""
    print("⚡ Анти-спящий механизм запущен! Пинг каждые 10 минут")
    
    # Свои URL-ы
    self_urls = [
        "https://osm-api-17mp.onrender.com",
        "https://osm-api-17mp.onrender.com/api/nations",
        "https://osm-api-17mp.onrender.com/api/osm"
    ]
    
    while True:
        time.sleep(600)  # 600 секунд
        for url in self_urls:
            try:
                # Пингуем с таймаутом 10 секунд
                response = requests.get(url, timeout=10)
                print(f"✅ Self-ping успешен: {url} - {response.status_code}")
                break  # Достаточно одного успешного пинга
            except Exception as e:
                print(f"❌ Self-ping ошибка для {url}: {e}")

# Запускаем в отдельном потоке
threading.Thread(target=keep_awake, daemon=True).start()
print("🚀 Анти-спящий поток запущен!")

try:
    from apscheduler.schedulers.background import BackgroundScheduler
    import atexit
    
    # Запасной планировщик
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: requests.get("https://osm-api-17mp.onrender.com", timeout=5),
        trigger="interval",
        minutes=10,
        id="keep_awake_job"
    )
    scheduler.start()
    print("⏰ Планировщик APScheduler запущен!")
    atexit.register(lambda: scheduler.shutdown())
except ImportError:
    print("📦 APScheduler не установлен, используем threading")

# БАЗА ДАННЫХ ВИРТУАЛЬНЫХ ГОСУДАРСТВ

nations = [
    {
        "id": "jakid-republic",
        "name": "Республика Жакид",
        "official_name": "Республика Жакид",
        "capital": "-",
        "government_type": "Парламентская республика",
        "head_of_state": "Президент Денис Кошелев",
        "founded": "11.11.2024",
        "population": 4901,
        "area_km2": 0,
        "currency": "Жад (JDC)",
        "languages": ["русский", "жакидский"],
        "flag_emoji": "🏛️",
        "description": "Демократическое государство, основанное на принципах свободы и прогресса",
        "join_date": "-",
        "status": "member"
    },
    {
        "id": "imperial-order",
        "name": "Имперский Порядок",
        "official_name": "Имперский Порядок",
        "capital": "-",
        "government_type": "Дуалистическая монархия",
        "head_of_state": "Император Александр",
        "founded": "20.06.2025",
        "population": 30,
        "area_km2": 0,
        "currency": "Империал (IO)",
        "languages": ["русский", "имперский диалект"],
        "flag_emoji": "⚔️",
        "description": "Государство, основанное на традициях и порядке",
        "join_date": "12.02.2026",
        "status": "member"
    },
    {
        "id": "rone-republic",
        "name": "Республика Роне",
        "official_name": "Республика Роне",
        "capital": "-",
        "government_type": "Президентская республика",
        "head_of_state": "Президент Алексей Якунин",
        "founded": "2024-01-10",
        "population": 1,
        "area_km2": 0,
        "currency": "Роне (RN)",
        "languages": ["русский", "ронийский"],
        "flag_emoji": "🌹",
        "description": "Молодое государство с динамично развивающейся экономикой",
        "join_date": "11.02.2026",
        "status": "member"
    }
]

# ===========================================
# ДАННЫЕ ОСМ
# ===========================================
osm_info = {
    "id": "osm",
    "name": "Организация Союзных Микрогосударств",
    "abbreviation": "ОСМ",
    "founded": "11.08.2025",
    "headquarters": "Тула",
    "member_count": 3,
    "observer_count": 0,
    "working_languages": ["русский"],
    "description": "Международная организация, объединяющая виртуальные микрогосударства",
    "logo_emoji": "🤝",
    "current_chair": "Республика Жакид"
}

# ===========================================
# МАРШРУТЫ API
# ===========================================

@app.route('/')
def home():
    """Главная страница API"""
    return jsonify({
        "api": "OSM Nations API",
        "version": "2.0.0",
        "description": "API для Организации Союзных Микрогосударств",
        "status": "active",
        "anti_sleep": "✅ Активен - пинг каждые 10 минут",
        "endpoints": {
            "GET /": "Информация об API",
            "GET /api/nations": "Список всех государств",
            "GET /api/nations/<id>": "Информация о конкретном государстве",
            "GET /api/nations/status/<status>": "Государства по статусу",
            "GET /api/osm": "Информация об ОСМ",
            "POST /api/nations": "Добавить новое государство",
            "PUT /api/nations/<id>": "Обновить государство",
            "DELETE /api/nations/<id>": "Удалить государство",
            "GET /api/ping": "Проверка работы API"
        },
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/ping')
def ping():
    """Эндпоинт для пинга (держит API активным)"""
    return jsonify({
        "status": "alive",
        "message": "pong",
        "timestamp": datetime.now().isoformat(),
        "anti_sleep": "API бодрствует! 🚀"
    })

@app.route('/api/nations', methods=['GET'])
def get_nations():
    """Получить все государства"""
    return jsonify({
        "count": len(nations),
        "nations": nations,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/nations/<string:nation_id>', methods=['GET'])
def get_nation(nation_id):
    """Получить государство по ID"""
    nation = next((n for n in nations if n['id'] == nation_id), None)
    if nation:
        return jsonify({
            "nation": nation,
            "timestamp": datetime.now().isoformat()
        })
    return make_response(jsonify({
        "error": "Государство не найдено",
        "timestamp": datetime.now().isoformat()
    }), 404)

@app.route('/api/nations/status/<string:status>', methods=['GET'])
def get_nations_by_status(status):
    """Получить государства по статусу"""
    filtered_nations = [n for n in nations if n['status'] == status]
    return jsonify({
        "status": status,
        "count": len(filtered_nations),
        "nations": filtered_nations,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/osm', methods=['GET'])
def get_osm_info():
    """Получить информацию об ОСМ"""
    # Обновляем количество членов
    osm_info['member_count'] = len([n for n in nations if n['status'] == 'member'])
    
    return jsonify({
        "organization": osm_info,
        "member_nations": [n for n in nations if n['status'] == 'member'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/nations', methods=['POST'])
def create_nation():
    """Создать новое государство"""
    data = request.get_json()
    
    # Проверка обязательных полей
    required_fields = ['name', 'capital']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({
                "error": f"Отсутствует обязательное поле: {field}",
                "timestamp": datetime.now().isoformat()
            }), 400)
    
    # Генерация ID из названия
    nation_id = data['name'].lower().replace(' ', '-').replace('ё', 'е')
    
    # Проверка уникальности ID
    if any(n['id'] == nation_id for n in nations):
        return make_response(jsonify({
            "error": "Государство с таким названием уже существует",
            "timestamp": datetime.now().isoformat()
        }), 409)
    
    new_nation = {
        "id": nation_id,
        "name": data['name'],
        "official_name": data.get('official_name', data['name']),
        "capital": data['capital'],
        "government_type": data.get('government_type', 'Не указано'),
        "head_of_state": data.get('head_of_state', 'Не указано'),
        "founded": data.get('founded', datetime.now().strftime('%Y-%m-%d')),
        "population": data.get('population', 0),
        "area_km2": data.get('area_km2', 0),
        "currency": data.get('currency', 'Не указано'),
        "languages": data.get('languages', ['русский']),
        "flag_emoji": data.get('flag_emoji', '🏁'),
        "description": data.get('description', ''),
        "join_date": datetime.now().strftime('%Y-%m-%d'),
        "status": data.get('status', 'member')
    }
    
    nations.append(new_nation)
    
    return jsonify({
        "message": "Государство успешно создано",
        "nation": new_nation,
        "timestamp": datetime.now().isoformat()
    }), 201

@app.route('/api/nations/<string:nation_id>', methods=['PUT'])
def update_nation(nation_id):
    """Обновить информацию о государстве"""
    nation = next((n for n in nations if n['id'] == nation_id), None)
    if not nation:
        return make_response(jsonify({
            "error": "Государство не найдено",
            "timestamp": datetime.now().isoformat()
        }), 404)
    
    data = request.get_json()
    
    # Обновляем поля
    nation['name'] = data.get('name', nation['name'])
    nation['official_name'] = data.get('official_name', nation['official_name'])
    nation['capital'] = data.get('capital', nation['capital'])
    nation['government_type'] = data.get('government_type', nation['government_type'])
    nation['head_of_state'] = data.get('head_of_state', nation['head_of_state'])
    nation['population'] = data.get('population', nation['population'])
    nation['area_km2'] = data.get('area_km2', nation['area_km2'])
    nation['currency'] = data.get('currency', nation['currency'])
    nation['languages'] = data.get('languages', nation['languages'])
    nation['flag_emoji'] = data.get('flag_emoji', nation['flag_emoji'])
    nation['description'] = data.get('description', nation['description'])
    nation['status'] = data.get('status', nation['status'])
    
    return jsonify({
        "message": "Государство успешно обновлено",
        "nation": nation,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/nations/<string:nation_id>', methods=['DELETE'])
def delete_nation(nation_id):
    """Удалить государство"""
    global nations
    
    nation = next((n for n in nations if n['id'] == nation_id), None)
    if not nation:
        return make_response(jsonify({
            "error": "Государство не найдено",
            "timestamp": datetime.now().isoformat()
        }), 404)
    
    nations = [n for n in nations if n['id'] != nation_id]
    
    return jsonify({
        "message": f"Государство {nation['name']} успешно удалено",
        "timestamp": datetime.now().isoformat()
    })

# ===========================================
# ОБРАБОТЧИКИ ОШИБОК
# ===========================================
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        "error": "Ресурс не найден",
        "timestamp": datetime.now().isoformat()
    }), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({
        "error": "Внутренняя ошибка сервера",
        "timestamp": datetime.now().isoformat()
    }), 500)

# ===========================================
# ЗАПУСК ПРИЛОЖЕНИЯ
# ===========================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    print(f"🚀 API запускается на порту {port}")
    print(f"✅ Загружено государств: {len(nations)}")
    print(f"⚡ Анти-спящий режим: АКТИВЕН (пинг каждые 10 минут)")
    app.run(host='0.0.0.0', port=port, debug=False)
