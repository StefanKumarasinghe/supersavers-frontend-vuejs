<template>
    <v-app>
      <v-main>
        <!-- Reset Password Form -->
        <v-container fluid>
          <v-row align="center" justify="center" class="">
            <v-col cols="12" md="6" lg="6">
              <v-card-title class="font-weight-bold orange--text text--darken-2 text-h4">Reset Password</v-card-title>
              <v-card-text class="text-lg-h6 font-weight-light">Enter your email to reset the password.</v-card-text>
              <v-card-text class="my-4">
                <v-form ref="loginForm" @submit.prevent="submitRegistration">
                  <v-text-field
                    class="text-lg-h6 mb-2"
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    required
                    prepend-inner-icon="mdi-email"
                    solo
                    flat
                    rounded
                    outlined
                  ></v-text-field>
                  <v-btn color="orange" class="white--text mt-4 text-h6 font-weight-bold" width="100%" rounded height="45" @click="submitRegistration">
                    Submit
                  </v-btn>
                </v-form>
              </v-card-text>
            </v-col>
  
            <!-- The image will be hidden on small screens (md and below) -->
            <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="6" lg="6">
              <v-img
                :src="require('@/assets/register.jpg')"
                alt="Login Image"
                width="100%"
                height="100%"
              ></v-img>
              <p style="font-size: 10px; margin-top: 5px;" class="text-center">
                Image by <a href="https://www.freepik.com/free-vector/tiny-family-grocery-bag-with-healthy-food-parents-kids-fresh-vegetables-flat-illustration_12291304.htm#page=2&query=grocery%20cartoon&position=0&from_view=search&track=ais&uuid=3a3d4e0d-173d-46b5-beaf-de16b25ebd7e" target="_blank" rel="noopener noreferrer">pch.vector</a> on Freepik
              </p>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        email: '',
        emailRules: [
          value => {
            if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
            return 'Must be a valid e-mail.'
          },
        ],
      }
    },
    methods: {
      async submitRegistration() {
        if (this.$refs.loginForm.validate()) {
          // Send a POST request to the FastAPI endpoint
          try {
            const response = await fetch('http://127.0.0.1:8000/forgot-password', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded', // Change content type if necessary
  },
  body: new URLSearchParams({ email: this.email }),
});


  
            if (response.ok) {
              alert("Reset password link was sent successfully to your email!");
            } else {
              alert("Failed to request password reset. Please try again.");
            }
          } catch (error) {
            console.error('Error:', error);
            alert("An unexpected error occurred. Please try again.");
          }
        } else {
          alert("Please enter a valid email address.");
        }
      },
    },
  }
  </script>
  
  <style>
  </style>
  