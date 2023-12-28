<template>
    <v-app>
        <nav class="navbar navbar-expand-lg py-4 shadow-sm mb-5 bg-white rounded fixed-top">
          <div class="container-fluid mx-3">
            <router-link class="navbar-brand" to="/"><h4 class="green--text font-weight-bold">Supersavers</h4></router-link>
            <button class="navbar-toggler"  data-bs-toggle="collapse" data-bs-target="#nav-collapse" aria-controls="nav-collapse" aria-expanded="true" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="nav-collapse">
                <ul class="navbar-nav mx-auto">
                  <li class="nav-item me-lg-4">
                      <router-link :to="{ path: '/', hash: '#product' }" :class="{ 'navlink-highlighted': this.routeHash === 'product' }" @click.native="scrollToAbout('product')">
                        <a href="#product" class="black--text nav-link font-weight-bold" :class="{ 'green--text': this.routeHash === 'product' }">Product</a>
                      </router-link>                 
                  </li>
                  <li class="nav-item me-lg-4">
                    <router-link :to="{ path: '/', hash: '#about' }" :class="{ 'navlink-highlighted': this.routeHash === 'about' }" @click.native="scrollToAbout('about')">
                      <a href="#about" class="black--text nav-link" :class="{ 'green--text': this.routeHash === 'about' }">About</a>
                    </router-link>   
                  </li>
                  <li class="nav-item me-lg-4">
                    <router-link :to="{ path: '/', hash: '#services' }" :class="{ 'navlink-highlighted': this.routeHash === 'services' }" @click.native="scrollToAbout('services')">
                      <a href="#services" class="black--text nav-link" :class="{ 'green--text': this.routeHash === 'services' }">Services</a>
                    </router-link>  
                  </li>
                  
                  <li class="nav-item me-lg-4">
                    <router-link :to="{ path: '/billing-support' }"  >
                      <a  class="black--text nav-link" >Billing</a>
                    </router-link>
                  </li>
                  <li class="nav-item me-lg-4">
                    <router-link :to="{ path: '/privacy-policy' }" >
                      <a  class="black--text nav-link" >Privacy</a>
                    </router-link>
                  </li>
                
                </ul>
                <ul class="navbar-nav">
                  <li class="nav-item me-lg-4">
                    <router-link to="login" :class="{ 'navlink-highlighted': this.routeHash === 'login' }">
                      <a class="black--text nav-link" :class="{ 'green--text': this.routeHash === 'login' }">Login</a>
                    </router-link>
                  </li>
                  <li class="nav-item">
                    <router-link to="register" :class="{ 'navlink-highlighted': this.routeHash === 'register' }">
                      <a class="black--text nav-link" :class="{ 'green--text': this.routeHash === 'register' }">Register</a>
                    </router-link>    
                  </li>
                </ul>
            </div>
            </div>
        </nav>
    </v-app>
</template>

<script>
    export default {
      data() {
        return {
          routeHash: this.$route.hash,
        };
      },
      created() {
        // Update routeHash when the component is created
        this.updateRouteHash();
      },
      watch: {
        '$route.path'() {
          // Update routeHash when the route path changes
          this.updateRouteHash();
        },
      },
      mounted() {
        // Add a scroll event listener when the component is mounted
          window.addEventListener('scroll', this.handleScroll);
      },
      destroyed() {
        // Remove the scroll event listener when the component is destroyed
        window.removeEventListener('scroll', this.handleScroll);
      },
      methods: {
        updateRouteHash() {
          this.routeHash = '';
          if (this.$route.path === '/login') {
            this.routeHash = 'login';
          } else if (this.$route.path === '/register') {
            this.routeHash = 'register';
          } else if (this.$route.path === '/') {
            this.routeHash = 'product';
          }
        },
        handleScroll() {
          const scrollPosition = window.scrollY || window.pageYOffset;
          // Logic to determine the active section based on scroll position
          // For simplicity, let's assume each section has a fixed height
          const productSection = document?.getElementById('product');
          const aboutSection = document?.getElementById('about');
          const servicesSection = document?.getElementById('services');

          if (productSection != null && aboutSection != null && servicesSection != null) {
            if (
              scrollPosition >= productSection.offsetTop &&
              scrollPosition < aboutSection.offsetTop
            ) {
              this.routeHash = 'product';
            } else if (
              scrollPosition >= aboutSection.offsetTop &&
              scrollPosition < servicesSection.offsetTop
            ) {
              this.routeHash = 'about';
            } else if (scrollPosition >= servicesSection.offsetTop) {
              this.routeHash = 'services';
            } 
          }
        },
        scrollToAbout(section) {
          // Assuming you have a function to handle smooth scrolling
          this.smoothScrollToElement(section);
        },
        smoothScrollToElement(elementId) {
          const element = document.getElementById(elementId);
          if (element) {
            element.scrollIntoView({
            behavior: 'smooth',
            block: 'start',
            });
          }
        },
      }
    }
