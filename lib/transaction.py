from __future__ import division
from datetime import datetime, timedelta

class Transaction():

    def __init__(self, active, isinsideallowlist, limit ,merchant, amount, \
    last_transactions, denylist, time_transaction):

        self.__active = active
        self.__isinsideallowlist = isinsideallowlist
        self.__limit = limit
        self.__amount = amount
        self.__merchant = merchant
        self.__last_transactions = last_transactions
        self.__denylist = denylist
        self.__time_transaction = time_transaction

    def validateFields(self):
        if not isinstance(self.__active, bool):
            raise Exception('The value of active should be boolean')

        if not isinstance(self.__isinsideallowlist, bool):
            raise Exception('The value of insideallowlist should be boolean')

        if not isinstance(self.__limit,  (float, int)):
            raise Exception('The value of limit should be int or float')

        if not isinstance(self.__amount, (float, int)):
            raise Exception('The value of amount should be int or float')

        if not isinstance(self.__merchant, (unicode, str)):
            raise Exception('The value of merchant should be unicode or string')

        if not isinstance(self.__last_transactions, list):
            raise Exception('The type of last_transactions should be list')

        if not isinstance(self.__denylist, list):
            raise Exception('The type of denylist should be list')
        else:
            for item in self.__denylist:
                if not isinstance(item, (str, unicode)):
                    raise Exception('The type of items in denylist should be unicode or string')
        try:
            datetime.strptime(self.__time_transaction, '%Y-%m-%d %H:%M:%S')
        except:
            raise Exception('Invalid date format shoud be %Y-%m-%d %H:%M:%S')

        return True

    def getkWithinLimit(self):
        if self.__limit >= self.__amount:
            return True
        else:
            return False

    def getActive(self):
        if self.__active == True:
            return True
        else:
            return False

    def getNewLimit(self):
        new_limit = self.__limit - self.__amount
        return new_limit

    def getFirstBelowPercent(self):
        if len(self.__last_transactions) == 0:
            try:
                percent = ( self.__amount / self.__limit ) * 100
            except ZeroDivisionError:
                return False
            if percent <= 90:
                return True
            else:
                self.__last_transactions = []
                return False
        else:
            return True

    def checkLessTenMerchantRule(self):
        merchants = {}
        for last_transaction in self.__last_transactions:
            if last_transaction['merchant'] not in merchants:
                merchants[last_transaction['merchant']] = 1
            else:
                merchants[last_transaction['merchant']] +=1
        for key, value in merchants.items():
            if value > 10 and self.__merchant == key:
                return False
        return True

    def checkOutDenyList(self):
        if self.__merchant in self.__denylist:
            return False
        else:
            return True

    def checkLessThanFourInTwoMinutes(self):
        if len(self.__last_transactions) >= 3:
            dates = []
            for item in self.__last_transactions:
                dates.append(datetime.strptime(item['time'],'%Y-%m-%d %H:%M:%S'))

            dates.sort()
            interval = datetime.strptime(self.__time_transaction, '%Y-%m-%d %H:%M:%S') - dates[-3]
            if interval < timedelta(minutes=2):
                return False
            else:
                return True
        else:
            return True
