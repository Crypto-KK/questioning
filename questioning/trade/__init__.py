from enum import Enum

ORDER_STATUS = (
    ('TRADE_SUCCESS', '支付成功'),
    ('TRADE_CLOSED', '未付款交易超时关闭'),
    ('WAIT_BUYER_PAY', '交易创建'),
    ('TRADE_FINISHED', '交易结束'),
    #('paying', '待支付'),
    ('paying', '待支付'),
)


class Status(Enum):
    """交易状态枚举类"""
    TRADE_SUCCESS = 'TRADE_SUCCESS'
    PAYING = 'paying'
    TRADE_CLOSED = 'TRADE_CLOSED'
    WAIT_BUYER_PAY = 'WAIT_BUYER_PAY'
    TRADE_FINISHED = 'TRADE_FINISHED'
