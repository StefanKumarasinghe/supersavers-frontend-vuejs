<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
      <v-container fluid>
        <!-- User Information Section -->
        <!-- ... (your existing code) -->
  
        <!-- Stripe Payment Section -->
        <div class="mx-3 mt-5">
          <h2>Payment Details</h2>
          <v-divider :thickness="12" color="black"></v-divider>
  
          <!-- Stripe Payment Form -->
          <div class="row">
            <div class="col-lg-12 col-md-12 col-12">
              <h5 class="font-weight-bold">
                <v-icon color="black">mdi-credit-card</v-icon> Payment Information
              </h5>
            </div>
            <div class="col-lg-12 col-md-12 col-12">
              <!-- Styled credit card element -->
              <div id="card-element" class="credit-card"></div>
  
              <!-- Display any errors that occur during submission -->
              <div id="card-errors" class="error" role="alert"></div>
  
              <!-- Button to submit the form -->
              <v-btn @click="handlePayment" color="blue" class="w-100 mx-auto font-weight-bold" height="50" outlined>
                Pay Now
              </v-btn>
            </div>
          </div>
  
          <v-divider :thickness="12" color="black"></v-divider>
  
          <!-- Change Card Details Section -->
          <v-container v-if="isSubscribed" class="row mt-5">
            <div class="col-lg-4 col-md-3 col-12">
              <h5 class="font-weight-bold">
                <v-icon color="black">mdi-credit-card-plus</v-icon> Change Card Details
              </h5>
            </div>
            <div class="col-lg-8 col-md-9 col-12">
              <!-- Form for updating card details -->
              <!-- Add necessary fields and logic for updating card details -->
              <v-btn color="orange" class="w-100 mx-auto font-weight-bold" height="50" outlined>
                Update Card Details
              </v-btn>
            </div>
          </v-container>
  
          <v-divider :thickness="12" color="black"></v-divider>
  
          <!-- Subscription Management Section -->
          <div class="row mt-5">
            <div class="col-lg-4 col-md-3 col-12">
              <h5 class="font-weight-bold">
                <v-icon color="black">mdi-cash-usd</v-icon> Subscription Management
              </h5>
            </div>
            <div class="col-lg-12 col-md-12 col-12">
              <!-- Logic to handle subscription actions -->
              <v-btn v-if="!isSubscribed" @click="subscribeMonthly" color="blue" class="w-100 mx-auto font-weight-bold" height="50" outlined>
                Subscribe Monthly ($2.99/month)
              </v-btn>
              <v-btn v-if="!isSubscribed" @click="subscribeYearly" color="blue" class="w-100 mx-auto mt-3 font-weight-bold" height="50" outlined>
                Subscribe Yearly ($19.99/year)
              </v-btn>
              <v-btn v-if="isSubscribed" @click="deactivateSubscription" color="red" class="w-100 mx-auto font-weight-bold" height="50" outlined>
                Deactivate Subscription
              </v-btn>
              <v-btn v-if="isSubscribed" @click="resumeSubscription" color="green" class="w-100 mx-auto mt-3 font-weight-bold" height="50" outlined>
                Resume Subscription
              </v-btn>
            </div>
          </div>
        </div>
      </v-container>
    </v-app>
  </template>
  
  <script>
  import { loadStripe } from '@stripe/stripe-js';
  
  export default {
    data() {
      return {
        card: null,
        isSubscribed: false, // Replace with logic to check user's subscription status
      };
    },
  
    async mounted() {
      const stripe = await loadStripe('YOUR_PUBLISHABLE_KEY');
      const elements = stripe.elements();
  
      // Create an instance of the card Element.
      this.card = elements.create('card');
  
      // Add an instance of the card Element into the `card-element` div.
      this.card.mount('#card-element');
    },
  
    methods: {
      async handlePayment() {
        const stripe = await loadStripe('YOUR_PUBLISHABLE_KEY');
        const result = await stripe.confirmCardPayment('YOUR_SECRET_KEY', {
          payment_method: {
            card: this.card,
          },
        });
  
        if (result.error) {
          // Display error to your user.
          const errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
        } else {
          // The payment has been processed!
          if (result.paymentIntent.status === 'succeeded') {
            // Handle successful payment and update your server/database accordingly.
            console.log('Payment succeeded:', result.paymentIntent);
            this.isSubscribed = true; // Update subscription status
          }
        }
      },
  
      subscribeMonthly() {
        // Logic to subscribe the user monthly
        console.log('Subscribed Monthly');
        this.isSubscribed = true; // Update subscription status
      },
  
      subscribeYearly() {
        // Logic to subscribe the user yearly
        console.log('Subscribed Yearly');
        this.isSubscribed = true; // Update subscription status
      },
  
      deactivateSubscription() {
        // Logic to deactivate the subscription
        console.log('Deactivated Subscription');
        this.isSubscribed = false; // Update subscription status
      },
  
      resumeSubscription() {
        // Logic to resume the subscription
        console.log('Resumed Subscription');
        this.isSubscribed = true; // Update subscription status
      },
    },
  };
  </script>
  
  <style scoped>
  .credit-card {
    width: 100%;
    padding: 20px;
    background-color: #ffd700; /* Yellow background color */
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.1);
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  