<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <!-- Top App Bar -->
    <v-app-bar app clipped-left color="green darken-2" dark dense>
      <v-toolbar-title class="pa-3">Alpha</v-toolbar-title>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <!-- Login Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mb-5 mt-5">
          <v-col cols="6" md="6" lg="6">
            <v-img src="https://source.unsplash.com/random?cartoon," height="500px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"></v-img>
          </v-col>
          <v-col cols="6" md="6" lg="6">
            <v-card class="shadow-none mb-5 pa-4">
              <v-card-title class="font-weight-bold green--text text--darken-2">Login</v-card-title>
              <v-card-text>Login to view the best deals and save on groceries.</v-card-text>
              <v-card-text>
                <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                  <v-text-field v-model="usernameOrEmail" label="Username or Email" required></v-text-field>
                  <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
                  
                  <v-btn color="green" class="text-white mt-4" type="submit">Login</v-btn>
                </v-form>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      usernameOrEmail: '',
      password: '',
    };
  },
  methods: {
    submitLogin() {
      // Handle the login logic (e.g., send data to the server, etc.)
      console.log('Login data:', {
        usernameOrEmail: this.usernameOrEmail,
        password: this.password,
      });
      this.resetLoginForm();
    },

    resetLoginForm() {
      this.usernameOrEmail = '';
      this.password = '';
    }
  }
};
</script>
