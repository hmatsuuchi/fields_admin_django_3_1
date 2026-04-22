from django.db import models, transaction
from django.core.exceptions import ValidationError

class Account(models.Model):
    ACCOUNT_CHOICES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('EQUITY', 'Equity'),
        ('REVENUE', 'Revenue'),
        ('EXPENSE', 'Expense'),
    ]

    code = models.CharField(max_length=20, unique=True)
    name_japanese = models.CharField(max_length=255)
    name_english = models.CharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_CHOICES)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.code} [{self.account_type}] - {self.name_japanese} ({self.name_english})'

    @property
    def normal_balance(self):
        if self.account_type in ('ASSET', 'EXPENSE'):
            return 'debit'
        return 'credit'

    def balance(self, as_of=None):
        lines = JournalEntryLine.objects.filter(account=self)
        if as_of:
            lines = lines.filter(entry__date__lte=as_of)
        debits = lines.filter(side='DEBIT').aggregate(
            total=models.Sum('amount'))['total'] or 0
        credits = lines.filter(side='CREDIT').aggregate(
            total=models.Sum('amount'))['total'] or 0
        if self.normal_balance == 'debit':
            return debits - credits
        return credits - debits


class JournalEntry(models.Model):
    date = models.DateField()
    description = models.TextField()
    reference = models.CharField(max_length=100, blank=True)
    date_time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date} - {self.description}'

    @transaction.atomic
    def save_with_lines(self, lines_data):
        """
        Save entry and lines atomically, then enforce balance.
        lines_data: list of dicts with keys 'account', 'side', 'amount'
        """
        if not lines_data:
            raise ValidationError('A journal entry must have at least one line.')
        if len(lines_data) < 2:
            raise ValidationError('A journal entry must have at least two lines.')
        if not any(l['side'] == 'DEBIT' for l in lines_data):
            raise ValidationError('A journal entry must have at least one debit line.')
        if not any(l['side'] == 'CREDIT' for l in lines_data):
            raise ValidationError('A journal entry must have at least one credit line.')
        self.save()
        for line in lines_data:
            if line.get('amount') is None or line['amount'] <= 0:
                raise ValidationError('Amount must be greater than zero.')
            JournalEntryLine.objects.create(entry=self, **line)
        debits = sum(l['amount'] for l in lines_data if l['side'] == 'DEBIT')
        credits = sum(l['amount'] for l in lines_data if l['side'] == 'CREDIT')
        if debits != credits:
            raise ValidationError('Debits must equal credits.')


class JournalEntryLine(models.Model):
    JOURNAL_ENTRY_LINE_CHOICES = [
        ('DEBIT', 'Debit'),
        ('CREDIT', 'Credit'),
    ]

    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE, related_name='lines')
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    side = models.CharField(max_length=6, choices=JOURNAL_ENTRY_LINE_CHOICES)
    amount = models.IntegerField()

    def __str__(self):
        return f'{self.entry} | {self.account} | {self.side} {self.amount}'

    def clean(self):
        if self.amount is not None and self.amount <= 0:
            raise ValidationError('Amount must be greater than zero.')
