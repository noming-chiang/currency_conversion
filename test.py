from app import currency_conversion
from common import Base
from transfer import Transfer


class TestCurrencyConversion:

    def test_check_params_data_in_the_template_when_source_not_in_template(self) -> None:
        data = {'source': 'KRW', 'target': 'THP', 'amount': 100}
        template = Base.transfer_template()["currencies"]
        result = {'code': 400, 'message': 'Template缺少source參數'}
        assert currency_conversion().check_params_data_in_the_template(data, template) == result

    def test_check_params_data_in_the_template_when_target_not_in_template(self) -> None:
        data = {'source': 'USD', 'target': 'THP', 'amount': 100}
        template = Base.transfer_template()["currencies"]
        result = {'code': 400, 'message': 'Template缺少target參數'}
        assert currency_conversion().check_params_data_in_the_template(data, template) == result

    def test_check_data_type_when_source_type_is_int(self) -> None:
        data = {'source': 50, 'target': 'THP', 'amount': 100}
        result = {'code': 400, 'message': 'source參數型態錯誤'}
        assert currency_conversion().check_data_type(data) == result

    def test_check_data_type_when_target_type_is_int(self) -> None:
        data = {'source': 'USD', 'target': 99, 'amount': 100}
        result = {'code': 400, 'message': 'target參數型態錯誤'}
        assert currency_conversion().check_data_type(data) == result

    def test_check_data_type_when_amount_type_is_str(self) -> None:
        data = {'source': 'USD', 'target': 'THP', 'amount': '100'}
        result = {'code': 400, 'message': 'amount參數型態錯誤'}
        assert currency_conversion().check_data_type(data) == result

    def test_check_params_data_when_missing_source_field(self) -> None:
        data = {'target': 'THP', 'amount': '100'}
        result = {'code': 400, 'message': '缺少source參數'}
        assert currency_conversion().check_params_data(data) == result

    def test_check_params_data_when_missing_target_field(self) -> None:
        data = {'source': 'USD', 'amount': '100'}
        result = {'code': 400, 'message': '缺少target參數'}
        assert currency_conversion().check_params_data(data) == result

    def test_check_params_data_when_missing_amount_field(self) -> None:
        data = {'source': 'USD', 'target': 'THP'}
        result = {'code': 400, 'message': '缺少amount參數'}
        assert currency_conversion().check_params_data(data) == result


class TestTransfer:

    def test_get_transfer_amount(self) -> None:
        amount = 100
        target_currencies = 111.801
        transfer_amount = '11,180.10'
        assert Transfer().get_transfer_amount(amount, target_currencies) == transfer_amount
