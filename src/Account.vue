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
                      <v-alert colored-border type="info" elevation="2" color="red" prominent class="mt-5" width="auto">
          Supersavers will only be free until it is tested. You are using a testing version
        </v-alert>

              </v-row>
              <v-row class="text-center">
               
                <p><b>Next Renewal Date:</b> N/A</p>
                <p><b>Membership Status:</b> BETA</p>
              </v-row>
              <v-btn color="success" class="font-weight-bold text-center" to="">Manage</v-btn> 
            </div>
            <div class="text-black box-border my-5 pe-5 pb-5 text-center">
              <v-row class="text-center align-center"> <!-- Added align-center class -->
                <h5 class="font-weight-bold">Monthly Savings</h5>
                <h4 class="green--text font-weight-bold">$ AUD {{ saving }}</h4>
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
            <v-btn @click="logout" color="red" class="w-100 mx-auto font-weight-bold"  height="50" outlined>
              Logout
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
      authenticated:false,
      AuthToken:null,
      user: {
        name: null,
        saving:0,
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
    };
  },
  async beforeMount() {
      await this.TokenPromise();
      await this.Saving();
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
          this.saving= data
        
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

.box-border {
  border: 1px solid lightgray;
  border-radius: 5px;
  padding-left: 25px;
  padding-top: 25px;
  padding-bottom: 15px;
  box-shadow: 1px 1px 10px 0px lightgray;
}

</style>
