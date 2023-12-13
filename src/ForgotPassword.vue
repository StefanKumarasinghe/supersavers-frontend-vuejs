<template>
  <v-app>
    <v-main>
      <!-- Reset Password Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="5" lg="5">
            <div class="py-5">
              <h4 class="font-weight-bold green--text text--darken-2 text-h4">Forgot Password</h4>
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
      <div class="text-center ma-2">
        <v-snackbar v-model="snackbarError" :timeout="snackbarTimeout" >
          <v-avatar color="red" size="30px" class="me-3"><v-icon>mdi-alert-circle</v-icon></v-avatar>
          <span class="white--text font-weight-bold">{{ this.error }}!</span>
          <template v-slot:action="{ attrs }">
            <v-btn
              color="red"
              text
              v-bind="attrs"
              @click="snackbar = false"
            >
              <b>Close</b>
            </v-btn>
          </template>
        </v-snackbar>
      </div>
    </v-main>
  </v-app>
</template>
  
<script>
  export default {
    data() {
      return {
        email: '',
        snackbarError:false,
        snackbarTimeout:2500,
        message:null,
        emailRules: [
          value => {
            if (/^[a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
            if (value.length < 1) return 'Email is required'
            return 'Must be a valid e-mail.'
          },
        ],
      }
    },
    methods: {
      async submitRegistration() {
        if (this.$refs.forgotForm.validate()) {
          // Send a POST request to the FastAPI endpoint
          try {
            const response = await fetch(`${this.$GroceryAPI}/forgot-password`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Change content type if necessary
              },
              body: new URLSearchParams({ email: this.email }),
            });
            if (response.ok) {
              this.error = 'Successfully sent a password recovery email';
              this.snackbarError = true;

            } 
          } catch (error) {
            console.error('Error:', error);
            this.error = 'Could not recover your password';
            this.snackbarError = true;
            
          }
        } 
      },
    },
  }
</script>
