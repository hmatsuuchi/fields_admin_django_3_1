from rest_framework import serializers
from .models import Account, JournalEntry, JournalEntryLine


class JournalEntryLineInputSerializer(serializers.Serializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.filter(archived=False))
    side = serializers.ChoiceField(choices=['DEBIT', 'CREDIT'])
    amount = serializers.IntegerField(min_value=1)


class JournalEntryCreateSerializer(serializers.Serializer):
    date = serializers.DateField()
    description = serializers.CharField()
    reference = serializers.CharField(required=False, allow_blank=True, default='')
    lines = JournalEntryLineInputSerializer(many=True)

    def validate_lines(self, lines):
        if len(lines) < 2:
            raise serializers.ValidationError('A journal entry must have at least two lines.')
        if not any(l['side'] == 'DEBIT' for l in lines):
            raise serializers.ValidationError('A journal entry must have at least one debit line.')
        if not any(l['side'] == 'CREDIT' for l in lines):
            raise serializers.ValidationError('A journal entry must have at least one credit line.')
        debits = sum(l['amount'] for l in lines if l['side'] == 'DEBIT')
        credits = sum(l['amount'] for l in lines if l['side'] == 'CREDIT')
        if debits != credits:
            raise serializers.ValidationError('Debits must equal credits.')
        return lines

    def create(self, validated_data):
        lines_data = validated_data.pop('lines')
        entry = JournalEntry(**validated_data)
        entry.save_with_lines([
            {'account': l['account'], 'side': l['side'], 'amount': l['amount']}
            for l in lines_data
        ])
        return entry


class JournalEntryLineSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()

    class Meta:
        model = JournalEntryLine
        fields = ['id', 'account', 'side', 'amount']


class JournalEntrySerializer(serializers.ModelSerializer):
    lines = JournalEntryLineSerializer(many=True, read_only=True)

    class Meta:
        model = JournalEntry
        fields = ['id', 'date', 'description', 'reference', 'date_time_created', 'lines']