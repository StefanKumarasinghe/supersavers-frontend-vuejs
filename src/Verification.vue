<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-main>
      <div v-if="showSplashScreen" class="splash-screen" @animationend="onAnimationEnd">
        <v-row align="center" justify="center">
          <v-col cols="12" md="6" lg="6" class="splash-card">
              <v-card-text class="font-weight-bold"><h2>Supersaver</h2></v-card-text>
          </v-col>
        </v-row>
      </div>
      <div v-else>
        <v-container fluid>
          <v-row align="center" justify="center" class="mt-5 pt-5">
            <v-col cols="12" md="6" lg="6">
              <h1 class="font-weight-bold green--text">Verify Email</h1>
              <h5 class="fw-bold text-success my-5">
                You are not yet done. To use the app, we will need you to verify your account before accessing the features
              </h5>
                <v-btn color="green" class="white--text font-weight-bold mx-0 mt-3" @click="resendEmail" >Send another email</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </div>
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
    </v-main>
  </v-app>
</template>
  
<script>
  export default {
    data() {
      return {
        token: null,
        AuthToken: null,
        showSplashScreen: true,
        snackbarError:false,
        snackbar:false,
        snackbarTimeout:2500,
      };
    },
    created() {
      this.TokenPromise();
      this.token = this.ExtractToken();
      this.CheckToken();
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
        if (!token) {
          return null;
        } else {
          return token;
        }
      },
      async CheckToken() {
        if (this.token) {
          try {
            const response = await fetch(`${this.$GroceryAPI}/verify-email?token=${this.token}`);
            if (response.ok) {
              this.$router.push('/search');
            } else {
              const data = await response.json();
              console.error('Error:', data.error || 'Unknown error');
              this.snackbarError= true;
              this.message = "The token is not correct. Could not verify email";
               this.snackbar = true;
            }
          } catch (error) {
            console.error('Error:', error);
          }
        }
      },
      async VerifyAuth() {
        const response = await fetch(`${this.$GroceryAPI}/verified`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });
        if (response.ok) {
          this.snackbarError= false;
          this.message = "Seems like you are verified...";
          this.snackbar = true;
          this.$nextTick(() => {
           this.$router.push('/search');
          });
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
        this.verifyAuthProcess();
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
          }
        } catch (error) {
          console.error('Error:', error);
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
            this.snackbarError= false;
            this.message = "Successfully resent your email. Only valid for 1 hour...";
            this.snackbar = await true;
          } else {
            this.snackbarError= true;
            this.message = "Error sending that email. Try again later";
            this.snackbar = await true;
          }
        } catch (error) {
          console.error('Error:', error);
          this.snackbarError= true;
          this.message = "Something went wrong";
          this.snackbar = await true;
        }
      },
      

      async CheckAuthenticationStatus() {
        this.TokenPromise();
        if (!this.AuthToken) {
          this.$router.push('/search');
        }
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