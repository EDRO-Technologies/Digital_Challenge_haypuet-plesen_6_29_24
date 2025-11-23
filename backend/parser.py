import pandas as pd
import re
import warnings
import json
from typing import List, Dict, Any, BinaryIO


class ScheduleParser:
    def __init__(self, file: BinaryIO | None = None, file_path: str = ""):
        self.file_path = file_path
        self.file = file
        self.file.seek(0)
        self.sheets_data = {}

    def parse_file(self) -> Dict[str, List[Dict]]:
        """Основной метод для парсинга всего файла"""
        try:
            if hasattr(self.file, "getbuffer"):
                print("size:", len(self.file.getbuffer()))
            excel_file = pd.ExcelFile(self.file, engine='openpyxl')

            for sheet_name in excel_file.sheet_names:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    df = pd.read_excel(self.file, sheet_name=sheet_name, header=None, engine='openpyxl')
                    self.file.seek(0)

                self.sheets_data[sheet_name] = self._parse_sheet(df, sheet_name)

            return self.sheets_data

        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return {}

    def _parse_sheet(self, df: pd.DataFrame, sheet_name: str) -> List[Dict]:
        """Парсинг отдельного листа с несколькими группами"""
        schedule_data = []

        # Ищем все группы на листе
        groups_info = self._find_all_groups(df)

        for group_info in groups_info:
            group_schedule = self._parse_group_schedule(df, group_info)
            schedule_data.extend(group_schedule)

        return schedule_data

    def _find_all_groups(self, df: pd.DataFrame) -> List[Dict]:
        """Находит все группы на листе"""
        groups_info = []

        # Ищем заголовки с номерами групп - более строгий паттерн
        group_pattern = r'\d{3}-\d{2}'  # Только номера групп вида 606-XX

        for row_idx in range(len(df)):
            for col_idx in range(len(df.columns)):
                cell_value = self._safe_get_cell(df, row_idx, col_idx)
                if cell_value and re.search(group_pattern, str(cell_value)):
                    group_number = str(cell_value).strip()

                    # Пропускаем если это год (2025-2026)
                    if re.search(r'202[0-9]-202[0-9]', group_number):
                        continue

                    # Определяем структуру группы
                    group_structure = self._analyze_group_structure(df, row_idx, col_idx, group_number)

                    # Проверяем, что это новая группа (избегаем дубликатов)
                    if not any(g['group_number'] == group_number for g in groups_info):
                        groups_info.append(group_structure)

        return groups_info

    def _analyze_group_structure(self, df: pd.DataFrame, group_row: int, group_col: int, group_number: str) -> Dict:
        """Анализирует структуру группы и определяет границы"""
        # Определяем начало данных (ищем строку с заголовком "д/н" или дни недели)
        start_row = self._find_data_start_row(df, group_row)

        # Определяем конец данных
        end_row = self._find_group_end_row(df, start_row)

        # Определяем границы колонок для этой группы
        start_col, end_col = self._find_group_columns(df, group_col, start_row)

        return {
            'start_row': start_row,
            'end_row': end_row,
            'start_col': start_col,
            'end_col': end_col,
            'group_number': group_number
        }

    def _find_data_start_row(self, df: pd.DataFrame, group_row: int) -> int:
        """Находит начало данных расписания"""
        # Ищем строку с заголовком "д/н" или первую строку с днями недели
        for row_idx in range(group_row, min(group_row + 5, len(df))):
            for col_idx in range(len(df.columns)):
                cell_value = self._safe_get_cell(df, row_idx, col_idx)
                if cell_value and (str(cell_value).strip() in ['д/н', 'ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']):
                    return row_idx + 1  # Данные начинаются на следующей строке

        return group_row + 2  # fallback

    def _find_group_columns(self, df: pd.DataFrame, group_col: int, start_row: int) -> tuple:
        """Определяет границы колонок для группы"""
        # Для левой группы (колонка < 8) - границы 0-6
        # Для правой группы (колонка >= 8) - границы 7-13
        if group_col < 8:
            start_col = 0
            end_col = 6
        else:
            start_col = 7
            end_col = min(13, len(df.columns) - 1)

        return start_col, end_col

    def _find_group_end_row(self, df: pd.DataFrame, start_row: int) -> int:
        """Находит конец данных группы"""
        # Ищем строку с подписями директора или пустые строки
        for row_idx in range(start_row + 10, len(df)):
            for col_idx in range(len(df.columns)):
                cell_value = self._safe_get_cell(df, row_idx, col_idx)
                if cell_value and any(keyword in str(cell_value) for keyword in
                                      ['Директор', 'Зав. кафедрой', 'Примечание']):
                    return row_idx - 1

        # Если не нашли подписи, ищем первую полностью пустую строку
        for row_idx in range(start_row + 10, len(df)):
            row_empty = True
            for col_idx in range(len(df.columns)):
                if self._safe_get_cell(df, row_idx, col_idx) not in [None, '']:
                    row_empty = False
                    break
            if row_empty:
                return row_idx - 1

        return len(df) - 3

    def _parse_group_schedule(self, df: pd.DataFrame, group_info: Dict) -> List[Dict]:
        """Парсит расписание для конкретной группы"""
        schedule = []
        current_day = None

        for row_idx in range(group_info['start_row'], group_info['end_row']):
            # Получаем данные из соответствующих колонок
            day_cell = self._safe_get_cell(df, row_idx, group_info['start_col'])
            pair_cell = self._safe_get_cell(df, row_idx, group_info['start_col'] + 1)
            subject_cell = self._safe_get_cell(df, row_idx, group_info['start_col'] + 2)
            additional_subject_cell = self._safe_get_cell(df, row_idx, group_info['start_col'] + 4)
            teacher_cell = self._safe_get_cell(df, row_idx, group_info['start_col'] + 6)

            # Обновляем текущий день
            if day_cell and day_cell in ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ']:
                current_day = day_cell

            # Парсим пару, если есть данные
            if pair_cell and (subject_cell or additional_subject_cell):
                pair_num_str = str(pair_cell).strip()
                if pair_num_str.isdigit() or '//' in pair_num_str:
                    schedule_items = self._parse_complex_subject_item(
                        current_day, pair_cell, subject_cell, additional_subject_cell,
                        teacher_cell, group_info['group_number']
                    )
                    schedule.extend(schedule_items)

        return schedule

    def _parse_complex_subject_item(self, day: str, pair_num: Any, subject1: Any, subject2: Any, teacher: Any,
                                    group: str) -> List[Dict]:
        """Парсит сложные записи с разделителями //"""
        items = []

        if not day or not pair_num:
            return items

        teacher_str = str(teacher) if pd.notna(teacher) else ""
        teachers_list = self._parse_teacher_info(teacher_str)
        pair_number = self._extract_pair_number(str(pair_num))

        # Обрабатываем первый предмет (основная колонка)
        if pd.notna(subject1) and str(subject1).strip():
            subject1_str = str(subject1)

            # Проверяем, содержит ли строка разделитель //
            if '//' in subject1_str:
                # Разделяем на части по //
                parts = [part.strip() for part in subject1_str.split('//') if part.strip()]

                if len(parts) == 2:
                    # Случай: "Предмет1// Предмет2" - первый числитель, второй знаменатель
                    subject1_info = self._parse_subject_info(parts[0])
                    subject2_info = self._parse_subject_info(parts[1])

                    # Распределяем преподавателей
                    teacher1 = self._assign_teacher_to_subject(teachers_list, subject1_info, 0)
                    teacher2 = self._assign_teacher_to_subject(teachers_list, subject2_info, 1)

                    items.append({
                        'day': day,
                        'pair_number': pair_number,
                        'group': group,
                        'subject': subject1_info['name'],
                        'type': subject1_info['type'],
                        'classroom': subject1_info['classroom'],
                        'subgroup': subject1_info['subgroup'],
                        'teacher': teacher1,
                        'week_type': 'numerator',
                        'full_string': parts[0]
                    })

                    items.append({
                        'day': day,
                        'pair_number': pair_number,
                        'group': group,
                        'subject': subject2_info['name'],
                        'type': subject2_info['type'],
                        'classroom': subject2_info['classroom'],
                        'subgroup': subject2_info['subgroup'],
                        'teacher': teacher2,
                        'week_type': 'denominator',
                        'full_string': parts[1]
                    })
                else:
                    # Если только один разделитель, но много частей
                    for i, part in enumerate(parts):
                        subject_info = self._parse_subject_info(part)
                        week_type = 'numerator' if i == 0 else 'denominator'
                        teacher_assigned = self._assign_teacher_to_subject(teachers_list, subject_info, i)

                        items.append({
                            'day': day,
                            'pair_number': pair_number,
                            'group': group,
                            'subject': subject_info['name'],
                            'type': subject_info['type'],
                            'classroom': subject_info['classroom'],
                            'subgroup': subject_info['subgroup'],
                            'teacher': teacher_assigned,
                            'week_type': week_type,
                            'full_string': part
                        })
            else:
                # Обычный предмет без разделителей
                subject1_info = self._parse_subject_info(subject1_str)
                teacher1 = self._assign_teacher_to_subject(teachers_list, subject1_info, 0)

                items.append({
                    'day': day,
                    'pair_number': pair_number,
                    'group': group,
                    'subject': subject1_info['name'],
                    'type': subject1_info['type'],
                    'classroom': subject1_info['classroom'],
                    'subgroup': subject1_info['subgroup'],
                    'teacher': teacher1,
                    'week_type': 'both',
                    'full_string': subject1_str
                })

        # Обрабатываем второй предмет (дополнительная колонка)
        if pd.notna(subject2) and str(subject2).strip():
            subject2_str = str(subject2)

            if '//' in subject2_str:
                # Аналогичная обработка для второй колонки
                parts = [part.strip() for part in subject2_str.split('//') if part.strip()]

                for i, part in enumerate(parts):
                    subject_info = self._parse_subject_info(part)
                    week_type = 'numerator' if i == 0 else 'denominator'
                    teacher_assigned = self._assign_teacher_to_subject(teachers_list, subject_info, len(items) + i)

                    items.append({
                        'day': day,
                        'pair_number': pair_number,
                        'group': group,
                        'subject': subject_info['name'],
                        'type': subject_info['type'],
                        'classroom': subject_info['classroom'],
                        'subgroup': subject_info['subgroup'],
                        'teacher': teacher_assigned,
                        'week_type': week_type,
                        'full_string': part
                    })
            else:
                # Обычный предмет во второй колонке
                subject2_info = self._parse_subject_info(subject2_str)
                teacher2 = self._assign_teacher_to_subject(teachers_list, subject2_info, len(items))

                items.append({
                    'day': day,
                    'pair_number': pair_number,
                    'group': group,
                    'subject': subject2_info['name'],
                    'type': subject2_info['type'],
                    'classroom': subject2_info['classroom'],
                    'subgroup': subject2_info['subgroup'],
                    'teacher': teacher2,
                    'week_type': 'both',
                    'full_string': subject2_str
                })

        return items

    def _parse_week_type(self, text: str) -> str:
        """Определяет тип недели: числитель, знаменатель или обе недели"""
        text = str(text).strip()

        if re.search(r'[^/]//', text) or text.endswith('//'):
            return 'numerator'
        elif re.search(r'^//', text) or re.search(r'[^/]//[^/]', text):
            return 'denominator'
        return 'both'

    def _extract_pair_number(self, pair_text: str) -> int:
        """Извлекает номер пары из текста"""
        numbers = re.findall(r'\d+', str(pair_text))
        if numbers:
            return int(numbers[0])
        return 0

    def _assign_teacher_to_subject(self, teachers: List[str], subject_info: Dict, subject_index: int) -> List[str]:
        """Назначает преподавателей предметам на основе подгрупп"""
        if not teachers:
            return []

        if len(teachers) > 1:
            if subject_index < len(teachers):
                return [teachers[subject_index]]
            else:
                return [teachers[-1]]
        else:
            return teachers

    def _parse_subject_info(self, subject_str: str) -> Dict:
        """Парсит информацию о предмете из строки"""
        cleaned_str = re.sub(r'^\s*//|//\s*$', '', subject_str).strip()

        subject_pattern = r'^([^(,]+)'
        type_pattern = r'\((лек|пр|лаб)\)'
        classroom_pattern = r'([А-Я]\d{2,})'
        subgroup_pattern = r'п/г\s*(\d+)'

        subject_name = re.search(subject_pattern, cleaned_str)
        lesson_type = re.search(type_pattern, cleaned_str)
        classroom = re.search(classroom_pattern, cleaned_str)
        subgroup = re.search(subgroup_pattern, cleaned_str)

        return {
            'name': subject_name.group(1).strip() if subject_name else cleaned_str,
            'type': lesson_type.group(1) if lesson_type else '',
            'classroom': classroom.group(1) if classroom else '',
            'subgroup': subgroup.group(1) if subgroup else ''
        }

    def _parse_teacher_info(self, teacher_str: str) -> List[str]:
        """Парсит информацию о преподавателях"""
        if not teacher_str or teacher_str.strip() == '':
            return []

        teachers = re.split(r'[;/]', teacher_str)
        return [teacher.strip() for teacher in teachers if teacher.strip()]

    def _safe_get_cell(self, df: pd.DataFrame, row: int, col: int) -> Any:
        """Безопасное получение значения ячейки"""
        try:
            if row < len(df) and col < len(df.columns):
                value = df.iloc[row, col]
                return value if pd.notna(value) else None
        except:
            pass
        return None

    def get_all_groups(self) -> List[str]:
        """Возвращает список всех групп"""
        groups = set()
        for sheet_name, schedule in self.sheets_data.items():
            for item in schedule:
                groups.add(item['group'])
        return sorted(list(groups))

    def to_flat_json(self, filename: str = 'schedule.json') -> list[dict]:
        """Конвертирует расписание в плоский JSON и сохраняет в файл"""
        flat_schedule = []

        # Маппинг дней недели в числа
        day_to_number = {
            'ПН': 1, 'пн': 1,
            'ВТ': 2, 'вт': 2,
            'СР': 3, 'ср': 3,
            'ЧТ': 4, 'чт': 4,
            'ПТ': 5, 'пт': 5,
            'СБ': 6, 'сб': 6
        }

        # Маппинг периодичности в числа
        periodicity_map = {
            'both': 1,  # каждая неделя
            'denominator': 2,  # знаменатель
            'numerator': 3  # числитель
        }

        for sheet_name, schedule in self.sheets_data.items():
            for item in schedule:
                # Создаем плоскую запись в нужном формате
                flat_item = {
                    "group_name": item['group'],
                    "week_day": day_to_number.get(item['day'], 0),
                    "periodicity": periodicity_map.get(item['week_type'], 1),
                    "event_num": item['pair_number'],
                    "event_name": f"{item['subject']} ({item['type']})" if item['type'] else item['subject'],
                    "room": item['classroom'],
                    "teacher_name": ", ".join(item['teacher']) if item['teacher'] else ""
                }
                flat_schedule.append(flat_item)

        # Сохраняем в файл
        # with open(filename, 'w', encoding='utf-8') as f:
        #     json.dump(flat_schedule, f, ensure_ascii=False, indent=2)

        # print(f"Расписание сохранено в {filename}")

        # Возвращаем JSON строку для вывода
        # return json.dumps(flat_schedule, ensure_ascii=False, indent=2)

        return flat_schedule

    def print_flat_json_schedule(self, filename: str = 'schedule.json'):
        """Выводит расписание в плоском JSON формате и сохраняет в файл"""
        json_output = self.to_flat_json(filename)
        print(json_output)

    def return_json_schedule(self):
        return json.dumps(self.to_flat_json())


# Пример использования
if __name__ == "__main__":
    parser = ScheduleParser(file_path="ИСиТ.xlsx")
    schedule_data = parser.parse_file()

    if schedule_data:
        parser.print_flat_json_schedule('schedule.json')

    else:
        print("Не удалось распарсить файл")