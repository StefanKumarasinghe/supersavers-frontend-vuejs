import Vue from 'vue';
import App from './App.vue';
import Register from './Register.vue';
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
import Account from './Account.vue';
import Subscription from './Subscription.vue';

// Import Firebase
import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';

Vue.config.productionTip = false;

// Use the router
Vue.use(VueRouter);

Vue.prototype.$GroceryAPI = "https://api.supersavers.au";

// Define routes
const routes = [
  { path: '/', name:'explore', component: Explore },
  { path: '/register', component: Register },
  { path: '/verify', name: 'verify', component: Verification },
  { path: '/notification', name: 'notification', component: Notification },
  { path: '/search', name: 'search', component: Search },
  { path: '/login', name: 'login', component: Login },
  { path: '/cart', name: 'cart', component: Cart },
  { path: '/forgot-password', component: ForgotPassword },
  { path: '/reset-password', component: ResetPassword },
  { path: '/account',name:'account', component: Account },
  { path: '/subscription', name:'subscription', component: Subscription}
];

// Create the router instance
const router = new VueRouter({
  mode: 'history',
  routes
});

// Navigation guard to check authentication before navigating to each route
router.beforeEach((to, from, next) => {
  // These routes do not require login token
  const requiresAuth = !['/', '/login', '/register', '/forgot-password', '/reset-password', '/verify'].includes(to.path);

  // If authentication is required and the user is not authenticated, redirect to login
  if (requiresAuth && !store.getters.getToken) {
    next('/login');
  } else {
    // Continue to the next route
    next();
  }
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