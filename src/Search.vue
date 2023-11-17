<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app >
    <!-- Home Page -->
    <v-container>
      <!-- Search bar -->
      <v-toolbar>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="searchTerm"
          @change="fetchProducts()"
          label="Search"
          class="d-none d-sm-flex"
          filled
          prepend-inner-icon="mdi-magnify"
          solo
          flat
          rounded
          outlined
        ></v-text-field>
        <v-spacer></v-spacer>

        <!-- Filter button -->
        <v-menu transition="slide-y-transition">
          <template v-slot:activator="{ on, attrs }">
            <v-btn class="text-center" v-on="on" v-bind="attrs">
              <v-icon left>mdi-filter</v-icon>
              <b>Stores</b>
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
      </v-toolbar>

      <!-- Results display -->
      <div class="py-3 mt-5">
        <h1>COMPARE PRICES</h1>
        <p>A Great Way To Save Money. Please enter the specific product you are looking for to get the most affordable item.</p>
      </div>

      <!-- Category bar -->
      <v-app-bar color="transparent" flat class="">
        <v-tabs v-model="tab" stacked active-class="active">
          <v-tabs-slider color="transparent"></v-tabs-slider>
          <v-tab @click="handleTabClick(tab.name)" v-for="(tab, index) in tabs" :key="index" class="withoutupercase normalize font-weight-bold" :value="'tab-' + (index + 1)">
            <v-icon>{{ tab.icon }}</v-icon>{{ tab.name }}
          </v-tab>                
        </v-tabs>
      </v-app-bar>
      <v-divider class="my-5" color="grey" v-if="!loading"></v-divider>

      <!-- Progress linear -->
      <v-progress-linear class="my-2"  v-if="loading"
        :height="4"
        color="orange"
        indeterminate
      ></v-progress-linear>

      <!-- Pagination 
      <v-toolbar class="mx-auto">
        <v-btn class="mr-2" outlined>
          <v-icon left>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn class="mr-2" outlined>
          <v-icon right>mdi-chevron-right</v-icon>
        </v-btn>
      </v-toolbar>
      -->

      <!-- Lowest price product -->
      <v-container v-if="lowestPricedProduct" class="my-4 text-center-sm text-left-md">
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
              <v-container>
                <v-btn
                  @click="addProductToGrocery(lowestPricedProduct)"
                  color="success"
                >
                  Add to Grocery
                </v-btn>
              </v-container>
              <v-card-title>
                <strong
                  >Deal Available At
                  {{ bestStoreForProduct(lowestPricedProduct) }}</strong
                >
              </v-card-title>
            </v-col>
          </v-row>
      </v-container>

      <!-- Skeleton loader -->
      <v-container v-if="loading_start" class="mt-5 pt-5 text-center">
        <v-row>
          <v-col v-for="i in 4" :key="i" cols="12" md="3">
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-col>
        </v-row>
      </v-container>

      <!-- Best deal at Woolworths and Coles -->
      <v-container v-if="combinedProducts.length" class="my-4">
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
            <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
              <v-img :src="product.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
              <v-toolbar color="transparent" flat>
                <v-avatar color="yellow" rounded width="100" height="35">
                <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && !product.iga_price">
                  {{ 
                    (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2)) == 0 
                    ? 'Best Price'  
                    : 'Save $' + (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2))
                  }}
                </span>
                <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && product.iga_price">
                  Save ${{ 
                    parseFloat(Math.max(product.coles_price, product.woolworths_price, product.iga_price) - Math.min(product.coles_price, product.woolworths_price, product.iga_price)).toFixed(2) 
                  }}
                </span>
              </v-avatar>
              </v-toolbar>
              <v-card-text class="py-1">
              <strong>
                    <v-span v-if="product.woolworths_price">
                    Woolies ${{ product.woolworths_price }}</v-span>
              
              
                    <v-span v-if="product.coles_price">
                    , Coles ${{ product.coles_price }}</v-span>
            
              
                    <v-span v-if="product.iga_price">
                    & ${{ product.iga_price }} at IGA</v-span>
              </strong>
              </v-card-text>
              <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ product.name }} | {{product.size}}
              </v-card-title>
              <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
              <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
                <v-btn class="text-none text-subtitle-1 mb-3 white--text" color="green" size="small" variant="flat">
                  Add To List
                </v-btn>
                <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat">
                  Listen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Popular items -->
      <v-container v-if="categoryProduct.length" class="my-4">
        <v-row>
          <v-col cols="12">
            <h2>Popular Items</h2>
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
            <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
              <v-img :src="product.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
              <v-toolbar color="transparent" flat>
                <v-avatar color="yellow" rounded width="100" height="35">
                <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && !product.iga_price">
                  {{ 
                    (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2)) == 0 
                    ? 'Best Price'  
                    : 'Save $' + (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2))
                  }}
                </span>
                <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && product.iga_price">
                  Save ${{ 
                    parseFloat(Math.max(product.coles_price, product.woolworths_price, product.iga_price) - Math.min(product.coles_price, product.woolworths_price, product.iga_price)).toFixed(2) 
                  }}
                </span>
              </v-avatar>
              </v-toolbar>
              <v-card-text class="py-1">
              <strong>
                    <v-span v-if="product.woolworths_price">
                    Woolies ${{ product.woolworths_price }}</v-span>
              
              
                    <v-span v-if="product.coles_price">
                    , Coles ${{ product.coles_price }}</v-span>
            
              
                    <v-span v-if="product.iga_price">
                    & ${{ product.iga_price }} at IGA</v-span>
              </strong>
              </v-card-text>
              <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ product.name }} | {{product.size}}
              </v-card-title>
              <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
              <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
                <v-btn class="text-none text-subtitle-1 mb-3 white--text" color="green" size="small" variant="flat">
                  Add To List
                </v-btn>
                <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat">
                  Listen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Crazy deals at Woolworths -->
      <v-container v-if="weeklyDeals_w.length && storeFilters['Deals At Woolies']" class="m-2">
        <v-row>
          <v-col cols="12" md="8">
            <h2>Crazy Deals at <span class="green--text font-weight-bold">Woolworths</span></h2>
          </v-col>
          <v-col cols="12" md="4" class="d-flex align-center justify-end">
            <span class="mr-2 text-h6 font-weight-bold">See All</span>
            <!-- Add a router-link or an action for "See All" as needed -->
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_w" 
            :key="deal.name"
          >
            <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
              <v-img :src="deal.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
              <v-toolbar color="transparent" flat>
                <v-avatar color="yellow" rounded width="100" height="35">
                  <span class="black--text  font-weight-bold p-0">
                    Save ${{ parseFloat(deal.coles_price - deal.woolworths_price).toFixed(2) }}
                  </span>
                </v-avatar>
              </v-toolbar>
              <v-card-text class="text-h5">
                <span class="green--text font-weight-bold mx-2">${{ deal.woolworths_price }}</span>
                <span class="text-decoration-line-through gray--text">${{ deal.coles_price }}</span>
              </v-card-text>
              <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ deal.name }} | {{deal.size}}
              </v-card-title>
              <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
              <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
                <v-btn class="text-none text-subtitle-1 mb-3 white--text" @click="AddToNotify(product)" color="green" size="small" variant="flat">
                  Add To List
                </v-btn>
                <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat">
                  Listen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      
      <!-- Crazy deals at Coles -->
      <v-container v-if="weeklyDeals_coles.length && storeFilters['Deals At Coles']" class="my-5">
        <v-row>
          <v-col cols="12">
            <h2>Crazy Deals at Coles</h2>
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_coles" 
            :key="deal.name"
          >
            <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
              <v-img :src="deal.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
              <v-toolbar color="transparent" flat>
                <v-avatar color="yellow" rounded width="100" height="35">
                  <span class="black--text  font-weight-bold p-0">
                    Save ${{ parseFloat(deal.coles_price - deal.iga_price).toFixed(2) }}
                  </span>
                </v-avatar>
              </v-toolbar>
              <v-card-text class="text-h5">
                <span class="green--text font-weight-bold mx-2">${{ deal.coles_price }}</span>
                <span class="text-decoration-line-through gray--text">${{ deal.iga_price }}</span>
              </v-card-text>
              <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ deal.name }} | {{deal.size}}
              </v-card-title>
              <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
              <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
                <v-btn class="text-none text-subtitle-1 mb-3 white--text" @click="AddToNotify(product)" color="green" size="small" variant="flat">
                  Add To List
                </v-btn>
                <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat">
                  Listen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <!-- Crazy deals at IGA -->
      <v-container v-if="weeklyDeals_iga.length && storeFilters['Deals At IGA']" class="m-2">
        <v-row>
          <v-col cols="12">
            <h2>Crazy Deals at IGA</h2>
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="3"
            lg="3"
            v-for="deal in weeklyDeals_iga" 
            :key="deal.name"
          >
            <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
              <v-img :src="deal.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
              <v-toolbar color="transparent" flat>
                <v-avatar color="yellow" rounded width="100" height="35">
                  <span class="black--text font-weight-bold p-0">
                    Save ${{ parseFloat(deal.coles_price - deal.iga_price).toFixed(2) }}
                  </span>
                </v-avatar>
              </v-toolbar>
              <v-card-text class="text-h5">
                <span class="green--text font-weight-bold mx-2">${{ deal.iga_price }}</span>
                <span class="text-decoration-line-through gray--text">${{ deal.coles_price }}</span>
              </v-card-text>
              <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ deal.name }} | {{deal.size}}
              </v-card-title>
              <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
              <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
                <v-btn class="text-none text-subtitle-1 mb-3 white--text" color="green" size="small" variant="flat">
                  Add To List
                </v-btn>
                <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat">
                  Listen
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
    
      </v-container>

    </v-container>
  </v-app>
