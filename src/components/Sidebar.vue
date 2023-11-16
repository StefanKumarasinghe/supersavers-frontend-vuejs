<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable vue/no-mutating-props -->
<template>
  
  <v-navigation-drawer
    class="nav-drawer"
    v-show="drawer"
    app
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
            <v-list-item-content>
                <v-icon
                    :color="active ? 'white' : 'grey lighten-1'"
                >{{item.icon}}</v-icon>
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
      <v-avatar size="40">
        <v-img
          src="https://cdn.vuetifyjs.com/images/lists/1.jpg"
          class="image"
        ></v-img>
      </v-avatar>
    </div>
  </v-navigation-drawer>
</template>

<script>
export default {
  data: () => ({
    selectedItem: 0,

    items: [
      { icon: "mdi-home-outline" },
      { icon: "mdi-cart-outline" },
      { icon: "mdi-bell-outline" },
      { icon: "mdi-account-outline" }
    ],

  }),
  props: ["drawer"],
  watch: {
    drawer(newValue) {
    this.selectedItem = newValue;
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

</style>