</script>

<style>
/*--------------------------------------------------------------
# Header
--------------------------------------------------------------*/
#header {
  z-index: 997;
  padding: 15px 0;
}

#header.header-scrolled,
#header.header-inner-pages {
  background: rgba(40, 58, 90, 0.9);
}

#header .logo {
  font-size: 30px;
  margin: 0;
  padding: 0;
  line-height: 1;
  font-weight: 500;
  letter-spacing: 2px;
  text-transform: uppercase;
}


#header .logo img {
  max-height: 40px;
}

.v-application a:hover {
    color: black;
}

/*--------------------------------------------------------------
# Navigation Menu
--------------------------------------------------------------*/
/**
* Desktop Navigation 
*/
.navbar {
  padding: 0;
}

.navbar ul {
  margin: 0;
  padding: 0;
  display: flex;
  list-style: none;
  align-items: center;
}

.navbar li {
  position: relative;
}

.navbar a,
.navbar a:focus {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 17px;
  font-weight: 500;
  color: black;
  font-weight: bold;
  white-space: nowrap;
  transition: 0.3s;
}

.navbar a i,
.navbar a:focus i {
  font-size: 12px;
  line-height: 0;
  margin-left: 5px;
}

.navbar a:hover,
.navbar .active,
.navbar .active:focus,
.navbar li:hover>a {
  color: #228B22;
}

.navbar .getstarted,
.navbar .getstarted:focus {
  padding: 8px 20px;
  margin-left: 30px;
  border-radius: 50px;
  color: #fff;
  font-size: 14px;
  border: 2px solid #47b2e4;
  font-weight: 600;
}

.navbar .getstarted:hover,
.navbar .getstarted:focus:hover {
  color: #fff;
  background: #31a9e1;
}

.navbar .dropdown ul {
  display: block;
  position: absolute;
  left: 14px;
  top: calc(100% + 30px);
  margin: 0;
  padding: 10px 0;
  z-index: 99;
  opacity: 0;
  visibility: hidden;
  background: #fff;
  box-shadow: 0px 0px 30px rgba(127, 137, 161, 0.25);
  transition: 0.3s;
  border-radius: 4px;
}

.navlink-highlighted {
  border-bottom: 1px solid #43A047;
  padding-bottom: 0px;
  transition:0.3s; /* Adjust the duration and timing function as needed */
}


@media (max-width: 1366px) {
  .navbar .dropdown .dropdown ul {
    left: -90%;
  }

  .navbar .dropdown .dropdown:hover>ul {
    left: -100%;
  }
}

/**
* Mobile Navigation 
*/
.mobile-nav-toggle {
  color: #fff;
  font-size: 28px;
  cursor: pointer;
  display: none;
  line-height: 0;
  transition: 0.5s;
}

.mobile-nav-toggle.bi-x {
  color: #fff;
}

.navbar-mobile {
  position: fixed;
  overflow: hidden;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  background: rgba(40, 58, 90, 0.9);
  transition: 0.3s;
  z-index: 999;
}

.navbar-mobile .mobile-nav-toggle {
  position: absolute;
  top: 15px;
  right: 15px;
}

.navbar-mobile ul {
  display: block;
  position: absolute;
  top: 55px;
  right: 15px;
  bottom: 15px;
  left: 15px;
  padding: 10px 0;
  border-radius: 10px;
  background-color: #fff;
  overflow-y: auto;
  transition: 0.3s;
}

.navbar-mobile a,
.navbar-mobile a:focus {
  padding: 10px 20px;
  font-size: 15px;
  color: #37517e;
}

.navbar-mobile a:hover,
.navbar-mobile .active,
.navbar-mobile li:hover>a {
  color: #47b2e4;
}

.navbar-mobile .getstarted,
.navbar-mobile .getstarted:focus {
  margin: 15px;
  color: #37517e;
}

.navbar-mobile .dropdown ul {
  position: static;
  display: none;
  margin: 10px 20px;
  padding: 10px 0;
  z-index: 99;
  opacity: 1;
  visibility: visible;
  background: #fff;
  box-shadow: 0px 0px 30px rgba(127, 137, 161, 0.25);
}

.navbar-mobile .dropdown ul li {
  min-width: 200px;
}

.navbar-mobile .dropdown ul a {
  padding: 10px 20px;
}

.navbar-mobile .dropdown ul a i {
  font-size: 12px;
}

.navbar-mobile .dropdown ul a:hover,
.navbar-mobile .dropdown ul .active:hover,
.navbar-mobile .dropdown ul li:hover>a {
  color: #47b2e4;
}

.navbar-mobile .dropdown>.dropdown-active {
  display: block;
  visibility: visible !important;
}

</style>