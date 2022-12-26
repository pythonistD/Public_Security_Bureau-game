from city.models import Sybil
from django.db import connection


def get_last_sybil_record(analyst_id):
    return Sybil.objects.filter(fk_analyst=analyst_id).order_by('-pk')[0]


def increase_day_counter(analyst_id):
    last_sybil = get_last_sybil_record(analyst_id)
    next_day = last_sybil.day_counter + 1
    return next_day


def number_crimes_for_the_day(analyst_id):
    with connection.cursor() as cursor:
        cursor.callproc('number_of_crimes_for_the_day', [analyst_id])
        return cursor.fetchall()[0][0]


def calc_blackening_coeff(crimes, analyst_id):
    with connection.cursor() as cursor:
        cursor.callproc('calc_blackening_coeff_diff', [crimes])
        diff = cursor.fetchone()[0]
        last_sybil = get_last_sybil_record(analyst_id)
        return last_sybil.blackening_coefficient + diff


def create_crime_report(crimes, day, coeff):
    return f'День: {day}\n' \
           f'Число преступлений: {crimes}\n' \
           f'Коэфф почернения: {(round(coeff, 2))}'


def additional_data_for_new_sybil_record(data):
    analyst_id = data['fk_analyst']
    crimes = number_crimes_for_the_day(analyst_id)
    day = increase_day_counter(analyst_id)
    coeff = calc_blackening_coeff(crimes, analyst_id)
    data['crimes_report'] = create_crime_report(crimes, day, coeff)
    data['day_counter'] = day
    data['number_of_crimes'] = crimes
    data['blackening_coefficient'] = round(coeff, 2)
    return data
