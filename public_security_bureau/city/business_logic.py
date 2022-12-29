from city.models import Sybil
from django.db import connection
from .models import Citizen, PsychoPassport
from names import get_full_name
import random


def get_last_sybil_record(analyst_id):
    query_set = Sybil.objects.filter(fk_analyst=analyst_id).order_by('-pk')
    if query_set:
        return query_set[0]
    else:
        return None


def get_last_day_and_blackening_coeff(last_sybil_record):
    if last_sybil_record is None:
        return 0, 0.0
    else:
        return last_sybil_record.day_counter, last_sybil_record.blackening_coefficient


def increase_day_counter(last_day):
    next_day = last_day + 1
    return next_day


def number_crimes_for_the_day(analyst_id):
    with connection.cursor() as cursor:
        cursor.callproc('number_of_crimes_for_the_day', [analyst_id])
        return cursor.fetchall()[0][0]


def calc_blackening_coeff(crimes, blackening_coefficient_last):
    with connection.cursor() as cursor:
        cursor.callproc('calc_blackening_coeff_diff', [crimes])
        diff = cursor.fetchone()[0]
        return blackening_coefficient_last + diff


def create_crime_report(crimes, day, coeff):
    return f'День: {day}\n' \
           f'Число преступлений: {crimes}\n' \
           f'Коэфф почернения: {(round(coeff, 2))}'


def create_additional_data(analyst_id):
    last_record = get_last_sybil_record(analyst_id)
    last_day, last_coeff = get_last_day_and_blackening_coeff(last_record)
    crimes = number_crimes_for_the_day(analyst_id)
    day = increase_day_counter(last_day)
    coeff = round(calc_blackening_coeff(crimes, last_coeff), 2)
    crime_report = create_crime_report(crimes, day, coeff)
    return [crime_report, day, crimes, coeff]


def additional_data_for_new_sybil_record(data_from_req, data_to_add):
    data_from_req['crimes_report'] = data_to_add[0]
    data_from_req['day_counter'] = data_to_add[1]
    data_from_req['number_of_crimes'] = data_to_add[2]
    data_from_req['blackening_coefficient'] = data_to_add[3]
    return data_from_req


def random_name():
    return get_full_name().split(' ')


def create_n_citizens(n, analyst_id):
    for i in range(n):
        name = random_name()
        Citizen.objects.create(fk_analyst=analyst_id, first_name=name[0], second_name=name[1],
                               stamina=random.randint(1, 5), intelligence=random.randint(50, 200))


def random_unique_numbers(low, high, n):
    result = []
    seen = set()
    for i in range(n):
        x = random.randint(low, high)
        while x in seen:
            x = random.randint(low, high)
        seen.add(x)
        result.append(x)
    return result


def create_random_psycho_passport_for_citizens(analyst):
    series = random.randint(1000, 9999)
    query_set = Citizen.objects.filter(fk_analyst_id=analyst.pk)
    number_l = random_unique_numbers(100000, 999999, len(query_set))
    for i, citizen in enumerate(query_set):
        PsychoPassport.objects.create(fk_citizen_id=citizen.citizen_id, series=series,
                                      number=number_l[i], crime_rate=random.randint(10, 340))
