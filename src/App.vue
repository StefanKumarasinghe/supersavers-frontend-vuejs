<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar v-if="isDesktop && authToken && this.$route.name !== 'verify'" />

    <!-- Toolbar with Menu Icon -->
    <router-view :class="isMobile? 'mb-5' : ''"></router-view>
    <BottomNav v-if="isMobile && authToken  && this.$route.name !== 'subscription' && this.$route.name !== 'explore'"/>
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
  },
  mounted() {
    document.addEventListener('click', this.handleDocumentClick);
    this.TokenPromise();
  },
  beforeDestroy() {
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
    handleDocumentClick(event) {
      if (this.isMobile) {
        const sidebarElement = this.$refs.sidebar?.$el;
        if (sidebarElement && !sidebarElement.contains(event.target)) {
          this.showSidebar = false;
        }
      }
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
    authToken() {
      if (this.authToken == null) {
        this.TokenPromise();
      }
    },
  },
};
</script>
