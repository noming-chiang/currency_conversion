from typing import Tuple
from common import Base
import sys
import traceback


class Transfer:

    def transfer_source_to_target(self, source: str, target: str, amount: int) -> dict:
        try:
            template_data = Base.transfer_template()
            currencies = template_data["currencies"]
            source_currencies = currencies[source]
            target_currencies = source_currencies[target]
            transfer_amount = self.get_transfer_amount(amount, target_currencies)
            response_data = {'target_type': target, 'transfer_amount': transfer_amount}
            return {'code': 200, 'message': response_data}
        except Exception as e:
            error_class = e.__class__.__name__  # 取得錯誤類型
            detail = e.args[0]  # 取得詳細內容
            cl, exc, tb = sys.exc_info()  # 取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
            fileName = lastCallStack[0]  # 取得發生的檔案名稱
            lineNum = lastCallStack[1]  # 取得發生的行號
            funcName = lastCallStack[2]  # 取得發生的函數名稱
            return {'code': 400, 'message': f"{funcName} error"}

    @staticmethod
    def get_transfer_amount(amount: int, target_currencies: float) -> str:
        return f"{amount * target_currencies:,.2f}"
