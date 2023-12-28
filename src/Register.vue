<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app id="register-page">
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
    <v-main v-if="authenticated">
      <!-- Register Form -->
        <v-row class="d-flex align-center justify-center register-container">
          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="6" lg="6">
            <v-row class="align-items-center">
            <v-col cols="6">
              <v-img
              :src="require('@/assets/register-image.png')"
              alt="Choose what items you want to be notified when they are on Sale at Woolworths, Coles and IGA with Supersavers"
              height="100%"
              max-width="400"
              max-height="500"
            ></v-img>   
          </v-col>
          <v-col cols="4"> <p class=" fw-bold ">Choose what items you want to be notified when they are on Sale at <span class="text-success">Woolworths</span>, <span class="text-danger">Coles</span> and <span class="text-white bg-danger p-1">IGA</span> </p>
         </v-col>
        </v-row>
        <p class=" fw-bold text-success text-center">Save Heaps with Supersavers.au</p>
          </v-col>
          <v-col cols="12" md="4" lg="4" align-self="center">
            <div class="py-5">
              <h2 class="font-weight-bold green--text text--darken-2 ">Register</h2>
            </div>
            <v-form ref="regForm" v-on:submit.prevent="submitRegistration">
              <div>
                <label for="username" class="font-weight-bold pb-2" >Username:</label>
                <v-text-field
                  single-line
                  dense
                  required
                  v-model="username"
                  outlined
                  prepend-inner-icon="mdi-account"
                  label="johndoe123"
                  :rules="nameRules"
                ></v-text-field>              
              </div>

              <div>
                <label for="email" class="font-weight-bold pb-2" >Email:</label>
                <v-text-field
                  single-line
                  outlined
                  dense
                  required
                  v-model="email"
                  prepend-inner-icon="mdi-email"
                  label="johndoe@gmail.com"
                  :rules="emailRules"
                ></v-text-field>              
              </div>

              <div>
                <label for="password" class="font-weight-bold pb-2" >Password:</label>
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

              <div>
                <label for="confirmPassword" class="font-weight-bold pb-2" >Confirm Password:</label>
                <v-text-field
                  single-line
                  outlined
                  dense
                  required
                  v-model="confirmPassword"
                  prepend-inner-icon="mdi-lock"
                  label="Enter your password"
                  :rules="confirmPasswordRules"
                  :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  @click:append="showConfirmPassword = !showConfirmPassword"
                ></v-text-field>              
              </div>
              <div>
      <v-checkbox
        class="fw-bold"
        label="I agree to all terms and conditions"
        required
      ></v-checkbox>
    </div>
              <div class="d-flex justify-content-center">
                <v-btn color="green" class="white--text mt-4 font-weight-bold"  height="45" width="100%" @click="submitRegistration">register</v-btn>
              </div>
              <p class="text-center mt-3">Has an account? <router-link to="login" class="font-weight-bold green--text text-decoration-underline">Login</router-link></p>            </v-form>
          </v-col>
        </v-row>
        <Toast ref="Toast" />
    </v-main>
  </v-app>
</template>

<script>
import Toast from './components/Toast.vue';

export default {
  metaInfo: {
  // Page Title
  title: 'Supersavers | Sign up  ',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Create a Supersavers account and access exclusive discounts on groceries. Register today to start saving on your favorite items. Compare prices across Woolworths, Coles, and IGA.' }, // Page description
    { name: 'keywords', content: 'Supersavers, register, sign up, create account, groceries, discounts, savings, exclusive deals, compare prices, Woolworths, Coles, IGA, online grocery shopping, best prices, money-saving' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Unlock Exclusive Discounts by Registering Today' }, // Open Graph title
    { property: 'og:description', content: 'Create a Supersavers account and access exclusive discounts on groceries. Register today to start saving on your favorite items. Compare prices across Woolworths, Coles, and IGA.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/register' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Unlock Exclusive Discounts by Registering Today' }, // Twitter title
    { name: 'twitter:description', content: 'Create a Supersavers account and access exclusive discounts on groceries. Register today to start saving on your favorite items. Compare prices across Woolworths, Coles, and IGA.' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

  components: {
    Toast
  },
  async beforeMount() {
    await this.TokenPromise();
  },
  data() {
    return {
      AuthToken: null,
      authenticated:false,
      username: '',
      error: null,
      nameRules: [
        value => {
          if (value.length >= 3 && !/\s/.test(value)) return true;
          if (value.length < 3) return 'Username needs to be at least 3 characters';
          return 'Username should not contain spaces';
        }
      ],
      email: '',
      emailRules: [
        value => {
          if (/^[0-9a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true
          if (value.length < 1) return 'Email is required';
          return 'Must be a valid e-mail.'
        },
      ],
      password: '',
      showPassword: false,
      passwordRules: [
        value => { 
          if (value?.length >= 8) return true;
          if (value.length < 1) return 'Password is required';
          return 'Password needs to be at least 8 characters.';
        }
      ],
      confirmPassword: '',
      showConfirmPassword: false,
      confirmPasswordRules: [
        value => {
          if (value?.length < 1) return 'Confirm password is required';
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
    async submitRegistration() {
      if (this.$refs.regForm.validate()) {
        try {
          const response = await fetch(`${this.$GroceryAPI}/register`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              username: this.username.toLowerCase().trim(),
              email: this.email.toLowerCase(),
              hashed_password: this.password,
            }),
          });
          if (response.ok) {
            const data = await response.json();
            this.$refs.Toast.showSnackbar('You have successfully created your account!', 'green', 'mdi-check-circle');
            new Promise(resolve => setTimeout(resolve, 1000));
            const token = data.access_token;
            await this.$store.dispatch('setToken', token);
            window.location.reload(); // IMPORTANT!!!!: to ensure the sidebar is displayed AFTER SIGNING IN
            this.$nextTick(() => {
              this.$router.push('/verify');
          });
          }else {
            const errorData = await response.json();
            this.$refs.Toast.showSnackbar('Error: '+ errorData.detail, 'red', 'mdi-alert-circle');
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('Something went wrong with signing up', 'red', 'mdi-alert-circle');
        }
      }
    },
  },
};
</script>
<style>
#register-page {
  font-family: "Quicksand";
  padding-top:80px !important;
  font-size: 17px;
}

.v-application .v-application--wrap {
  min-height: 0vh;
}

#register-page .register-container {
  margin-left: 0px;
  margin-right: 0px;
}

@media (max-width: 952px) {
  #register-page .register-container {
    margin-left: 15px;
    margin-right: 15px;
  }
}

</style>
