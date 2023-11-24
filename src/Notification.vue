<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
      <v-main>
        <v-container fluid class="notify-deals-container">
        <h1 class="font-weight-bold mx-auto">Notify Deals</h1>
          <v-row class="my-1 p-0">
            <v-col v-for="product in products" :key="product.woolworths_code" cols="12" md="12">
              <v-container class="product-card">
                <v-row align="center" justify="start">
                  <v-col cols="4">
                    <v-img :src="product.image" height="200" class="py-2 product-image" contain></v-img>
                  </v-col>
                  <v-col cols="8">
                    <v-card-title class="display-1 mb-2 orange--text product-title">
                      <strong>{{ product.name }}</strong>
                    </v-card-title>
                    <v-card-subtitle class="mb-3 product-description">
                      {{ product.description }}
                    </v-card-subtitle>
                    <v-btn @click="removeProduct(product)" color="orange white--text" class="ml-3 remove-button">
                      Remove
                    </v-btn>
                    <v-card-subtitle class="product-sale-info">
                      <strong>The Item is on Sale at Woolies!</strong>
                    </v-card-subtitle>
                  </v-col>
                </v-row>
              </v-container>
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        products: [],
        AuthToken: null,
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

          
              await this.VerifyAuth();
              this.fetchProducts()
            
          } else {
            console.error('Error:', response.statusText);
            this.$router.push('/login');
          }
        } catch (error) {
          console.error('Error:', error);
          this.$router.push('/login');
        }
    },
      async fetchProducts() {
        try {
          const response = await fetch('http://127.0.0.1:8000/retrieve_notify', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          const data = await response.json();
          this.products = data; // Update with your actual data structure
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      },
      async removeProduct(product) {
        try {
         await fetch('http://127.0.0.1:8000/remove_item_notify', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: String(product.name),
              woolworths_code: String(product.woolworths_code),
              coles_code: String(product.coles_code),
              iga_code: String(product.iga_code),
              image: String(product.image),
              description: String(product.description),
            }),
          });
  

          this.products = this.products.filter((prod) => prod.woolworths_code !== product.woolworths_code);
  
        } catch (error) {
          console.error('Error removing product:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* Custom styling */
  .notify-deals-container {
    padding: 20px;
  }
  
  .product-card {
    margin: 10px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease-in-out;
  }
  
  .product-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
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
  