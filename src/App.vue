<template>
  <div id="app">
    <Sidebar />
    <router-view></router-view>
  </div>
</template>

<script>
  import Sidebar from './components/Sidebar.vue'
  export default {
    components: {
      Sidebar
    }
  }
</script>
