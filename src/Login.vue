<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app  id="login-page">
    <v-container v-if="!(authenticated)" fill-height>
      <v-row align="center" justify="center">
        <v-col>
          <div class="text-center">
            <!-- Vuetify Progress Circular -->
            <v-progress-circular
              :size="64"
              color="green"
              :width="7"
              indeterminate
            ></v-progress-circular>
            <h2 class="text-success fw-bold mt-3">Signing you in...</h2>
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-main v-if="authenticated" >
      <!-- Login Form -->
      <v-row class="mx-auto h-100 d-flex align-center align-items-center justify-center">
          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" class="" cols="6" md="6" lg="6">
            <v-row class="align-items-center">
            <v-col cols="6">
              <v-img
              :src="require('@/assets/login-image.png')"
              alt="Plan ahead before your next visit to your grocery store to save as much as you can on deals at Woolworths, Coles and IGA with Supersavers"
              height="100%"
              max-width="400"
              max-height="500"
            ></v-img>   
          </v-col>
          <v-col cols="4"> <p class=" fw-bold ">Plan ahead before your next visit to your grocery store to save as much as you can on deals at <span class="text-success">Woolworths</span>, <span class="text-danger">Coles</span> and <span class="text-white bg-danger p-1">IGA</span> </p>
         </v-col>
        </v-row>
        <p class=" fw-bold text-success text-center">Save Heaps with Supersavers.au</p>
        </v-col>
          <v-col cols="12" md="4" lg="4" align-self="center">
            <div class="py-5">
              <h2 class="font-weight-bold green--text text--darken-2 ">Login</h2>
            </div>
            <v-form ref="loginForm" v-on:submit.prevent="submitRegistration">
              <div>
                <label for="username" class="font-weight-bold pb-2" >Username/Email:</label>
                <v-text-field
                  single-line
                  dense
                  required
                  v-model="username"
                  outlined
                  prepend-inner-icon="mdi-account"
                  label="johndoe123/johndoe@gmail.com"
                  :rules="usernameRules"
                ></v-text-field>              
              </div>
              <div>
                <div class="mb-1 me-2 d-flex align-items-center justify-content-between">
                  <label for="password" class="font-weight-bold pb-2" >Password:</label>
                  <span class="text-end">
                    <router-link to="/forgot-password" class="font-weight-bold green--text text-decoration-underline">Forgot password?</router-link>
                  </span>
                </div>
                <v-text-field
                  single-line
                  outlined
                  dense
                  required
                  v-model="password"
                  prepend-inner-icon="mdi-lock"
                  label="Enter your password"
                  :rules="passwordRules"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                ></v-text-field>              
              </div>
              <div class="d-flex justify-content-center">
                <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%"  height="45" @click="submitLogin">Login</v-btn>
              </div>
              <br>
              <router-link to="/register" class="font-weight-bold green--text  text-decoration-underline">Sign up instead?</router-link>
            </v-form>
          </v-col>
        </v-row>
        <div class="text-center ma-2">
          <Toast ref="Toast" />
        </div>
    </v-main>
  </v-app>
</template>

<script>
import Toast from './components/Toast.vue';

export default {
    components: {
     Toast
    },
    metaInfo: {
  // Page Title
  title: 'Supersavers | Sign in ',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Sign in to your Supersavers account and unlock exclusive discounts on groceries. Save big with our deals and compare prices across Woolworths, Coles, and IGA to maximize your savings.' }, // Page description
    { name: 'keywords', content: 'Supersavers, login, sign in, groceries, discounts, savings, exclusive deals, compare prices, Woolworths, Coles, IGA, online grocery shopping, best prices, money-saving' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Save Heaps by Joining Today' }, // Open Graph title
    { property: 'og:description', content: 'Sign in to your Supersavers account and unlock exclusive discounts on groceries. Save big with our deals and compare prices across Woolworths, Coles, and IGA to maximize your savings.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/login' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Save Heaps by Joining Today' }, // Twitter title
    { name: 'twitter:description', content: 'Sign in to your Supersavers account and unlock exclusive discounts on groceries. Save big with our deals and compare prices across Woolworths, Coles, and IGA to maximize your savings.' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

  async beforeMount() {
    await this.TokenPromise();
  },
  data() {
    return {
      authenticated:false,
      AuthToken: null,
      username: '',
      snackbar:false,
      snackbarError: false,
      snackbarTimeout: 2500,
      error: null,
      usernameRules: [
        (value) => {
          if (value?.length > 2) return true;
          return 'Must be a valid username/email.';
        },
      ],
      password: '',
      showPassword: false,
      passwordRules: [
        (value) => {
          if (value?.length >= 8) return true;
          return 'Password needs to be at least 8 characters.';
        },
      ],
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
      if (this.AuthToken !== null) {
        try {
          const response = await fetch(`${this.$GroceryAPI}/protected`, {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${this.AuthToken}`,
            },
          });
          if (response.ok) {
              this.$router.push('/search');
          }
          this.authenticated = true;
        } catch (error) {
          this.$refs.Toast.showSnackbar('Something went wrong with authentication', 'red', 'mdi-alert-circle')
        }
      }else {
        this.authenticated = true;
      }
    },
    async submitLogin() {
      if (this.$refs.loginForm.validate()) {
        try {
          const response = await fetch(`${this.$GroceryAPI}/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username: this.username.toLowerCase().trim(), // Convert username to lowercase
              password: this.password,
            }),
          });
          if (response.ok) {
            const data = await response.json();
            this.$refs.Toast.showSnackbar('Successfully signed in', 'green', 'mdi-check-circle')
            const token = data.access_token;
            await this.$store.dispatch('setToken', token);
            // Redirect to /search
            this.$nextTick(() => {
            this.$router.push('/search');
            });
            window.location.reload(); // IMPORTANT!!!!: to ensure the sidebar is displayed AFTER SIGNING IN
          
          }else {
            const data = await response.json();
            this.$refs.Toast.showSnackbar(data.detail, 'red', 'mdi-alert-circle')
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('Something went wrong signing in ...', 'red', 'mdi-alert-circle');
        }
      }
    },
  },
};
</script>
<style>
#login-page {
  font-family: "Quicksand";
  padding-top:80px !important;
  font-size: 17px;
}
.v-application .v-application--wrap {
  min-height: 0vh;
}

</style>
