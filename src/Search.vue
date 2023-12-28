<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
    <v-container fluid>
      <div class="mx-3">
      <!-- Modal -->
      <div class="bg-dark mx-auto position-fixed top-25 m-3" style="top:20%; left: 0; right: 0; margin:auto; z-index: 20;" v-show="barshow">
  <div class="w-100 text-center p-4 ">
    <v-progress-linear
            :value="counterStatus*20"
            height="4"
            
            color="green"
            background-color="white"
          ></v-progress-linear>
    <div id="barcode_canvas" class="scanner-box w-100 overflow-hidden" style="max-height: 300px;"></div>
    <button class="btn btn-block w-100 bg-danger text-white fw-bold p-4" @click="stopBar()">Cancel Scan</button>
  </div>
</div>
        <h1 class="fw-bold">What's new?</h1>
        <p class="fw-bold" >Save Heaps on Groceries by Comparing deals from <span class="text-success">Woolworths</span>, <span class="text-danger">Coles</span> and <span class="text-white bg-danger p-1">IGA</span></p>
        <p class="fw-bold text-danger">
        <v-icon large color="red">mdi-piggy-bank</v-icon> <span class="text-success" v-if="savingload">{{ saving }}</span>
        <span class="spinner-border spinner-border-sm text-danger" v-else></span> AUD Saved this Month...</p>
      </div>
      <div style="position: relative;">
      <v-row align="center" class="my-5 align-item-center">
      <v-col cols="7" md="8" lg="6">
        <v-text-field
          v-model="searchTerm"
          @keydown.enter="fetchProducts"
          @input="getSearchRecommendations"
          @focus="savingload =true"
          label="Search your grocery item"
          class="fw-bold"
          filled
          prepend-inner-icon="mdi-magnify"
          solo
          flat
          outlined
          hide-details="true"
        ></v-text-field>
      </v-col>
      <v-col class="d-sm-none" cols="3" md="1" lg="1">  <button @click="initScanner()" style="border:3px solid black; border-radius:30px; width:60px; height:60px;" type="button" >
      <v-icon class="text-dark fw-bold">mdi-barcode-scan</v-icon>
    </button></v-col>
      <v-col cols="1" md="1" lg="1">
        <v-menu  offset-y :close-on-content-click="false">
            <template v-slot:activator="{ on, attrs }">
              <v-span fab v-on="on" v-bind="attrs"  ><img src="@/assets/filter.png" style="width:30px" alt="Filter Icon" /> </v-span>            
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
      <v-container fluid class="py-0 px-0 my-3"  v-if="membership">
         <div class="fw-bold p-3 bg-danger my-3 text-white">
          <h5 class="fw-bold">Your Free Trial has Expired</h5>
          <p>To continue using supersavers, you must choose a subscription. You can manage your subscription <a href="/subscription">here</a></p>
         </div>
      </v-container>
      <v-container class="py-0 px-0 position-absolute" style="z-index:3; top: 90%;" v-if="(shownlist.length > 1) && savingload">
          <v-list class="shadow-lg">
            <v-list-item v-for="recommendation in shownlist" :key="recommendation">
              <v-list-item-content class="hover p-3" @click="selectRecommendation(recommendation)">
                {{ recommendation }}
              </v-list-item-content>
            </v-list-item>
          </v-list>
      </v-container>
    </v-row>
  </div>
      <v-app-bar color="transparent" flat class="">
        <v-tabs v-model="tab" stacked style="height:auto" active-class="custom-active-tab">
    <v-tab  style="height:auto" v-for="(tab, index) in tabs" :key="index" :value="'tab-' + (index + 1)" @click="handleTabClick(tab.name)">
      <v-img style="max-width:40px" class="mx-auto d-block" :src="require(`@/assets/${tab.icon}`)"></v-img><v-span class="fw-bold" >{{ tab.name }}</v-span>
    </v-tab>
    <v-tabs-slider color="transparent"></v-tabs-slider>
  </v-tabs>
 
      </v-app-bar>
   
      <v-divider class="my-5" color="grey" v-if="!loading"></v-divider>
      <!-- Progress linear -->
      <v-progress-linear class="my-2"  v-if="loading"
        :height="4"
        color="green"
        indeterminate
      ></v-progress-linear>
      <div v-show="showButtons" class="" >
        <h2 class="fw-bold ">Top finds at Stores</h2>
        <div>
        <v-row class="text-center align-items-center justify-center my-0 py-0" >
  <v-col cols="4">
    <a v-if="IGAproducts.length > 0" href="#iga-top-finds" :to="{ path: '/search', hash: '#iga-top-finds' }" class=" d-block text-white py-2 px-2 fw-bold ">
      <h4 class="fw-bold bg-danger text-white p-3">IGA</h4>
    </a>
  </v-col>
  <v-col cols="4">
    <a v-if="Woolproducts.length > 0" href="#woolworths-top-finds" :to="{ path: '/search', hash: '#woolworths-top-finds' }" class="text-success fw-bold  px-2 ">
      <h4 class="fw-bold">Woolworths</h4>
    </a>
  </v-col>
  <v-col cols="4">
    <a v-if="Colesproducts.length > 0" href="#coles-top-finds" :to="{ path: '/search', hash: '#coles-top-finds' }" class="px-2 text-danger  fw-bold ">
      <h4 class="fw-bold">Coles</h4>
    </a>
  </v-col>
