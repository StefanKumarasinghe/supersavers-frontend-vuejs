<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar v-if="isDesktop && authToken && $route.name != 'explore'" />

    <!-- Toolbar with Menu Icon -->
    <router-view></router-view>
    <BottomNav v-if="isMobile && authToken" />
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';
import BottomNav from './components/BottomNav.vue';

export default {
  components: {
    Sidebar,
    BottomNav,
  },
  data() {
    return {
      isDesktop: false,
      isMobile: false,
      showSidebar: false,
      showBottomNav: false,
      authToken:null
    };
  },
  async beforeMount() {
    this.TokenPromise();
    this.checkIsMobile();
    this.checkIsDesktop();
    this.checkRoute(); // Check route during initial mount
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
    document.addEventListener('click', this.handleDocumentClick);
    this.checkRoute(); // Check route when the component is mounted
    this.TokenPromise();
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    checkIsDesktop() {
      this.isDesktop = window.innerWidth > 701;
      window.addEventListener('resize', () => {
        this.isDesktop = window.innerWidth > 701;
      });
    },
    checkIsMobile() {
      this.isMobile = window.innerWidth <= 701;
      window.addEventListener('resize', () => {
        this.isMobile = window.innerWidth <= 701;
      });
    },
    handleResize() {
      this.checkRoute(); // Adjust based on the new screen size
    },
    handleDocumentClick(event) {
      if (this.isMobile) {
        const sidebarElement = this.$refs.sidebar?.$el;
        if (sidebarElement && !sidebarElement.contains(event.target)) {
          this.showSidebar = false;
        }
      }
    },
    checkRoute() {
      const isRestrictedRoute = this.$route.path === '/' || this.$route.path === '/login' || 
                                this.$route.path === '/register' || this.$route.path === '/forgotpassword' ||
                                this.$route.path === '/resetpassword';
      this.showSidebar = this.isDesktop && !isRestrictedRoute;
      this.showBottomNav = this.isMobile && !isRestrictedRoute;
    },
    // get Auth token
    async TokenPromise() {
      this.authToken = await this.getToken();
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
  watch: {
    $route() {
      // When the route changes, check and update navigation bars
      this.checkRoute();
    },
    authToken() {
      console.log("authtoken:" + this.authToken);
      if (this.authToken == null) {
        this.TokenPromise();
      }
    },
  },
};
</script>
