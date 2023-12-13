<!-- eslint-disable vue/multi-word-component-names -->
<template>

  <v-app class="vapplication">
    <div>
      <!-- Header -->
      <nav class="navbar navbar-expand-lg py-4 px-5 bg-white shadow-sm fixed-top">
        <div class="container-fluid">
          <a class="navbar-brand" href="#"><h4 class="green--text font-weight-bold">SuperSavers</h4></a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav-collapse" aria-controls="nav-collapse" aria-expanded="true" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="nav-collapse">
            <ul class="navbar-nav mx-auto">
              <li class="nav-item">
                <a class="black--text nav-link me-lg-4" href="#product">Product</a>
              </li>
              <li class="nav-item">
                <a class="black--text nav-link me-lg-4" href="#about">About</a>
              </li>
              <li class="nav-item">
                <a class="black--text nav-link" href="#services">Subscriptions</a>
              </li>
            </ul>
            <ul class="navbar-nav">
              <li class="nav-item my-sm-3 my-3 my-lg-0 my-md-0 d-flex">
                <v-btn elevation="0" color="green" class="font-weight-bold" outlined to="login">Login</v-btn>
                <v-btn elevation="0" color="green" class="font-weight-bold ms-4 white--text" to="register">Signup</v-btn>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      <!-- Hero Section -->
      <div id="product">
          <div class="row justify-content-center py-5 my-5">
            <div class="col-lg-2 col-md-1 col-sm-0 col-0"></div>
            <div class="col-lg-4 col-md-5 col-sm-12 col-12 mx-auto d-flex align-items-center" data-aos="fade-up" data-aos-delay="200">
              <span class="mx-auto">
                <h1 class="font-weight-bold green--text">SuperSavers </h1><p class="py-3"> Compare Deals and Save on Groceries At Coles, Woolies & IGA!</p>
                <a href="/search" class="white--text btn btn-success w-50 h-50 rounded-pill">Get started</a>
              </span>              
            </div>
            <div class="col-lg-4 col-md-5 hero-img" data-aos="zoom-in" data-aos-delay="200">
              <img src="@/assets/hero-img.png" class="animated mx-auto d-block img-fluid" alt="">
            </div>
            <div class="col-lg-2 col-md-1 col-sm-0 col-0"></div>
          </div>
      </div>

      <!-- Clients Section -->
      <div class="clients section-bg py-5">
        <div class="container">
          <div class="row" data-aos="zoom-in">
            <div class="col-lg-3 col-md-0 col-sm-0 col-0"></div>
            <div class="col-lg-2 col-md-4 col-sm-4 col-12 d-flex align-items-center justify-content-center">
              <h3 class="text-success fw-bold">Woolworths</h3>
            </div>
            <div class="col-lg-2 col-md-4 col-sm-4 col-12 d-flex align-items-center justify-content-center">
              <h2 class="text-danger fw-bold">Coles</h2>
            </div>
            <div class="col-lg-2 col-md-4 col-sm-4 col-12 d-flex align-items-center justify-content-center">
              <h2 class="bg-danger text-white p-3 fw-bold">IGA</h2>
            </div>
            <div class="col-lg-3 col-md-0 col-sm-0 col-0"></div>
          </div>
        </div>
      </div>

      <!-- About Us Section -->
      <div id="about" class="about py-5" data-aos="fade-up">
        <div class="about-container">
          <div class="section-title pt-5 mt-5">
            <h2>Save Big</h2>
          </div>
          <div class="row px-3">
            <div class="col-lg-6">
              <p style="text-align: justify;">SuperSaver helps you save money on groceries by comparing the best prices between
                <span class="text-success fw-bold">Woolworths</span>,
                <span class="text-danger fw-bold">Coles</span>, and
                <span class="bg-danger text-white fw-bold p-1">IGA</span>.
                Our platform provides real-time price comparisons, allows you to create a grocery list, and shows your potential savings.
              </p>
            </div>
            <div class="col-lg-6" style="text-align: justify;">
              <p>We understand the value of your money, and with SuperSaver, you can make informed decisions to get the best deals. Subscribe now and start saving!</p>
            </div>
          </div>
          <table class="table text-center">
            <tbody>
              <tr v-for="item in ['Compare real-time prices', 'Calculate and manage your grocery list', 'Notfiy you when something is on sale','Direct Comparison of prices', 'Famous deals and products from Woolies, Coles and IGA']" :key="item">
                <td><i class="bi bi-check2"></i></td>
                <td>{{ item }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Services Section -->
      <div id="services" class="services section-bg mt-5 pt-5 pb-5" data-aos="fade-up">
        <div class="service-container">
          <div class="section-title py-5">
            <h2>Best Deals</h2>
            <p>Save more when you get more</p>
          </div>
          <div class="row justify-content-center">
            <div class="col-xl-4 col-md-4 col-sm-12 col-lg-4" data-aos="zoom-in" data-aos-delay="200">
              <div class="icon-box">
                <h3 class="font-weight-medium text-center">Free trial</h3>
                <div class="text-center"><span class="price">A$ 0.00</span> /7 days</div>
                <v-divider class="service-divider text-center"></v-divider>
                <ul>
                  <li class="pt-3">Register to get a free account</li>
                  <li class="pt-3">Compare real-time prices</li>
                  <li class="pt-3">Notifications on sales items</li>
                  <li class="pt-3">Cancel at any time</li>
                </ul>
                <div class="text-center">
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold">Join Now</v-btn>
                </div>
              </div>
            </div>
            <div class="col-xl-4 col-md-4 col-sm-12 col-lg-4" data-aos="zoom-in" data-aos-delay="200">
              <div class="icon-box">
                <h3 class="font-weight-medium text-center">Monthly Plan</h3>
                <div class="text-center"><span class="price">A$ 2.99</span> /month</div>
                <v-divider class="service-divider text-center"></v-divider>
                <ul>
                  <li class="pt-3">Most popular for starters</li>
                  <li class="pt-3">Compare real-time prices</li>
                  <li class="pt-3">Notifications on sales items</li>
                  <li class="pt-3">Cancel at any time</li>
                </ul>
                <div class="text-center">
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold">Subscribe Now</v-btn>
                </div>
              </div>
            </div>
            <div class="col-xl-4 col-md-4 col-sm-12 col-lg-4" data-aos="zoom-in" data-aos-delay="300">
              <div class="icon-box">
                <h3 class="font-weight-medium text-center">Yearly Plan</h3>
                <div class="text-center"><span class="price">A$ 19.99</span> /year</div>
                <v-divider class="service-divider text-center"></v-divider>
                <ul>
                  <li class="pt-3">Save almost A$ 16.00 per year</li>
                  <li class="pt-3">Compare real-time prices</li>
                  <li class="pt-3">Notifications on sales items</li>
                  <li class="pt-3">Cancel at any time</li>
                </ul>
                <div class="text-center">
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold">Subscribe Now</v-btn>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cta Section -->
      <div class="bg-success text-white py-5" data-aos="zoom-in">
        <div class="container ">
          <div class="row">
            <div class="col-lg-9 text-center text-lg-start">
              <h3 class="font-weight-bold">Follow us</h3>
              <p>Never miss an update? Save on deals as soon as SuperSavers is Online</p>
            </div>
            <div class="col-lg-3 social-links mt-lg-3 mt-md-3 col-lg-3 display-5 justify-content-center text-center">
              <a href="#" class="mx-2"><v-icon color="white" large>mdi-email-outline</v-icon></a>
              <a href="#" class="mx-2"><v-icon color="white" large>mdi-linkedin</v-icon></a>
              <a href="#" class="mx-2"><v-icon color="white" large>mdi-instagram</v-icon></a>
            </div>
          </div>
          <div class="copyright pt-5 text-center">
            &copy; Copyright <strong><span>SuperSavers.au</span></strong>. All Rights Reserved
          </div>
        </div>
      </div>

      <b-back-top class="d-flex align-items-center justify-content-center"></b-back-top>
    </div>
  </v-app>

</template>



<script>

</script>

<style>

body {
  font-family: "Quicksand";
  color: #444444;
  padding-top:60px;
  font-size: 17px;
}

h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Quicksand", sans-serif;
}

