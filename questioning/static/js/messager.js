$(function () {

    // 滚动条下拉到底
    function scrollConversationScreen() {
        $("input[name='message']").focus();
        $('.messages-list').scrollTop($('.messages-list')[0].scrollHeight);
    }

    // 添加消息函数
    function addNewMessage(message_id) {
        $.ajax({
            url: '/messages/receive-message/',
            data: {'message_id': message_id},
            cache: false,
            success: function (data) {
                $(".send-message").before(data); // 将接收到的消息插入到聊天框
                scrollConversationScreen(); // 滚动条下拉到底
            }
        });
    }

    // AJAX POST发送消息
    $("#send").submit(function () {
        $.ajax({
            url: '/messages/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: 'POST',
            success: function (data) {
                $(".send-message").before(data);  // 将接收到的消息插入到聊天框
                $("input[name='message']").val(''); // 消息发送框置为空
                scrollConversationScreen();  // 滚动条下拉到底
            }
        });
        return false;
    });

    const ws_scheme = window.location.protocol === 'https' ? 'wss': 'ws';
    const ws_path = ws_scheme + '://' + window.location.host + '/ws/' + currentUser + '/'
    const ws = new ReconnectingWebSocket(ws_path);

    //监听后端发送的消息

    ws.onmessage = function (event) {
        console.log(event)
        const data = JSON.parse(event.data);
        if (data.sender === activeUser) { //当前选中的用户
            $('.send-message').before(data.message);
            scrollConversationScreen(); //下拉滚动条
        }
    }


});
