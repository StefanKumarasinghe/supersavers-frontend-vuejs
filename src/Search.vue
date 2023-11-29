<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <v-container fluid>
      <div class="mx-3 mt-5">
        <h1>COMPARE PRICES</h1>
        <span>A Great Way To Save Money. Please enter the specific product you are looking for to get the most affordable item.</span>
      </div>

      <v-row align="center" class="my-5">
        <v-col cols="9" md="10" lg="6">
          <v-text-field
            v-model="searchTerm"
            @change="fetchProducts()"
            label="Search"
            filled
            prepend-inner-icon="mdi-magnify"
            solo
            flat
            rounded
            outlined
            hide-details="true"
          ></v-text-field>
        </v-col>
        <v-col cols="2" md="2" lg="2">
          <v-menu rounded="lg" offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-btn fab v-on="on" v-bind="attrs" outlined color="grey darken-1">
                <v-icon >
                  mdi-filter
                </v-icon>
              </v-btn>              
            </template>
            <v-list>
              <v-list-item v-for="(value, key) in storeFilters" :key="key">
                <v-list-item-action>
                  <strong>
                    <v-checkbox
                      v-model="storeFilters[key]"
                      small
                      :label="key.charAt(0).toUpperCase() + key.slice(1)"
                    ></v-checkbox>
                  </strong>
                </v-list-item-action>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-col>
      </v-row>

      <!-- Category bar -->
      <v-app-bar color="transparent" flat class="">
        <v-tabs v-model="tab" stacked active-class="active">
          <v-tabs-slider color="transparent"></v-tabs-slider>
          <v-tab style="height:auto" @click="handleTabClick(tab.name)" v-for="(tab, index) in tabs" :key="index" class="withoutupercase normalize font-weight-bold" :value="'tab-' + (index + 1)">
            <v-icon>{{ tab.icon }}</v-icon>{{ tab.name }}
          </v-tab>                
        </v-tabs>
      </v-app-bar>
      <v-divider class="my-5" color="grey" v-if="!loading"></v-divider>

      <!-- Progress linear -->
      <v-progress-linear class="my-2"  v-if="loading"
        :height="4"
        color="green"
        indeterminate
      ></v-progress-linear>

      <!-- Lowest price product -->
      <div fluid v-if="lowestPricedProduct" class="my-5 py-3 text-center-sm text-left-md">
        <h2 class="my-2">Lowest product found</h2>
          <v-row align="center" class="my-1 p-0">
            <v-col cols="12" md="4" class="text-center-sm text-left-md">
              <v-img
                :src="lowestPricedProduct.image"
                width="300"
                contain
              ></v-img>
            </v-col>
            <v-col cols="12" md="7">
              <v-card-title class="display-1">
                <strong>{{ lowestPricedProduct.name }}</strong>
              </v-card-title>
              <v-card-title class="display-6 green--text">
                ${{ smallestPrice(lowestPricedProduct) }} /
                {{ lowestPricedProduct.size }}
              </v-card-title>
                <v-btn
                  @click="addItemToCart(lowestPricedProduct)"
                  color="success"
                >
                  Add to Grocery
                </v-btn>
              
              <v-card-title>
                <strong
                  >Deal Available At
                  {{ bestStoreForProduct(lowestPricedProduct) }}</strong
                >
              </v-card-title>
            </v-col>
          </v-row>
      </div>

      <!-- Skeleton loader -->
      <div v-if="loading_start" class="mt-5 pt-5 text-center">
        <v-row>
          <v-col v-for="i in 4" :key="i" 
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3">
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-col>
        </v-row>
      </div>

      <!-- Best deal at Woolworths and Coles -->
      <div v-if="combinedProducts.length" class="my-4">
        <v-row>
          <v-col cols="12">
            <h2>Best Prices Across Stores</h2>
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="product in combinedProducts" 
            :key="product.name"
          >
            <SearchCard :product="product" />
          </v-col>
        </v-row>
      </div>

      <!-- Best deal at Category -->
      <div v-if="categoryProduct.length" class="my-4">
        <v-row>
          <v-col cols="12">
            <h1>Popular Items</h1>
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="product in categoryProduct" 
            :key="product.name"
          >
            <SearchCard :product="product"/> 
          </v-col>
        </v-row>
      </div>

      <!-- Crazy deals at Woolworths -->
      <div v-if="weeklyDeals_w.length && storeFilters['Deals At Woolies'] && !categoryProduct.length && !combinedProducts.length" class="my-5 py-5">
        <v-toolbar>
          <h2>Deals at <span class="green--text font-weight-bold">Woolworths</span></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_w" 
            :key="deal.name"
          >
            <DealsCard :deal="deal"/>
          </v-col>
        </v-row>
      </div>
      
      <!-- Crazy deals at Coles -->
      <div v-if="weeklyDeals_coles.length && storeFilters['Deals At Coles'] && !categoryProduct.length && !combinedProducts.length" class="my-5 py-5">
        <v-toolbar>
          <h2>Deals at <span class="red--text font-weight-bold ">Coles</span></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_coles" 
            :key="deal.name"
          >
            <DealsCard :deal="deal"/>
          </v-col>
        </v-row>
      </div>

      <!-- Crazy deals at IGA -->
      <div v-if="weeklyDeals_iga.length && storeFilters['Deals At IGA'] && !categoryProduct.length && !combinedProducts.length" class="py-5 my-5">
        <v-toolbar>
          <h2>Deals at <span class="white--text font-weight-bold iga_logo ">  &nbsp; IGA  &nbsp;</span></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_iga" 
            :key="deal.name"
          >
            <DealsCard :deal="deal"/>
          </v-col>
        </v-row>
    
      </div>
      <v-snackbar v-model="snackbar" color="white" dark>
        <v-row align="center" justify="center" class="ma-0">
          <v-col cols="12" sm="10" md="8" lg="6" class="black--text font-weight-bold text-center">
            {{ this.error }}
          </v-col>
          <v-btn
              color="pink"
              variant="text"
              @click="snackbar = false"
            >
              Got it
          </v-btn>
        </v-row>
      </v-snackbar>
    </v-container>
  </v-app>
