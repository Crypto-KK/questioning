$(function () {

    function getCookie(name) {
        if (document.cookie && document.cookie.length) {
            var cookies = document.cookie
                .split(';')
                .filter(function (cookie) {
                    return cookie.indexOf(name + "=") !== -1;
                })[0];
            try {
                return decodeURIComponent(cookies.trim().substring(name.length + 1));
            } catch (e) {
                if (e instanceof TypeError) {
                    console.info("No cookie with key \"" + name + "\". Wrong name?");
                    return null;
                }
                throw e;
            }
        }
        return null;
    }

    function csrfSafeMethod(method) {
        // These HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = getCookie('csrftoken');
    // This sets up every ajax call with proper headers.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });


    let money = 0.00;
    let all_money_label = $('#all_money');
    let money_5 = $('#money_5');
    let money_10 = $('#money_10');
    let money_50 = $('#money_50');
    let money_100 = $('#money_100');
    let money_500 = $('#money_500');
    let money_1000 = $('#money_1000');
    let money_other = $('#money_other');

    money_5.click(function () {
        onMoneyClick($(this), 5.00)
    });

    money_10.click(function () {
        onMoneyClick($(this), 10.00)
    });

    money_50.click(function () {
        onMoneyClick($(this), 50.00)
    });

    money_100.click(function () {
        onMoneyClick($(this), 100.00)
    });

    money_500.click(function () {
        onMoneyClick($(this), 500.00)
    });

    money_1000.click(function () {
        onMoneyClick($(this), 1000.00)
    });

    money_other.click(function () {
        onMoneyClick($(this), 0.00);
        $('.money-other').show();
        // $('#money-input').on('input propertychange', function () {
        //     onMoneyClick($(this), $('#money-input').val())
        // })
    });

    function onMoneyClick (obj, balance) {
        $('.money-other').hide();
        money = balance;
        removeSelect();
        obj.addClass('money-select');
        updateAllMoney();
    }

    $('#pay').click(function () {
        if (money === 0.00) {
            alert('请选择充值金额！');
        } else {
            $.ajax({
            url: '/trade/pay/',
            data: {
                'money': money,
            },
            type: 'post',
            cache: false,
            success: function (data) {
                if (data.pay_url && data.order_sn) {
                    $('#order-sn').attr('data-ordersn', data.order_sn)
                    window.open(data.pay_url)

                } else {
                }

            }
        });

        }
    });

    $('#pay-success').click(function () {
        // 验证是否支付成功
        $.ajax({
            url: '/trade/pay/verify/',
            data: {
                order_sn: $('#order-sn').attr('data-ordersn')
            },
            type: 'post',
            cache: false,
            success: function (data) {
                if (data.status === "ok") {
                    alert('充值成功！');
                    window.location.href = '/users/' + currentUser
                } else {
                    alert('充值失败，网络可能存在延时原因，请稍候重试！')
                }
            }
        })
    });

    $('#pay-question').click(function () {
        alert('如果付款了金币还没有到账，请联系客服！')
    });


    function updateAllMoney() {
        all_money_label.text('需支付 ' + money + '.00元')
    }

    function removeSelect() {
        money_5.removeClass('money-select');
        money_10.removeClass('money-select');
        money_50.removeClass('money-select');
        money_100.removeClass('money-select');
        money_500.removeClass('money-select');
        money_1000.removeClass('money-select');
        money_other.removeClass('money-select');
    }
});
