<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable vue/no-mutating-props -->
<template>
  
  <v-navigation-drawer
    class="nav-drawer"
    v-show="drawer"
    app
    touch
    mini-variant
    mini-variant-width="80"
    style="transform: translateX(0%);"
  >
    <v-avatar class="d-block text-center mx-auto mt-4 mb-10" size="80">
      <v-icon color="gray" x-large>mdi-basket</v-icon>
    </v-avatar>

    <v-card flat class="rounded-xl mx-4 mx-auto text-center">
      <v-list flat class="">
        <v-list-item-group v-model="selectedItem">
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            active-class="border"
            v-slot="{ active }"
            :ripple="false"
          >
            <v-list-item-content >
              <router-link :to="item.route">
                <v-list-item-content>
                  <v-icon :color="active ? 'white' : 'grey lighten-1'">
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
        <v-icon v-if="this.AuthToken" @click="logout()" class="mdi mdi-logout" ></v-icon>
        <v-icon v-if="!(this.AuthToken)" @click="login()" class="mdi mdi-login" ></v-icon>
      </v-avatar>
    </div>
  </v-navigation-drawer>
</template>

<script>
export default {
  async beforeMount() {
    await this.TokenPromise();
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
      return new Promise(async (resolve) => {
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
    selectedRoute: "search", // Initialize with the default route
    items: [
      { icon: "mdi-home-outline", route: "search" },
      { icon: "mdi-cart-outline", route: "cart" },
      { icon: "mdi-bell-outline", route: "login" },
      { icon: "mdi-account-outline", route: "login" }
    ],
  }),
  props: ["drawer"],
  watch: {
    drawer(newValue) {
      // If the drawer is closing, don't change the selected route
      if (!newValue) return;

      // When the drawer is open, update the selected route based on the current route
      const currentRoute = this.$route.name;
      const selectedItem = this.items.find(item => item.route === currentRoute);

      if (selectedItem) {
        this.selectedRoute = selectedItem.route;
      }
    },
  },
};
</script>

<style>
.v-navigation-drawer.nav-drawer{
  transform: translateX(0%);
}
.border {
  margin: 0px 8px;
  background: orange;
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
.v-list-item__content {
  padding: 10px 0 !important;
}
.v-card {
    margin-top: 22px;
}

</style>