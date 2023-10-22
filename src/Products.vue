<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <!-- Navigation Drawer for Grocery List -->

    
    <!-- Top App Bar -->
    <v-app-bar app clipped-left color="green darken-2" dark dense>
      <v-toolbar-title class="pa-3">Alpha</v-toolbar-title>

      <v-spacer></v-spacer>
      
      <!-- Search Bar -->
      <v-text-field class="mx-2" v-model="groceryItem" label="Search for an item" hide-details single-line outlined dense></v-text-field>
      
      <!-- Notification Icon with Dropdown -->
      <v-menu offset-y dense>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-badge>
              <template v-slot:badge><span>{{ notifications.length }}</span></template>
              <v-icon>mdi-bell</v-icon>
            </v-badge>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item v-for="notification in notifications" :key="notification.id">
            <v-list-item-content>
              {{ notification.message }}
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
      
      <!-- Login Account Icon with Dropdown -->
      <v-menu offset-y dense>
        <template v-slot:activator="{ on, attrs }">
          <v-btn icon v-bind="attrs" v-on="on">
            <v-icon>mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list dense>
          <v-list-item @click="login()">
            <v-list-item-content>
              Login
            </v-list-item-content>
          </v-list-item>
          <v-list-item @click="register()">
            <v-list-item-content>
              Register
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>



<v-main>
        <v-container fluid>
            <!-- Product Details -->
            <v-col class=" px-3">
                <v-row align="center">
                    <v-col cols="12" md="6">
                    <LineGraph :chartData="lineChartData" :options="lineChartOptions" />
                    

      </v-col>
                    <v-col cols="12" md="6" class="pl-md-5">
                        <v-card-title class="headline mb-2">{{ product.name }}</v-card-title>
                        <v-row align="center" class="my-3">
                            <v-col cols="4">
                                <v-chip outlined color="green" class="text-uppercase">Woolworths: ${{ product.stores.Woolies }}</v-chip>
                            </v-col>
                            <v-col cols="4">
                                <v-chip outlined color="red" class="text-uppercase">Coles: ${{ product.stores.Coles }}</v-chip>
                            </v-col>
                            <v-col cols="4">
                                <v-chip outlined color="blue" class="text-uppercase">Aldi: ${{ product.stores.Aldi }}</v-chip>
                            </v-col>
                        </v-row>
                        <!-- Graph for past prices -->
                       

                        <!-- User price update and voting -->
                        <v-row class="mt-4">
                            <v-col cols="8">
                                <v-text-field prepend-icon="mdi-cash" label="Update Price" v-model="updatedPrice" class="mr-3"></v-text-field>
                            </v-col>
                            <v-col cols="4" class="d-flex justify-center">
                                <v-btn icon color="green" @click="upvote" class="mr-1"><v-icon>mdi-thumb-up</v-icon></v-btn>
                                <v-btn icon color="red" @click="downvote" class="ml-1"><v-icon>mdi-thumb-down</v-icon></v-btn>
                            </v-col>
                        </v-row>
                        <v-row class="mt-4">
                            <v-col>
                                <v-checkbox v-model="notifyMe" label="Notify me when on sale" color="primary"></v-checkbox>
                            </v-col>
                            <v-col class="d-flex justify-end">
                                <v-btn color="primary" @click="updatePrice" class="text-uppercase">Update Price</v-btn>
                            </v-col>
                        </v-row>
                    </v-col>
                </v-row>
            </v-col>

        </v-container>
    </v-main>
  </v-app>
</template>


<script>
import LineGraph from "@/components/LineGraph.vue";

export default {
  components: {
    LineGraph
  },
  data() {
    return {
      product: {
        name: "Orea Ice Cream",
        image: "https://source.unsplash.com/featured/?product",
        stores: {
          Woolies: "4.99",
          Coles: "3.99",
          Aldi: "3.99"
        },
        pastPrices: [4.99, 2.99,4.99, 3.99,4.99],
      },
      relatedProducts: [
        { id: 1, name: "Reece Ice Cream" },
        { id: 2, name: "Cadbury Ice Cream" },
         { id: 3, name: "Milk Dairy" }
      ],
      updatedPrice: "",
      notifyMe: false,
    };
  },
  methods: {
    updatePrice() {
      // Logic to update the product price and possibly inform admin or save in the DB
    },
    upvote() {
      // Logic to upvote the price
    },
    downvote() {
      // Logic to downvote the price
    },
    fetchRelatedProducts() {
      // Mock fetching related products
      this.relatedProducts = [
        { id: 1, name: "Related Product 1" },
        { id: 2, name: "Related Product 2" },
        // ... Add more if needed
      ];
    }
  },
  mounted() {
    this.fetchRelatedProducts();
  },
  computed: {
   pastDays() {
        const d = new Date();
        let days = [];

        for(let i = 0; i < 10; i++) {
            const pastDay = new Date(d);
            pastDay.setDate(d.getDate() - i);
            days.unshift(`${pastDay.getMonth() + 1}/${pastDay.getDate()}`);
        }

        return days;
    },
    lineChartData() {
        return {
            labels: this.pastDays,
        datasets: [
            {
                label: 'Woolies',
                data: [4.99, 2.5, 4.99, 5.5, 2.75],  // Sample data for Woolies
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            },
            {
                label: 'Coles',
                data: [3.99, 2.5, 3, 3.69, 5],  // Sample data for Coles
                borderColor: 'rgba(99, 255, 132, 1)',
                fill: false
            },
            {
                label: 'Aldi',
                data: [3.89, 3.89, 3.89, 3.89, 3.89],  // Sample data for Aldi
                borderColor: 'rgba(99, 99, 255, 1)',
                fill: false
            }
        ]
    }
},
   lineChartOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    width: 500,  // Add these lines to specify the size
    height: 400
  }
}

}

};
</script>

<style scoped>
/* Add custom styles if necessary */
</style>
