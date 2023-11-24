<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar :drawer="drawer" ref="sidebar" />
    
    <!-- Toolbar with Menu Icon -->
   
    
    <router-view></router-view>

    <v-bottom-navigation v-if="isMobile" fixed>
      <v-btn value="recent">
        <v-icon>mdi-history</v-icon>
        <span>Recent</span>
      </v-btn>

      <v-btn value="favorites">
        <v-icon>mdi-heart</v-icon>
        <span>Favorites</span>
      </v-btn>

      <v-btn value="nearby">
        <v-icon>mdi-map-marker</v-icon>
        <span>Nearby</span>
      </v-btn>
    </v-bottom-navigation>

    <BottomNav :drawer="drawer" />
    
  </div>
  
</template>


<script>
import Sidebar from './components/Sidebar.vue';
import Bottom from './components/BottomNav.vue';
import BottomNav from './components/BottomNav.vue';

export default {
  components: {
    Sidebar,
    Bottom,
    BottomNav
},
  data() {
    return {
      drawer: window.innerWidth >= 1280,

    };
  },
  mounted() {
        // Check if the screen width is less than 600 pixels (adjust as needed)
     

// Update isMobile when the window is resized

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
   
  },
};
</script>