.vapplication {
  margin-bottom: 0rem !important;
}
/*--------------------------------------------------------------
# Preloader
--------------------------------------------------------------*/
#preloader {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 9999;
  overflow: hidden;
  background: #37517e;
}

#preloader:before {
  content: "";
  position: fixed;
  top: calc(50% - 30px);
  left: calc(50% - 30px);
  border: 6px solid #37517e;
  border-top-color: #fff;
  border-bottom-color: #fff;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: animate-preloader 1s linear infinite;
}

@keyframes animate-preloader {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

/*--------------------------------------------------------------
# Back to top button
--------------------------------------------------------------*/
.back-to-top {
  position: fixed;
  visibility: hidden;
  opacity: 0;
  right: 15px;
  bottom: 15px;
  z-index: 996;
  background: #47b2e4;
  width: 40px;
  height: 40px;
  border-radius: 50px;
  transition: all 0.4s;
}

.back-to-top i {
  font-size: 24px;
  color: #fff;
  line-height: 0;
}

.back-to-top:hover {
  background: #6bc1e9;
  color: #fff;
}

.back-to-top.active {
  visibility: visible;
  opacity: 1;
}

/*--------------------------------------------------------------
# Header
--------------------------------------------------------------*/
#header {
  transition: all 0.5s;
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

/*--------------------------------------------------------------
# Hero Section
--------------------------------------------------------------*/
.animated {
  animation: up-down 2s ease-in-out infinite alternate-reverse both;
}

@media (max-width: 991px) {
  #hero {
    height: 100vh;
    text-align: center;
  }

.animated {
    animation: none;
  }

  #hero .hero-img {
    text-align: center;
  }

  #hero .hero-img img {
    width: 50%;
  }
}

