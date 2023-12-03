<template>
  <v-app>
    <v-layout class="overflow-visible">
    <v-bottom-navigation class="bar" fixed grow v-model="selectedItem">
      <v-btn
        rounded
        v-for="(item, i) in items"
        :key="i"
        :to="item.route"
        :value="item.route"
        class="nav"
        :class="{
          'green-btn': selectedItem === item.route,
          'white--text': selectedItem === item.route,
          'black--text': selectedItem !== item.route
        }"
      >
        <span class="label font-weight-bold">
          {{ item.label }}
        </span>       
        <v-icon class="icon">
          {{ item.icon }}
        </v-icon>
      </v-btn>
    </v-bottom-navigation>
    </v-layout>
  </v-app>
</template>

<script>
  export default {
    async beforeMount() {
      this.selectedItem = this.$route.name;
    },
    data: () => ({
      selectedItem: "search",
      items: [
        { icon: "mdi-home-outline", route: "search", label: "Search" },
        { icon: "mdi-cart-outline", route: "cart", label: "Cart" },
        { icon: "mdi-bell-outline", route: "notification", label: "Notification" },
        { icon: "mdi-account-outline", route: "account", label: "Account" },
      ],
    })
  };
</script>

<style>
  /* Add any additional styles for the bottom navigation here */
  .icon {
    width: 100%; /* Ensure the icon takes up the full width of the button */
    padding-top: 10px;
    color: black;
    background-color: transparent;
  }
  .label {
    padding-top: 5px;
    padding-bottom: 10px;
    background-color: transparent;
  }
  .nav {
    background-color: white !important;
    box-shadow: none;
    height:auto !important;
  }
  .bar {
    height:auto !important;
    box-shadow: none !important;
  }
  .green-btn {
    background-color: #2E7D32 !important;
  }
  .green-btn .white--text {
    color: white !important;
  }
</style>  