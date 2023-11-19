<template>
  <div id="app">
    <!-- Sidebar -->
    <Sidebar :drawer="drawer" ref="sidebar" />
    
    <!-- Toolbar with Menu Icon -->
    <v-toolbar>
      <v-btn
        icon
        class=""
        @click.stop="drawer = !drawer"
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
      drawer: window.innerWidth >= 1280, // Show sidebar for screens 1280px and wider
    };
  },
  mounted() {
    // Listen to window resize events to update the sidebar state
    window.addEventListener('resize', this.handleResize);

    // Listen to click events on the document to close the sidebar
    document.addEventListener('click', this.handleDocumentClick);
  },
  beforeDestroy() {
    // Remove the resize event listener to prevent memory leaks
    window.removeEventListener('resize', this.handleResize);

    // Remove the click event listener
    document.removeEventListener('click', this.handleDocumentClick);
  },
  methods: {
    handleResize() {
      // Update the drawer state based on the window width
      this.drawer = window.innerWidth >= 1280; // Show sidebar for screens 1280px and wider
    },
    handleDocumentClick(event) {
      // Check if the click event target is outside the sidebar
      const sidebarElement = this.$refs.sidebar?.$el;
      if (sidebarElement && !sidebarElement.contains(event.target)) {
        // If outside, close the sidebar
        this.drawer = false;
      }
    },
  },
};
</script>