@media (max-width: 768px) {
  #hero h1 {
    font-size: 28px;
    line-height: 36px;
  }

  #hero h2 {
    font-size: 18px;
    line-height: 24px;
    margin-bottom: 30px;
  }

  #hero .hero-img img {
    width: 70%;
  }
}

@media (max-width: 575px) {
  #hero .hero-img img {
    width: 80%;
  }

  #hero .btn-get-started {
    font-size: 16px;
    padding: 10px 24px 11px 24px;
  }
}

@keyframes up-down {
  0% {
    transform: translateY(10px);
  }

  100% {
    transform: translateY(-10px);
  }
}

/*--------------------------------------------------------------
# Sections General
--------------------------------------------------------------*/
section {
  padding: 60px 0;
  overflow: hidden;
}

.section-bg {
  background-color: #f3f5fa;
}

.section-title {
  text-align: center;
  padding-bottom: 10px;
}

.section-title h2 {
  font-size: 32px;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 20px;
  padding-bottom: 20px;
  position: relative;
  color: #37517e;
}

.section-title h2::before {
  content: "";
  position: absolute;
  display: block;
  width: 120px;
  height: 1px;
  background: #ddd;
  bottom: 1px;
  left: calc(50% - 60px);
}

.section-title h2::after {
  content: "";
  position: absolute;
  display: block;
  width: 40px;
  height: 3px;
  background: #47b2e4;
  bottom: 0;
  left: calc(50% - 20px);
}

.section-title p {
  margin-bottom: 0;
}

/*--------------------------------------------------------------
# Clients
--------------------------------------------------------------*/
.clients {
  padding: 12px 0;
  text-align: center;
}

