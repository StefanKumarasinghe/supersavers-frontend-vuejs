<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
      <v-main>
        <div v-if="showSplashScreen" class="splash-screen" @animationend="onAnimationEnd">
          <v-row align="center" justify="center">
            <v-col cols="12" md="6" lg="6" class="splash-card">
                <v-card-text class="font-weight-bold"><h2>Vmart</h2></v-card-text>
            </v-col>
          </v-row>
        </div>
        <div v-else>
          <v-container fluid>
            <v-row align="center" justify="center" class="">
              <v-col cols="12" md="6" lg="6">
                <v-card-title class="font-weight-bold orange--text">Verify Email</v-card-title>
                <v-card-text class="text-lg-h6 font-weight-bold">
                  You are not yet done. To use the app, we will need you to verify your account before accessing the features
                </v-card-text>
                <v-card-text>
                  <v-btn color="orange" class="font-weight-bold">Send another email</v-btn>
                </v-card-text>
              </v-col>
            </v-row>
          </v-container>
        </div>
      </v-main>
    </v-app>
  </template>
  
  <style>
  .splash-screen {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: orange;
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
  
  <script>
  export default {
    data() {
      return {
        token: null,
        AuthToken: null,
        showSplashScreen: true,
      };
    },
    created() {
      this.TokenPromise();
      this.token = this.ExtractToken();
      this.CheckToken();
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
            const response = await fetch(`http://127.0.0.1:8000/verify-email?token=${this.token}`);
            if (response.ok) {
              this.$router.push('/search');
            } else {
              const data = await response.json();
              console.error('Error:', data.error || 'Unknown error');
              alert("An unexpected error occurred. Please try again.");
            }
          } catch (error) {
            console.error('Error:', error);
          }
        }
      },
      async VerifyAuth() {
        const response = await fetch('http://127.0.0.1:8000/verified', {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });
        if (response.ok) {
          this.$router.push('/search');
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
          const response = await fetch('http://127.0.0.1:8000/protected', {
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
    },
  };
  </script>
  