</template>

<script>
  import DealsCard from './components/DealsCard.vue';
  import SearchCard from './components/SearchCard.vue';
  
  export default {
    data() {
      return {
        loading: false,
        loading_start:true,
        storeFilters: {
           Woolies: true,
           IGA: true,
           Coles: true,
          "Deals At Woolies": true,
          "Deals At Coles": true,
          "Deals At IGA": true,
        },
        AuthToken:null,
        searchTerm: '',
        postalCode: null,
        searchSuggestions:[],
        products: [],
        categoryProduct:[],
        completed:[],
        groceryList: [],
        savings: 0,
        exclusiveStores: [],
        weeklyDeals_w: [],
        weeklyDeals_iga: [],
        weeklyDeals_coles: [],
        snackbar: false,
        error: null,
        // searchClosed: true, -> search field open and close
        selection:1,
        tab: null,
        tabs: [
          { name: 'Deals', icon: 'mdi-currency-usd' },
          { name: 'All', icon: 'mdi-all-inclusive' },
          { name: 'Fruits', icon: 'mdi-fruit-watermelon' },
          { name: 'Vegetables', icon: 'mdi-carrot' },
          { name: 'Breakfast', icon: 'mdi-baguette' },
          { name: 'Frozen Foods', icon: 'mdi-snowflake' },
          { name: 'Dairy', icon: 'mdi-cow' },
          { name: 'Egg', icon: 'mdi-egg' },
          { name: 'Meat', icon: 'mdi-food-steak' },
          { name: 'Seafood', icon: 'mdi-fish' },
          { name: 'Snacks', icon: 'mdi-french-fries' },
          { name: 'Personal care', icon: 'mdi-toothbrush' }
        ]
      };
    },
    computed: {
      smallestPrice() {
        return (product) => {
          const prices = [
            parseFloat(product.woolworths_price) || Infinity,
            parseFloat(product.iga_price) || Infinity,
            parseFloat(product.coles_price) || Infinity,
            parseFloat(product.aldi_price) || Infinity
          ];
          const smallest = Math.min(...prices);
          return smallest === Infinity ? null : smallest;
        };
      },
      woolworthsProducts() {
        return this.products.filter(p => p.source === 'Woolworths');
      },
      colesProducts() {
        return this.products.filter(p => p.source === 'Coles');
      },
      colesGroceryList() {
        return this.groceryList.filter(item => item.bestStore === 'Coles');
      },
      IGAGroceryList() {
        return this.groceryList.filter(item => item.bestStore === 'IGA');
      },
      woolworthsGroceryList() {
        return this.groceryList.filter(item => item.bestStore === 'Woolworths');
      },
      bestStore(product) {
        return this.bestStoreForProduct(product)
      },
      filteredExclusiveStores() {
        return this.exclusiveStores.filter(store => {
          if(store.name === 'Woolworths' && this.storeFilters.woolies) return true;
          if(store.name === 'IGA' && this.storeFilters.iga) return true;
          if(store.name === 'Chemist Warehouse' && this.storeFilters.chemist) return true;
          if(store.name === 'Aldi' && this.storeFilters.aldi) return true;
          if(store.name === 'Coles' && this.storeFilters.coles) return true;
          return false;
        });
      },
      combinedProducts() {
        return this.products.filter(p => p.source === 'Combined' && p.coles_price && p.woolworths_price);
      },
      lowestPricedProduct() {
        if (!this.products.length || !this.searchTerm) return null;

        let lowest = null;
        let minPrice = 0;

        for (const product of this.products) {
          const prices = [
            parseFloat(product.woolworths_price) || null,
            parseFloat(product.coles_price) || null,
            parseFloat(product.aldi_price) || null,
            parseFloat(product.iga_price) || null,
            parseFloat(product.chemist_price) || null,
          ];
          const filteredPrices = prices.filter(price => price !== null);

          if (filteredPrices.length === 0) {
            continue;
          }
          const currentMinPrice = Math.min(...filteredPrices);

          if ((lowest === null) || (minPrice > currentMinPrice) || (minPrice === currentMinPrice)) {
            minPrice = currentMinPrice;
            lowest = product;
          }
        }
        return lowest;
      },
    },
    async created() {
      this.getUserLocation();
      await this.TokenPromise();

    },
    watch: {
      products: function(newProducts) {
        let stores = [ 'IGA', 'Woolworths' ,'Coles' ,'Chemist Warehouse'];
        this.exclusiveStores = stores.map(storeName => {
          return {
            name: storeName,
            products: newProducts.filter(p => p.source === storeName)
          };
        });
      }
    },
    mounted() {
      // Retrieve the groceryList from local storage when the component is mounted
      this.retrieveGroceryList();
    },
    methods: {
      async OnCallSuggestion() {
        try {
          const response = await fetch(`http://127.0.0.1:8000/search_suggestions`);
          // Assuming the API returns a list of suggestions
          this.searchSuggestions = response.data.suggestions;
        } catch (error) {
          console.error("Error fetching suggestions:", error);
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
            const data = await response.json();
            if (data.user == null) {
              this.$router.push('/login');
            }else{
              this.fetchWeeklyDeals();
              await this.VerifyAuth();
            }
          } else {
            console.error('Error:', response.statusText);
          }
        } catch (error) {
          console.error('Error:', error);
        }
      },
      async handleTabClick(category) {
        this.loading=true;
        this.combinedProducts=[]
        switch (category) {
          case 'Deals':
          this.storeFilters['Deals At Woolies']=true;
          this.storeFilters['Deals At Coles']=true;
          this.storeFilters['Deals At IGA']=true;
          this.categoryProduct =[]
          this.loading=false
          break;
          case 'All':
          this.categoryProduct = await this.fetchProductsCat(['Chips', 'Shampoo', 'Chocolate', 'Deodorant', 'Toothbrush','Oreo', 'Ice Cream', 'Apples','Biscuits','Kellogs']);
            break;
          case 'Fruits':
            this.categoryProduct = await this.fetchProductsCat(['Apple', 'Banana', 'Orange', 'Strawberry', 'Grapes', 'Mandarin']);
            break;
          case 'Vegetables':
            this.categoryProduct = await this.fetchProductsCat(['Carrot', 'Broccoli', 'Tomato', 'Spinach', 'Potato', 'Corn']);
            break;
          case 'Breakfast':
            this.categoryProduct = await this.fetchProductsCat(['Kellogs', 'Uncle Toby', 'Milk', 'Frosty', 'Eggs', 'Granola']);
            break;
          case 'Frozen Foods':
            this.categoryProduct = await this.fetchProductsCat(['Ice Cream', 'Frozen Pizza', 'Frozen Vegetables', 'Frozen Fish', 'Frozen Desserts']);
            break;
          case 'Dairy':
            this.categoryProduct = await this.fetchProductsCat(['Milk', 'Cheese', 'Yogurt', 'Butter', 'Ice Cream']);
            break;
          case 'Egg':
            this.categoryProduct = await this.fetchProductsCat(['Free ranged Eggs', 'Caged Eggs', 'Cage Free eggs']);
            break;
          case 'Meat':
            this.categoryProduct = await this.fetchProductsCat(['Steak', 'Chicken Breast', 'Pork Chops', 'Lamb', 'Ground Beef']);
            break;
          case 'Seafood':
            this.categoryProduct = await this.fetchProductsCat(['Salmon', 'Shrimp', 'Tuna', 'Lobster', 'Crab']);
            break;
          case 'Snacks':
            this.categoryProduct = await this.fetchProductsCat(['Potato Chips', 'Popcorn', 'Pretzels', 'Chocolate', 'Nuts']);
            break;
          case 'Personal Care':
            this.categoryProduct = await this.fetchProductsCat(['Toothpaste', 'Shampoo', 'Soap', 'Deodorant', 'Toothbrush']);
            break;
          // ... handle other categories
          default:
            this.categoryProduct = await this.fetchProductsCat(['Chips', 'Shampoo', 'Chocolate', 'Deodorant', 'Toothbrush','Oreo', 'Ice Cream', 'Apples',]);
            break;
        }
      },
      async fetchProductsCat(productNames) {  
        const products = [];
        try {
          for (const productName of productNames) {
            const response = await fetch(`http://127.0.0.1:8000/search/${encodeURIComponent(productName)}/${encodeURIComponent(this.postalCode)}`, {
              method: 'GET', // or 'POST' or other HTTP methods
              headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json', // Adjust the content type if needed
              },
            });    
            products.push(...(await response.json()));
          }
          this.products=[]
          this.storeFilters['Deals At Woolies']=false;
          this.storeFilters['Deals At Coles']=false;
          this.storeFilters['Deals At IGA']=false;
        }catch {
          this.error = "Couldn't retrieve the items from the specific category";
          this.snackbar = true;
        }
        this.loading=false;
        return products;
      },
      async fetchProducts() {
        this.loading = true;

        try {
          const response = await fetch(`http://127.0.0.1:8000/search/${encodeURIComponent(this.searchTerm)}/${encodeURIComponent(this.postalCode)}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            this.products = data;
          } else {
            console.error('Error:', response.statusText);
            this.error = response.statusText;
            this.snackbar = true;
          }
        } catch (error) {
          console.error('Error:', error);
          this.error = "Error in retrieving data..."
          this.snackbar = true;
        }

        this.loading = false;
      }, 
      Completed(index) {
        this.completed.push(this.groceryList.splice(index, 1)[0])
        this.saveGroceryList()
      },
      retrieveGroceryList() {
        const storedGroceryList = localStorage.getItem('groceryList');
        if (storedGroceryList) {
          this.groceryList = JSON.parse(storedGroceryList);
        }
      },
      bestStoreForProduct(product) {
        const storePrices = {
          'Woolworths': product.woolworths_price,
          'Coles': product.coles_price,
          'Aldi': product.aldi_price,
          'IGA': product.iga_price,
          'Chemist Warehouse': product.chemist_price
        };
        let bestStore = '';
        let lowestPrice = Infinity;
        for (const [store, price] of Object.entries(storePrices)) {
          if (price && parseFloat(price) < lowestPrice) {
            bestStore = store;
            lowestPrice = parseFloat(price);
          }
        }
        return bestStore;
      },
      updateSavingsAndBestStore(product) {
        // Update overall savings
        this.savings += this.productSavings(product);

        // TODO: You will need logic here to update the 'bestStore' value.
        // This can be based on the minimum price amongst all stores or some other logic.
      },  
      async fetchWeeklyDeals() {
        this.loading_start = true;
        try {
         
          
          const responseWoolies = await fetch(`http://127.0.0.1:8000/half-price-deals_woolies`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_w = await responseWoolies.json();
          this.weeklyDeals_w = this.weeklyDeals_w.slice(0, 8);
          
        } catch (error) {
          console.error("Failed to fetch weekly deals:", error);
          this.error = "Failed to get deals from Woolies"
          this.snackbar = true;
        } 
        try {
          const responseColes = await fetch('http://127.0.0.1:8000/half-price-deals_coles', {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_coles= await responseColes.json();
          this.weeklyDeals_coles = this.weeklyDeals_coles.slice(0, 8); // Get only the first 8 elements
         
        } catch (error) {
          console.error("Failed to fetch weekly deals:", error);
        }
        try {
          const responseIga = await fetch('http://127.0.0.1:8000/half-price-deals_iga', {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_iga =  await responseIga.json();
          this.weeklyDeals_iga = this.weeklyDeals_iga.slice(0, 8); // Get only the first 8 elements
        } catch (error) {
          console.error("Failed to fetch weekly deals:", error);
        } finally {
          this.loading_start= false;
        }
      },
      async AddToNotify(item){
        try {
          const response = await fetch('http://127.0.0.1:8000/add_item_notify', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              item: item,  // Assuming item is an object with properties like item, woolworths_code, coles_code, iga_code
            }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }else {
            this.error = "Item Successfully added to the Notification List";
            this.snackbar = true;
          }
          const result = await response.json();
          console.log(result.message);  // Log the response from the backend
        } catch (error) {
          console.error('Failed to add Item', error);
          this.error = "Failed to add item";
          this.snackbar = true;
        }
      },
      getLowestPrice() {
        return this.lowestPricedProduct;
      },
      async getUserLocation() {
        try {
          if ('geolocation' in navigator) {
            // Request the user's location
            const position = await this.getCurrentPosition();

            // Use Nominatim for reverse geocoding to get the postal code
            this.retrievePostalCode(position.coords.latitude, position.coords.longitude);
          } else {
            console.error('Geolocation is not available in this browser.');
          }
        } catch (error) {
          console.error('Error getting user location:', error);
        }
      },
      getCurrentPosition() {
        return new Promise((resolve, reject) => {
          navigator.geolocation.getCurrentPosition(resolve, reject);
        });
      },
      async retrievePostalCode(latitude, longitude) {
        try {
          // Use Nominatim reverse geocoding API
          const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
          const data = await response.json();

          if (data.address && data.address.postcode) {
            this.postalCode = data.address.postcode;
          }
        } catch (error) {
          console.error('Error retrieving postal code:', error);
        }
      },
      async fetchDataForCategory(category) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/search/${category}/${encodeURIComponent(this.postalCode)}`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_iga = await response.json();
          this.weeklyDeals_iga = this.weeklyDeals_iga.slice(0, 8); // Get only the first 8 elements
          this.products = await response.json();
          // Process and use the data as needed
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
      addItemToCart(item) {
        item.quantity = 1;
        this.$store.dispatch('addItem', item);
        this.error = 'Item was successfully added to the list';
        this.snackbar = true;
      }
    },
    components: {
      SearchCard,
      DealsCard
    }
  };
</script>

<style>

  .container {
    width: 100%;
    padding-left: 100px;
    margin-right: auto;
    margin-left: auto;
    padding-right: 50px;
  }

  @media (max-width: 701px) {
    .container {
      padding-left: 25px;
      padding-right: 25px;
    }
  }

  /* filter icon button */
  .v-application--is-ltr .v-btn__content .v-icon--left {
    margin-left: 0px;
    margin-right: 0px;
  }

  .truncate-text {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .v-sheet.v-toolbar:not(.v-sheet--outlined) {
    box-shadow: none;
  }

  /*-- Category tabs --*/
  .v-tab {
    display:grid;
    height:65px;
  }

  .v-slide-group__next, .v-slide-group__prev {
    align-items: center;
    display: flex;
    flex: 0 1 15px;
    justify-content: center;
    min-width: 15px;
  }

  .active {
    color: white !important;
    background-color: green !important;
    border-radius: 5px;
    padding:5px;
  }

  .v-card__title {
    padding-top: 16px;
    padding-left: 16px;
  }

  .v-card__text {
    padding-left: 16px;
    padding-top: 5px;
    padding-bottom: 5px;
  }

  .v-application .text-subtitle-1 {
    line-height: 1.3rem;
  }

  .v-text-field.v-text-field--enclosed .v-text-field__details {
    padding-top: 0px;
    margin-bottom: 0px;
  }

  .v-toolbar__content, .v-toolbar__extension {
    align-items: none;
  }

  .iga_logo {
    background-color: red;
  }

</style>