</v-row>
</div>


    </div>
      <div fluid v-if="lowestPricedProduct" class="my-5 py-3 text-center-sm text-left-md">
        <h2 class="my-2 fw-bold bg-success text-white p-3">Lowest product found</h2>
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
              <v-card-title class="display-6 py-0" style="display: inline-block; word-break: break-word;">
               <p class="fw-bold">{{ lowestPricedProduct.description.replace(/<[^>]*>/g, ' ') }}</p>
              </v-card-title>
              <v-card-title class="display-6 font-weight-bold green--text py-0]">
                ${{ smallestPrice(lowestPricedProduct) }} /
                {{ lowestPricedProduct.size }}
              </v-card-title>
              <v-card-title class="fw-bold">
                Deal Available At 
                <strong style="display: inline-block; word-break: break-word;" :class="{ 'text-success': bestStoreForProduct(lowestPricedProduct).includes('Woolworths'), 'text-danger': bestStoreForProduct(lowestPricedProduct).includes('Coles') , 'bg-danger p-3 text-white': bestStoreForProduct(lowestPricedProduct).includes('IGA') }">{{ bestStoreForProduct(lowestPricedProduct) }}</strong>
              </v-card-title>
            </v-col>
          </v-row>
      </div>
      <!-- Best deal at Woolworths and Coles -->
    
      <div v-if="combinedProducts.length" class="my-4"> 
        <v-row>
          <v-col cols="12">
            <p class="bg-dark p-3 text-white fw-bold">Note that supersavers can make mistakes</p>
            <h2 class="bg-success p-3 text-white fw-bold" >Best Prices Across Stores</h2>
          </v-col>
          <v-col
            cols="12"
            xs="12"
            sm="6"
            md="4"
            lg="4"
            v-for="product in combinedProducts" 
            :key="product.name">
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
          <!-- Woolworths Products -->
          
      <div class="my-5 " >
      <br>
    <!-- Woolworths Products -->
    <h3 v-if="Woolproducts.length > 0" id="woolworths-top-finds" class="fw-bold mt-5 mx-3 mb-3">Top finds from <span class="text-success">Woolworths</span></h3>
    <v-row>
      <v-col v-for="product in Woolproducts.slice(0, 4)" :key="product.name" cols="6" sm="6" md="4" lg="3">
        <v-card>
          <v-img :src="product.image" class="mx-auto" width="90%" height="200"></v-img>
          <v-card-title class="fw-bold" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          {{ product.name }}
          </v-card-title>

          <v-card-subtitle class="fw-bold text-success" v-if="product.woolworths_price">{{ ` AUD $${product.woolworths_price}` }}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- Coles Products -->
    <h3 v-if="Colesproducts.length > 0" id="coles-top-finds" class="fw-bold mt-5 mb-3 mx-3">Top finds from <span class="text-danger">Coles</span></h3>
    <v-row>
      <v-col v-for="product in Colesproducts.slice(0, 4)" :key="product.name" cols="6" sm="6" md="4" lg="3">
        <v-card>
          <v-img :src="product.image" class="mx-auto" width="90%"  height="200"></v-img>
          <v-card-title class="fw-bold" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          {{ product.name }}
          </v-card-title>
          <v-card-subtitle class="fw-bold text-success" v-if="product.coles_price">{{ `AUD $${product.coles_price}` }}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>

    <!-- IGA Products -->
    <h3 v-if="IGAproducts.length > 0" id="iga-top-finds" class="fw-bold mt-5 mb-3 mx-3">Top finds from <span class="text-white bg-danger p-1">IGA</span></h3>
    <v-row>
      <v-col v-for="product in IGAproducts.slice(0, 4)" :key="product.name" cols="6" sm="6" md="4" lg="3">
        <v-card>
          <v-img :src="product.image"  class="mx-auto" width="90%" height="200"></v-img>
          <v-card-title class="fw-bold" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
          {{ product.name }}
          </v-card-title>
          <v-card-subtitle class="fw-bold text-success" v-if="product.iga_price">{{ `AUD $${product.iga_price}` }}</v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </div>

      <Toast ref="Toast" />
    </v-container>
    <!--LOOKUP-->



  </v-app>
