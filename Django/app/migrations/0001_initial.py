# Generated by Django 5.0.9 on 2024-11-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HistoricalReturn",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField(unique=True, verbose_name="日期")),
                (
                    "market_historical_return",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="大盤歷史回報率"
                    ),
                ),
                (
                    "portfolio_historical_return",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="本投資組合歷史回報率"
                    ),
                ),
            ],
            options={
                "verbose_name": "Historical Return",
                "verbose_name_plural": "Historical Returns",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "stock_code",
                    models.CharField(
                        max_length=20,
                        primary_key=True,
                        serialize=False,
                        verbose_name="股票代號",
                    ),
                ),
                ("company_name", models.CharField(max_length=100, verbose_name="公司名稱")),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2, max_digits=5, verbose_name="權重"
                    ),
                ),
                (
                    "opening_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="開盤價"
                    ),
                ),
                (
                    "closing_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="收盤價"
                    ),
                ),
                (
                    "transaction_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="成交價"
                    ),
                ),
                (
                    "highest_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="最高價"
                    ),
                ),
                (
                    "lowest_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="最低價"
                    ),
                ),
                (
                    "average_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="均價"
                    ),
                ),
                (
                    "price_change_rate",
                    models.DecimalField(
                        decimal_places=2, max_digits=5, verbose_name="漲跌幅"
                    ),
                ),
                (
                    "total_transaction_volume",
                    models.BigIntegerField(verbose_name="總成交量"),
                ),
            ],
            options={"verbose_name": "Stock", "verbose_name_plural": "Stocks",},
        ),
    ]
