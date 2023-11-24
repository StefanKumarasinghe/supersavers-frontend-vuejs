<template>
  <v-app>
    <v-main>
      <!-- Login Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold orange--text text--darken-2 text-h4">Login</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Login to view the best deals and save on groceries.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                <v-text-field 
                  class="text-lg-h6 mb-2" 
                  v-model="username" 
                  :rules="usernameRules" 
                  label="Username"
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
                <v-btn color="orange" class="white--text mt-4 text-h6 font-weight-bold" width="100%" rounded height="45" @click="submitLogin">Login</v-btn>
                <p class="text-center mt-4">Don't have an account? <router-link to="register" class="font-weight-bold orange--text text-decoration-underline">Register</router-link></p>
                <p class="text-center">Forgot password? <router-link to="forgotpassword" class="font-weight-bold orange--text text-decoration-underline">Reset</router-link></p>
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
        <v-snackbar v-model="snackbar" color="white " dark>
          <v-row align="center" justify="center" class="ma-0">
            <v-col cols="12" sm="10" md="8" lg="6" class="black--text font-weight-bold text-center">
              {{ this.error }}
              
            </v-col>
            <v-btn
                color="pink"
                variant="text"
                class="text-h6"
                @click="snackbar = false"
              >
                Got it
          </v-btn>
          </v-row>
        </v-snackbar>
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
      snackbar: false,
      error: null,
      usernameRules: [
        (value) => {
          if (/^[0-9a-z.-]+@[a-z.-]+\.[a-z]+$/i.test(value)) return true;
          return 'Must be a valid username.';
        },
      ],
      password: '',
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
            const data = await response.json();
            const token = data.access_token;

            // Store the token globally
            await this.$store.dispatch('setToken', token);

            // Redirect to /search
            this.$router.push('/search');
          } else {
            // Handle non-successful response
  
            this.error = data.statusText;
            this.snackbar = true;
          }
        } catch (error) {
   
          // Handle error
          this.error = data.statusText;
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
