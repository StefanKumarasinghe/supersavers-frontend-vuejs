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
  },
  actions: {
    setToken({ commit }, token) {
      commit('setToken', token);
    },
    clearToken({ commit }) {
      commit('clearToken');
    },
    clearTokenSimple({ commit }) {
      commit('clearTokenSimple');
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
