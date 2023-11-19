import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: null,
    active:null,
  },
  mutations: {
    setToken(state, token) {
      state.active = true
      state.token = token;
      const expirationTime = new Date().getTime() + 24 * 60 * 60 * 1000; // 1 day in milliseconds
      localStorage.setItem('token', JSON.stringify({ value: token, expires: expirationTime }));
    },
    clearToken(state) {
      state.active = false
      state.token = null;
      
      localStorage.removeItem('token');
    },
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
  },
  getters: {
    // Example getter to retrieve the token
    getTokenSimple: (state) => {
        return state.token;
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
