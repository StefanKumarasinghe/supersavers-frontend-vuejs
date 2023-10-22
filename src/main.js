import Vue from 'vue';
import App from './App.vue';
import Register from './Register.vue';
import Products from './Products.vue';
import Search from './Search.vue';
import Login from './Login.vue';
import Explore from './Explore.vue';
import vuetify from './plugins/vuetify';
import VueRouter from 'vue-router';

Vue.config.productionTip = false;

// Use the router
Vue.use(VueRouter);

// Define routes
const routes = [
  { path: '/', component: Explore },
  { path: '/register', component: Register },
  { path: '/search', component: Search },
  { path: '/product', component: Products},
  { path: '/login', component: Login }
];

// Create the router instance
const router = new VueRouter({
  mode: 'history',
  routes
});

new Vue({
  vuetify,
  router, // Use the router
  render: h => h(App)
}).$mount('#app');
