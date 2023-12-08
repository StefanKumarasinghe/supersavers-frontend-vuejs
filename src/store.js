import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    active: null,
    weeklyDealsW: [],
    weeklyDealsIGA: [],
    weeklyDealsColes: [],
    cart: [],
  },
  mutations: {
    setToken(state, token) {
      Vue.set(state, 'active', true);
      Vue.set(state, 'token', token);

      const expirationTime = new Date().getTime() + 24 * 60 * 60 * 1000; // 1 day in milliseconds
      localStorage.setItem('token', JSON.stringify({ value: token, expires: expirationTime }));
    },
    clearToken(state) {
      Vue.set(state, 'token', null);
      localStorage.removeItem('token');
    },
    clearTokenSimple(state) {
      Vue.set(state, 'token', null);
    },
    setWeeklyDealsW(state, deals) {
      state.weeklyDealsW = deals;
    },
    setWeeklyDealsIGA(state, deals) {
      state.weeklyDealsIGA = deals;
    },
    setWeeklyDealsColes(state, deals) {
      state.weeklyDealsColes = deals;
    },
    addItem(state, item) {
      // Check if the item already exists in the cart
      const existingItem = state.cart.find((cartItem) => cartItem.name === item.name && cartItem.bought === false && cartItem.source === item.source);
      // Item doesn't exist in the cart, add it
      if (!existingItem) {
        state.cart.push(item);
        localStorage.setItem('cart', JSON.stringify(state.cart));
      }
    },
    removeItem(state, item) {
      const index = state.cart.findIndex((cartItem) => cartItem.name === item.name && cartItem.source === item.source);
      if (index !== -1) {
        state.cart.splice(index, 1);
        localStorage.setItem('cart', JSON.stringify(state.cart));
      }
    },
    updateItem(state, item) {
      const index = state.cart.findIndex((cartItem) => cartItem.name === item.name && cartItem.source === item.source);
      if (index !== -1) {
        state.cart[index] = item;
      }
      
      localStorage.setItem('cart', JSON.stringify(state.cart));
    }
  },
  actions: {
    // Example action to set the token
    setToken({ commit }, token) {
      commit('setToken', token);
    },
    
    // Example action to clear the token
    clearToken({ commit }) {
      commit('clearToken');
    },
    clearTokenSimple({ commit }) {
      commit('clearTokenSimple');
    },
    addItem({ commit }, item) {
      commit('addItem', item);
    },
    removeItem({ commit }, item) {
      commit('removeItem', item);
    },
    updateItem({ commit }, item) {
      commit('updateItem', item);
    },
  },
  getters: {
    // Example getter to retrieve the token
    getTokenSimple: (state) => {
      return state.token;
    },
    // Getter to retrieve the cart list
    getList: (state) => {
      const cart = JSON.parse(localStorage.getItem('cart')) || [];
      Vue.set(state, 'cart', cart);
      return cart;
    },
    getToken: () => {
      // Retrieve token from localStorage and check expiration
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        const { value, expires } = JSON.parse(storedToken);
        if (expires > new Date().getTime()) {
          return value;
        } else {
          // Token has expired, clear it
          localStorage.removeItem('token');
        }
      }
      return null;
    },
  },
});
