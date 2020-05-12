from questioning.trade.models import OrderInfo, AccountDetail

import xadmin


class OrderInfoAdmin:
    list_display = ['order_sn', 'trade_no', 'user', 'pay_status', 'order_mount', 'created_at']
    list_filter = ['order_sn', 'user', 'pay_status', 'trade_no']
    search_fields = ['order_sn', 'trade_no']
    ordering = ['-created_at']
    readonly_fields = ['pay_status', 'user', 'order_sn', 'trade_no', 'order_mount']


class AccountDetailAdmin:
    list_display = ['uuid_id', 'user', 'mount', 'current_money', 'description', 'created_at']
    list_filter = ['description', 'user']
    search_fields = ['description']
    ordering = ['-created_at']
    readonly_fields = ['uuid_id', 'user', 'current_money', 'mount']


xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(AccountDetail, AccountDetailAdmin)

