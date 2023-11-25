<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar :drawer="drawer" ref="sidebar" />
    
    <!-- Toolbar with Menu Icon -->
   
    
    <router-view></router-view>



    <BottomNav :drawer="drawer" />
    
  </div>
  
</template>


<script>
import Sidebar from './components/Sidebar.vue';
import BottomNav from './components/BottomNav.vue';

export default {
  components: {
    Sidebar,
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
      this.isMobile = false;
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
