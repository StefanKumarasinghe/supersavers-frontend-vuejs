<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app id="login-page">
    <v-main>
      <!-- Login Form -->
      <v-row class="mx-auto d-flex align-center justify-center">
          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="7" lg="7">
            <v-img
              :src="require('@/assets/login.jpg')"
              alt="Login Image"
              height="80%"
              max-height="440"
            ></v-img>
            <p style="font-size: 10px; margin-top: 5px;" class="text-center">
              Image by <a href="https://www.freepik.com/free-vector/people-keeping-healthy-diet_8610283.htm#query=grocery&position=14&from_view=search&track=sph&uuid=eac254f5-c45a-4e03-9939-58c50c521fae" target="_blank" rel="noopener noreferrer">pch.vector</a> on Freepik
            </p>        
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
          const response = await fetch(`${this.$GroceryAPI}/protected`, {
            method: 'GET',
            headers: {
              Authorization: `Bearer ${this.AuthToken}`,
            },
          });

          if (response.ok) {
              this.snackbarError = false;
              this.error = "You are already logged in ...";
              this.snackbar = true;
              this.$router.push('/search');
         
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
          const response = await fetch(`${this.$GroceryAPI}/login`, {
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
            const data = await response.json();
            this.snackbarError= false,
            this.message = 'Successfully signed in';
            this.snackbar = true;
           
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
#login-page {
  font-family: "Quicksand";
  padding-top:80px !important;
  font-size: 17px;
}
.v-application .v-application--wrap {
  min-height: 0vh;
}

</style>
