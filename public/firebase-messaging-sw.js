importScripts('https://www.gstatic.com/firebasejs/9.1.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.1.0/firebase-messaging-compat.js');

const firebaseConfig = {
    apiKey: "AIzaSyAe9k5tAHaQednuCXEwMdJAzwv7dDKRhMk",
    authDomain: "groceryapi-1fb2f.firebaseapp.com",
    projectId: "groceryapi-1fb2f",
    storageBucket: "groceryapi-1fb2f.appspot.com",
    messagingSenderId: "189392397627",
    appId: "1:189392397627:web:105f908902eec12720431e",
    measurementId: "G-FJV09ELD10"
  };
// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging(app);

messaging.onBackgroundMessage((payload) => {
  console.log('Received background message:', payload);
  // Customize this to handle the received message
});
