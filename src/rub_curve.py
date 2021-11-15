from interpolation import Interpolator
import numpy as np
import datetime
from datetime import date

class CurveTransofmator(object):
    def __init__(self, ccy1DiscountFactors, ccy1ccy2SwapPoints, spot, pip):
        self.ccy1DiscountFactors = ccy1DiscounrFactors
        self.ccy1ccy2SwapPoints = ccy1ccy2SwapPoints
        self.spot = spot
        self.pip = pip
        
    def _getInterpolatedData(self, data, dates):
        _data = list(map(list, zip(*data)))
        interpolatedData = []
        for _date in dates:
            tmp = Interpolator.interpolate(_data[0], _data[1], _date)
            interpolatedData.append(tmp)
        return interpolatedData
        
    def getTransformedCurve(self, dates):
        # we can use 2 equations of fx forwards (with swap points and with discount factors)
        
        #extrapolation and interpolation tests assumed in class Interpolator
        ccy1DiscountFactors = self._getInterpolatedData(self.ccy1DiscountFactors, dates)
        ccy1ccy2SwapPoints =  self._getInterpolatedData(self.ccy1ccy2SwapPoints, dates)
        ccy2DiscountFactors = np.array(ccy1DiscountFactors) / (1 + np.array(ccy1ccy2SwapPoints) * self.pip / self.spot)
        
        result = list(map(list, zip(dates, ccy2DiscountFactors)))
        return result
        
if __name__ == "__main__":
    # can be result of USD discount factor frunction
    # https://www.cashbackforex.com/tools/pip-calculator/USDRUB
    # assumed that datetime tranformed into float tenor, because interpolator can't read datetime
    USDRUB_pip = 0.0001
    spot = 72    
    calcDate = datetime.date(2021, 11, 1)
    
    # some test unrealistic data, ccy1DiscounrFactors is result of df function
    # ccy1DiscounrFactors = [[0.1, 0.98], [0.2, 0.95]]
    # ccy1ccy2SwapPoints = [[0.1, 1233], [0.2, 15002]]
    # ccy1ccy2SwapPoints = [[0.1, 933], [0.2, 2269]]
    # dates = [0.1, 0.12, 0.14, 0.16, 0.2]
    
    ccy1DiscounrFactors = [[date(2021, 11, 8), 0.98], [date(2021, 11, 15), 0.95]]
    ccy1ccy2SwapPoints = [[date(2021, 11, 8), 933], [date(2021, 11, 15), 2269]]
    dates = [date(2021, 11, 8), date(2021, 11, 10), date(2021, 11, 13), date(2021, 11, 15)]
    
    # we want to get RUB discount factors from USD discount factors + USDRUB swap points
    ct = CurveTransofmator(ccy1DiscounrFactors, ccy1ccy2SwapPoints, spot, USDRUB_pip)
    ccy2DiscounrFactors = ct.getTransformedCurve(dates)
    
    print(ccy2DiscounrFactors)
    print("Done")