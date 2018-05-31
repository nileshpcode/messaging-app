// [START get_messaging_object]
// Retrieve Firebase Messaging object.
const messaging = firebase.messaging();
// [END get_messaging_object]

messaging.requestPermission().then(function () {
        console.log('Notification permission granted.');
        fetchToken();
    }).catch(function (err) {
        console.log('Unable to get permission to notify.', err);
    });

function fetchToken() {
    messaging.getToken()
    .then(function (currentToken) {
        if (currentToken) {
            sendTokenToServer(currentToken);
        } else {
            // Show permission request.
            console.log('No Instance ID token available. Request permission to generate one.');
            // Show permission UI.
            setTokenSentToServer(false);
        }
    })
    .catch(function (err) {
        console.log('An error occurred while retrieving token. ', err);
        setTokenSentToServer(false);
    });
}


messaging.onTokenRefresh(function () {
    messaging.getToken()
    .then(function (refreshedToken) {
        console.log('Token refreshed.');
        setTokenSentToServer(false);
        sendTokenToServer(refreshedToken);
    })
    .catch(function (err) {
        console.log('Unable to retrieve refreshed token ', err);
    });
});

function isTokenSentToServer() {
    return window.localStorage.getItem('sentToServer') == 1;
}

function setTokenSentToServer(sent) {
    window.localStorage.setItem('sentToServer', sent ? 1 : 0);
}

var token = window.localStorage.getItem('token');

function sendTokenToServer(currentToken) {
    if (!isTokenSentToServer()) {
        console.log('Sending token to server...');
        $.ajax({
            type: "post",
            dataType: "json",
            data: {'device_id': currentToken},
            headers: '',
            url: "/message/token/create/",
            success: function (responseData, textStatus, jqXHR) {
                console.log('Token set successfully')
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log(jqXHR, errorThrown);
            }
        });
        setTokenSentToServer(true);
    } else {
        console.log('Token already sent to server so won\'t send it again unless it changes');
    }
}

messaging.onMessage(function (payload) {
    const title = 'Icon Notification';
    const options = {};
    registration.showNotification(title, options);
});