# Generated by Django 4.2.16 on 2024-09-19 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investmentmanager', '0003_remove_transaction_code_remove_transaction_language_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transactiontype',
            field=models.CharField(choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')], default='deposit', max_length=100),
        ),
    ]