</template>

<script>
  import DealsCard from './components/DealsCard.vue';
  import SearchCard from './components/SearchCard.vue';
  import Toast from './components/Toast.vue';
  import Quagga from 'quagga';
  

  export default {
    metaInfo: {
  // Page Title
  title: 'Supersavers | Search and Save on Groceries',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Search for anything and compare prices directly with Coles, Woolworths, and IGA. View exclusive deals, add items to your grocery list, and get notified about the latest savings. Supersavers helps you save heaps on groceries!' }, // Page description
    { name: 'keywords', content: 'Supersavers, search, compare prices, groceries, exclusive deals, savings, grocery list, notifications, Coles, Woolworths, IGA' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | Search and Save on Groceries' }, // Open Graph title
    { property: 'og:description', content: 'Search for anything and compare prices directly with Coles, Woolworths, and IGA. View exclusive deals, add items to your grocery list, and get notified about the latest savings. Supersavers helps you save heaps on groceries!' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/search' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | Search and Save on Groceries' }, // Twitter title
    { name: 'twitter:description', content: 'Search for anything and compare prices directly with Coles, Woolworths, and IGA. View exclusive deals, add items to your grocery list, and get notified about the latest savings. Supersavers helps you save heaps on groceries!' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

    data() {
      return {
        barshow:false,
        productsLookup:[],
        membership:false,
        counterStatus:0,
        scannedBarcode: null,
        savingload: false,
        saving:0,
        authenticated:false,
        loading: false,
        loading_start:true,
        showButtons:false,
        storeFilters: {
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
        error: null,
        shownlist:[],
        // searchClosed: true, -> search field open and close
        selection:1,
        tab: null,
        tabs: [
        
          { name: 'Deals', icon: 'deal.png' },
          { name: 'All', icon: 'shopping-bag.png' },
          { name: 'Fruits', icon: 'fruit.png' },
          { name: 'Vegetables', icon: 'vegetable.png' },
          { name: 'Breakfast', icon: 'cereal.png' },
          { name: 'Frozen Foods', icon: 'pizza.png' },
          { name: 'Dairy', icon: 'milk.png' },
          { name: 'Egg', icon: 'egg.png' },
          { name: 'Meat', icon: 'chicken.png' },
          { name: 'Seafood', icon: 'crab.png' },
          { name: 'Snacks', icon: 'chips.png' },
          { name: 'Personal care', icon: 'toothpaste.png' }
         
         
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
      Woolproducts() {
        return this.productsLookup.filter(item => item.source === "Woolworths");

      },
      Colesproducts() {
        return this.productsLookup.filter(item => item.source === "Coles");
      },
      IGAproducts() {
        return this.productsLookup.filter(item => item.source === "IGA");
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
        if (!this.products.length) return null;
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

    async beforeMount() {
      
      try {
        await Promise.all([
            this.getUserLocation(),
            this.TokenPromise(),
            
        ]);
        } catch (error) {
            console.error('Error:', error);
            // Handle errors as needed
        }
    },
    methods: {
      async SubscriptionCheck() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/valid_subscription`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });

        if (!response.ok) {
        this.membership=true
      } 
    } catch (error) {
        console.error('Something went wrong with your subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong when accessing our server', 'red', 'mdi-alert-circle');
    }
    },
      async initScanner() {
      this.barshow =true;
  // Ensure the target element exists
  const targetElement = document.querySelector('#barcode_canvas');


  // Initialize Quagga
Quagga.init({
  inputStream: {
    name: 'Live',
    type: 'LiveStream',
    target: targetElement,
    constraints: {
      facingMode: 'environment', // or 'user'
      width: { ideal: 640 },
  height: { ideal: 480 }
    },
    area: {
        top: "0%",
        right: "0%",
        left: "0%",
        bottom: "0%"
    },
  },
  decoder: {
    readers: ['ean_reader'],
    debug: {
      drawScanline: true,
      showPattern: true,
    },
    multiple: false,
  },
  locator: {
    patchSize: 'medium',
    halfSample: false,
  },
  numOfWorkers: navigator.hardwareConcurrency || 4,
  frequency: 10,
  locate: true,
}, (err) => {
  if (err) {
    console.error(err);
    return;
  }

  // Customize the scan box styles
  const scanBox = document.querySelector('.drawingBuffer');

  if (scanBox) {
  scanBox.classList.add('scanner-box');
}


  // Quagga initialization successful, start the live stream
  Quagga.start();
// Initialize a map to store code frequencies
const codeFrequencyMap = new Map();

// Initialize a counter to keep track of the number of detections
let detectionCounter = 0;



Quagga.onDetected((result) => {

  if (this.loading) {
    return;
  }
  
  // Increment detection counter
  detectionCounter++;
  this.counterStatus = detectionCounter

  // Get the detected code
  const code = result.codeResult.code;
  console.log(code);

  // Update code frequency in the map
  if (codeFrequencyMap.has(code)) {
    codeFrequencyMap.set(code, codeFrequencyMap.get(code) + 1);
  } else {
    codeFrequencyMap.set(code, 1);
  }

  // Check if 20 detections have been reached
  if (detectionCounter >= 5) {
    // Find the code with the highest frequency
    let maxFrequency = 0;
    let mostFrequentCode;
    codeFrequencyMap.forEach((frequency, currentCode) => {
      if (frequency > maxFrequency) {
        maxFrequency = frequency;
        mostFrequentCode = currentCode;
      }
    });

    // Optionally, stop Quagga to prevent further detections
    Quagga.stop();

    // Call your handling function with the most frequent code
    this.handleBarcode(mostFrequentCode);

    // Reset counters
    detectionCounter = 0;
    this.counterStatus = 0;
    codeFrequencyMap.clear();
  }
});




});

// Add CSS for the scanner animation
const style = document.createElement('style');
style.innerHTML = `
  @keyframes scanner-animation {
    0% { background-position: 0 0; }
    100% { background-position: 100% 100%; }
  }
`;
document.head.appendChild(style);

},
async handleBarcode(code) {
  this.loading=true
  this.scannedBarcode = code;
  this.$refs.Toast.showSnackbar('Barcode was scanned. Now checking if it is correct', 'green', 'mdi-check-circle');
  this.stopBar()
  try {
          const response = await fetch(`${this.$GroceryAPI}/barcode/${encodeURIComponent(this.scannedBarcode)}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          if (response.ok) {
            const data = await response.json();
    if (data.Products && data.Products.length > 0) {
        const productName = data.Products[0].Name;
        const firstThreeWords = productName.split(' ').slice(0, 4).join(' ');
        this.searchTerm = firstThreeWords + " " + data.Products[0].PackageSize ;
    }
          await this.fetchProducts();
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar("Something went wrong with the barcode search", 'red', 'mdi-alert-circle');
  } 
 
},
    async OnCallSuggestion() {
        try {
          const response = await fetch(`${this.$GroceryAPI}/search_suggestions`);
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
              this.authenticated=true
              await this.Saving()
              await this.SubscriptionCheck()
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
              await this.fetchWeeklyDeals()
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
          let responses;
          this.showButtons=false
          try {
              // Use Promise.all to run the promises concurrently
              responses = await Promise.all(
                  productNames.map(async (productName) => {
                      const response = await fetch(`${this.$GroceryAPI}/search/${encodeURIComponent(productName)}/${encodeURIComponent(this.postalCode)}`, {
                          method: 'GET',
                          headers: {
                              'Authorization': `Bearer ${this.AuthToken}`,
                              'Content-Type': 'application/json',
                          },
                      });

                      return response;
                  })
              );

              // Process the responses
              for (const response of responses) {
                  if (response.ok) {
                      products.push(...(await response.json()));
                  } else {
                      this.$refs.Toast.showSnackbar('The server rejected your request. Perhaps try reloading the site', 'red', 'mdi-alert-circle');
                  }
              }
          } catch (error) {
              console.error("Couldn't retrieve the items from that specific category:", error);
              this.$refs.Toast.showSnackbar('Something went wrong retrieving the products. Try again later', 'red', 'mdi-alert-circle');
          }

          this.loading = false;
          this.productsLookup = []
          this.products = products; // Set the products after all responses have been processed
          this.storeFilters['Deals At Woolies'] = false;
          this.storeFilters['Deals At Coles'] = false;
          this.storeFilters['Deals At IGA'] = false;

          return products;
      },
      async fetchProducts() {
        try {
          this.loading = true;
          this.showButtons = false;
          this.savingload = false;
          this.shownlist = [];
          const response = await fetch(`${this.$GroceryAPI}/search/${encodeURIComponent(this.searchTerm)}/${encodeURIComponent(this.postalCode)}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          if (response.ok) {
            const data = await response.json();
            this.products = data;
            this.loading = false;
            await this.fetchLookup()
            
           
          } else {
            const errorData = await response.json();
            this.$refs.Toast.showSnackbar('Error: '+errorData.detail, 'red', 'mdi-alert-circle');
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar("Error in retrieving data...", 'red', 'mdi-alert-circle');
        } 
      },
      async fetchLookup() {
      try {
        const response = await fetch(`${this.$GroceryAPI}/quick/lookup/${encodeURIComponent(this.searchTerm)}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });

        if (response.ok) {
          const data = await response.json();

          // Assuming data is an array with three categories [Woolworths, Coles, IGA]
          this.productsLookup = [
            ...data[0].slice(0, 5), // Add the first 5 Woolworths products
            ...data[1].slice(0, 5), // Add the first 5 Coles products
            ...data[2].slice(0, 5), // Add the first 5 IGA products
          ];
          this.showButtons = true
        }
      } catch (error) {
        console.error(error);
      }
    },
      bestStoreForProduct(product) {
        const storePrices = {
          'Woolworths': product.woolworths_price,
          'Coles': product.coles_price,
          'IGA': product.iga_price,
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
      async Saving() {
        try {
          const response = await fetch(`${this.$GroceryAPI}/retrieve_saving_user`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
          },
        });
        if (response.ok) {
            const data = await response.json()
            this.saving= data.amount
            this.savingload = true; 
        } else {
            console.error('Error:', response.statusText);
            this.$refs.Toast.showSnackbar("Server rejected your request. Please reload the site", 'red', 'mdi-alert-circle');
        }
      } catch (error) {
        console.error('Error:', error);
        this.$refs.Toast.showSnackbar("Something went wrong when retrieving the savings", 'red', 'mdi-alert-circle');
      }
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
          if (responseWoolies.ok) {
          this.weeklyDeals_w = await responseWoolies.json();
          this.weeklyDeals_w = this.weeklyDeals_w.slice(0, 6);
          this.$store.commit('setWeeklyDealsW', this.weeklyDeals_w);
          }else {
            console.log(responseWoolies);
          }
        } catch (error) {
           this.$refs.Toast.showSnackbar('Something went wrong fetching deals from Woolworths', 'red', 'mdi-alert-circle');
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
          if (responseColes.ok) {
          this.weeklyDeals_coles= await responseColes.json();
          this.weeklyDeals_coles = this.weeklyDeals_coles.slice(0, 6);
          this.$store.commit('setWeeklyDealsColes',  this.weeklyDeals_coles);
          }else {
            console.log(responseColes);
          }
        } catch (error) {      
          this.$refs.Toast.showSnackbar('Something went wrong when fetching deals from Coles', 'red', 'mdi-alert-circle');
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
          if (responseIga.ok) {
          this.weeklyDeals_iga =  await responseIga.json();
          this.weeklyDeals_iga = this.weeklyDeals_iga.slice(0, 6); 
          this.$store.commit('setWeeklyDealsIGA', this.weeklyDeals_iga);
          } else {
            console.log(responseIga);
          }
        } catch (error) {
          this.$refs.Toast.showSnackbar('Something went wrong when fetching deals from IGA', 'red', 'mdi-alert-circle');
        } 
      },
      async selectRecommendation(recommendation) {
      this.savingload=false
      this.searchTerm = recommendation;
      await this.fetchProducts();
      },
      async getSearchRecommendations() {
     
      if (this.searchTerm.length > 0) {
        this.savingload = true
        try {
          const response = await fetch(
            `${this.$GroceryAPI}/get-suggestions/${this.searchTerm}`
          );
          if (response.ok) {
            const data = await response.json();
            this.shownlist = data.suggestions.suggestions.slice(0,5) || [];
          } else {
            console.error('Error fetching search suggestions');
          }
        } catch (error) {
          console.error('Error fetching search suggestions', error);
        }
      } else {
        this.shownlist = [];
        this.savingload = false
      }
      },
      async fetchWeeklyDeals() {
        this.weeklyDeals_w=this.$store.state.weeklyDealsW;
        this.weeklyDeals_iga=this.$store.state.weeklyDealsIGA;
        this.weeklyDeals_coles=this.$store.state.weeklyDealsColes;  
        this.loading_start = true;
        try {
        // Use Promise.all to execute the promises concurrently
        await Promise.all([
            this.fetchWoolDeals(),
            this.fetchColesDeals(),
            this.fetchIGADeals()
        ]);
        } catch (error) {
            console.error('Error fetching weekly deals:', error);
            // Handle error as needed
        } finally {
            this.loading_start = false;
        } 
      },
      getLowestPrice() {
        return this.lowestPricedProduct;
      },
      async getUserLocation() {
        try {
          if ('geolocation' in navigator) {
            const position = await this.getCurrentPosition();
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
          const response = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`);
          const data = await response.json();
          if (data.address && data.address.postcode) {
            this.postalCode = data.address.postcode;
          }
        } catch (error) {
          console.error('Error retrieving postal code:', error);
        }
      },
      stopBar () {
        this.counterStatus = 0
        this.barshow =false;
        Quagga.stop()
      }
    },
    beforeDestroy() {
    Quagga.stop();
    },
    
    components: {
      SearchCard,
      DealsCard,
      Toast
    }
  };
</script>

<style>

.custom-active-tab {
  color: green; /* Change to your desired active tab text color */
}


  .container {
    width: 100%;
    padding-left: 100px;
    margin-right: auto;
    margin-left: auto;
    padding-right: 50px;
  
  }
  .hover:hover {
    background-color:#aaaaaa;
  }

  @media (max-width: 701px) {
  .snackbar-custom-style {
  margin-bottom: 76px; /* Adjust the margin to fit the height of the browser's controls */
  }
  .container {
      padding-left: 15px;
      padding-right: 15px;
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
    color: rgb(0, 0, 0) !important;
    background-color: rgb(151, 151, 151) !important;
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