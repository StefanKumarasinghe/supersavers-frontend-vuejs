<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app v-show="authenticated">
      <v-container fluid>
        <!-- Back Button -->
        <v-col cols="12" lg="1" align-self="center">
          <v-btn elevation="0" color="" class="bg-success text-white text-center font-weight-bold"  to="account" flat>
            <v-icon>mdi-keyboard-backspace</v-icon> Back
          </v-btn>
        </v-col>
       
      <div v-if="membership">
        <v-row class="text-center pt-5">
          <v-col cols="11" lg="11">
            <h3 class="font-weight-bold">Manage your subscription</h3>
            <p>You can cancel, resume or even change your credit card details</p>
          </v-col>
        </v-row>
        <v-row>
        <v-col
            cols="12"
            lg="6"
            md="12"
            class="d-flex justify-center"
          >
            <v-col
              cols="12"
              lg="12"
              md="6"
              sm="6"
              class="box-border me-lg-5 me-0"
            
            >
    <h2>Subscription Details</h2>
    <div class="fw-bold" v-if="meta.status == 'active'">
      <p><strong>Status:</strong> <span class="text-success">Active</span></p>
      <p><strong>Price:</strong> ${{ meta.price }}</p>
      <p><strong>Next Billing Date:</strong> {{ formatDate(meta.next_billing_date) }}</p>
      <p><strong>Subscription Created At:</strong> {{ formatDate(meta.created_at) }}</p>
    </div>
</v-col>
</v-col>
<v-col
            cols="12"
            lg="6"
            md="12"
            class="d-flex justify-center"
          >
            <v-col
              cols="12"
              lg="12"
              md="6"
              sm="6"
              class="box-border me-lg-5 me-0"
            
            >
    <h2>Manage subscriptions</h2>
    <div v-if="meta.status == 'active'">
      <div v-if="!meta.canceled_at">
      <div class="p-3  fw-bold bg-light">You can cancel anytime you want, and don't worry. You will be able to use the app until your billing period is over</div>
      <button  class="btn p-3 bg-danger my-3 text-white fw-bold" @click="cancelSubscription">Cancel</button>
      </div>
      <div v-if="canResume">
      <div class="p-3  fw-bold bg-light">You must resume before the billing date or you will automatically need to create a new subscription. If any issues occur, please contact support</div>
      <button class="btn p-3 bg-success my-3 text-white fw-bold" @click="resumeSubscription">Resume</button>
      </div>
    </div>

<div v-else>
  <p class="fw-bold">Want to resume?</p>
  <p><strong>Reason:</strong> {{ meta.canceled_at ? 'Canceled' : 'Not yet active' }}</p>
</div>

  

</v-col>
</v-col>
</v-row>
<div class="bg-light  p-3 my-2 fw-bold">Supersavers does not save any card details, we use Stripe to securely process transactions. Your latest card will be used for billing. If you want to change your card details before your subscription ends, contact billing@supersavers.au</div>

</div>


<div v-else>
        <!-- Title and Description -->
        <v-row class="text-center pt-5">
          <v-col cols="11" lg="11">
            <h3 class="font-weight-bold">Complete your Payment</h3>
            <p>Select the best type based on your needs</p>
          </v-col>
        </v-row>
  
        <!-- Payment Options with Radio Effect -->
        <v-row>
          <!-- Monthly Payment Option -->
          <div class="bg-success text-white p-3 my-2 fw-bold">Please choose a plan before you continue with your card details. For more details, of privacy and subscription policy, please visit here</div>
          <v-col
            cols="12"
            lg="6"
            md="12"
            class="d-flex justify-center"
          >
            <v-col
              cols="12"
              lg="12"
              md="6"
              sm="6"
              class="box-border me-lg-5 me-0"
              @click="selectPaymentOption('monthly')"
              :class="{ 'box-shadow-blue': row === 'monthly' }"
            >
              <h5 class="green--text font-weight-bold">Monthly payment</h5>
              <h5 class="font-weight-bold pt-4">$ AUD 4</h5>
              <p class="font-weight-bold">per month</p>
              <div class="py-1">
                <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon> Access to everything
              </div>
              <div class="py-1">
                <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon> Best for starters
              </div>
            </v-col>
          </v-col>
  
          <!-- Yearly Payment Option -->
          <v-col
            cols="12"
            lg="6"
            md="12"
            class="d-flex justify-center"
          >
            <v-col
              cols="12"
              lg="12"
              md="6"
              sm="6"
              class="box-border me-lg-5 me-0"
              @click="selectPaymentOption('yearly')"
              :class="{ 'box-shadow-blue': row === 'yearly' }"
            >
              <h5 class="green--text font-weight-bold">Yearly payment</h5>
              <h5 class="font-weight-bold pt-4">$ AUD 35</h5>
              <p class="font-weight-bold">per year</p>
              <div class="py-1">
                <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon> Access to everything
              </div>
              <div class="py-1">
                <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon> Save AUD 13 and stay committed
              </div>
            </v-col>
          </v-col>
           <!-- Card Details Section -->
         
        </v-row>
        <div class="bg-warning  p-3 my-2 fw-bold">Note you will be charged based on the package chosen. You can cancel anytime</div>
         
        <v-col cols="12" lg="6" class="mx-0 box px-0 mx-auto" md="12" sm="12">
        <v-card class="p-2 elevation-0">
          <v-card-title class="fw-bold text-success">Card Details</v-card-title>
          <v-card-text>
            <div id="card-element" class="my-4"></div>
            <v-spacer></v-spacer>
            <v-btn class="mt-4 bg-success text-white p-3" @click="submitPayment">Subscribe</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
       </div>
      <Toast ref="Toast" />

      </v-container>
    
    

    
    </v-app>
  </template>
  
  <script>
  import { loadStripe } from '@stripe/stripe-js';
  import Toast from './components/Toast.vue';

