<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
      <v-container fluid>
        <div class="mx-3 mt-5">
          <h1>NOTIFY DEALS</h1>
          <p>With the notifications feature, you won't miss out on the item with the best deal!</p>
        </div>
        <div v-for="(product, i) in products" :key="i" class="d-flex justify-center">
          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10">
            <div class="col-12 col-md-3 col-lg-3 col-sm-12 py-0">
              <div class="p-1">
                <v-img :src="product.image" alt="Item Image" contain class="mx-auto" min-width="150" max-width="170"></v-img>
              </div>
            </div>
            <div class="col-12 col-md-9 col-lg-9 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
              <div class="row">
                <div class="col-12 col-md-12 col-lg-12 col-sm-12"> 
                  <div class="text-overline font-weight-bold">
                    <h5>{{product.name}}</h5>
                  </div>
                  <div class="py-5">
                    <div class="mb-3 product-description">
                      {{ product.description }}
                    </div>
                  </div>
                  <div>
                    <v-btn rounded class="font-weight-bold white--text text-subtitle-1 " color="red" height="40" width="150" @click="removeProduct(product)">Remove</v-btn>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <v-alert colored-border  elevation="2" color="green" prominent class="mt-5" width="100%">
                        <h2>Manage your account</h2>
          <p class="fw-bold">You could manage how you would like to be notified for products. Never miss out on deals and get alerted to your phone or email once that item is on sale</p>
          <v-btn color="green" class="white--text mt-3" to="/account">Manage</v-btn>
        </v-alert>
      </v-container>

    </v-app>
</template>
  
<script>
  export default {
    data() {
      return {
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
          const response = await fetch(`${this.$GroceryAPI}/retrieve_notify`, {
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
         await fetch(`${this.$GroceryAPI}/remove_item_notify`, {
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
  

          this.products = this.products.filter((prod) => prod.woolworths_code !== product.woolworths_code);
  
        } catch (error) {
          console.error('Error removing product:', error);
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
  