.clients img {
  max-width: 45%;
  transition: all 0.4s ease-in-out;
  display: inline-block;
  padding: 15px 0;
  filter: grayscale(100);
}

.clients img:hover {
  filter: none;
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .clients img {
    max-width: 40%;
  }
}

/*--------------------------------------------------------------
# About Us
--------------------------------------------------------------*/

.about .about-container {
  margin-left: 100px;
  margin-right: 100px;
}

.about .content h3 {
  font-weight: 600;
  font-size: 26px;
}

.about .content ul {
  list-style: none;
  padding: 0;
}

.about .content ul li {
  padding-left: 28px;
  position: relative;
}

.about .content ul li+li {
  margin-top: 10px;
}

.about .content ul i {
  position: absolute;
  left: 0;
  top: 2px;
  font-size: 20px;
  color: #47b2e4;
  line-height: 1;
}

.about .content p:last-child {
  margin-bottom: 0;
}

.about .content .btn-learn-more {
  font-family: "Quicksand", sans-serif;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 1px;
  display: inline-block;
  padding: 12px 32px;
  border-radius: 4px;
  transition: 0.3s;
  line-height: 1;
  color: #47b2e4;
  animation-delay: 0.8s;
  margin-top: 6px;
  border: 2px solid #47b2e4;
}

.about .content .btn-learn-more:hover {
  background: #47b2e4;
  color: #fff;
  text-decoration: none;
}



@media (max-width: 1024px) {
  .why-us .content,
  .why-us .accordion-list {
    padding-left: 0;
    padding-right: 0;
  }
}

@media (max-width: 992px) {
  .why-us .img {
    min-height: 400px;
  }

  .why-us .content {
    padding-top: 30px;
  }

  .why-us .accordion-list {
    padding-bottom: 30px;
  }
}

@media (max-width: 575px) {
  .why-us .img {
    min-height: 200px;
  }

  .about .about-container {
    margin-left: 10px;
    margin-right: 10px;
  }
}


/*--------------------------------------------------------------
# Services
--------------------------------------------------------------*/



.services .service-container {
  margin-left: 50px;
  margin-right: 50px;
  margin-bottom: 50px;
}

.services .icon-box {
  box-shadow: 0px 0 25px 0 rgba(0, 0, 0, 0.1);
  padding: 40px 30px;
  transition: all ease-in-out 0.4s;
  background: #fff;
  border: 1px solid lightgray;
  border-radius: 5px;
}

.services .icon-box .icon {
  margin-bottom: 10px;
}

.services .icon-box .icon i {
  color: #47b2e4;
  font-size: 36px;
  transition: 0.2s;
}

.services .icon-box h4 {
  font-weight: 500;
  margin-bottom: 15px;
  font-size: 24px;
}

.services .icon-box h4 a {
  color: #37517e;
  transition: ease-in-out 0.3s;
}

.services .icon-box p {
  line-height: 24px;
  font-size: 14px;
  margin-bottom: 0;
}

.services .icon-box:hover {
  transform: translateY(-20px);
}

.services .icon-box:hover h4 a {
  color: #47b2e4;
}

.price {
  font-size: 22px;
  font-weight: bold;
}

.services ul {
  list-style: none;
}

.services ul li:before {
  content: '✓';
  color: white;
  padding: 2px 6px;
  margin: 0px 5px;
  background-color: green;
  border-radius: 30px;
}

.service-divider {
  border: 2px solid green;
  background-color: green;
  border-radius: 20px;
  width: 50%;
  margin: 15px auto;
}

@media (max-width: 600px) {
  .services .service-container {
    margin-left: 10px;
    margin-right: 10px;
  }

  .services .icon-box {
    padding: 40px 10px;
  }
}

/*--------------------------------------------------------------
# Cta
--------------------------------------------------------------*/
.cta {

  background-size: cover;
  padding: 120px 0;
}

.cta h3 {
  color: #fff;
  font-size: 28px;
  font-weight: 700;
}