export default {
  metaInfo: {
  // Page Title
  title: 'Supersavers | My Subscription',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Manage your Supersavers subscription and unlock exclusive features. Subscribe to maximize your savings on groceries with real-time price comparisons across Woolworths, Coles, and IGA.' }, // Page description
    { name: 'keywords', content: 'Supersavers, subscription management, subscribe, save on groceries, exclusive features, Woolworths, Coles, IGA' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Subscription Management' }, // Open Graph title
    { property: 'og:description', content: 'Manage your Supersavers subscription and unlock exclusive features. Subscribe to maximize your savings on groceries with real-time price comparisons across Woolworths, Coles, and IGA.' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/subscription' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Subscription Management' }, // Twitter title
    { name: 'twitter:description', content: 'Manage your Supersavers subscription and unlock exclusive features. Subscribe to maximize your savings on groceries with real-time price comparisons across Woolworths, Coles, and IGA.' }, // Twitter description
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
        row: "monthly",
        stripe: null,
        elements: null,
        card: null,
        meta: Object,
        membership:false,
      };
    },
    computed: {
        canResume() {
    // Add logic to determine if the user can resume
    // For example, check if the subscription is canceled
    if (this.meta.canceled_at) {
    const currentDateInSeconds = Math.floor(Date.now() / 1000);
    return currentDateInSeconds < this.meta.next_billing_date;
    }else{return false}
},
  },

     
    
    async beforeMount() {
      
      try {
        await Promise.all([
            this.TokenPromise(),
            
        ]);
        } catch (error) {
            console.error('Error:', error);
        }
    },
    methods: {
    async cancelSubscription() {
    try {
        const response = await fetch(`${this.$GroceryAPI}/cancel_subscription`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });

        if (!response.ok) {
        console.error('Error:', response.statusText);
        this.$refs.Toast.showSnackbar('Could not validate the token', 'red', 'mdi-alert-circle');
        } else {
        // Use await to get the actual data from the response
        this.$refs.Toast.showSnackbar('Cancelled your subscription, your subscription is valid until your billing duration', 'green', 'mdi-check-circle');
        await this.subscription_meta()
        }
    } catch (error) {
        console.error('Something went wrong with cancelling you subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong', 'red', 'mdi-alert-circle');
    }
    },
    async resumeSubscription() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/resume_subscription`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });

        if (!response.ok) {
        console.error('Error:', response.statusText);
        this.$refs.Toast.showSnackbar('Could not resume your subscription. Please contact support', 'red', 'mdi-alert-circle');
        } else {
        // Use await to get the actual data from the response
        this.$refs.Toast.showSnackbar('Resumed your subscription, your subscription will continue and you will be charged as normal', 'green', 'mdi-check-circle');
        await this.subscription_meta()
        }
    } catch (error) {
        console.error('Something went wrong with resuming you subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong', 'red', 'mdi-alert-circle');
    }
    },
    async TokenPromise() {
      this.AuthToken = await this.getToken();
      await this.verifyAuthProcess();
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
    async SubscriptionCheck() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/valid_subscription`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });

        if (!response.ok) {
        console.log("No Subscription") 
      } else {
        await this.subscription_meta();
      }
    } catch (error) {
        console.error('Something went wrong with verifying your subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong when accessing our server', 'red', 'mdi-alert-circle');
    }
    },
    async VerifyAuth() {
      try {
          const response = await fetch(`${this.$GroceryAPI}/verified`, {
              method: 'GET',
              headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
              },
            });
            if (!(response.ok)) {
              console.error('Error:', response.statusText);
              this.$router.push('/verify');
            }else {
              this.initializeStripe();
              await this.subscription_meta();
              await this.SubscriptionCheck()
            }
          } catch (error) {
          console.error('Something went wrong with verification', error);
          this.$refs.Toast.showSnackbar('Something went wrong', 'red', 'mdi-alert-circle');
        }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp * 1000);
      return date.toLocaleDateString(); // Adjust date formatting as needed
    },
    async subscription_meta() {
    try {
        const response = await fetch(`${this.$GroceryAPI}/subscription/meta`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });

        if (!response.ok) {
        console.error('Error:', response.statusText);
        this.$refs.Toast.showSnackbar('Could not validate the token', 'red', 'mdi-alert-circle');
        } else {
        // Use await to get the actual data from the response
        this.meta = await response.json();
        if (this.meta) {
        this.membership = (this.meta.status == 'active') }
        this.authenticated=true
        }
    } catch (error) {
        console.error('Something went wrong with verification', error);
        this.$refs.Toast.showSnackbar('Something went wrong', 'red', 'mdi-alert-circle');
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
              await this.VerifyAuth();
              
          } else {
            console.error('Error:', response.statusText);
            this.$store.commit('clearToken');
            this.$router.push('/login');
            window.location.reload();
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('Session was invalidated', 'red', 'mdi-alert-circle');
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
        }
      },
      async initializeStripe() {
        
        
        // Load Stripe.js asynchronously
        const stripe = await loadStripe('pk_test_51OKXuWGNjAGfAcEWlb7wlHl8TnbYrWhE2LsMc17YtOCxgtVr0sg9GZ9QieVYKSc7TdWrJorsE5YJmkHHUI011pEl00pq9OamFc');
        const elements = stripe.elements();
  
        // Create an instance of the card Element
        const card = elements.create('card', {
    hidePostalCode: true, // Exclude the postal code field
  });
  
        // Mount the card Element to the card-element div
        card.mount('#card-element');
  
        this.stripe = stripe;
        this.elements = elements;
        this.card = card;
      },
      async submitPayment() {
        // Create a PaymentMethod using the card Element
        this.$refs.Toast.showSnackbar('Processing, please do not reload or press the button again', 'yellow', 'mdi-alert-circle');
        const { token, error } = await this.stripe.createToken(this.card);
  
        if (error) {
          console.error(error);
          // Handle error (e.g., display error message)
        } else {
          // Send the token and product details to your server to create a PaymentIntent
          await this.handlePaymentIntentCreation(token.id, this.row);
        }
      },
      async handlePaymentIntentCreation(token, selectedProduct) {
        try {
          // Replace with your server-side endpoint to create a PaymentIntent
          const response = await fetch(`${this.$GroceryAPI}/subscription`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
               Authorization: `Bearer ${this.AuthToken}`,
            },
            body: JSON.stringify({
              token,
              product: selectedProduct, // Include the selected product in the request
            }),
          });
  
          if (!response.ok) {
            this.$refs.Toast.showSnackbar('Unable to process the payment', 'red', 'mdi-alert-circle');
            console.error('Server-side error:', response.statusText);
          } else {
            // Payment succeeded, handle success (e.g., redirect, show success message)
            this.$refs.Toast.showSnackbar('Payment processed, successfully redirecting you to supersavers', 'green', 'mdi-check-circle');
            new Promise(resolve => setTimeout(resolve, 2000));
            console.log('Payment succeeded:', await response.json());
            this.$router.push('/search');

          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
      selectPaymentOption(value) {
        this.row = value;
      },
    },
  };
  </script>
  
  <style scoped>
  .box-border {
    border: 4px solid black;
    border-radius: 5px;
    padding: 25px;
    cursor: pointer;
    transition: box-shadow 0.3s ease-in-out;
  }
  
  .box {
    border: 4px solid black;
    border-radius: 20px 0 20px 0;
  }
  .box-shadow-blue {
    box-shadow: 0 4px 20px rgb(0, 204, 14);
  }
  </style>
  