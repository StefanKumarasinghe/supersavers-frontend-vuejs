<template>
  <v-app>
    <v-main>
      <!-- Reset Password Form -->
      <v-container fluid>
        <v-row align="center" justify="center" class="mt-5 py-5">
          <v-col cols="12" md="5" lg="5">
            <div class="py-5">
              <h2 class="font-weight-bold green--text text--darken-2 ">Reset Password</h2>
              <div class="text-subtitle-1 font-weight-light">Enter new password and confirm password.</div>
            </div>
            <v-form ref="resetForm" v-on:submit.prevent="submitRegistration">
              <div>
                <label for="password" class="font-weight-bold pb-2" >Password:</label>
                <v-text-field
                  class="mb-3"
                  v-model="password"
                  label="Password"
                  :rules="passwordRules"
                  required
                  prepend-inner-icon="mdi-lock"
                  :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showPassword ? 'text' : 'password'"
                  @click:append="showPassword = !showPassword"
                  dense
                  outlined
                  single-line
                ></v-text-field>          
              </div>
              <div>
                <label for="password" class="font-weight-bold pb-2" >Confirm Password:</label>
                <v-text-field
                  v-model="confirmPassword"
                  label="Confirm Password"
                  :rules="confirmPasswordRules"
                  required
                  prepend-inner-icon="mdi-lock"
                  :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  @click:append="showConfirmPassword = !showConfirmPassword"
                  dense
                  outlined
                  single-line
                ></v-text-field>
              </div>
              <v-btn color="green" class="white--text mt-4 font-weight-bold" width="100%" height="45" @click="submitRegistration">submit</v-btn>
            </v-form>
          </v-col>
          <!-- The image will be hidden on small screens (md and below) -->
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="7" lg="7">
            <v-row class="align-items-center">
            <v-col cols="6">
              <v-img
              :src="require('@/assets/reset-image.png')"
              alt="Track your spendings and savings at Woolworths, Coles and IGA with Supersavers"
              height="100%"
              max-width="400"
              max-height="500"
            ></v-img>   
          </v-col>
          <v-col cols="4"> <p class=" fw-bold ">Track your spendings and savings at <span class="text-success">Woolworths</span>, <span class="text-danger">Coles</span> and <span class="text-white bg-danger p-1">IGA</span> </p>
         </v-col>
        </v-row>
        <p class=" fw-bold text-success text-center">Save Heaps with Supersavers.au</p>
          </v-col>
        </v-row>
      </v-container>
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
        password: '',
        showPassword: false,
        passwordRules: [
          (value) => {
            if (value?.length >= 8) return true;
            if (value.length < 1) return 'Password is required';
            return 'Password needs to be at least 8 characters.';
          },
        ],
        confirmPassword: '',
        showConfirmPassword: false,
        confirmPasswordRules: [
          (value) => {
            if (value.length < 1) return 'Confirm Password is required';
            if (this.password == value) return true;
            return 'Passwords need to match.';
          },
        ],
      };
    },
    methods: {
    async submitRegistration() {
      if (this.$refs.resetForm.validate()) {
        // Retrieve the token from the URL
        const urlSearchParams = new URLSearchParams(window.location.search);
        const params = Object.fromEntries(urlSearchParams.entries());
        const token = params.token;

        // Check if token exists
        if (!token) {
          this.$refs.Toast.showSnackbar('No token found, please use the email link provided', 'red', 'mdi-alert-circle');
        } else {
          await this.resetPassword(token, this.password);
        }
      }
    },
    async resetPassword(token, password) {
      try {
        const formData = new FormData();
        formData.append('token', token);
        formData.append('password', password);
        const response = await fetch(`${this.$GroceryAPI}/reset-password`, {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          // Handle different HTTP error codes with appropriate messages
          const errorMessage = response.status === 401 ? 'Invalid token or expired link' : 'Error in recovering your password';
          this.$refs.Toast.showSnackbar(errorMessage, 'red', 'mdi-alert-circle');
        } else {
          this.$refs.Toast.showSnackbar('Successfully reset your password', 'green', 'mdi-check-circle');
          this.$store.commit('clearToken');
          window.location.reload();
          this.$router.push('/login');
        }
        return response.json();
      } catch (error) {
        console.error('Error resetting password:', error);
        this.$refs.Toast.showSnackbar('An unexpected error occurred', 'red', 'mdi-alert-circle');
      }
    }
}

  };
</script>