.cta p {
  color: #fff;
}

.cta .cta-btn {
  font-family: "Quicksand", sans-serif;
  font-weight: 500;
  font-size: 16px;
  letter-spacing: 1px;
  display: inline-block;
  padding: 12px 40px;
  border-radius: 50px;
  transition: 0.5s;
  margin: 10px;
  border: 2px solid #fff;
  color: #fff;
}

.cta .cta-btn:hover {
  background: #47b2e4;
  border: 2px solid #47b2e4;
}

@media (max-width: 1024px) {
  .cta {
    background-attachment: scroll;
  }
}

@media (min-width: 769px) {
  .cta .cta-btn-container {
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
}


/*--------------------------------------------------------------
# Pricing
--------------------------------------------------------------*/
.pricing .row {
  padding-top: 40px;
}

.pricing .box {
  padding: 60px 40px;
  box-shadow: 0 3px 20px -2px rgba(20, 45, 100, 0.1);
  background: #fff;
  height: 100%;
  border-top: 4px solid #fff;
  border-radius: 5px;
}

.pricing h3 {
  font-weight: 500;
  margin-bottom: 15px;
  font-size: 20px;
  color: #37517e;
}

.pricing h4 {
  font-size: 48px;
  color: #37517e;
  font-weight: 400;
  font-family: "Quicksand""", sans-serif;
  margin-bottom: 25px;
}

.pricing h4 sup {
  font-size: 28px;
}

.pricing h4 span {
  color: #47b2e4;
  font-size: 18px;
  display: block;
}

.pricing ul {
  padding: 20px 0;
  list-style: none;
  color: #999;
  text-align: left;
  line-height: 20px;
}

.pricing ul li {
  padding: 10px 0 10px 30px;
  position: relative;
}

.pricing ul i {
  color: #28a745;
  font-size: 24px;
  position: absolute;
  left: 0;
  top: 6px;
}

.pricing ul .na {
  color: #ccc;
}

.pricing ul .na i {
  color: #ccc;
}

.pricing ul .na span {
  text-decoration: line-through;
}

.pricing .buy-btn {
  display: inline-block;
  padding: 12px 35px;
  border-radius: 50px;
  color: #47b2e4;
  transition: none;
  font-size: 16px;
  font-weight: 500;
  font-family: "Quicksand", sans-serif;
  transition: 0.3s;
  border: 1px solid #47b2e4;
}

.pricing .buy-btn:hover {
  background: #47b2e4;
  color: #fff;
}

.pricing .featured {
  border-top-color: #47b2e4;
}

.pricing .featured .buy-btn {
  background: #47b2e4;
  color: #fff;
}

.pricing .featured .buy-btn:hover {
  background: #23a3df;
}

@media (max-width: 992px) {
  .pricing .box {
    max-width: 60%;
    margin: 0 auto 30px auto;
  }
}

@media (max-width: 767px) {
  .pricing .box {
    max-width: 80%;
    margin: 0 auto 30px auto;
  }
}

@media (max-width: 420px) {
  .pricing .box {
    max-width: 100%;
    margin: 0 auto 30px auto;
  }
}


/*--------------------------------------------------------------
# Breadcrumbs
--------------------------------------------------------------*/
.breadcrumbs {
  padding: 15px 0;
  background: #f3f5fa;
  min-height: 40px;
  margin-top: 72px;
}

@media (max-width: 992px) {
  .breadcrumbs {
    margin-top: 68px;
  }
}

.breadcrumbs h2 {
  font-size: 28px;
  font-weight: 600;
  color: #37517e;
}

.breadcrumbs ol {
  display: flex;
  flex-wrap: wrap;
  list-style: none;
  padding: 0 0 10px 0;
  margin: 0;
  font-size: 14px;
}

.breadcrumbs ol li+li {
  padding-left: 10px;
}

.breadcrumbs ol li+li::before {
  display: inline-block;
  padding-right: 10px;
  color: #4668a2;
  content: "/";
}

/*--------------------------------------------------------------
# Footer
--------------------------------------------------------------*/
#footer {
  font-size: 14px;
  background: #37517e;
}

