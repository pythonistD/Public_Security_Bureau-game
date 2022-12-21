from django.test import TestCase
from .models import Citizen
from django.db import IntegrityError
import pytest

@pytest.mark.parametrize(
    'stamina',
    [
        (0),
        (-1),
        (100),
    ],
)
def test_stamina_amount(db, stamina):
    with pytest.raises(IntegrityError):
        Citizen.objects.create()