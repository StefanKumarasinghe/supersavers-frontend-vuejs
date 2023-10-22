<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <!-- Top App Bar -->
    <v-app-bar app clipped-left color="green darken-2" dark dense>
      <v-toolbar-title class="pa-3">Alpha</v-toolbar-title>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <!-- Registration Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class=" mb-5 mt-5">
        <v-col cols="6" md="6" lg="6" >
        <v-img src="https://source.unsplash.com/random?cartoon," height="500px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"></v-img>

        </v-col>
          <v-col cols="6" md="6" lg="6">
            <v-card class="shadow-none mb-5 pa-4">
              <v-card-title class="font-weight-bold green--text text--darken-2">Register</v-card-title>
              <v-card-text>Save a lot on Groceries and get the best deals from Coles, Woolworths and Aldi</v-card-text>
              <v-card-text>
                <v-form ref="registrationForm" v-on:submit.prevent="submitRegistration">
                  <v-text-field v-model="username" label="Username" required></v-text-field>
                  <v-text-field v-model="email" label="Email" required type="email"></v-text-field>
                  <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
                  <v-text-field v-model="confirmPassword" label="Confirm Password" type="password" required></v-text-field>
                  
                  <v-btn color="green" class="text-white mt-4" type="submit">Register</v-btn>
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
      // ... (other data properties you provided, like notifications and groceryItem)
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    };
  },
  methods: {
    // ... (other methods you provided, like login and register)

    submitRegistration() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords don't match!");
        return;
      }
      // Handle the registration logic (e.g., send data to the server, etc.)
      console.log('Registration data:', {
        username: this.username,
        email: this.email,
        password: this.password,
      });
      this.resetForm();
    },

    resetForm() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.confirmPassword = '';
    }
  }
};
</script>

