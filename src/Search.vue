<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
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
            @input="getSearchRecommendations()"
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
           <!-- Search recommendations container -->
           <v-container v-if="shownlist">
          <v-card>
            <v-list>
              <v-list-item v-for="recommendation in shownlist" :key="recommendation">
                <v-list-item-content @click="selectRecommendation(recommendation)">
                  {{ recommendation }}
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-container>
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
              <v-card-title class="display-1" style="display: inline-block; word-break: break-word;">
                <strong>{{ lowestPricedProduct.name }}</strong>
              </v-card-title>
              <v-card-title class="display-6" style="display: inline-block; word-break: break-word;">
               <p>{{ lowestPricedProduct.description.replace(/<[^>]*>/g, ' ') }}</p>
              </v-card-title>
              <v-card-title class="display-6 font-weight-bold green--text">
                ${{ smallestPrice(lowestPricedProduct) }} /
                {{ lowestPricedProduct.size }}
              </v-card-title>
              <v-card-title>
                Deal Available At 
                <strong :class="{ 'text-success': bestStoreForProduct(lowestPricedProduct).includes('Woolworths'), 'text-danger': bestStoreForProduct(lowestPricedProduct).includes('Coles') , 'bg-danger p-3 text-white': bestStoreForProduct(lowestPricedProduct).includes('IGA') }">
 {{ bestStoreForProduct(lowestPricedProduct) }}
</strong>

              </v-card-title>
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
            md="4"
            lg="4"
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
            md="4"
            lg="4"
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
          <h2>Deals at <span class="green--text font-weight-bold">Woolworths <v-icon @click="fetchWoolDeals()" large color="green" >mdi-refresh-circle</v-icon>
</span></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="4"
            lg="4"
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
          <h2>Deals at <span class="red--text font-weight-bold ">Coles</span>  <v-icon @click="fetchColesDeals()" large color="green" >mdi-refresh-circle</v-icon></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="4"
            lg="4"
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
          <h2>Deals at <span class="white--text font-weight-bold iga_logo ">  &nbsp; IGA  &nbsp;</span>  <v-icon @click="fetchIGADeals()" large color="green" >mdi-refresh-circle</v-icon></h2>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-row>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="4"
            lg="4"
            v-for="deal in weeklyDeals_iga" 
            :key="deal.name"
          >
            <DealsCard :deal="deal"/>
          </v-col>
        </v-row>
      </div>


       <!-- Skeleton loader -->
      <div v-if="loading_start" class="mt-5 pt-5 text-center">
        <v-row>
          <v-col v-for="i in 6" :key="i" 
            cols="12"
            xs="12"
            sm="6"
            md="4"
            lg="4">
            <v-skeleton-loader type="card"></v-skeleton-loader>
          </v-col>
        </v-row>
      </div>
      
      <div class="text-center ma-2">
        <v-snackbar v-model="snackbar" :timeout="snackbarTimeout">
          <v-avatar color="green" size="30px" class="me-3"><v-icon>mdi-check</v-icon></v-avatar>
          <span class="white--text font-weight-bold">{{ this.message }}!</span>
          <template v-slot:action="{ attrs }">
            <v-btn
              color="green"
              text
              v-bind="attrs"
              @click="snackbar = false"
            >
              <b>Close</b>
            </v-btn>
          </template>
        </v-snackbar>
      </div>
      <div class="text-center ma-2">
        <v-snackbar v-model="snackbarError" :timeout="snackbarTimeout" style="bottom: 0;" >
          <v-avatar color="red" size="30px" class="me-3"><v-icon>mdi-alert-circle</v-icon></v-avatar>
          <span class="white--text font-weight-bold">{{ this.error }}!</span>
          <template v-slot:action="{ attrs }">
            <v-btn
              color="red"
              text
              v-bind="attrs"
              @click="snackbar = false"
            >
              <b>Close</b>
            </v-btn>
          </template>
        </v-snackbar>
      </div>
    </v-container>
  </v-app>
</template>

