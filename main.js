<script>
const firebaseConfig = {
  apiKey: "AIzaSyBcTEVvxXmv5N8dJav4xNDRy5hXZRjVeM4",
  authDomain: "chatflow-59776.firebaseapp.com",
  databaseURL: "https://chatflow-59776-default-rtdb.firebaseio.com",
  projectId: "chatflow-59776",
  storageBucket: "chatflow-59776.appspot.com",
  messagingSenderId: "549003131640",
  appId: "1:549003131640:web:3f4a7b8cef4c0d8a2b990d",
  measurementId: "G-V2180PR5CR"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const database = firebase.database();
const messaging = firebase.messaging();

// Request permission to send notifications
messaging.requestPermission()
    .then(() => messaging.getToken())
    .then(token => console.log('FCM Token:', token))
    .catch(err => console.error('Error getting FCM token', err));

// Function to display messages
function displayMessages(messages) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML = ''; // Clear existing messages
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.textContent = `From: ${message.senderEmail}, To: ${message.receiverEmail}, Message: ${message.text}, Time: ${new Date(message.sentTime).toLocaleString()}`;
        messagesDiv.appendChild(messageDiv);
    });
}

// Fetch messages from the database
function fetchMessages() {
    database.ref('messages').on('value', snapshot => {
        const messages = [];
        snapshot.forEach(childSnapshot => {
            messages.push(childSnapshot.val());
        });
        displayMessages(messages);
    });
}

// Call fetchMessages on page load
fetchMessages();

// Function to send a push notification
function sendPushNotification(receiverFCMToken, senderEmail, text, sentTime) {
    const payload = {
        notification: {
            title: `New message from ${senderEmail}`,
            body: text,
            click_action: 'https://your-website.com',
            icon: '/icon.png'
        },
        data: {
            sentTime: sentTime.toString()
        }
    };

    fetch('https://fcm.googleapis.com/fcm/send', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'key=YOUR_SERVER_KEY'
        },
        body: JSON.stringify({
            to: receiverFCMToken,
            notification: payload.notification,
            data: payload.data
        })
    })
    .then(response => response.json())
    .then(data => console.log('Push notification sent:', data))
    .catch(err => console.error('Error sending push notification:', err));
}

// Listen for new messages and send notifications
database.ref('messages').on('child_added', snapshot => {
    const newMessage = snapshot.val();
    if (!newMessage.isRead) {
        sendPushNotification(newMessage.receiverFCMToken, newMessage.senderEmail, newMessage.text, newMessage.sentTime);
    }
});
</script>
