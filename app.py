from typing import Tuple, Dict, Any, Union

from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields, abort
from flask_cors import CORS

from common import Base
from transfer import Transfer

app = Flask(__name__)
api = Api(app, version='1.0', title='DataProvider API',
          description='KPI資料提供'
          )

CORS(app, supports_credentials=True, cors_allowed_origins='*')

transferNs = api.namespace('currency_conversion', description='匯率轉換')
transferML = api.model('currency_conversion', {
    'source': fields.String(required=True, description='來源幣別', default='TWD', example='TWD'),
    'target': fields.String(required=True, description='目標幣別', default="JPY", example="JPY"),
    'amount': fields.Integer(required=True, description='⾦額數字', default=100, example=100),
})


@transferNs.route('', methods=['POST'])
class currency_conversion(Resource):
    @transferNs.doc('取得參數')
    @transferNs.expect(transferML)
    def post(self) -> Tuple[Dict[str, Union[int, str]], int, dict]:
        result = self.check_request(request)
        if result['code'] != 204:
            return self.get_error_response_data(result)
        data = request.json
        result = self.check_params_data(data)
        if result['code'] != 204:
            return self.get_error_response_data(result)
        result = self.check_data_type(data)
        if result['code'] != 204:
            return self.get_error_response_data(result)
        template = Base.transfer_template()["currencies"]
        result = self.check_params_data_in_the_template(data, template)
        if result['code'] != 204:
            return self.get_error_response_data(result)
        result = Transfer().transfer_source_to_target(data['source'], data['target'], data['amount'])
        if result['code'] != 200:
            return self.get_error_response_data(result)
        return self.get_response_data(result)

    @staticmethod
    def get_response_data(result: dict) -> Tuple[Dict[str, Any], Any, dict]:
        return result['message'], result['code'], Base.get_header()

    @staticmethod
    def get_error_response_data(result: dict) -> Tuple[Dict[str, Any], Any, dict]:
        return {'message': result['message']}, result['code'], Base.get_header()

    @staticmethod
    def check_params_data_in_the_template(data: dict, template: dict) -> dict:
        if data['source'] not in template.keys():
            return {'code': 400, 'message': 'Template缺少source參數'}
        if data['target'] not in template.keys():
            return {'code': 400, 'message': 'Template缺少target參數'}
        return {'code': 204, 'message': ''}

    @staticmethod
    def check_data_type(data: dict) -> dict:
        if not isinstance(data['source'], str):
            return {'code': 400, 'message': 'source參數型態錯誤'}
        if not isinstance(data['target'], str):
            return {'code': 400, 'message': 'target參數型態錯誤'}
        if not isinstance(data['amount'], int):
            return {'code': 400, 'message': 'amount參數型態錯誤'}
        return {'code': 204, 'message': ''}

    @staticmethod
    def check_params_data(data: dict) -> dict:
        if 'source' not in data.keys():
            return {'code': 400, 'message': '缺少source參數'}
        if 'target' not in data.keys():
            return {'code': 400, 'message': '缺少target參數'}
        if 'amount' not in data.keys():
            return {'code': 400, 'message': '缺少amount參數'}
        return {'code': 204, 'message': ''}

    @staticmethod
    def check_request(request: request) -> dict:
        if not request:
            abort(400)
        if not request.json:
            return {'code': 400, 'message': '輸入參數為空或不是JSON型態'}
        return {'code': 204, 'message': ''}


if __name__ == '__main__':
    app.run(threaded=True, use_reloader=False, host='0.0.0.0', port=5000, debug=False)
