class MovingAvg(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    """
    params = (
        ('period_15',15),
        ('period_20',20),
    )
    """

    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #self.sma = bt.indicators.SimpleMovingAverage(self.data0, period = self.params.pfast)
        self.sma = bt.indicators.SMA(self.datas[0], period = self.p.pfast)

    def next(self):
        if not self.position:  # not in the market
            if self.datas[0].close[0] > self.sma[0]:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.datas[0].close[0] < self.sma[0]:  # in the market & cross to the downside
            self.order = self.sell()  # close long position

class SmaCross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30   # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy()  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position