var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var chat_socket = new ReconnectingWebSocket(ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname);


$('#msgform').on('submit', function(event) {
    var message = {
        reciever: $('#reciever').val(),
        message: $('#message').val(),
        sender: $('#sender').val()
    };
    chat_socket.send(JSON.stringify(message));
    return false;
});

chatsock.onmessage = function(message) {
    var data = JSON.parse(message.data);
    $('.msg-container').append('<tr>'
        + '<td>' + data.reciever + '</td>'
        + '<td>' + data.message + '</td>'
        + '<td>' + data.sender + ' </td>'
    + '</tr>');
};