<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar :drawer="drawer" ref="sidebar" />
    
    <!-- Toolbar with Menu Icon -->
    <v-toolbar v-if="showMenuButton()">
      <v-btn
        icon
        class=""
        @click.stop="toggleSidebar"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </v-toolbar>
    
    <router-view></router-view>
  </div>
</template>

<script>
import Sidebar from './components/Sidebar.vue';

export default {
  components: {
    Sidebar,
  },
  data() {
    return {
      drawer: window.innerWidth >= 1280,
    };
  },
  mounted() {
    if (this.$route.path === '/' || this.$route.path === '/login') {
      this.drawer = false;
    }
    window.addEventListener('resize', this.handleResize);
    document.addEventListener('click', this.handleDocumentClick);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    handleResize() {
      this.drawer = window.innerWidth >= 1280;
    },
    toggleSidebar() {
      this.drawer = !this.drawer;
    },
    handleDocumentClick(event) {
      if (window.innerWidth < 1280) {
        const sidebarElement = this.$refs.sidebar?.$el;
        if (sidebarElement && !sidebarElement.contains(event.target)) {
          this.drawer = false;
        }
      }
    },
    showMenuButton() {
      // TODO: Change to -> If auth is not verified, set the drawer to false.
      if (this.$route.path === '/login' || this.$route.path === '/' || 
      this.$route.path === '/register' || this.$route.path === '/forgotpassword' ||
      this.$route.path === '/resetpassword') {
        this.drawer = false;
        return false;
      } else {
        return true;
      }
    },
  },
};
</script>
