#!flask/bin/python
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify
from lib import transaction

application = Flask(__name__)

Account = {
    'cardIsActive': True,
    'isInsideAllowlist' : True,
    'limit': 1000,
    'denylist': ['Golpe Certo', 'Dinheiro Gratis']
}

last_transactions = []

class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
            Exception.__init__(self)
            self.message = message
            if status_code is not None:
                self.status_code = status_code
            self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@application.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@application.route('/authorize', methods=['POST'])
def postJsonHandler():

    if request.is_json:
        content = request.get_json()
        try:
            active = Account['cardIsActive']
            isinsideallowlist = Account['isInsideAllowlist']
            limit = Account['limit']
            merchant_deny_list = Account['denylist']

            merchant = content['Transaction']['merchant']
            amount = content['Transaction']['amount']
            time_transaction = content['Transaction']['time']

        except KeyError as e:
            raise InvalidUsage('Check if the key %s exist and is in correct format' % e ,status_code=410)

        try:
            t = transaction.Transaction(active, isinsideallowlist ,limit, \
            merchant, amount, last_transactions, merchant_deny_list, time_transaction)

            t.validateFields()

            has_limit = t.getkWithinLimit()
            is_active = t.getActive()
            first_below_percent = t.getFirstBelowPercent()
            ten_merchant_limit = t.checkLessTenMerchantRule()
            out_deny_list = t.checkOutDenyList()
            less_than_four_in_to_minutes = t.checkLessThanFourInTwoMinutes()

            json_output = {
                'approved': None,
                'newLimit': 0,
                'deniedReasons': []
            }

            if has_limit and is_active and first_below_percent and ten_merchant_limit \
            and out_deny_list and less_than_four_in_to_minutes:
                json_output['approved'] = True
                json_output['newLimit'] = Account['limit'] = t.getNewLimit()
                last_transactions.append(content['Transaction'])
            else:
                json_output['approved'] = False
                json_output['newLimit'] = limit
                if not has_limit:
                    json_output["deniedReasons"].append('limitExceeded')
                if not is_active:
                    json_output["deniedReasons"].append('cardIsBlocked')
                if not first_below_percent:
                    json_output["deniedReasons"].append('abovePercentLimitFirsTransaction')
                if not ten_merchant_limit:
                    json_output["deniedReasons"].append('moreThanTenTransactionsOnTheSameMerchant')
                if not out_deny_list:
                    json_output["deniedReasons"].append('merchantInDenyList')
                if not less_than_four_in_to_minutes:
                    json_output["deniedReasons"].append('moreThanThreeTransactionInLessThanTwoMinutes')

            #last_transactions.append(content['Transaction'])
            return jsonify(json_output)
        except Exception as e:
            raise InvalidUsage('%s' % e ,status_code=410)
    else:
        return abort(400)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000, debug=True)
