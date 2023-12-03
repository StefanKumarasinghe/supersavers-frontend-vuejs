<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-container fluid>
      <!-- User Information Section -->
      <div class="mx-3 mt-5">
        <h2>
          SETTINGS
        </h2>
        <v-alert border="left" colored-border type="info" elevation="2" color="green" prominent class="mt-5" width="auto">
          This is your profile page, you can manage notifications, subscriptions and even account details.
        </v-alert>

        <v-card flat>
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
                    </v-list-item-content>
                  </v-list-item>

                  <!-- Annual Savings -->
                  <v-card>
                    <v-list-item>
                      <v-list-item-avatar>
                        <v-icon color="success">mdi-currency-usd</v-icon>
                      </v-list-item-avatar>
                      <v-list-item-content>
                        <h4>Annual Savings</h4>
                        <h3 class="my-2 text--green">AUD 30</h3>
                      </v-list-item-content>
                    </v-list-item>
                  </v-card>

                  <!-- Monthly Savings -->
                  <v-card>
                    <v-list-item>
                      <v-list-item-avatar>
                        <v-icon color="success">mdi-currency-usd</v-icon>
                      </v-list-item-avatar>
                      <v-list-item-content>
                        <h4>Monthly Savings</h4>
                        <h3 class="my-2 text--green">AUD 5</h3>
                      </v-list-item-content>
                    </v-list-item>
                  </v-card>

                  <!-- Keep Saving -->
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
        <v-divider :thickness="12" color="black"></v-divider>

        <!-- Personal information -->
        <div class="row">
          <div class="col-lg-4 col-md-3 col-12">
            <h5 class="font-weight-bold">
            <v-icon color="black">mdi-account-box</v-icon> Personal information
            </h5>
          </div>
          <div class="col-lg-8 col-md-9 col-12">
            <div class="row font-weight-bold">
              Display Name:
            </div>
            <div class="row">
              <v-text-field
                single-line
                outlined
                v-model="user.name"
              ></v-text-field>
            </div>
            <div class="row font-weight-bold">
              Email Address:
            </div>
            <div class="row">
              <v-text-field
                single-line
                outlined
                v-model="user.email"
              ></v-text-field>
            </div>
          </div>
        </div>
        <v-divider :thickness="12" color="black"></v-divider>

        <!-- Change password -->
        <div class="row">
          <div class="col-lg-4 col-md-3 col-12">
            <h5 class="font-weight-bold">
            <v-icon color="black">mdi-shield-account</v-icon> Change Password
            </h5>
          </div>
          <div class="col-lg-8 col-md-9 col-12">
            <div class="row font-weight-bold">
              Old Password:
            </div>
            <div class="row">
              <v-text-field
                single-line
                outlined
                type="password"
              ></v-text-field>
            </div>
            <div class="row font-weight-bold">
              New Password:
            </div>
            <div class="row">
              <v-text-field
                single-line
                outlined
                type="password"
              ></v-text-field>
            </div>
            <div class="row font-weight-bold">
              Confirm New Password:
            </div>
            <div class="row">
              <v-text-field
                single-line
                outlined
                type="password"
              ></v-text-field>
            </div>
            <div class="row">
              <v-btn color="green font-weight-bold white--text" height="50">Change password</v-btn>
            </div>
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

        <v-row class="d-flex justify-center mb-5 align-center">
          <v-col cols="12" md="6">
            <!-- Logout Link -->
            <v-btn @click="logout" color="red" class="w-100 mx-auto font-weight-bold" height="50" outlined>
              Logout
            </v-btn>
          </v-col>

          <v-col cols="12" md="6">
            <!-- Cart Link -->
            <v-btn to="/cart" color="success" class="w-100 font-weight-bold" height="50">
              update
            </v-btn>
          </v-col>
        </v-row>
      </div>
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
      const response = await fetch('http://127.0.0.1:8000/verified', {
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
          const response = await fetch('http://127.0.0.1:8000/protected', {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });

          if (response.ok) {
              const data = await response.json()
              this.user.name = data.user
              this.user.email = data.email
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
</style>
