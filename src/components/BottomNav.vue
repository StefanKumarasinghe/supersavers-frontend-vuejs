<template>
    <v-app>
      <v-bottom-navigation class="bar" v-if="isMobile" fixed>
        <v-btn class="nav" v-for="(item, i) in items" :key="i" @click="navigateTo(item.route)" :value="item.route">
          <v-icon :color="selectedRoute === item.route ? 'orange' : 'black'" class="icon">
            {{ item.icon }}
          </v-icon>
          <span>{{ item.label }}</span>
        </v-btn>
      </v-bottom-navigation>
    </v-app>
  </template>
  
  <script>
  export default {
    data: () => ({
      selectedRoute: "search",
      items: [
        { icon: "mdi-home-outline", route: "search", label: "Search" },
        { icon: "mdi-cart-outline", route: "cart", label: "Cart" },
        { icon: "mdi-bell-outline", route: "notification", label: "Notification" },
        { icon: "mdi-account-outline", route: "login", label: "Account" },
      ],
      isMobile: false,
    }),
    async beforeMount() {
      this.checkIsMobile();
    },
    methods: {
      async navigateTo(route) {
        await this.$router.push({ name: route });
        this.selectedRoute=route
      },
      checkIsMobile() {
        this.isMobile = window.innerWidth <= 700;
  
        window.addEventListener('resize', () => {
          this.isMobile = window.innerWidth <= 700;
        });
      },
    },
  };
  </script>
  
  <style>
  /* Add any additional styles for the bottom navigation here */
  .icon {
    width: 100%; /* Ensure the icon takes up the full width of the button */
    /* Background color when active */
    padding: 16px; /* Adjust padding as needed */
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
  </style>
  