<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <!-- Top App Bar -->
    <v-app-bar app clipped-left color="green darken-2" dark dense>
      <v-toolbar-title class="pa-3">Alpha</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-text-field 
        v-model="searchTerm" 
        hide-details 
        single-line 
        outlined 
        dense 
      
        @change="fetchProducts()"
        label="Search for a product"  
        clearable>
      </v-text-field>
 
      <!-- Display Search Suggestions -->
      <div>
        <ul></ul>
      </div>
      <!-- Notification Icon with Dropdown -->
      <v-menu offset-y dense>
        <v-list dense></v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <v-navigation-drawer clipped app width="300">
        <v-container>
          <v-list nav dense>
            <v-subheader class="green--text text--darken-2 pa-2">Grocery Plan</v-subheader>
            <v-divider></v-divider>
             <v-alert small type="success">
    With Grocery Planner, you can plan your trip so you can save on the best deals when going for groceries
  </v-alert>
            <!-- Display Coles Products First -->
            <v-subheader v-if="colesGroceryList.length!=0">First Stop to Coles</v-subheader>
            <v-list-item-group>
              <v-list-item v-for="(item,index) in colesGroceryList" :key="item.id">
                <v-list-item-content>
                <v-row class="container">
                <v-col cols="4" md="4">
                <v-img :src="item.image"></v-img>
                </v-col>
                <v-col cols="8" md="8">
                  <v-list-item-title>
                    x{{ item.counter }} - {{ item.name }} 
                    <span v-if="item.counter && item.counter > 1"></span>
                  </v-list-item-title>
                  <v-list-item-title class="ma-2 green--text">
                    Save atleast ${{ item.savings }} for this item
                  </v-list-item-title>
                  <v-list-item-action>
                  <v-row>
                  <v-col cols="6">
                 <v-icon color="success"  @click="Completed(index)" >mdi-check-circle</v-icon> </v-col><v-col cols="6">  <v-icon @click="removeItemFromCart(index)" color="red">mdi-delete</v-icon></v-col>
                 </v-row>
                  </v-list-item-action>
                    </v-col>
                </v-row></v-list-item-action>
                   </v-col>
                </v-row>
                </v-list-item-content>
               
              </v-list-item>
            </v-list-item-group>
            <v-divider></v-divider>
                 <v-subheader v-if="IGAGroceryList.length!=0">Next at IGA</v-subheader>
            <v-list-item-group>
              <v-list-item v-for="(item,index) in IGAGroceryList" :key="item.id">
                <v-list-item-content>
                   <v-row class="container">
                <v-col cols="4" md="4">
                <v-img :src="item.image"></v-img>
                </v-col>
                 <v-col cols="8" md="8">
                  <v-list-item-title>
                    x{{ item.counter }} - {{ item.name }} 
                    <span v-if="item.counter && item.counter > 1"></span>
                  </v-list-item-title>
                  <v-list-item-title class="ma-2 green--text">
                    Save atleast ${{ item.savings }} for this item
                  </v-list-item-title>
                  <v-list-item-action>
                  <v-row>
                  <v-col cols="6">
                 <v-icon color="success"  @click="Completed(index)" >mdi-check-circle</v-icon> </v-col><v-col cols="6">  <v-icon @click="removeItemFromCart(index)" color="red">mdi-delete</v-icon></v-col>
                 </v-row>
                  </v-list-item-action>
                    </v-col>
                </v-row> </v-list-item-action>
                   </v-col>
                </v-row>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
            <v-divider></v-divider>
            <!-- Display Woolworths Products -->
            <v-subheader v-if="woolworthsGroceryList.length!=0" >Drive to Woolworths</v-subheader>
            <v-list-item-group>
              <v-list-item v-for="(item,index) in woolworthsGroceryList" :key="item.id">
                <v-list-item-content>
                    <v-row class="container">
                <v-col cols="4" md="4">
                <v-img :src="item.image"></v-img>
                </v-col>
                 <v-col cols="8" md="8">
                  <v-list-item-title>
                    x{{ item.counter }} - {{ item.name }} 
                    <span v-if="item.counter && item.counter > 1"></span>
                  </v-list-item-title>
                  <v-list-item-title class="ma-2 green--text">
                    Save atleast ${{ item.savings }} for this item
                  </v-list-item-title>
                  <v-list-item-action>
                  <v-row>
                  <v-col cols="6">
                 <v-icon color="success"  @click="Completed(index)" >mdi-check-circle</v-icon> </v-col><v-col cols="6">  <v-icon @click="removeItemFromCart(index)" color="red">mdi-delete</v-icon></v-col>
                 </v-row>
                  </v-list-item-action>
                    </v-col>
                </v-row>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
             <v-divider></v-divider>
        
            <v-subheader v-if="completed.length!=0" >Completed Groceries</v-subheader>
            <v-list-item-group>
              <v-list-item v-for="(item,index) in completed" :key="item.id">
                <v-list-item-content>
                    <v-row class="container">
                <v-col cols="4" md="4">
                <v-img :src="item.image"></v-img>
                </v-col>
                 <v-col cols="8" md="8">
                  <v-list-item-title>
                    x{{ item.counter }} - {{ item.name }} 
                    <span v-if="item.counter && item.counter > 1"></span>
                  </v-list-item-title>
            
                 
                 </v-col>
                </v-row>
                </v-list-item-content>
                
              </v-list-item>
              
            </v-list-item-group>
            <v-divider></v-divider>
            <!-- Display total savings here -->
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title class="green--text">Total Savings: ${{ savings }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-container>
      </v-navigation-drawer>
    
      <!-- Search bar -->
      <v-container>
       <v-container>
  <div style="overflow-x: auto; white-space: nowrap;">
    <v-chip 
      small strong 
      outlined 
      class="elevation-1 mx-2 rounded transition-shadow" 
      v-for="(value, key) in storeFilters" 
      :key="key"
    >
      <strong>
        <v-checkbox 
          v-model="storeFilters[key]" 
          small 
          :label="key.charAt(0).toUpperCase() + key.slice(1)">
        </v-checkbox>
      </strong>
    </v-chip>
  </div>
</v-container>


<v-container v-if="lowestPricedProduct" class="my-4">
  <h2 class="my-2">Lowest product found</h2>
  <v-alert type="success">
    Note that, you need to type in the specific product you are looking for to get the most affordable item
  </v-alert>
  <v-row align="center" class="my-1 p-0">
    <!-- Product Image -->
    <v-col cols="12" md="4">
      <v-img :src="lowestPricedProduct.image" width="300" contain></v-img>
    </v-col>

    <!-- Product Information -->
    <v-col cols="12" md="7">
      <v-card-title class="display-1">
        <strong>{{ lowestPricedProduct.name }}</strong>
      </v-card-title>
      <v-card-title class="display-6 green--text">
        ${{ smallestPrice(lowestPricedProduct) }} / {{ lowestPricedProduct.size }}
      </v-card-title>
      <v-container>
        <v-btn  @click="addProductToGrocery(lowestPricedProduct)" color="success">
          Add to Grocery
        </v-btn>
      </v-container>
      <v-card-title>
        <strong>Deal Available At {{ bestStoreForProduct(lowestPricedProduct) }}</strong>
      </v-card-title>
    </v-col>
  </v-row>
</v-container>



        <v-container v-if="loading_start" class="mt-5 pt-5 text-center">
          <v-row>
  <v-col cols="6" md="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
     <v-col cols="6" sm="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
     <v-col cols="6" sm="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
     <v-col cols="6" sm="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
    <v-col cols="6" sm="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
     <v-col cols="6" sm="2">
      <v-skeleton-loader type="card"></v-skeleton-loader>
    </v-col>
  </v-row>
   
</v-container>

  <v-container  v-if="loading" class="mt-5 pt-5 text-center">
    <v-progress-circular
        :size="70"
        :width="7"
        color="green"
        indeterminate
    ></v-progress-circular>
    <v-card-text class="my-3" color="green">Analysing and retrieving the best products</v-card-text>
   </v-container>



</v-container>


    <!-- Display combined products at the top -->
    <v-container v-if="combinedProducts.length" class="m-2">
     <v-col cols="12">
            <h2>Best Deals | Woolies V Coles</h2>
            <v-text>Comparing between extremely similar products or the same product at Woolies and Coles</v-text>
          </v-col>
<v-row>
  <v-col v-for="product in combinedProducts" :key="product.name"  cols="6" md="3">
<v-card class="elevation-2e mb-3">
    <!-- Product Image and Add Button -->
    <v-img :src="product.image" height="150" class="position-relative">
        <v-btn
            class="position-absolute top-0 right-0 mt-2 mr-2"
            icon
            @click="addProductToGrocery(product)"
            color="green accent-3"
            dark
        >
            <v-icon>mdi-plus</v-icon>
        </v-btn>
    </v-img>

    <!-- Product Name -->
    <v-card-text class="pl-4 pr-4 pt-2 pb-0 truncate-text">
    <strong>
        {{ product.name }}
        </strong>
        <br>
      
    </v-card-text>

    <v-card-text>
  
 
<v-chip label outlined v-if="product.woolworths_price || product.coles_price">
  <span v-if="product.woolworths_price <= product.coles_price" class="green--text py-0">
    Woolies ${{ product.woolworths_price }}
  </span>
  <span v-else class="red--text py-0">
    Woolies ${{ product.woolworths_price }}
  </span>
  <span v-if="product.coles_price <= product.woolworths_price" class="ml-2 my-2 green--text py-0">
    Coles ${{ product.coles_price }}
  </span>
  <span v-else class="ml-2 red--text py-0">
    Coles ${{ product.coles_price }}
  </span>
</v-chip>


<br>
<br>

          <v-chip class="" outlined small>PER {{ product.size }}</v-chip>
  </v-card-text>

</v-card>

  </v-col>
</v-row>

    </v-container>

    <!-- Display exclusive products for each store -->
    <v-container v-for="store in filteredExclusiveStores" :key="store.name">

        <v-row v-if="store.products">
          <v-col cols="12">
            <h2>Compare at {{ store.name }}</h2>
          </v-col>
        </v-row>
        <v-row>
          <v-col v-for="product in store.products" :key="product.name" cols="6" md="2">
            <!-- Product Card for exclusive products -->
            <v-card class="elevation-4 transition-shadow hover:shadow-lg">
                        <v-card class="elevation-4 transition-shadow hover:shadow-lg">
            <v-img :src="product.image" height="100" class="position-relative">
                    <v-btn
            class="position-absolute top-0 right-0 mt-2 mr-2"
            icon
            @click="addProductToGrocery(product)"
            color="green accent-3"
            dark
        >
            <v-icon>mdi-plus</v-icon>
        </v-btn>
              
            </v-img>
       <v-card-text class="blue-grey darken-1 white--text truncate-text">
    {{product.size}} | {{ product.name }} 
</v-card-text>

             <v-card-text class="green white--text truncate-text" col="6" v-if="product.woolworths_price" >Woolies: ${{ product.woolworths_price }}</v-card-text>
             <v-card-text class="red white--text truncate-text" col="6" v-if="product.coles_price" >Coles: ${{ product.coles_price }}</v-card-text>
             <v-card-text class="blue white--text truncate-text" col="6" v-if="product.aldi_price" >Aldi: ${{ product.aldi_price }}</v-card-text>
             <v-card-text class="black white--text truncate-text" col="6" v-if="product.iga_price">IGA: ${{ product.iga_price }}</v-card-text>
             <v-card-text class="purple white--text truncate-text" col="6" v-if="product.chemist_price">Chemist: ${{ product.chemist_price }}</v-card-text>
           
       
          
        </v-card>
            </v-card>
          </v-col>
        </v-row>
       

      </v-container>
<v-container v-if="weeklyDeals_w.length && storeFilters.WoolMania" class="m-2">
    <v-row>
        <v-col cols="12">
            <h2>Crazy Deals at Woolies</h2>
        </v-col>

        <v-col v-for="deal in weeklyDeals_w" :key="deal.name" cols="6" md="2">
            <v-card class="rounded elevation-2 mt-3 transition-shadow hover:shadow-lg">
                <v-img :src="deal.image" height="150" class="product-image position-relative">
                    <v-col class="fill-height" align="center" justify="center"> <!-- Flex utility classes for centering -->
                        <!-- This is empty, so you might want to add some content or remove this -->
                    </v-col>
                </v-img>
                <v-card-text class=" truncate-text">
                    {{ deal.size }} | {{ deal.name }}
                </v-card-text>
                <v-row class="my-0 pt-0">
    <v-col cols="12" md="6">
        <v-card-title v-if="deal.woolworths_price" class="green--text py-0">
           Now ${{ deal.woolworths_price }}  
        </v-card-title>
    </v-col>
    <v-col cols="12" md="6">
        <v-card-text class="red--text py-0">
            was ${{ deal.coles_price }}
        </v-card-text>
    </v-col>
</v-row>

            </v-card>
        </v-col>
    </v-row>
</v-container>

    <v-container v-if="weeklyDeals_iga.length && storeFilters.IGADeals" class="m-2">
     <v-col cols="12">
            <h2>Crazy Deals at IGA</h2>
     </v-col>
     <v-row>
         <v-col v-for="deal in weeklyDeals_iga" :key="deal.name" cols="12" md="2">
   <v-card class="rounded elevation-2 mt-3 transition-shadow hover:shadow-lg">
                <v-img :src="deal.image" height="150" class="product-image position-relative">
                    <v-col class="fill-height" align="center" justify="center"> <!-- Flex utility classes for centering -->
                        <!-- This is empty, so you might want to add some content or remove this -->
                    </v-col>
                </v-img>
                <v-card-text class=" truncate-text">
                    {{ deal.size }} | {{ deal.name }}
                </v-card-text>
                <v-row align="center" class="my-0 pt-0">
 <v-col cols="12" md="6">
        <v-card-title v-if="deal.iga_price" class="green--text py-0">
           Now ${{ deal.woolworths_price }}  
        </v-card-title>
    </v-col>
    <v-col cols="12" md="6">
        <v-card-text class="red--text py-0">
            was ${{ deal.coles_price }}
        </v-card-text>
    </v-col>
</v-row>

            </v-card>

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
      loading: false,
      loading_start:true,
      storeFilters: {
      woolies: true,
      iga: true,
      chemist: true,
      aldi: true,
      coles: true,
      WoolMania: true,
      IGADeals: true,
      
    },
      searchTerm: '',
      postalCode: null,
      searchSuggestions:[],
      products: [],
      completed:[],
      groceryList: [],
      savings: 0,
      exclusiveStores: [],
      weeklyDeals_w: [],
      weeklyDeals_iga: [],
    };
  },
  computed:
{
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
      let stores = [ 'IGA','ALDI', 'Woolworths', 'Coles','Chemist Warehouse'];
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
}
,
    
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
}
,



updateSavingsAndBestStore(product) {


    

    
    // Update overall savings
    this.savings += this.productSavings(product);
    
    // TODO: You will need logic here to update the 'bestStore' value. 
    // This can be based on the minimum price amongst all stores or some other logic.
}
,  async fetchWeeklyDeals() {
  try {
    this.loading_start = true;
    const responseWoolies = await fetch('http://127.0.0.1:8000/half-price-deals_woolies');
    this.weeklyDeals_w = await responseWoolies.json();
    const responseIga = await fetch('http://127.0.0.1:8000/half-price-deals_iga');
    this.weeklyDeals_iga = await responseIga.json();
  } catch (error) {
    console.error("Failed to fetch weekly deals:", error);
  } finally {
    this.loading_start= false;
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
    }

  }
};
</script>
<style scoped>
.truncate-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;

}



</style>
