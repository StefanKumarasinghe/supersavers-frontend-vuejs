<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
    <v-container fluid>
      <!-- User Information Section -->
      <div class="mx-3 mt-5">
        <h2>
          SETTINGS
        </h2>
        <v-alert border="left" colored-border type="info" elevation="2" color="green" prominent class="mt-5" width="auto">
          <h3>Hey, {{ user.name }}</h3>
          This is your profile page, you can manage notifications, subscriptions and even account details.
        </v-alert>
        <v-row fluid>
          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="12" md="4" lg="3" align-self="center">
            <v-img :src="require('@/assets/profile-1.png')" alt="Profile Image" class="profile-image"></v-img>
          </v-col>
          <v-col cols="12" md="8" lg="9">
            <!-- Keep Saving -->
            <div class="black--text box-border my-5 text-center">
              <v-row class="text-center">
                <h5 class="font-weight-bold">Monthly Subscription </h5>
              </v-row>
              <v-row class="text-center">
                <h4 class="green--text font-weight-bold">FREE</h4>
                <v-alert colored-border type="info" elevation="2" color="red" prominent class="mt-5" width="100%">
                  Supersavers will only be free until it is tested. You are using a testing version
                </v-alert>
              </v-row>
            </div>
            <div class="text-black box-border my-5 pe-5 pb-5 text-center">
              <v-row class="text-center align-center"> <!-- Added align-center class -->
                <h5 class="font-weight-bold">Monthly Savings</h5>
                <h4 class="green--text font-weight-bold" v-if="amount">$ AUD {{ amount }}</h4>
              </v-row>
          
            </div>
          </v-col>
        </v-row>
        <v-divider :thickness="12" color="black"></v-divider>

        <!-- Change password -->
        <div class="row">
          <div class="col-lg-4 col-md-3 col-12">
            <h5 class="font-weight-bold">
            <v-icon color="black">mdi-shield-account</v-icon> Change Password
            </h5>
          </div>
          <div class="col-lg-8 col-md-9 col-12">
            <v-form ref="changePassForm" v-on:submit.prevent="changePassword">
              <div class="row font-weight-bold">
                Old Password:
              </div>
              <div class="row">
                <v-text-field
                  single-line
                  dense
                  required
                  v-model="oldPassword"
                  outlined
                  prepend-inner-icon="mdi-lock"
                  label="Enter your old password"
                  :rules="oldPasswordRules"
                  :append-icon="showOldPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showOldPassword ? 'text' : 'password'"
                  @click:append="showOldPassword = !showOldPassword"
                ></v-text-field>   
              </div>
              <div class="row font-weight-bold">
                New Password:
              </div>
              <div class="row">
                <v-text-field
                  single-line
                  dense
                  required
                  v-model="newPassword"
                  outlined
                  prepend-inner-icon="mdi-lock"
                  label="Enter your old password"
                  :rules="newPasswordRules"
                  :append-icon="showNewPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showNewPassword ? 'text' : 'password'"
                  @click:append="showNewPassword = !showNewPassword"
                ></v-text-field> 
              </div>
              <div class="row font-weight-bold">
                New Confirm Password:
              </div>
              <div class="row">
                <v-text-field
                  single-line
                  dense
                  required
                  v-model="newConfirmPassword"
                  outlined
                  prepend-inner-icon="mdi-lock"
                  label="Enter your old password"
                  :rules="newConfirmPasswordRules"
                  :append-icon="showNewConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="showNewConfirmPassword ? 'text' : 'password'"
                  @click:append="showNewConfirmPassword = !showNewConfirmPassword"
                ></v-text-field>
              </div>
              <div class="row">
                <v-btn color="green font-weight-bold white--text" @click="changePassword()" height="50">Change password</v-btn>
              </div>
            </v-form>
          </div>
        </div>
        <v-divider :thickness="12" color="black"></v-divider>

        <!-- Notifications -->
        <div class="row">
          <div class="col-lg-4 col-md-3 col-12">
            <h5 class="font-weight-bold">
            <v-icon color="black">mdi-bell</v-icon> Notifications
            </h5>
          </div>
          <div class="col-lg-8 col-md-9 col-12">
            <div class="row" :v-model="selectedSubscriptions" v-for="(subscription, index) in subscriptions" :key="index">
              <div class="col-10 col-lg-11 col-md-11">
                <div class="font-weight-bold">{{subscription.name}}</div>
                <div>{{subscription.description}}</div>
              </div>
              <div class="col-2 col-lg-1 col-md-1">
                <v-switch v-model="subscription.enabled" color="green"></v-switch>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-lg-4 col-md-3 col-12"></div>
          <div class="col-lg-8 col-md-9 col-12">
            <v-btn @click="logout" color="red" class="w-100 mx-auto font-weight-bold"  height="50" outlined>
              Logout
            </v-btn>
          </div>
        </div>

      </div>
    </v-container>
    <div class="text-center ma-2">
        <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" style="bottom: 0;" >
          <v-avatar size="30px" class="me-3">
            <v-icon :color="snackbarColor">{{ snackbarIcon }}</v-icon>
          </v-avatar>
          <span class="white--text font-weight-bold">{{ snackbarMessage }}</span>
          <template v-slot:action="{ attrs }">
            <v-btn
              :color="snackbarColor"
              text
              v-bind="attrs"
              @click="snackbar = false"
            >
              <b>Close</b>
            </v-btn>
          </template>
        </v-snackbar>
      </div>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      snackbar:false,
      snackbarError:false,
      snackbarTimeout:2500,
      authenticated:false,
      AuthToken:null,
      snackbarMessage: '',
      snackbarColor: 'red',
      snackbarIcon: 'mdi-alert-circle',
      saving_amout:0,
      user: {
        name: null,
        newPassword:'',
        oldPassword:'',
        confimPassword:'',
        email: null
        // Add more user details as needed
      },
      subscriptions: [
        {
          name: 'Deal Alerts',
          description: 'You will get weekly notifications on your selected items. You choose what needs to be notified to your email',
  
        },
        {
          name: 'Potential Deals',
          description: 'Based on what you search and favorites, we will send you a weekly email of deals that we think suit you to your email',
        
        },
        {
          name: 'Mobile Alerts',
          description: 'Get Notified on your Mobile',

        },
        // Add more subscriptions as needed
      ],
      selectedSubscription: null,
      oldPassword: '',
      showOldPassword: false,
      oldPasswordRules: [
        (value) => {
          if (value?.length >= 8) return true;
          if (value?.length < 1) return 'Old Password is required'
          return 'Old Password needs to be at least 8 characters.';
        },
      ],
      newPassword: '',
      showNewPassword: false,
      newPasswordRules: [
        (value) => {
          if (value?.length >= 8) return true;
          if (value?.length < 1) return 'New Password is required'
          return 'New Password needs to be at least 8 characters.';
        },
      ],
      newConfirmPassword: '',
      showNewConfirmPassword: false,
      newConfirmPasswordRules: [
        (value) => {
          if (value?.length < 1) return 'New Confirm Password is required'
          if (this.newPassword == value) return true;
          return 'New passwords do not match.';
        },
      ]
    };
  },
  computed: {
  // Check if saving has a valid value
  amount() {
    return this.saving_amount
  },
},
  async beforeMount() {
      await this.TokenPromise();
    
    },
  methods : {
    closeNotification(id) {
      const index = this.notifications.findIndex((notification) => notification.id === id);
      if (index !== -1) {
        this.$set(this.notifications, index, { ...this.notifications[index], visible: false });
      }
    },
    async TokenPromise() {
      this.AuthToken = await this.getToken();
      this.verifyAuthProcess();
    },
    async logout() {
      await this.$store.commit('clearToken');
      location.href = "/";
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
    async changePassword() {
      if (this.$refs.changePassForm.validate()) {

        // Reset snackbar properties
        this.snackbar = false;
        this.snackbarMessage = '';
        this.snackbarColor = 'red';
        this.snackbarIcon = 'mdi-alert-circle';

        try {
          const response = await fetch(`${this.$GroceryAPI}/change-password`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${this.AuthToken}`
            },
            body: JSON.stringify({
              old_password: this.oldPassword,
              new_password: this.newPassword,
            }),
          });

          if (response.ok) {
            const responseData = await response.json();
            this.showSnackbar(responseData.message, 'green', 'mdi-check-circle');
            // Optionally, you can redirect or perform other actions on success
          } else {
            const errorData = await response.json();
            this.showSnackbar(errorData.detail, 'red', 'mdi-alert-circle');
            // Handle error, e.g., display an error message to the user
          }
        } catch (error) {
          this.showSnackbar('An unexpected error occurred.', 'red', 'mdi-alert-circle');
          // Handle error, e.g., display a generic error message to the user
        }
      }
    },
    showSnackbar(message, color, icon) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbarIcon = icon;
      this.snackbar = true;
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
              const data = await response.json()
              this.user.name = data.user
              this.user.email = data.email
              this.authenticated=true;
              await this.Saving()
              
            
          } else {
            console.error('Error:', response.statusText);
            this.$store.commit('clearToken');
            this.$router.push('/login');
            window.location.reload();
            
          }
        } catch (error) {
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
        }
      },
      async Saving() {
    
    try {
      const response = await fetch(`${this.$GroceryAPI}/retrieve_saving_user`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.AuthToken}`,
        },
      });

      if (response.ok) {
          const data = await response.json()
          this.saving_amount= data.amount
        
      } else {
        console.error('Error:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  }

  },
};
</script>

<style>
.notification-container {
  max-height: 300px; /* Set the maximum height for the container */
  overflow-y: auto;  /* Enable vertical scrolling */
}

/* Green Theme Styles */
.green-theme {
  background-color: #4CAF50; /* Green background color */
  color: white; /* White text color */
}

/* Profile Image Styles */
.profile-image {
  border-radius: 50%;
  width: 100%;
}

.box-border {
  border: 1px solid lightgray;
  border-radius: 5px;
  padding-left: 25px;
  padding-top: 25px;
  padding-bottom: 15px;
  box-shadow: 1px 1px 10px 0px lightgray;
}

</style>
