def get_free_windows_script(busy_intervals, start_time='09:00', end_time='21:00', window_length=30):
    '''

    :param busy_intervals: список словарей формата: [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},]
    :param start_time: время начала формата '09:00' (str)
    :param end_time: время окончания формата '21:00' (str)
    :param window_length: количество минут в свободных окнах (int)
    :return: список словарей с началом и окончанием свободных окон
    '''
    from datetime import datetime, timedelta

    def parse_time(time_str):
        # Преобразует строку времени в объект datetime
        return datetime.strptime(time_str, '%H:%M')

    def get_free_windows(busy_times, start_time, end_time, window_length):
        # Преобразуем начальное и конечное время в объекты datetime
        start = parse_time(start_time)
        end = parse_time(end_time)

        # Сортируем занятые интервалы по времени начала
        busy = sorted([(parse_time(i['start']), parse_time(i['stop'])) for i in busy_times], key=lambda x: x[0])

        free_windows = []
        current_start = start

        for start_busy, end_busy in busy:
            # Находим все свободные окна между текущим началом и началом занятого интервала
            while current_start + timedelta(minutes=window_length) <= start_busy:
                free_windows.append({'start': current_start.strftime('%H:%M'),
                                     'stop': (current_start + timedelta(minutes=window_length)).strftime('%H:%M')})
                current_start += timedelta(minutes=window_length)

            # Обновляем текущее начальное время, чтобы исключить текущий занятый интервал
            current_start = max(current_start, end_busy)

        # Находим свободные окна между последним занятым интервалом и концом рабочего дня
        while current_start + timedelta(minutes=window_length) <= end:
            free_windows.append({'start': current_start.strftime('%H:%M'),
                                 'stop': (current_start + timedelta(minutes=window_length)).strftime('%H:%M')})
            current_start += timedelta(minutes=window_length)

        return free_windows

    # Вызываем функцию get_free_windows с переданными параметрами
    return get_free_windows(busy_intervals, start_time, end_time, window_length)


# Используем функцию с заданными интервалами занятости
busy_intervals = [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},
    {'start': '14:40', 'stop': '15:50'},
    {'start': '16:40', 'stop': '17:20'},
    {'start': '20:05', 'stop': '20:20'}
]

# Получаем список свободных 30-минутных окон (ну или других окон по желанию)
free_30_min_windows = get_free_windows_script(busy_intervals)
free_22_min_windows = get_free_windows_script(busy_intervals, window_length=22)
free_30_min_windows_another_work_time = get_free_windows_script(busy_intervals, start_time='8:00', end_time='22:00')
print(*free_30_min_windows, sep='\n')
print('#'*44)
print(*free_22_min_windows, sep='\n')
print('#'*44)
print(*free_30_min_windows_another_work_time, sep='\n')