</template>

<script>
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
        // searchClosed: true, -> search field open and close
        selection:1,
        tab: null,
        tabs: [
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
    created() {
      this.getUserLocation();
      this.fetchWeeklyDeals();
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
          // Assuming you're making an API call to get suggestions
          // Here's an example using Axios:
          const response = await fetch(`http://127.0.0.1:8000/search_suggestions`);

          // Assuming the API returns a list of suggestions
          this.searchSuggestions = response.data.suggestions;
        } catch (error) {
          console.error("Error fetching suggestions:", error);
        }
      },
      async handleTabClick(category) {
        this.loading=true;
        switch (category) {
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

      for (const productName of productNames) {
        const response = await fetch(`http://127.0.0.1:8000/search/${encodeURIComponent(productName)}/${encodeURIComponent(this.postalCode)}`);
        products.push(...(await response.json()));
      }
        this.loading=false;
        return products;

      },
      async fetchProducts() {
        this.loading = true;
        const response = await fetch(`http://127.0.0.1:8000/search/${encodeURIComponent(this.searchTerm)}/${encodeURIComponent(this.postalCode)}`);
        this.products = await response.json();
        this.loading = false;
      },
      removeItemFromCart(index) {
        this.groceryList.splice(index, 1);
        this.saveGroceryList()
      }, Completed(index) {
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
      saveGroceryList() {
        console.log("stored")
        localStorage.setItem('groceryList', JSON.stringify(this.groceryList));
      },
      addProductToGrocery(product) {
        let existingProduct = this.groceryList.find(item => item.name === product.name);
        if (existingProduct) {
          existingProduct.counter += 1;
        } else {
          let bestPriceStore = this.bestStoreForProduct(product);
          let individualSavings = this.productSavings(product);
          this.groceryList.push({ ...product, counter: 1, bestStore: bestPriceStore, savings: individualSavings });
        }
        // Update overall savings
        this.updateTotalSavings();
        this.saveGroceryList();
      },
      updateTotalSavings() {
        // Total savings is the sum of all individual savings.
        this.savings = this.groceryList.reduce((acc, item) => {
          return acc + (item.savings * item.counter);
        }, 0);
      },
      productSavings(product) {
        const wooliesPrice = parseFloat(product.woolworths_price) || 0;
        const colesPrice = parseFloat(product.coles_price) || 0;
        const aldiPrice = parseFloat(product.aldi_price) || 0;
        const chemistPrice = parseFloat(product.chemist_price) || 0;
        const igaPrice = parseFloat(product.iga_price) || 0;

        // Calculate the average price
        const averagePrice = this.smallestPrice(this.lowestPricedProduct);
        // Determine which store's price to compare with
        let storeToCompare = '';

        if (wooliesPrice > 0 && colesPrice > 0) {
          // Both Woolworths and Coles prices are available
          storeToCompare = 'Coles';
        } else if (aldiPrice > 0) {
          // Aldi price is available
          storeToCompare = 'Aldi';
        } else if (chemistPrice > 0) {
          // Chemist Warehouse price is available
          storeToCompare = 'Chemist Warehouse';
        } else if (igaPrice > 0) {
          // IGA price is available
          storeToCompare = 'IGA';
        }

        // Calculate the price difference based on the available prices
        let diff = 0;
        switch (storeToCompare) {
          case 'Coles':
            diff = Math.abs(wooliesPrice - colesPrice);
            break;
          case 'Woolworths':
            diff = -wooliesPrice + averagePrice;
            break;
          case 'Aldi':
            diff = -aldiPrice +averagePrice;
            break;
          case 'Chemist Warehouse':
            diff = -chemistPrice + averagePrice;
            break;
          case 'IGA':
            diff = -igaPrice + averagePrice;
            break;
        }
        // Return the difference rounded to 2 decimal places or null
        return diff.toFixed(2);
      },
      updateSavingsAndBestStore(product) {
        // Update overall savings
        this.savings += this.productSavings(product);

        // TODO: You will need logic here to update the 'bestStore' value.
        // This can be based on the minimum price amongst all stores or some other logic.
      },  
      async fetchWeeklyDeals() {
        try {
          this.loading_start = true;
          const responseWoolies = await fetch('http://127.0.0.1:8000/half-price-deals_woolies?page_number=1');
          this.weeklyDeals_w = await responseWoolies.json();
          const responseIga = await fetch('http://127.0.0.1:8000/half-price-deals_iga');
          this.weeklyDeals_iga = await responseIga.json();
          const responseColes = await fetch('http://127.0.0.1:8000/half-price-deals_coles');
          this.weeklyDeals_coles= await responseColes.json();
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
          }

          const result = await response.json();
          console.log(result.message);  // Log the response from the backend
        } catch (error) {
          console.error('Failed to add Item', error);
        } finally {
          console.log('Added item');
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
          const response = await fetch(`http://127.0.0.1:8000/search/${category}/${encodeURIComponent(this.postalCode)}`);
          this.products = await response.json();
          // Process and use the data as needed
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      }
    },

  };
</script>

<style>
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
    background-color: orange !important;
    border-radius: 5px;
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

</style>
