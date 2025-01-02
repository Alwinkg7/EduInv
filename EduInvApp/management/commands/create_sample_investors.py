# EduInvApp/management/commands/create_sample_investors.py
from django.core.management.base import BaseCommand
from EduInvApp.models import investorapplicationdb

class Command(BaseCommand):
    help = 'Create sample investors for testing'

    def handle(self, *args, **kwargs):
        investors = [
            {'Investor_first_name': 'Alice', 'Investor_last_name': 'Smith', 'total_investment': 10000.00},
            {'Investor_first_name': 'Bob', 'Investor_last_name': 'Johnson', 'total_investment': 15000.00},
            {'Investor_first_name': 'Charlie', 'Investor_last_name': 'Brown', 'total_investment': 20000.00},
            {'Investor_first_name': 'David', 'Investor_last_name': 'Williams', 'total_investment': 25000.00},
            {'Investor_first_name': 'Eva', 'Investor_last_name': 'Davis', 'total_investment': 30000.00},
        ]
        for investor in investors:
            investorapplicationdb.objects.create(**investor)
        self.stdout.write(self.style.SUCCESS('Sample investors created successfully.'))
