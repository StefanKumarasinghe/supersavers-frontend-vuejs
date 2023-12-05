<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-container fluid>
      <!-- User Information Section -->
      <div class="mx-3 mt-5">
        <h1>User Information</h1>
        <v-row fluid>
          <v-col cols="12" md="12">
            <v-card class="mb-3" flat>
              <v-card-title class="h5 mb-2">Personal Details</v-card-title>
              <v-card-text>
                <v-row fluid>
                  <v-col cols="12" md="4" lg="3">
                    <v-img :src="require('@/assets/profile-1.png')" alt="Profile Image" class="profile-image"></v-img>
                  </v-col>
                  <v-col cols="12" md="8" lg="9">
                    <v-list fluid>
                      <v-list-item>
                        <v-list-item-content>
                          <h2>HEY {{ user.name.toUpperCase() }}</h2>
                          <v-alert color="success my-2 font-weight-bold white--text"
                                   class="mx-0">This is your profile page, you can manage notifications, subscriptions and even account details</v-alert>
                        </v-list-item-content>
                      </v-list-item>

                      <!-- Annual Savings -->
                      <v-row class="mb-4">
                        <v-col>
                          <v-card>
                            <v-list-item>
                              <v-list-item-avatar>
                                <v-icon color="success">mdi-currency-usd</v-icon>
                              </v-list-item-avatar>
                              <v-list-item-content>
                                <h3>Annual Savings</h3>
                                <h2 class="my-2 text--green">AUD 30</h2>
                              </v-list-item-content>
                            </v-list-item>
                          </v-card>
                        </v-col>
                      </v-row>

                      <!-- Monthly Savings -->
                      <v-row class="mb-4">
                        <v-col>
                          <v-card>
                            <v-list-item>
                              <v-list-item-avatar>
                                <v-icon color="success">mdi-currency-usd</v-icon>
                              </v-list-item-avatar>
                              <v-list-item-content>
                                <h3>Monthly Savings</h3>
                                <h2 class="my-2 text--green">AUD 5</h2>
                              </v-list-item-content>
                            </v-list-item>
                          </v-card>
                        </v-col>
                      </v-row>

                 

                      <!-- Keep Saving -->
                      <v-row class="mb-4">
                        <v-col>
                          <v-card>
                            <v-list-item>
                              <v-list-item-content>
                                <v-row>
      <v-col  cols="12" md="12" class="font-weight-bold">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="h5">Monthly Subscription</v-list-item-title>
              <v-list-item-subtitle>3.99 AUD</v-list-item-subtitle>
              <v-list-item-subtitle>Next Renewal Date: 23/10/2024</v-list-item-subtitle>
              <v-list-item-subtitle>Membership Status: Active</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-card-actions>
           <v-card-text><v-btn color="success" class="font-weight-bold" >Manage</v-btn> <v-btn color="red" class="white--text font-weight-bold">End</v-btn></v-card-text> 
          </v-card-actions>
      </v-col>
    </v-row></v-list-item-content>
                            </v-list-item>
                          </v-card>
                        </v-col>
                      </v-row>

                    </v-list>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <!-- Additional content if needed -->
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

  

      <div class="mx-3 mt-5">
        <h1>Manage</h1>

        <v-card class="mb-3" flat>
          <v-row>
            <v-col cols="12" md="6">
              <v-card-title class="h5 mb-2">Notification Preferences</v-card-title>
              <v-list>
                <v-list-item-group v-model="selectedSubscriptions">
                  <v-list-item v-for="(subscription, index) in subscriptions" :key="index">
                    <v-list-item-action>
                      <v-switch v-model="subscription.enabled" color="primary"></v-switch>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title class="font-weight-bold">{{ subscription.name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ subscription.description }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
              <v-divider></v-divider>
            </v-col>

            <v-col cols="12" md="6">
              <v-container fluid>
    <v-card-title>Change Password</v-card-title>
    <v-form @submit.prevent="changePassword">
      <!-- Old Password Input -->
      <v-text-field
        v-model="oldPassword"
        label="Old Password"
        type="password"
        required
      ></v-text-field>

      <!-- New Password Input -->
      <v-text-field
        v-model="newPassword"
        label="New Password"
        type="password"
        required
      ></v-text-field>

      <!-- Confirm New Password Input -->
      <v-text-field
        v-model="confirmPassword"
        label="Confirm New Password"
        type="password"
        required
      ></v-text-field>

      <!-- Change Password Button -->
      <v-btn type="submit" color="primary">Change Password</v-btn>
    </v-form>
  </v-container>
            </v-col>
          </v-row>
        </v-card>
      </div>
    </v-container>
    <v-container class="mb-5">
    <v-row class="d-flex justify-center mb-5 align-center">
      <v-col cols="12" md="4">
        <!-- Logout Link -->
        <v-btn @click="logout" color="red" class="w-100 mx-auto" outlined>
          Logout
        </v-btn>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Cart Link -->
        <v-btn to="/cart" color="success " class="w-100" outlined>
          Cart
        </v-btn>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Notifications Link -->
        <v-btn to="/notification" color="primary" class="w-100" outlined>
          Notifications
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
  </v-app>
</template>
<style scoped>
.notification-container {
  max-height: 300px; /* Set the maximum height for the container */
  overflow-y: auto;  /* Enable vertical scrolling */
}
</style>
<script>
export default {
  data() {
    return {
      AuthToken:null,
      user: {
        name: null,
        email: null
        // Add more user details as needed
      },
      notifications: [
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
        {
          message: "Oreo is on Sale at Coles",
          visible: true,
        },
      ],
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
    };
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
    async VerifyAuth() {
      const response = await fetch(`${this.$GroceryAPI}/verified`, {
             method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          if (!(response.ok)) {
            console.error('Error:', response.statusText);
            this.$router.push('/verify');
          }
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
              await this.VerifyAuth();
            
          } else {
            console.error('Error:', response.statusText);
            this.$router.push('/login');
          }
        } catch (error) {
          console.error('Error:', error);
          this.$router.push('/login');
        }
      }
  },
};
</script>

<style scoped>
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

/* Add your custom styles here */
</style>
