<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app class="vapplication" id="explore-page">
    <div>
      <!-- Hero Section -->
      <div id="product">
        <div class="product-container">
          <div class="row justify-content-center py-5 my-5">
            <div class="col-lg-2 col-md-1 col-sm-0 col-0"></div>
            <div class="col-lg-4 col-md-5 col-sm-12 col-12 mx-auto d-flex align-items-center" data-aos="fade-up" data-aos-delay="200">
              <span class="mx-auto">
                <h1 class="font-weight-bold green--text">Supersavers </h1><p class="py-3 fw-bold"> Compare Deals and Save on Groceries At Coles, Woolies & IGA!</p>
                <v-btn to="search" color="green fw-bold white--text ">Get Started</v-btn>
  <v-btn to="/login" class="btn-outline-success" color="black fw-bold  white--text mx-1 ">
    <v-icon left>mdi-android</v-icon>
     Download
  </v-btn>


              </span>
            </div>
            <div class="col-lg-4 col-md-5 hero-img" data-aos="zoom-in" data-aos-delay="200">
              <img src="@/assets/hero-img.png" class="animated mx-auto d-block img-fluid" alt="">
            </div>
            <div class="col-lg-2 col-md-1 col-sm-0 col-0"></div>
          </div>
        </div>
      </div>
      <!-- Clients Section -->
      <div class="clients section-bg py-5">
        <div class="container">
          <div class="row" data-aos="zoom-in">
            <div class="col-lg-3 col-md-0 col-sm-0 col-0"></div>
            <div class="col-lg-2 col-md-4 col-sm-4 col-6 d-flex align-items-center justify-content-center">
              <h3 class="text-success fw-bold">Woolworths</h3>
            </div>
            <div class="col-lg-2 col-md-4 col-sm-4 col-6 d-flex align-items-center justify-content-center">
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
          <div class="row">
            <div class="col-lg-6">
              <p style="text-align: justify;">Supersaver helps you save money on groceries by comparing the best prices between
                <span class="text-success fw-bold">Woolworths</span>,
                <span class="text-danger fw-bold">Coles</span>, and
                <span class="bg-danger text-white fw-bold p-1">IGA</span>.
                Our platform provides real-time price comparisons, allows you to create a grocery list, and shows your potential savings.
              </p>
            </div>
            <div class="col-lg-6" style="text-align: justify;">
              <p>We understand the value of your money, and with Supersaver, you can make informed decisions to get the best deals. Subscribe now and start saving!</p>
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
      <div id="services" class="services section-bg mt-5 py-5" data-aos="fade-up">
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
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold" to="register">Join Now</v-btn>
                </div>
              </div>
            </div>
            <div class="col-xl-4 col-md-4 col-sm-12 col-lg-4" data-aos="zoom-in" data-aos-delay="200">
              <div class="icon-box">
                <h3 class="font-weight-medium text-center">Monthly Plan</h3>
                <div class="text-center"><span class="price">A$ 4</span> /month</div>
                <v-divider class="service-divider text-center"></v-divider>
                <ul>
                  <li class="pt-3">Most popular for starters</li>
                  <li class="pt-3">Compare real-time prices</li>
                  <li class="pt-3">Notifications on sales items</li>
                  <li class="pt-3">Cancel at any time</li>
                </ul>
                <div class="text-center">
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold" to="register">Subscribe Now</v-btn>
                </div>
              </div>
            </div>
            <div class="col-xl-4 col-md-4 col-sm-12 col-lg-4" data-aos="zoom-in" data-aos-delay="200">
              <div class="icon-box">
                <h3 class="font-weight-medium text-center">Yearly Plan</h3>
                <div class="text-center"><span class="price">A$ 35</span> /year</div>
                <v-divider class="service-divider text-center"></v-divider>
                <ul>
                  <li class="pt-3">Save almost A$ 13.00 per year</li>
                  <li class="pt-3">Compare real-time prices</li>
                  <li class="pt-3">Notifications on sales items</li>
                  <li class="pt-3">Cancel at any time</li>
                </ul>
                <div class="text-center">
                  <v-btn elevation="1" color="green" class="white--text w-75 mt-5 font-weight-bold" to="register">Subscribe Now</v-btn>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cta Section -->
      <div class="cta-container text-white py-5" data-aos="zoom-in">
        <div class="container ">
          <div class="row">
            <div class="col-lg-9 text-center text-lg-start">
              <h3 class="font-weight-bold">Follow us</h3>
              <p>Never miss an update? Save on deals as soon as Supersavers is Online</p>
            </div>
            <div class="col-lg-3 social-links mt-lg-3 mt-md-3 col-lg-3 display-5 justify-content-center text-center">
              <a href="mailto:contact@supersavers.au" class="mx-2"><v-icon color="white" large>mdi-email-outline</v-icon></a>
              <a href="https://www.linkedin.com/company/supersavers" class="mx-2"><v-icon color="white" large>mdi-linkedin</v-icon></a>
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
export default {
  metaInfo: {
  // Page Title
  title: 'Supersavers | Save Heaps on Groceries ',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Welcome to Supersavers, your go-to platform for maximizing savings on groceries. Explore exclusive discounts, compare prices across Woolworths, Coles, and IGA, and start saving today.' }, // Page description
    { name: 'keywords', content: 'Supersavers, welcome, savings, exclusive discounts, groceries, compare prices, Woolworths, Coles, IGA, online grocery shopping, best prices, money-saving' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Welcome to Supersavers | Maximize Your Grocery Savings' }, // Open Graph title
    { property: 'og:description', content: 'Welcome to Supersavers, your go-to platform for maximizing savings on groceries. Explore exclusive discounts, compare prices across Woolworths, Coles, and IGA, and start saving today.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Welcome to Supersavers | Maximize Your Grocery Savings' }, // Twitter title
    { name: 'twitter:description', content: 'Welcome to Supersavers, your go-to platform for maximizing savings on groceries. Explore exclusive discounts, compare prices across Woolworths, Coles, and IGA, and start saving today.' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
}
}
</script>
<style>
#explore-page {
  font-family: "Quicksand";
  color: #444444;
  padding-top:60px !important;
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


#product .product-container {
  margin-left: 0px;
  margin-right: 0px;
}

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

  #product .product-container {
    margin-left: 15px;
    margin-right: 15px;
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
# About Us
--------------------------------------------------------------*/

.about .about-container {
  margin-top:70px;
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
    margin-left: 15px;
    margin-right: 15px;
  }
}


/*--------------------------------------------------------------
# Services
--------------------------------------------------------------*/



.services .service-container {
  margin: 50px;
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
    margin-left: 15px;
    margin-right: 15px;
  }

  .services .icon-box {
    padding: 40px 10px;
  }
}

/*--------------------------------------------------------------
# Cta
--------------------------------------------------------------*/
.cta-container {
  background-color: #43A047;
}

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
