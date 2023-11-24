// ToastPlugin.js

import Vue from 'vue';

const Toast = {
  install(Vue) {
    Vue.prototype.$toast = {
      success(message) {
        Vue.prototype.$bvToast.toast(message, {
          title: 'Success',
          variant: 'success',
          solid: true,
        });
      },
      error(message) {
        Vue.prototype.$bvToast.toast(message, {
          title: 'Error',
          variant: 'danger',
          solid: true,
        });
      },
      info(message) {
        Vue.prototype.$bvToast.toast(message, {
          title: 'Info',
          variant: 'info',
          solid: true,
        });
      },
    };
  },
};

Vue.use(Toast);

export default Toast;
