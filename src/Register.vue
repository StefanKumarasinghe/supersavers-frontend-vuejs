<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-main>
      <!-- Register Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
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
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold green--text text--darken-2 text-h4">Register</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Register to view the best deals and save on groceries.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                <v-text-field 
                  class="mb-3" 
                  v-model="username" 
                  :rules="nameRules" 
                  label="Username"
                  required
                  prepend-inner-icon="mdi-account"
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <v-text-field 
                  class="mb-3" 
                  v-model="email" 
                  :rules="emailRules" 
                  label="Email"
                  required
                  prepend-inner-icon="mdi-email"
                  flat
                  rounded
                  outlined
                ></v-text-field>
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
                <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%" rounded height="45" @click="submitRegistration">register</v-btn>
                <p class="text-center mt-4">Has an account? <router-link to="login" class="font-weight-bold green--text text-decoration-underline">Login</router-link></p>
              </v-form>
            </v-card-text>
          </v-col>
        </v-row>
        <div class="text-center ma-2">
          <v-snackbar v-model="snackbar" :timeout="snackbarTimeout">
            <v-avatar v-if="snackbarError !== true" color="green" size="30px" class="me-3">
              <v-icon>mdi-check</v-icon>
            </v-avatar>
            <v-avatar v-else color="red" size="30px" class="me-3">
              <v-icon>mdi-alert-circle-outline</v-icon>
            </v-avatar>

          <span class="white--text font-weight-bold">{{ this.message }}!</span>
          <template v-slot:action="{ attrs }">
            <v-btn
              color="green"
              text
              v-bind="attrs"
              @click="snackbar = false"
            >
              <b>Close</b>
            </v-btn>
          </template>
        </v-snackbar>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  async beforeMount() {
    await this.TokenPromise();
  },
  data() {
    return {
      AuthToken: null,
      username: '',
      snackbarError: false,
      snackbarTimeout: 2500,
      snackbar:false,
      error: null,
      nameRules: [
        value => {
          if (value.length > 2) return true;
          return 'Username needs to be at least 3 characters';
        }
      ],
      email: '',
      emailRules: [
        value => {
          if (/^[0-9a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
          return 'Must be a valid e-mail.'
        },
      ],
      password: '',
      showPassword: false,
      passwordRules: [
        value => { 
          if (value?.length >= 8) return true;
          return 'Password needs to be at least 8 characters.';
        }
      ],
      confirmPassword: '',
      showConfirmPassword: false,
      confirmPasswordRules: [
        value => {
          if (this.password == value) return true;
          return 'Passwords need to match.';
        }
      ]
    };
  },
  methods: {
    async TokenPromise() {
      this.AuthToken = await this.getToken();
      this.verifyAuthProcess();
    },
    getToken() {
      return new Promise((resolve) => {
        const tokenSimple = this.$store.getters.getTokenSimple;

        if (tokenSimple) {
          resolve(tokenSimple);
        } else {
          const token = this.$store.getters.getToken;
          resolve(token);
        }
      });
    },
    async verifyAuthProcess() {
      if (this.AuthToken != null) {
        try {
          const response = await fetch(`${this.$GroceryAPI}/protected`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            if (data.user != null) {
              this.snackbarError = true;
              this.error = "You are already logged in ...";
              this.snackbar = true;
              this.$router.push('/search');
            }
          } else {
            console.error('Error:', response.statusText);
          }
        } catch (error) {
          console.error('Error:', error);
      
        }
      }
    },
    async submitRegistration() {
      if (this.password !== this.confirmPassword) {
        this.$toast.error("Passwords don't match!");
        return;
    }
      try {
        const response = await fetch(`${this.$GroceryAPI}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username.toLowerCase(),
            email: this.email.toLowerCase(),
            hashed_password: this.password,
          }),
        });
        if (response.ok) {
            const data = await response.json();
            this.snackbarError= false;
            this.message = "Successfully created your super savers account";
            this.snackbar = await true;
            
            const token = data.access_token;
            // Store the token globally
            await this.$store.dispatch('setToken', token);

            // Redirect to /search
            this.$nextTick(() => {
            this.$router.push('/search');
            });
            window.location.reload(); // IMPORTANT!!!!: to ensure the sidebar is displayed AFTER SIGNING IN
          }else {
            const data = await response.json();
            this.snackbarError= true,
            this.message = "Something is wrong : "+data.detail;
            this.snackbar = true;
          }
      } catch (error) {
        console.error('Registration failed:', error);
        this.snackbarError= true,
        this.message = "Something is went wrong";
        this.snackbar = true;
      
      }
    },
  },
};
</script>

<style>
.v-application .v-application--wrap {
  min-height: 0vh;
}
</style>
