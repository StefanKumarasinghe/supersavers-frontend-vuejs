<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app v-show="authenticated">

      <v-container fluid>
        <div class="mx-3">
          <h1 class="fw-bold">Never Miss a Deal</h1>
          <p class="fw-bold">With the notifications feature, you won't miss out on the item with the best deal!</p>
          <p class=" fw-bold text-white p-3 bg-success">You can manage your your notiification setting at <a class="text-white text-decoration-underline" href="/account">Accounts</a></p>
        </div>
        <v-container v-if="loading" fill-height>
        <v-row align="center" justify="center">
          <v-col>
            <div class="text-center">
              <!-- Vuetify Progress Circular -->
              <v-progress-circular
                :size="64"
                color="green"
                :width="7"
                indeterminate
              ></v-progress-circular>
              <h2 class="text-success fw-bold mt-3">Fetching your wishlist...</h2>
            </div>
          </v-col>
        </v-row>
        </v-container>
        <div v-for="(product, i) in products" :key="i" class="d-flex justify-center">
          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-12">
            <div class="col-12 col-md-3 col-lg-3 col-sm-12 py-0">
              <div class="p-1">
                <v-img :src="product.image" alt="Item Image" contain class="mx-auto" min-width="150" max-width="170"></v-img>
              </div>
            </div>
            <div class="col-12 col-md-9 col-lg-9 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
              <div class="row">
                <div class="col-12 col-md-12 col-lg-12 col-sm-12"> 
                  <div class="fw-bold">
                    <h5 class="fw-bold">{{product.name}}</h5>
                  </div>
                  <div class="py-5">
                    <div class="mb-3 fw-bold product-description">
                      <p>{{ product.description.replace(/<[^>]*>/g, ' ') }}</p>
                    </div>
                  </div>
                  <div>
                    <v-btn rounded class="font-weight-bold white--text text-subtitle-1  " outlined color="red" height="40" width="150" style="border-radius:0" @click="removeProduct(product)">Remove</v-btn>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-container>
      <div class="text-center ma-2">
          <Toast ref="Toast" />
        </div>
    </v-app>
</template>
  
<script>
import Toast from './components/Toast.vue';

export default {
    components: {
     Toast
    },
    metaInfo: {
  // Page Title
  title: 'Supersavers | Deals & Notifications',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Manage your deal notifications with Supersavers. Choose items you want to be notified about when they go on sale at Woolworths, Coles, and IGA. Customize your notifications and save more on groceries!' }, // Page description
    { name: 'keywords', content: 'Supersavers, deal notifications, manage notifications, customize alerts, grocery deals, Woolworths, Coles, IGA' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Deal Notifications' }, // Open Graph title
    { property: 'og:description', content: 'Manage your deal notifications with Supersavers. Choose items you want to be notified about when they go on sale at Woolworths, Coles, and IGA. Customize your notifications and save more on groceries!' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/notifications' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Deal Notifications' }, // Twitter title
    { name: 'twitter:description', content: 'Manage your deal notifications with Supersavers. Choose items you want to be notified about when they go on sale at Woolworths, Coles, and IGA. Customize your notifications and save more on groceries!' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

    data() {
      return {
        loading:true,
        authenticated:false,
        products: [],
        AuthToken: null,
        quantities: []
      };
    },
    async beforeMount() {
      await this.TokenPromise();
    },
    methods: {
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
    async SubscriptionCheck() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/valid_subscription`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });
        if (!response.ok) {
        this.$router.push('/subscription')
        }else{
        this.authenticated=true
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
              this.SubscriptionCheck()
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
              await this.fetchProducts()
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
    async fetchProducts() {
      try {
        const response = await fetch(`${this.$GroceryAPI}/retrieve_notify`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          this.products = data; // Update with your actual data structure
          this.loading = false;
        } else {
          console.error('Error fetching products:', response.statusText);
          this.$refs.Toast.showSnackbar('Something went wrong fetching your wishlist', 'red', 'mdi-alert-circle');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
        this.$refs.Toast.showSnackbar('Something went wrong fetching your wishlist', 'red', 'mdi-alert-circle');
      }
    },

    async removeProduct(product) {
      try {
        const response = await fetch(`${this.$GroceryAPI}/remove_item_notify`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            woolworths_code: String(product.woolworths_code),
            coles_code: String(product.coles_code),
            iga_code: String(product.iga_code),
          }),
        });
        if (response.ok) {
          this.products = this.products.filter((prod) => prod.woolworths_code !== product.woolworths_code);
          this.$refs.Toast.showSnackbar('Successfully removed the item', 'green', 'mdi-check-circle');
        } else {
          console.error('Error removing product:', response.statusText);
          this.$refs.Toast.showSnackbar('Could not find the item to be removed', 'red', 'mdi-alert-circle');
        }
      } catch (error) {
        this.$refs.Toast.showSnackbar('Something went wrong removing your item', 'red', 'mdi-alert-circle');
      }
    },

    },
  };
  </script>
  
  <style scoped>
  
  .product-card {
    margin: 10px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease-in-out;
  }
  
  .product-card:hover {
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  }
  
  .product-image {
    border-radius: 8px;
  }
  
  .product-title {
    color: #ff5722; /* Orange color */
  }
  
  .product-description {
    color: #607d8b; /* Blue-gray color */
  }
  
  .remove-button {
    background-color: #ff5722;
  }
  
  .product-sale-info {
    color: #4caf50; /* Green color */
  }
  </style>
  