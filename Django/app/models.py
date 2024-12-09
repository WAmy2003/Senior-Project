from django.db import models
from django.utils.translation import gettext_lazy as _

class Stock(models.Model):
    stock_code = models.CharField(_("股票代號"), max_length=20, primary_key=True)
    company_name = models.CharField(_("公司名稱"), max_length=100)
    weight = models.DecimalField(_("權重"), max_digits=5, decimal_places=2)
    opening_price = models.DecimalField(_("開盤價"), max_digits=10, decimal_places=2)
    closing_price = models.DecimalField(_("收盤價"), max_digits=10, decimal_places=2)
    transaction_price = models.DecimalField(_("成交價"), max_digits=10, decimal_places=2)
    highest_price = models.DecimalField(_("最高價"), max_digits=10, decimal_places=2)
    lowest_price = models.DecimalField(_("最低價"), max_digits=10, decimal_places=2)
    average_price = models.DecimalField(_("均價"), max_digits=10, decimal_places=2)
    price_change_rate = models.DecimalField(_("漲跌幅"), max_digits=5, decimal_places=2)
    total_transaction_volume = models.BigIntegerField(_("總成交量"))

    def __str__(self):
        return f"{self.company_name} ({self.stock_code})"

    class Meta:
        verbose_name = _("Stock")
        verbose_name_plural = _("Stocks")

class HistoricalReturn(models.Model):
    date = models.DateField(_("日期"), unique=True)
    market_historical_return = models.DecimalField(_("大盤歷史回報率"), max_digits=10, decimal_places=2)
    portfolio_historical_return = models.DecimalField(_("本投資組合歷史回報率"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - 市場: {self.market_historical_return}%, 投資組合: {self.portfolio_historical_return}%"

    class Meta:
        verbose_name = _("Historical Return")
        verbose_name_plural = _("Historical Returns")
        ordering = ['-date']  # 根據日期降序排列

class HistoryReturns(models.Model):
    date = models.DateField()
    return_0050 = models.FloatField()
    return_0000 = models.FloatField()
    smart_pick = models.FloatField()

    class Meta:
        db_table = 'history_returns'

class PortfolioWeights(models.Model):
    stock_id = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=50)
    weights = models.FloatField()

    class Meta:
        db_table = 'portfolio_weights'  # 對應資料表名稱

class PortfolioWeights0050(models.Model):
    stock_id = models.CharField(max_length=10)
    stock_name = models.CharField(max_length=50)
    weights = models.FloatField()

    class Meta:
        db_table = 'portfolio_weights_0050'  # 對應資料表名稱
