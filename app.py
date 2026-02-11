from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
import uuid

app = Flask(__name__)
CORS(app)  # Включаем CORS для доступа с любых доменов

# База данных виртуальных государств
nations = [
    {
        "id": "jakid-republic",
        "name": "Республика Жакид",
        "official_name": "Республика Жакид",
        "capital": "Жакид-Сити",
        "government_type": "Парламентская республика",
        "head_of_state": "Президент Алексей Жакидов",
        "founded": "2023-01-15",
        "population": 15000,
        "area_km2": 450,
        "currency": "Жакидский рубль (JKR)",
        "languages": ["русский", "жакидский"],
        "flag_emoji": "🏛️",
        "description": "Демократическое государство, основанное на принципах свободы и прогресса",
        "join_date": "2023-01-15",
        "status": "member"
    },
    {
        "id": "imperial-order",
        "name": "Имперский Порядок",
        "official_name": "Имперский Орден Вечного Порядка",
        "capital": "Цитадель Порядка",
        "government_type": "Дуалистическая монархия",
        "head_of_state": "Император Константин I",
        "founded": "2022-11-20",
        "population": 8900,
        "area_km2": 280,
        "currency": "Имперский солид (IMS)",
        "languages": ["русский", "имперский диалект"],
        "flag_emoji": "⚔️",
        "description": "Государство, основанное на традициях и порядке, где каждый гражданин служит высшей цели",
        "join_date": "2022-11-20",
        "status": "member"
    }
]

# Данные ОСМ (Организация Союзных Микрогосударств)
osm_info = {
    "id": "osm",
    "name": "Организация Союзных Микрогосударств",
    "abbreviation": "ОСМ",
    "founded": "2022-10-01",
    "headquarters": "Жакид-Сити",
    "member_count": 2,
    "observer_count": 0,
    "working_languages": ["русский"],
    "description": "Международная организация, объединяющая виртуальные микрогосударства",
    "logo_emoji": "🤝",
    "current_chair": "Республика Жакид"
}

@app.route('/')
def home():
    """Главная страница API"""
    return jsonify({
        "api": "OSM Nations API",
        "version": "1.0.0",
        "description": "API для Организации Союзных Микрогосударств",
        "endpoints": {
            "GET /": "Информация об API",
            "GET /api/nations": "Список всех государств",
            "GET /api/nations/<id>": "Информация о конкретном государстве",
            "GET /api/nations/status/<status>": "Государства по статусу",
            "GET /api/osm": "Информация об ОСМ",
            "POST /api/nations": "Добавить новое государство",
            "PUT /api/nations/<id>": "Обновить государство",
            "DELETE /api/nations/<id>": "Удалить государство"
        },
        "timestamp": datetime.now().isoformat()
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
    required_fields = ['name', 'capital', 'government_type']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({
                "error": f"Отсутствует обязательное поле: {field}",
                "timestamp": datetime.now().isoformat()
            }), 400)
    
    # Генерация ID из названия
    nation_id = data['name'].lower().replace(' ', '-')
    
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
        "government_type": data['government_type'],
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
    
    # Обновляем количество членов в ОСМ
    if new_nation['status'] == 'member':
        osm_info['member_count'] += 1
    
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
    old_status = nation['status']
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
    
    # Обновляем статус и счетчик ОСМ
    new_status = data.get('status', nation['status'])
    if new_status != old_status:
        nation['status'] = new_status
        if new_status == 'member':
            osm_info['member_count'] += 1
        elif old_status == 'member':
            osm_info['member_count'] -= 1
    
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
    
    # Удаляем государство
    nations = [n for n in nations if n['id'] != nation_id]
    
    # Обновляем счетчик ОСМ
    if nation['status'] == 'member':
        osm_info['member_count'] -= 1
    
    return jsonify({
        "message": f"Государство {nation['name']} успешно удалено",
        "timestamp": datetime.now().isoformat()
    })

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)
