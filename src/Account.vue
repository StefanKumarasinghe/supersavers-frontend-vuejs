<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
    <v-container fluid>
      <!-- User Information Section -->
      <div class="mx-3">
        <h1 class="fw-bold">Account</h1>
        <v-alert
          border="left"
          colored-border
          type="info"
          elevation="2"
          color="green"
          prominent
          class="mt-5"
          width="auto"
        >
          <h3>Hey, {{ user.name }}</h3>
          This is your profile page, you can manage notifications, subscriptions
          and even account details.
        </v-alert>
        <v-row fluid>
          <v-col
            v-if="$vuetify.breakpoint.mdAndUp"
            cols="12"
            md="4"
            lg="3"
            align-self="center"
          >
            <v-img
              :src="require('@/assets/profile-1.png')"
              alt="Profile Image"
              class="profile-image"
            ></v-img>
          </v-col>
          <v-col cols="12" md="8" lg="9">
            <!-- Keep Saving -->
            <div class="black--text p-3 my-5 mx-auto w-100 text-center">
              <v-row class="text-center">
                <h5 class="font-weight-bold">Monthly Subscription</h5>
              </v-row>
              <v-row class="text-center" v-if="active || submessage =='Free Trial'">
                <h4 class="green--text font-weight-bold"><v-span v-if="submessage =='Free Trial'">7 Day </v-span>{{ submessage }}</h4>

                <a href="/subscription" class="btn text-white py-2 my-2 btn-success fw-bold">Manage</a>
              </v-row>
              <v-row class="text-center" v-else>
                <h4 class="red--text font-weight-bold">Inactive</h4>

                <a href="/subscription" class="btn text-white py-2 my-2 btn-success fw-bold">Manage</a>
              </v-row>
            </div>
            <div class="text-black box-border my-5 pe-5 pb-5 text-center">
              <v-row class="text-center align-center">
                <!-- Added align-center class -->
                <h5 class="font-weight-bold">Monthly Savings</h5>
                <h2 class="green--text display-5" v-if="amount_saved">
                  ${{ amount_saved }}
                </h2>
                <v-btn
                  color="fw-bold success mt-4"
                  @click="shareApp()"
                  height="60"
                  >Share this to your friends</v-btn
                >
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
              <div class="row font-weight-bold">Old Password:</div>
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
              <div class="row font-weight-bold">New Password:</div>
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
              <div class="row font-weight-bold">New Confirm Password:</div>
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
                <v-btn
                  color="green font-weight-bold white--text"
                  @click="changePassword()"
                  height="50"
                  >Change password</v-btn
                >
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
            <div
              class="row"
              :v-model="selectedSubscriptions"
              v-for="(subscription, index) in subscriptions"
              :key="index"
            >
              <div class="col-10 col-lg-11 col-md-11">
                <div class="font-weight-bold">{{subscription.name}}</div>
                <div>{{subscription.description}}</div>
              </div>
              <div class="col-2 col-lg-1 col-md-1">
                <v-switch
                  @click ="enableMobileAlerts()"
                  v-model="mobile"
                  color="green"
                ></v-switch>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-lg-4 col-md-3 col-12"></div>
          <div class="col-lg-8 col-md-9 col-12">
            <v-btn
              @click="logout"
              color="red"
              class="w-100 mx-auto font-weight-bold"
              height="50"
              outlined
            >
              Logout
            </v-btn>
          </div>
        </div>
        <Toast ref="Toast" />
      </div>
    </v-container>
  </v-app>
</template>

<script>
import Toast from './components/Toast.vue';

