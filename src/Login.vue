<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-main>
      <!-- Login Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="">
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold orange--text text--darken-2 text-h4">Login</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Login to view the best deals and save on groceries.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
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
                <v-text-field 
                  class="text-lg-h6" 
                  v-model="password" 
                  label="Password" 
                  :rules="passwordRules" 
                  required
                  type="password" 
                  prepend-inner-icon="mdi-lock"
                  solo
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <v-btn color="orange" class="white--text mt-4 text-h6 font-weight-bold" width="100%" rounded height="45" @click="validateForm">Login</v-btn>
                <p class="text-center mt-4">Don't have an account? <router-link to="register" class="font-weight-bold orange--text text-decoration-underline">Register</router-link></p>
                <p class="text-center">Forgot password? <router-link to="login" class="font-weight-bold orange--text text-decoration-underline">Reset</router-link></p>
              </v-form>
            </v-card-text>
          </v-col>

          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="6" lg="6">
            <v-img
              :src="require('@/assets/login.jpg')"
              alt="Login Image"
              width="100%"
              height="100%"
            ></v-img>
            <p style="font-size: 10px; margin-top: 5px;" class="text-center">
              Image by <a href="https://www.freepik.com/free-vector/people-keeping-healthy-diet_8610283.htm#query=grocery&position=14&from_view=search&track=sph&uuid=eac254f5-c45a-4e03-9939-58c50c521fae" target="_blank" rel="noopener noreferrer">pch.vector</a> on Freepik
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
      password: '',
      passwordRules: [
        value => { 
          if (value?.length > 8) return true
          return 'Password needs to be at least 8 characters.'
        }
      ]
    };
  },
  methods: {
    submitLogin() {
      // Validate the form before handling the login logic
      this.$refs.loginForm.validate().then(valid => {
        if (valid) {
          // Form is valid, proceed with login logic
          console.log('Login data:', {
            email: this.email,
            password: this.password,
          });
        }
      });
    },
    validateForm() {
      // Trigger form validation without submitting
      this.$refs.loginForm.validate();
    }
  }
};
</script>

<style>
.v-application .v-application--wrap {
    min-height: 0vh;
}
</style>
