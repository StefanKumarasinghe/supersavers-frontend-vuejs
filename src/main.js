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




Vue.config.productionTip = false;

// Use the router
Vue.use(VueRouter);



if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js')
    .then((registration) => {
      console.log('Service Worker registered with scope:', registration.scope);
    })
    .catch((error) => {
      console.error('Service Worker registration failed:', error);
    });
}

// Define routes
const routes = [
  { path: '/', component: Explore },
  { path: '/register', component: Register },
  { path: '/verify', component: Verification },
  { path: '/notification',name: 'notification', component: Notification},
  { path: '/search',name: 'search', component: Search },
  { path: '/product', component: Products},
  { path: '/login', name: 'login', component: Login },
  { path: '/cart',name: 'cart', component: Cart },
  { path: '/forgotpassword', component: ForgotPassword},
  { path: '/resetpassword', component: ResetPassword}
];

// Create the router instance
const router = new VueRouter({
  mode: 'history',
  routes
});

new Vue({
  vuetify,
  store,
  router,
  render: h => h(App)
}).$mount('#app');
