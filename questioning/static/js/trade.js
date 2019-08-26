$(function () {
    let money = 0.00;
    let all_money_label = $('#all_money');
    let money_5 = $('#money_5');
    let money_10 = $('#money_10');
    let money_50 = $('#money_50');
    let money_100 = $('#money_100');
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

    money_other.click(function () {
        onMoneyClick($(this), 999.00);
        $('.money-other').show()
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
        }
    });

    function updateAllMoney() {
        all_money_label.text('总金额' + money + '.00元')
    }

    function removeSelect() {
        money_5.removeClass('money-select');
        money_10.removeClass('money-select');
        money_50.removeClass('money-select');
        money_100.removeClass('money-select');
        money_other.removeClass('money-select');
    }
});
