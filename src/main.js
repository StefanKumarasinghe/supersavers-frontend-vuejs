import Vue from 'vue';
import App from './App.vue';
import Register from './Register.vue';
import Products from './Products.vue';
import Search from './Search.vue';
import Login from './Login.vue';
import Explore from './Explore.vue';
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';
import Cart from './Cart.vue';
import ForgotPassword from './ForgotPassword.vue';
import Verification from './Verification.vue';
import Notification from './Notification.vue';
import ResetPassword from './ResetPassword.vue';
import store from './store';

// Import Firebase
import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';

Vue.config.productionTip = false;

// Use the router
Vue.use(VueRouter);

// Define routes
const routes = [
  { path: '/', component: Explore },
  { path: '/register', component: Register },
  { path: '/verify', component: Verification },
  { path: '/notification', name: 'notification', component: Notification },
  { path: '/search', name: 'search', component: Search },
  { path: '/product', component: Products },
  { path: '/login', name: 'login', component: Login },
  { path: '/cart', name: 'cart', component: Cart },
  { path: '/forgotpassword', component: ForgotPassword },
  { path: '/resetpassword', component: ResetPassword }
];

// Create the router instance
const router = new VueRouter({
  mode: 'history',
  routes
});

// Your web app's Firebase configuration
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
const firebaseApp = initializeApp(firebaseConfig);
getAnalytics(firebaseApp);
console.log(firebaseApp)

new Vue({
  vuetify,
  store,
  firebase: firebaseApp,  // Pass the Firebase app instance here
  router,
  render: h => h(App)
}).$mount('#app');