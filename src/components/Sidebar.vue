<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable vue/no-mutating-props -->
<template>
  <v-app>
    <v-navigation-drawer
      class="nav-drawer"
      app
      touch
      mini-variant
      mini-variant-width="80"
      style="transform: translateX(0%);"
    >
      <v-avatar class="d-block text-center mx-auto mt-4" size="80">
        <v-icon color="black" @click="$router.push('/')" x-large>mdi-basket</v-icon>
      </v-avatar>

      <v-card flat class=" mx-4 mx-auto text-center">
        <v-list flat>
          <v-list-item-group v-model="selectedItem">
            <v-list-item
              v-for="(item, i) in items"
              :key="i"
              active-class="border"
              v-slot="{ active }"
              :ripple="false"
              :value="item.route"
              :to="item.route"
            >
              <v-list-item-content style="position:relative">
                <v-icon :color="active ? 'white' : 'black'">
                  {{ item.icon }}
                </v-icon>
              </v-list-item-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card>
      <div
  class="d-none d-md-block" 
  style="
    position: absolute;
    bottom: 20px;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
    text-align: center;
  "
>
  <v-avatar>
    <v-icon v-if="this.AuthToken" @click="logout()" class="mdi mdi-logout black--text"></v-icon>
  </v-avatar>
</div>

    </v-navigation-drawer>
  </v-app>
</template>

<script>
export default {
  async beforeMount() {
    await this.TokenPromise();
    this.selectedItem = this.$route.name;
  },

  watch: {
    $route(to) {
      this.selectedItem = to.name;
    },
  },
  methods: {
    async logout() {
      this.$store.commit('clearToken');
      this.$router.push('/');
    },
    async login() {
      this.$router.push('/login');
    },
    async TokenPromise() {
      this.AuthToken = await this.getToken();
    },
    getToken() {
      return new Promise((resolve) => {
        const tokenSimple = this.$store.getters.getTokenSimple;
        if (tokenSimple) {
          resolve(tokenSimple);
        } else {
          const token = this.$store.getters.getToken;
          resolve(token);
        }
      });
    },
  },
  data: () => ({
    AuthToken: null,
    selectedItem: "search",
    items: [
      { icon: "mdi-home-outline", route: "search" },
      { icon: "mdi-cart-outline", route: "cart" },
      { icon: "mdi-bell-outline", route: "notification" },
      { icon: "mdi-account-outline", route: "account" },
    ],
  }),
};
</script>

<style>
/* Common styles for both mobile and desktop */
.v-navigation-drawer.nav-drawer {
  transition: transform 0.3s ease-in-out;
}

/* Desktop styles */
@media (min-width: 701px) {
  .v-navigation-drawer.nav-drawer {
    transform: translateX(0%);
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 80px; /* Adjust the width as needed */
  }

  /* Additional desktop styles if needed */
  .border {
    margin: 8px 8px;
    background: green;
    border-radius: 15px;
    text-decoration: none;
    width: 60px;
    height: 60px;
    color: white;
  }

  .v-card {
    margin-top: 22px;
  }

  .v-list-item {
    padding: 8px 16px;
  }
}

/* Add your existing styles here */

.image {
  border: 1px solid white;
}

.v-navigation-drawer--close {
  visibility: visible;
}

.router-link {
  text-decoration: none;
}

a:-webkit-any-link {
  text-decoration: none;
}
</style>
