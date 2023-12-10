<template>
  <v-app>
    <v-main>
      <!-- Reset Password Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold green--text text--darken-2 text-h4">Reset Password</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Enter new password and confirm password.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitRegistration">
                <v-text-field
                  class="mb-3"
                  v-model="password"
                  label="Password"
                  :rules="passwordRules"
                  required
                  prepend-inner-icon="mdi-lock"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <v-text-field
                  v-model="confirmPassword"
                  label="Confirm Password"
                  :rules="confirmPasswordRules"
                  required
                  prepend-inner-icon="mdi-lock"
                  :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  @click:append="showConfirmPassword = !showConfirmPassword"
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%" rounded height="45" @click="submitRegistration">submit</v-btn>
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
        password: '',
        snackbar:false,
        snackbarError:false,
        snackbarTimeout:2500,
        message:null,
        showPassword: false,
        passwordRules: [
          (value) => {
            if (value?.length >= 8) return true;
            return 'Password needs to be at least 8 characters.';
          },
        ],
        confirmPassword: '',
        showConfirmPassword: false,
        confirmPasswordRules: [
          (value) => {
            if (this.password == value) return true;
            return 'Passwords need to match.';
          },
        ],
      };
    },
    methods: {
      async submitRegistration() {
        if (this.$refs.loginForm.validate()) {
          if (this.password !== this.confirmPassword) {
            alert("Passwords don't match!");
          } else {
            // Retrieve the token from the URL
            const urlSearchParams = new URLSearchParams(window.location.search);
            const params = Object.fromEntries(urlSearchParams.entries());
            const token = params.token;

            // Check if token exists
            if (!token) {
              this.message = 'No token found, please use the email link provided';
              this.snackbarError = true;
              this.snackbar = true;
              return;
            }
            const response = await this.resetPassword(token, this.password);
            // Handle the response as needed
            console.log(response);

            this.$router.push('/login');
          }
        }
      },
      async resetPassword(token, password) {
        // Create a FormData object and append both token and password
        const formData = new FormData();
        formData.append('token', token);
        formData.append('password', password);

        // Use the FormData object in the fetch request
        const response = await fetch(`${this.$GroceryAPI}/reset-password`, {
          method: 'POST',
          body: formData,
        });

        if (!(response.ok)) {
          this.message = 'Could not recover your password';
          this.snackbarError = true;
          this.snackbar = true;
        }

        return response.json();
      }
    },
  };
</script>