<template>
  <v-app>
    <v-main>
      <!-- Reset Password Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="5" lg="5">
            <div class="py-5">
              <h2 class="font-weight-bold green--text text--darken-2 ">Forgot Password</h2>
              <div class="text-subtitle-1 font-weight-light">Enter your email to reset the password.</div>
            </div>
              <v-form ref="forgotForm" @submit.prevent="submitRegistration">
                <div>
                  <label for="username" class="font-weight-bold pb-2" >Email:</label>
                  <v-text-field
                    single-line
                    required
                    v-model="email"
                    outlined
                    prepend-inner-icon="mdi-email"
                    label="Enter your email"
                    :rules="emailRules"
                  ></v-text-field>              
                </div>
                <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%" height="45" @click="submitRegistration">
                  Submit
                </v-btn>
              </v-form>
          </v-col>

          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="7" lg="7">
            <v-row class="align-items-center">
            <v-col cols="6">
              <v-img
              :src="require('@/assets/forgot-image.png')"
              alt="Take a visit to the products you bought in the past at Woolworths, Coles and IGA with Supersavers"
              height="100%"
              max-width="400"
              max-height="500"
            ></v-img>   
          </v-col>
          <v-col cols="4"> <p class=" fw-bold ">Take a visit to the products you bought in the past at <span class="text-success">Woolworths</span>, <span class="text-danger">Coles</span> and <span class="text-white bg-danger p-1">IGA</span> </p>
         </v-col>
        </v-row>
        <p class=" fw-bold text-success text-center">Save Heaps with Supersavers.au</p>
          </v-col>
        </v-row>
      </v-container>
      <Toast ref="Toast" />
    </v-main>
  </v-app>
</template>
  
<script>
import Toast from './components/Toast.vue';
  export default {
    metaInfo: {
  // Page Title
  title: 'Supersavers | Forgot Password',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Forgot your Supersavers password? No worries! Recover your account and regain access to exclusive discounts on groceries. Follow the steps to reset your password and continue saving.' }, // Page description
    { name: 'keywords', content: 'Supersavers, forgot password, password recovery, account recovery, reset password, regain access, exclusive discounts, groceries, savings' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Forgot Password' }, // Open Graph title
    { property: 'og:description', content: 'Forgot your Supersavers password? No worries! Recover your account and regain access to exclusive discounts on groceries. Follow the steps to reset your password and continue saving.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/forgot-password' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Forgot Password' }, // Twitter title
    { name: 'twitter:description', content: 'Forgot your Supersavers password? No worries! Recover your account and regain access to exclusive discounts on groceries. Follow the steps to reset your password and continue saving.' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},
    components: {
      Toast
    },
    data() {
      return {
        email: '',
        emailRules: [
          value => {
            if (/^[0-9a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
            if (value.length < 1) return 'Email is required'
            return 'Must be a valid e-mail.'
          },
        ],
      }
    },
    methods: {
      async submitRegistration() {
        if (this.$refs.forgotForm.validate()) {
          try {
            const response = await fetch(`${this.$GroceryAPI}/forgot-password`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Change content type if necessary
              },
              body: new URLSearchParams({ email: this.email }),
            });
            if (response.ok) {
              this.$refs.Toast.showSnackbar('Successfully sent a password recovery email', 'green', 'mdi-check-circle');
            } else {
              const errorData = await response.json();
              this.$refs.Toast.showSnackbar('Oops: '+errorData.detail, 'red', 'mdi-alert-circle');
            }
          } catch (error) {
            this.$refs.Toast.showSnackbar('Something went wrong in recovering your password', 'red', 'mdi-alert-circle');
          }
        } 
      },
    },
  }
</script>
