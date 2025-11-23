import requests
import config
from typing import Optional, Dict, Any
from datetime import datetime

class APIClient:
    @staticmethod
    def create_event(event_data: Dict[str, Any]) -> Optional[Dict]:
        """Создание мероприятия через API"""
        try:
            print("Данные об ивенте:", event_data)
            
            # Получение ид пользователя
            url = f"{config.API_URL}/users/telegram_id/{event_data['created_by']}"
            userdata = requests.get(f"{config.API_URL}/users/telegram_id/{event_data['created_by']}")
            userdata.raise_for_status()

            # Создание ивента и получение его ид
            event_data['created_by'] = userdata.json()['id']
            print(event_data)
            response = requests.post(config.EVENTS_API_URL, json={"name": event_data['title'], "week_day": 0, "num": 0, "date": event_data["date"], "duration": event_data["duration"], "periodicity": 0, "created_by": event_data['created_by']})
            print("Создание ивента: ", response.json())
            event_id = response.json()['id']
            response.raise_for_status()
            
            # Создание группы участников
            url = f"{config.API_URL}/groups"
            response = requests.post(url, json={"name": f"Участники {event_data['title']}"})
            print("Создание группы участников:", response.json())
            group_id = response.json()['id']
            response.raise_for_status()
            
            # создание связки ивент - группа
            url = f"{config.API_URL}/event-groups"
            print(event_id,group_id)
            response = requests.post(url, json={"event_id": event_id, "group_id": group_id})
            print("Создание ивента-группы ", response.json())
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"API Error (create_event): {e}")
            return None

    @staticmethod
    def participate_event(event_id: str, user_data: Dict[str, Any]) -> bool:
        """Участие в мероприятии"""
        try:
            print("111")
            # Получение системный ид пользователя
            userdata = requests.get(f"{config.API_URL}/users/telegram_id/{user_data['id']}")
            userdata.raise_for_status()
            print("userdata", userdata.json())
            
            # Получение ид группы по ид ивента
            eventgroupdata = requests.get(f"{config.API_URL}/event-groups?event_id={event_id}", json={})
            eventgroupdata.raise_for_status()
            print("eventgroupdata", eventgroupdata.json())
            # Создаем связь пользователь - группа участников
            response = requests.post(f"{config.API_URL}/user-groups", json={"user_id": userdata.json()['id'], "group_id": eventgroupdata.json()[0]['group_id']})
            response.raise_for_status()
            print("response", response.json())
            return True
        except Exception as e:
            print(f"API Error (participate_event): {e}")
            return False

    @staticmethod
    def get_users_with_notifications() -> list:
        """Получение пользователей с включенными уведомлениями"""
        try:
            print("Getting users with notif")
            headers = {'Authorization': f'Bearer {config.API_TOKEN}'}
            response = requests.get(config.NOTIFICATIONS_API_URL, headers=headers)
            response.raise_for_status()
            print(response.json())
            return response.json()
        except Exception as e:
            print(f"API Error (get_users_with_notifications): {e}")
            return []
          
    @staticmethod
    def update_user_settings(user_id: int, notifications_enabled: bool) -> bool:
        """Обновление настроек пользователя"""
        try:
            # ЗАГЛУШКА для API - в реальности здесь будет POST/PUT запрос
            print(f"🔧 Saving user settings: user_id={user_id}, notifications={notifications_enabled}")
            
            # Имитация успешного сохранения
            # В реальном приложении здесь будет:
            headers = {'Authorization': f'Bearer {config.API_TOKEN}'}
            data = {'need_notification': notifications_enabled}
            response = requests.patch(f"{config.API_URL}/users/telegram_id/{user_id}", json=data, headers=headers)
            response.raise_for_status()
            
            return True
        except Exception as e:
            print(f"API Error (update_user_settings): {e}")
            return False

    @staticmethod
    def get_user_settings(user_id: int) -> Dict[str, Any]:
        """Получение настроек пользователя"""
        try:
            # ЗАГЛУШКА для API - в реальности здесь будет GET запрос
            print(f"🔧 Getting user settings for: {user_id}")
            
            # Имитация получения настроек (по умолчанию включены)
            # В реальном приложении здесь будет:
            headers = {'Authorization': f'Bearer {config.API_TOKEN}'}
            response = requests.get(f"{config.API_URL}/users/telegram_id/{user_id}", headers=headers)
            response.raise_for_status()
            print('2:',response.json())
            return {'notifications_enabled': response.json()['need_notification']}
            
            return {'notifications_enabled': True}  # Заглушка - всегда включено
        except Exception as e:
            print(f"API Error (get_user_settings): {e}")
            return {'notifications_enabled': True}  # По умолчанию включено
          
    @staticmethod
    def check_time_conflict(user_tgid: int, event_date: str, event_time: str, event_duration: int) -> Dict[str, Any]:
        """Проверка конфликта времени с учетом продолжительности"""
        try:
            user_id = APIClient.user_by_tgid(user_tgid)
            print(f"🔍 Checking time conflict for user {user_tgid} (user_id) on {event_date} at {event_time} for {event_duration}min")
            
            # Получаем мероприятия пользователя
            # user_events = _get_mock_user_events(user_id)
            
            all_events = APIClient.get_all_events()
            
            user_events = []
    
            for event in all_events:
                if user_id in event['participants']:
                    user_events.append(event)
            
            
            
            # Конвертируем время нового мероприятия в минуты от начала дня
            new_event_start_minutes = _time_to_minutes(event_time)
            new_event_end_minutes = new_event_start_minutes + event_duration
            print("Time:", new_event_start_minutes,new_event_end_minutes)
            # print("all_events", all_events)
            # print("user_events", user_events)
            
            
            conflicts = []
            for event in user_events:
                event['time'] = datetime.fromisoformat(event['date']).strftime('%H:%M')
                event['date'] = datetime.fromisoformat(event['date']).strftime('%d.%m.%Y')
                print(event['date'], event_date, event['date'] == event_date)
                # Проверяем только мероприятия на ту же дату
                if event['date'] == event_date:
                    event_start_minutes = _time_to_minutes(event['time'])
                    event_end_minutes = event_start_minutes + event['duration']
                    print('event_start_minutes', event_start_minutes, 'event_end_minutes', event_end_minutes, 'new_event_start_minutes', new_event_start_minutes, 'new_event_end_minutes', new_event_end_minutes)
                    # Проверяем пересечение интервалов
                    if (new_event_start_minutes < event_end_minutes and 
                        new_event_end_minutes > event_start_minutes):
                        conflicts.append(event)
            
            return {
                'has_conflict': len(conflicts) > 0,
                'conflicting_events': conflicts
            }
            
        except Exception as e:
            print(f"API Error (check_time_conflict): {e}")
            return {'has_conflict': False, 'conflicting_events': []}
          
    @staticmethod
    def user_database_check(user) -> bool:
        """Участие в мероприятии"""
        try:
            # Получение системный ид пользователя
            userdata = requests.get(f"{config.API_URL}/users/telegram_id/{user.id}", timeout=3)
            if 'detail' in userdata.json() and userdata.json()['detail'] == 'User not found':
              if user.last_name:
                json = {  "name": f"{user.first_name} {user.last_name}",  "telegram_id": user.id,  "role": 3,  "need_notification": True }
              else:
                json = {  "name": f"{user.first_name}",  "telegram_id": user.id,  "role": 3,  "need_notification": True }
              req = requests.post(f"{config.API_URL}/users", json=json)
              print("Создан пользователь:", req.json())
              req.raise_for_status()
            else:
              userdata.raise_for_status()
            
            
            return True
        except Exception as e:
            print(f"API Error (user_database_check): {e}")
            return False
    
    @staticmethod
    def user_by_tgid(tgid) -> int:
        """Участие в мероприятии"""
        try:
            # Получение системный ид пользователя
            userdata = requests.get(f"{config.API_URL}/users/telegram_id/{tgid}", timeout=3)
            userdata.raise_for_status()
            
            return userdata.json()['id']
        except Exception as e:
            print(f"API Error (user_database_check): {e}")
            return 0
          
    @staticmethod
    def get_all_events() -> Dict[str, Any]:
        """Участие в мероприятии"""
        try:
            # Получение системный ид пользователя
            eventsdataall = requests.get(f"{config.API_URL}/events?date_from={str(datetime.now())}", timeout=3)
            eventsdataall.raise_for_status()
            
            res = []
            for eventsdata in eventsdataall.json():
              eventgroupdata = requests.get(f"{config.API_URL}/event-groups?event_id={eventsdata['id']}", timeout=3)
              eventgroupdata.raise_for_status()
                  
              usergroupdata = requests.get(f"{config.API_URL}/user-groups?group_id={eventgroupdata.json()[0]['group_id']}", timeout=3)
              usergroupdata.raise_for_status()
              
              userlist = []
              for user in usergroupdata.json():
                userlist.append(user['user_id'])
            
              eventsdata['participants'] = userlist
              eventsdata['participants_count'] = len(userlist)
              eventsdata['title'] = eventsdata['name']
              res.append(eventsdata)
            
            return res
        except Exception as e:
            print(f"API Error (get_all_events): {e}")
            return {
                'Error': True
            }
    @staticmethod    
    def get_user_group(user_tgid: int) -> Dict[str, Any]:
        try:
            print(f"Getting group for user {user_tgid}")
            user_id = APIClient.user_by_tgid(user_tgid)
            response = requests.get(f"{config.API_URL}/user-groups?user_id={user_id}")
            
            for usergroup in response.json():
                print("usergroup",usergroup['group_id'])
                responsegroup = requests.get(f"{config.API_URL}/groups/{usergroup['group_id']}")
                print("responsegroup.json()", responsegroup.json())
                if responsegroup.json()['name'][0].isdigit():
                    return responsegroup.json()
                
        except Exception as e:
            print(f"STUB Error (get_user_group): {e}")
            return ""
    @staticmethod
    def update_user_group(user_id: int, group_data: Dict[str, Any]) -> bool:
        try:
            print(f"Updating user {user_id} group to {group_data}")
            
            
            # Заглушка успешного сохранения
            return True
        except Exception as e:
            print(f"STUB Error (update_user_group): {e}")
            return False
        
    @staticmethod
    def get_events_by_group(group: int) -> Dict[str, Any]:
        try:
            print(f"Loading event data for group {group}")
            
            response = requests.get(f"{config.API_URL}/events/by_group_id/{group['id']}")
            print(response.json())
            # Заглушка успешного сохранения
            return response.json()
        except Exception as e:
            print(f"STUB Error (get_events_by_group): {e}")
            return {'error': True}
    
    

def _time_to_minutes(time_str: str) -> int:
    """Конвертирует время в формате 'HH:MM' в минуты от начала дня"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        print(hours, minutes)
        return hours * 60 + minutes
    except:
        return 0

# def _get_mock_user_events(user_id: int):
#     """ЗАГЛУШКА: получение мероприятий пользователя для проверки конфликтов"""
    
    
#     return [
#         {
#             'id': 'event_001',
#             'title': 'Встреча IT-клуба',
#             'date': '15.12.2024',
#             'time': '18:00',
#             'duration': 120,  # 2 часа в минутах
#             'description': 'Обсуждение новых технологий'
#         },
#         {
#             'id': 'event_002',
#             'title': 'Мастер-класс по Python', 
#             'date': '17.12.2024',
#             'time': '16:30',
#             'duration': 90,  # 1.5 часа в минутах
#             'description': 'Практическое занятие'
#         }
#     ]