<script>
  import DealsCard from './components/DealsCard.vue';
  import SearchCard from './components/SearchCard.vue';
  
  export default {
    data() {
      return {
        authenticated:false,
        loading: false,
        loading_start:true,
        storeFilters: {
          "Deals At Woolies": true,
          "Deals At Coles": true,
          "Deals At IGA": true,
        },
        AuthToken:null,
        searchRecommendations:{
  "groceries": [
    "Milk",
    "Bread",
    "Eggs",
    "Chicken",
    "Rice",
    "Pasta",
    "Fresh fruits (e.g., apples, bananas, oranges)",
    "Fresh vegetables (e.g., tomatoes, lettuce, carrots)",
    "Cheese",
    "Yogurt",
    "Cereal",
    "Butter",
    "Cooking oil",
    "Frozen vegetables",
    "Ground beef",
    "Coffee",
    "Tea",
    "Sugar",
    "Flour",
    "Snack items (e.g., chips, crackers)",
    "Canned goods (e.g., beans, tomatoes, soup)",
    "Peanut butter",
    "Jam or jelly",
    "Toilet paper",
    "Paper towels",
    "Cleaning supplies (e.g., dish soap, laundry detergent)",
    "Toothpaste",
    "Shampoo",
    "Soap",
    "Diapers (if applicable)",
    "Woolworths Select brand items",
    "Coles Own brand items",
    "Applesauce",
    "Almond milk",
    "Gluten-free products",
    "Quinoa",
    "Greek yogurt",
    "Soy sauce",
    "Hummus",
    "Avocado",
    "Salmon",
    "Baby formula",
    "Oatmeal",
    "Honey",
    "Maple syrup",
    "Granola",
    "Deli meats",
    "Coconut water",
    "Sparkling water",
    "Baby wipes",
    "Fabric softener",
    "Dishwasher detergent",
    "Fresh herbs (e.g., cilantro, parsley, basil)",
    "Sparkling water",
    "Gourmet cheese",
    "Artisanal bread",
    "Probiotic drinks",
    "Plant-based milk alternatives"
  ]
}
,
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
        error: null,
        shownlist:[],
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
        ],
        snackbar: false,
        snackbarError: false,
        snackbarTimeout: 2500
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
    async beforeMount() {
      await this.TokenPromise();
    },
    methods: {
      async OnCallSuggestion() {
        try {
          const response = await fetch(`${this.$GroceryAPI}/search_suggestions`);
          // Assuming the API returns a list of suggestions
          this.searchSuggestions = response.data.suggestions;
        } catch (error) {
          console.error("Error fetching suggestions:", error);
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
          }else {
            this.authenticated = true
            await this.fetchWeeklyDeals()
            
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
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
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
            const response = await fetch(`${this.$GroceryAPI}/search/${encodeURIComponent(productName)}/${encodeURIComponent(this.postalCode)}`, {
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
          console.log("Couldn't retrieve the items from the specific category");
        }
        this.loading=false;
        return products;
      },
      async fetchProducts() {
        this.loading = true;

        try {
          const response = await fetch(`${this.$GroceryAPI}/search/${encodeURIComponent(this.searchTerm)}/${encodeURIComponent(this.postalCode)}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });

          if (response.ok) {
            const data = await response.json();
            this.products = data;
          } else {
            this.error = response.statusText;
            this.snackbarError = true;
          }
        } catch (error) {
          this.error = "Error in retrieving data..."
          this.snackbarError = true;
        }

        this.loading = false;
      },
      bestStoreForProduct(product) {
        const storePrices = {
          'Woolworths': product.woolworths_price,
          'Coles': product.coles_price,
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
      async fetchWoolDeals() {
        try{
          const responseWoolies = await fetch(`${this.$GroceryAPI}/half-price-deals_woolies`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_w = await responseWoolies.json();
  
          this.weeklyDeals_w = this.weeklyDeals_w.slice(0, 6);
          this.$store.commit('setWeeklyDealsW', this.weeklyDeals_w);

          
        } catch (error) {
          this.error = "Failed to fetch Woolworths weekly deals: " + error;
          this.snackbarError = true;  
        } 
      },
      async fetchColesDeals() {
        try {
          const responseColes = await fetch(`${this.$GroceryAPI}/half-price-deals_coles`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_coles= await responseColes.json();
          this.weeklyDeals_coles = this.weeklyDeals_coles.slice(0, 6);
          this.$store.commit('setWeeklyDealsColes',  this.weeklyDeals_coles);
         
        } catch (error) {
          this.error = "Failed to fetch Coles weekly deals: " + error;
          this.snackbarError = true;          
        }
      },
      async fetchIGADeals() {
        try {
          const responseIga = await fetch(`${this.$GroceryAPI}/half-price-deals_iga`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_iga =  await responseIga.json();
          this.weeklyDeals_iga = this.weeklyDeals_iga.slice(0, 6); 
          this.$store.commit('setWeeklyDealsIGA', this.weeklyDeals_iga);
        } catch (error) {
          console.error('Failed to get the deals from iga')
        } 
      },
      selectRecommendation(recommendation) {
      // Implement logic when a recommendation is selected
      console.log(`Selected recommendation: ${recommendation}`);
      // You can close the recommendations or perform any other action here
      this.showRecommendations = false;
    },
    async getSearchRecommendations() {
      if (this.searchTerm.length > 3) {
        try {
          const response = await fetch(
            `${this.$GroceryAPI}/get-suggestions/${this.searchTerm}`
          );

          if (response.ok) {
            const data = await response.json();
            // Assuming the response structure has an array of suggestions
            this.shownlist = data.suggestions || [];
          } else {
            console.error('Error fetching search suggestions');
          }
        } catch (error) {
          console.error('Error fetching search suggestions', error);
        }
      } else {
        this.shownlist = [];
      }
    },
    
      async fetchWeeklyDeals() {

     
        this.weeklyDeals_w=this.$store.state.weeklyDealsW;
        this.weeklyDeals_iga=this.$store.state.weeklyDealsIGA;
        this.weeklyDeals_coles=this.$store.state.weeklyDealsColes;  
        this.loading_start = true;
        await this.fetchWoolDeals()
        await this.fetchColesDeals()
        await this.fetchIGADeals()
        this.loading_start= false;
        
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
          const response = await fetch(`${this.$GroceryAPI}/search/${category}/${encodeURIComponent(this.postalCode)}`, {
            method: 'GET', // or 'POST' or other HTTP methods
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json', // Adjust the content type if needed
              // Add other headers as needed
            },
          }); 
          
          this.weeklyDeals_iga = await response.json();
          this.weeklyDeals_iga = this.weeklyDeals_iga.slice(0, 6); 
          this.products = await response.json();
          // Process and use the data as needed
        } catch (error) {
          console.error('Error fetching data:', error);
        }
      },
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
    .snackbar-custom-style {
  margin-bottom: 76px; /* Adjust the margin to fit the height of the browser's controls */
}
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