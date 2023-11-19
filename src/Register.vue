<!-- eslint-disable vue/multi-word-component-names -->
<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-main>
      <!-- Register Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="">
          <v-col cols="12" md="6" lg="6">
            <v-card-title class="font-weight-bold orange--text text--darken-2 text-h4">Register</v-card-title>
            <v-card-text class="text-lg-h6 font-weight-light">Register to view the best deals and save on groceries.</v-card-text>
            <v-card-text class="my-4">
              <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                <v-text-field 
                  class="text-lg-h6 mb-2" 
                  v-model="username" 
                  :rules="nameRules" 
                  label="Name"
                  required
                  prepend-inner-icon="mdi-account"
                  solo
                  flat
                  rounded
                  outlined
                ></v-text-field>
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
                <v-text-field 
                  class="text-lg-h6" 
                  v-model="confirmPassword" 
                  label="Confirm Password" 
                  :rules="confirmPasswordRules" 
                  required
                  type="password" 
                  prepend-inner-icon="mdi-lock"
                  solo
                  flat
                  rounded
                  outlined
                ></v-text-field>
                <v-btn color="orange" class="white--text mt-4 text-h6 font-weight-bold" width="100%" rounded height="45" @click="submitRegistration">register</v-btn>
                <p class="text-center mt-4">Has an account? <router-link to="login" class="font-weight-bold orange--text text-decoration-underline">Login</router-link></p>
              </v-form>
            </v-card-text>
          </v-col>

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
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>



export default {
  mounted() {
  this.AuthToken = this.getToken();
  this.verifyAuthProcess();
  },
  data() {
    return {

      AuthToken: null,
      username: '',
      nameRules: [
        value => {
          if (value.length > 3) return true
          return 'Username needs to be at least 3 characters'
        }
      ],
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
          if (value?.length >= 8) return true
          return 'Password needs to be at least 8 characters.'
        }
      ],
      confirmPassword: '',
      confirmPasswordRules: [
        value => {
          if (this.password == value) return true
          return 'Passwords needs to match.'
        }
      ]
    };
  },
  methods: {
    getToken() {
  return new Promise(async (resolve) => {
    const tokenSimple = this.$store.getters.getTokenSimple;

    if (tokenSimple) {
      resolve(tokenSimple);
    } else {
      // If tokenSimple is not available, wait for the asynchronous action
      await this.$store.dispatch('fetchToken'); // replace 'fetchToken' with your actual action
      const token = this.$store.getters.getToken;
      resolve(token);
    }
  });
}
,
      async verifyAuthProcess() {
        if (this.AuthToken!=null) {
        try {
          const response = await fetch('http://127.0.0.1:8000/protected', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
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
     }
      ,
    async submitRegistration() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords don't match!");
        return;
      }

      try {
        // Make a request to your server for authentication using fetch
        const response = await fetch('http://127.0.0.1:8000/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            hashed_password: this.password,
          }),
        });

        // Check if the request was successful (status code 2xx)
        if (response.ok) {
          // Assuming your server responds with a token
          const data = await response.json();
          const token = data.access_token;

          await this.$store.dispatch('setToken', token);
          
          // Store the token globally (you might want to use a state management library)
          
          // Redirect to the search route
          this.$router.push('/search');
        } else {
          // Handle non-successful response (e.g., show a notification to the user)
          console.error('Registration failed:', response.statusText);
          alert('Registration failed. Please try again.');
        }
      } catch (error) {
        console.error('Registration failed:', error);
        // Handle error (e.g., show a notification to the user)
        alert('Registration failed. Please try again.');
      }

      // Reset the form after successful registration
      this.resetForm();
    },

    resetForm() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.confirmPassword = '';
    },
  },
};
</script>




<style>
.v-application .v-application--wrap {
    min-height: 0vh;
}
</style>

