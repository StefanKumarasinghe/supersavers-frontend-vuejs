<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="notAuthenticated">
    <v-main>   
      <div v-if="showSplashScreen" class="splash-screen" @animationend="onAnimationEnd">
        <v-row align="center" justify="center">
          <v-col cols="12" md="6" lg="6" class="splash-card">
              <v-card-text class=""><h2>Supersaver</h2></v-card-text>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-container fluid>
          <v-row align="center" justify="center" class="mt-5 pt-5">
            <v-col cols="12" md="6" lg="6">
              <h1 class=" green--text">Verify Email</h1>
              <h5 class=" my-5">
                You are not yet done. To use the app, we will need you to verify your account before accessing the features
              </h5>
                <v-btn color="green" outlined class="white--text font-weight-bold mx-0 mt-3" @click="resendEmail" >Send another email</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </div>
      <Toast ref="Toast" />
    </v-main>
  </v-app>
</template>
  
<script>
import Toast from './components/Toast.vue';

export default {
    components: {
     Toast
    },
    data() {
      return {
        notAuthenticated:false,
        token: null,
        AuthToken: null,
        showSplashScreen: true,
        snackbarError:false,
        snackbar:false,
        snackbarTimeout:2500,
      };
    },
   async beforeMount() {
      await this.TokenPromise();
      this.token = this.ExtractToken();
      await this.CheckToken();
      this.authCheckInterval = setInterval(this.CheckAuthenticationStatus, 5000);
    },
    beforeDestroy() {
      clearInterval(this.authCheckInterval);
    },
    methods: {
      onAnimationEnd() {
        this.showSplashScreen = false;
      },
      ExtractToken() {
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        const token = params.token;
        if (this.isValidToken(token)) {
          return token;
        } else {
          return null;
        }
      },
      isValidToken(token) {
        const minLength = 10; // Minimum length required for a valid toke
        if (token && token.length >= minLength) {
          return true;
        } else {
          console.error('Invalid token:', token);
          return false;
        }
      },
      async CheckToken() {
          try {
            const response = await fetch(`${this.$GroceryAPI}/verify-email?token=${this.token}`);
            if (response.ok) {
              this.$router.push('/search');
            } else {
              const data = await response.json();
              console.error('Error:', data.error || 'Unknown error');
              this.$refs.Toast.showSnackbar('The token was invalid', 'red', 'mdi-alert-circle');
            }
          } catch (error) {
            console.error('Error:', error);
            this.$refs.Toast.showSnackbar('Something went wrong when validating the token', 'red', 'mdi-alert-circle');
          }
      },
      async VerifyAuth() {
      try { 
        const response = await fetch(`${this.$GroceryAPI}/verified`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });
        if (response.ok) {
           this.$router.push('/search');
        }else{
           this.notAuthenticated=true;
        }
      }
      catch (error) {
            console.error('Error:', error);
            this.$refs.Toast.showSnackbar('Something went wrong when validating verification', 'red', 'mdi-alert-circle');
      }
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
      async TokenPromise() {
        this.AuthToken = await this.getToken();
        await this.verifyAuthProcess();
      },
      async verifyAuthProcess() {
        try {
          const response = await fetch(`${this.$GroceryAPI}/protected`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          if (response.ok) {
              await this.VerifyAuth();
          } else {
            console.error('Error:', response.statusText);
            this.$store.commit('clearToken');
            this.$router.push('/login');
            window.location.reload();
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('Session was invalidated', 'red', 'mdi-alert-circle');
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
        }
      },
      async resendEmail() {
        try {
          const response = await fetch(`${this.$GroceryAPI}/resend-email`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          if (response.ok) {
            this.$refs.Toast.showSnackbar('A new verification email was sent successfully', 'green', 'mdi-check-circle');
          } else {
            this.$refs.Toast.showSnackbar('The credentials were rejected by our server', 'red', 'mdi-alert-circle');
          }
        } catch (error) {
          console.error('Error:', error);
          this.$refs.Toast.showSnackbar('Something went wrong when resending your email', 'red', 'mdi-alert-circle');
        }
      },
      async CheckAuthenticationStatus() {
        this.VerifyAuth();
      }
    },
  };
</script>

<style>
  .splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: green;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fade-out 2s ease-out; /* Adjust the duration as needed */
  }
  
  @keyframes fade-out {
    0% {
      opacity: 1;
    }
    50%{
      opacity: 1;
    }
    100% {
      opacity: 0;
    }
  }
  
  .splash-card {
    background-color: transparent;
    color: white;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
  }
</style>