export default {
  metaInfo: {
  // Page Title
  title: 'Supersavers | My Supersavers',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Manage your Supersavers account. Update subscriptions, change passwords, and customize notifications to enhance your grocery savings experience. Compare prices across Woolworths, Coles, and IGA.' }, // Page description
    { name: 'keywords', content: 'Supersavers, my account, manage subscriptions, change password, customize notifications, grocery savings, Woolworths, Coles, IGA' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | My Account' }, // Open Graph title
    { property: 'og:description', content: 'Manage your Supersavers account. Update subscriptions, change passwords, and customize notifications to enhance your grocery savings experience. Compare prices across Woolworths, Coles, and IGA.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/my-account' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | My Account' }, // Twitter title
    { name: 'twitter:description', content: 'Manage your Supersavers account. Update subscriptions, change passwords, and customize notifications to enhance your grocery savings experience. Compare prices across Woolworths, Coles, and IGA.' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

  components: {
    Toast
  },
  data() {
    return {
      authenticated:false,
      AuthToken:null,
      amount_saved:0,
      mobile: false,
      active:null,
      submessage:"FREE TRIAL",
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
          name: 'Mobile Alerts',
          description: 'Get Notified on your Mobile',
          
        },
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
  async beforeMount() {
    await this.TokenPromise();
    await this.enableMobileAlerts();
  },
  methods : {
    async SubscriptionCheck() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/valid_subscription`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });
        
        if (response.ok) {
        const r = await response.json();
        const startTrialDate = new Date(r.start_trial);
        const currentDate = new Date();

        // Calculate the difference in milliseconds between the current date and start_trial date
        const timeDifference = currentDate - startTrialDate;

        // Calculate the difference in days
        const daysDifference = timeDifference / (1000 * 3600 * 24);

        if (daysDifference <= 7) {
            // If current date is within 7 days after start_trial, display free trial message
            this.submessage = "Free Trial";
        } else {
            // If not, display active subscription message
            this.submessage = "Active Subscription";
        }

        this.active = r.active;
    }

    } catch (error) {
        console.error('Something went wrong with verifying your subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong when accessing our server', 'red', 'mdi-alert-circle');
    }
    },
    async enableMobileAlerts() {
      if (!("Notification" in window)) {
        console.error("This browser does not support desktop notification");
        this.$refs.Toast.showSnackbar('it seems as your device does not allow notifications', 'red', 'mdi-alert-circle');
        return;
      }
      if (Notification.permission === "granted") {
        this.mobile = true;
        this.$refs.Toast.showSnackbar('Notifications are enabled. You are now able to add items to your wishlist. To disable, please go to your app settings and disable notifications', 'green', 'mdi-check-circle');
       
      } else if (Notification.permission !== "denied") {
        this.mobile = false;
        this.$refs.Toast.showSnackbar('Permissions denied', 'red', 'mdi-alert-circle');
        Notification.requestPermission().then((permission) => {
          if (permission === "granted") {
            this.$refs.Toast.showSnackbar('Notififications are enabled. You are now able to add to your wishlist', 'green', 'mdi-check-circle');
          }
        });
      }
    },
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
      this.$store.commit('clearToken');
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
            this.$refs.Toast.showSnackbar('Success: '+responseData.message, 'green', 'mdi-check-circle');
          } else {
            const errorData = await response.json();
            this.$refs.Toast.showSnackbar('Error: '+errorData.detail, 'red', 'mdi-alert-circle');
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('An unexpected error occurred.', 'red', 'mdi-alert-circle');
        }
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
            this.user.email = data.email
            this.authenticated=true;
            await this.Saving()
            await this.SubscriptionCheck()
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
    shareApp() {
      if (navigator.share) {
        navigator
          .share({
            title: `🌟 Hey, I've saved $${this.amount_saved} using supersavers! 💰`,
            text: `🚀 Hey, I've saved $${this.amount_saved} using supersavers! 💰. You too can save heaps at Coles, Woolies, and IGA with supersavers by never missing out on deals. Visit (https://supersavers.au) 🌐`,
          })
          .then(() => this.$refs.Toast.showSnackbar('Shared Successfully', 'green', 'mdi-check-circle'))
          .catch(() => this.$refs.Toast.showSnackbar('Sorry, it was not shared successfully', 'red', 'mdi-alert-circle'));
      } else {
        this.$refs.Toast.showSnackbar('Sadly, you canceled your message', 'red', 'mdi-alert-circle')
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
            this.amount_saved= data.amount

        } else {
          this.$refs.Toast.showSnackbar('Could not retrieve your monthly savings', 'red', 'mdi-alert-circle')
        }
      } catch (error) {
        this.$refs.Toast.showSnackbar('Something went wrong with retrieving your savings', 'red', 'mdi-alert-circle')
      }
    }
  },
};
</script>

<style>
.notification-container {
  max-height: 300px;
  overflow-y: auto;
}

.green-theme {
  background-color: #4caf50;
  color: white;
}

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
