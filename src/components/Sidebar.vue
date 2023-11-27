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
    <v-avatar class="d-block text-center mx-auto mt-4 mb-10" size="80">
      <v-icon color="green" x-large>mdi-basket</v-icon>
    </v-avatar>

    <v-card flat class="rounded-xl mx-4 mx-auto text-center">
      <v-list flat>
        <v-list-item-group v-model="selectedItem">
          <v-list-item    
            v-for="(item, i) in items"
            :key="i"
            active-class="border"
            v-slot="{ active }"
            :ripple="false"
            :value="item.route"
          >
            <v-list-item-content>
              <router-link :to="item.route">
                <v-list-item-content>
                  <v-icon :color="active ? 'white' : 'black'">
                    {{ item.icon }}
                  </v-icon>
                </v-list-item-content>
              </router-link>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card>

    <div
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
      <v-avatar >
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

  methods: {
    async logout() {
      await this.$store.commit('clearToken');
      location.href="/login"
    },
    async login() {
      location.href="/login"
    },
    async TokenPromise() {
      this.AuthToken = await this.getToken();
    },
    getToken() {
      return new Promise( (resolve) => {
        const tokenSimple = this.$store.getters.getTokenSimple;
        if (tokenSimple) {
          resolve(tokenSimple);
        } else {
          const token = this.$store.getters.getToken;
          resolve(token);
        }
      });
    }
  },
  data: () => ({
    AuthToken:null,
    selectedItem: "search",
    items: [
      { icon: "mdi-home-outline", route: "search" },
      { icon: "mdi-cart-outline", route: "cart" },
      { icon: "mdi-bell-outline", route: "notification" },
      { icon: "mdi-account-outline", route: "login" }
    ],
  })
};
</script>

<style>
/* Common styles for both mobile and desktop */
.v-navigation-drawer.nav-drawer {
  transition: transform 0.3s ease-in-out;
}

/* Mobile styles */
@media (max-width: 700px) {
  .v-navigation-drawer.nav-drawer {
    transform: translateX(0%);
    position: fixed;
    bottom: 0;
    left: 0;
    top: auto;
    height: 60px; /* Adjust the height as needed */
  }

  /* Additional mobile styles if needed */
  .border {
    margin: 0px 8px;
    background: green;
    border-radius: 15px;
    text-decoration: none;
    width: 60px;
    height: 60px;
  }

  .v-list-item-group .v-list-item--active {
    color: white !important;
  }

  .v-list-item__content {
    padding: 10px 0 !important;
  }

  .v-card {
    margin-top: 22px;
  }
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
    margin: 0px 8px;
    background: green;
    border-radius: 15px;
    text-decoration: none;
    width: 60px;
    height: 60px;
  }

  .v-list-item-group .v-list-item--active {
    color: white !important;
  }

  .v-list-item__content {
    padding: 20px 0 !important;
  }

  .v-card {
    margin-top: 22px;
  }
  
  .v-list-item__content {
    padding: 10px 0 !important;
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
  color: white;
  cursor: pointer;
  text-decoration: none;
}
</style>
