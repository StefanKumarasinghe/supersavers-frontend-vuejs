<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-container fluid>
      <!-- User Information Section -->
      <div class="mx-3 mt-5">
        <h1>User Information</h1>
        <v-row>
          <v-col cols="12" md="6">
            <v-card class="mb-3" flat>
              <v-card-title class="h5 mb-2">Personal Details</v-card-title>
              <v-card-text>
                <v-row>
                  <v-col cols="12" sm="4">
                    <v-img :src="require('@/assets/profile-1.png')" alt="Profile Image" class="profile-image"></v-img>
                  </v-col>
                  <v-col cols="12" sm="8">
                    <v-list>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title class="font-weight-bold">Name:</v-list-item-title>
                          <v-list-item-subtitle>{{ user.name }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>
                          <v-list-item-title class="font-weight-bold">Email:</v-list-item-title>
                          <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                      <!-- Add more user details as needed -->
                    </v-list>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <!-- Subscriptions Section -->
      <div class="mx-3 mt-5">
        <h1>Subscriptions</h1>
        <v-row>
          <v-col cols="12" md="6">
            <v-card class="mb-3" flat>
              <v-card-title class="h5 mb-2">Notification Preferences</v-card-title>
              <v-card-text>
                <v-list-group v-model="selectedSubscription">
                    <v-list-item-group>
                        <v-list-item v-for="(subscription, index) in subscriptions" :key="index">
                            <v-list-item-content>
                                <v-list-item-title class="font-weight-bold">{{ subscription.name }}</v-list-item-title>
                                <v-list-item-subtitle>{{ subscription.description }} ({{ subscription.monthlyPayment }}/mo)</v-list-item-subtitle>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list-group>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </div>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      user: {
        name: 'John Doe',
        email: 'john.doe@example.com'
        // Add more user details as needed
      },
      subscriptions: [
        {
          name: 'Deal Alerts',
          description: 'Receive notifications for the best deals.',
          monthlyPayment: 5,
        },
        {
          name: 'Premium Membership',
          description: 'Unlock exclusive deals and offers.',
          monthlyPayment: 10,
        },
        // Add more subscriptions as needed
      ],
      selectedSubscription: null,
    };
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