#footer .footer-newsletter {
  padding: 50px 0;
  background: #f3f5fa;
  text-align: center;
  font-size: 15px;
  color: #444444;
}

#footer .footer-newsletter h4 {
  font-size: 24px;
  margin: 0 0 20px 0;
  padding: 0;
  line-height: 1;
  font-weight: 600;
  color: #37517e;
}

#footer .footer-newsletter form {
  margin-top: 30px;
  background: #fff;
  padding: 6px 10px;
  position: relative;
  border-radius: 50px;
  box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.06);
  text-align: left;
}

#footer .footer-newsletter form input[type=email] {
  border: 0;
  padding: 4px 8px;
  width: calc(100% - 100px);
}

#footer .footer-newsletter form input[type=submit] {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  border: 0;
  background: none;
  font-size: 16px;
  padding: 0 20px;
  background: #47b2e4;
  color: #fff;
  transition: 0.3s;
  border-radius: 50px;
  box-shadow: 0px 2px 15px rgba(0, 0, 0, 0.1);
}

#footer .footer-newsletter form input[type=submit]:hover {
  background: #209dd8;
}

#footer .footer-top {
  padding: 60px 0 30px 0;
  background: #fff;
}

#footer .footer-top .footer-contact {
  margin-bottom: 30px;
}

#footer .footer-top .footer-contact h3 {
  font-size: 28px;
  margin: 0 0 10px 0;
  padding: 2px 0 2px 0;
  line-height: 1;
  text-transform: uppercase;
  font-weight: 600;
  color: #37517e;
}

#footer .footer-top .footer-contact p {
  font-size: 14px;
  line-height: 24px;
  margin-bottom: 0;
  font-family: "Quicksand", sans-serif;
  color: #5e5e5e;
}

#footer .footer-top h4 {
  font-size: 16px;
  font-weight: bold;
  color: #37517e;
  position: relative;
  padding-bottom: 12px;
}

#footer .footer-top .footer-links {
  margin-bottom: 30px;
}

#footer .footer-top .footer-links ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

#footer .footer-top .footer-links ul i {
  padding-right: 2px;
  color: #47b2e4;
  font-size: 18px;
  line-height: 1;
}

#footer .footer-top .footer-links ul li {
  padding: 10px 0;
  display: flex;
  align-items: center;
}

#footer .footer-top .footer-links ul li:first-child {
  padding-top: 0;
}

#footer .footer-top .footer-links ul a {
  color: #777777;
  transition: 0.3s;
  display: inline-block;
  line-height: 1;
}

#footer .footer-top .footer-links ul a:hover {
  text-decoration: none;
  color: #47b2e4;
}

#footer .footer-top .social-links a {
  font-size: 18px;
  display: inline-block;
  background: #47b2e4;
  color: #fff;
  line-height: 1;
  padding: 8px 0;
  margin-right: 4px;
  border-radius: 50%;
  text-align: center;
  width: 36px;
  height: 36px;
  transition: 0.3s;
}

#footer .footer-top .social-links a:hover {
  background: #209dd8;
  color: #fff;
  text-decoration: none;
}

#footer .footer-bottom {
  padding-top: 30px;
  padding-bottom: 30px;
  color: #fff;
}

#footer .copyright {
  float: left;
}

#footer .credits {
  float: right;
  font-size: 13px;
}

#footer .credits a {
  transition: 0.3s;
}

@media (max-width: 768px) {
  #footer .footer-bottom {
    padding-top: 20px;
    padding-bottom: 20px;
  }

  #footer .copyright,
  #footer .credits {
    text-align: center;
    float: none;
  }

  #footer .credits {
    padding-top: 4px;
  }
}</style>
