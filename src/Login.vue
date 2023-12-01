<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-main>
      <!-- Login Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold green--text text--darken-2 text-h4">Login</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Login to view the best deals and save on groceries.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                <v-text-field 
                  v-model="username" 
                  :rules="usernameRules" 
                  label="Username or Email"
                  required
                  prepend-inner-icon="mdi-email"
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <div class="text-end mb-1 me-2"><router-link to="forgotpassword" class="font-weight-bold green--text text-decoration-underline">Forgot password?</router-link></div>
                <v-text-field 
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
                <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%" rounded height="45" @click="submitLogin">Login</v-btn>
                <p class="text-center mt-4">Don't have an account? <router-link to="register" class="font-weight-bold green--text text-decoration-underline">Register</router-link></p>
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
          const response = await fetch('http://127.0.0.1:8000/protected', {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${this.AuthToken}`,
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
    async submitLogin() {
      if (this.$refs.loginForm.validate()) {
        try {
          const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
              username: this.username.toLowerCase(), // Convert username to lowercase
              password: this.password,
            }),
          });

          if (response.ok) {
            this.snackbarError= false,
            this.message = 'Successfully signed in';
            
            this.snackbar = true;
            const data = await response.json();
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
        this.snackbarError= true,
        this.message = 'Something went wrong with loggin in';
        this.snackbar = true;
        }
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
