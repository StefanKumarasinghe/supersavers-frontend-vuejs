<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app>
    <!-- Navigation Drawer for Grocery List -->

    
    <!-- Top App Bar -->
    <v-app-bar app clipped-left color="green darken-2" dark dense>
      <v-toolbar-title class="pa-3">Alpha</v-toolbar-title>

      <v-spacer></v-spacer>
      
     <!-- Search Bar -->
  <v-text-field 
    class="mx-2" 
    v-model="groceryItem" 
    label="Search for an item" 
    hide-details single-line outlined dense 
    @input="onSearch"
  ></v-text-field>

  <!-- Display Search Suggestions -->
  <div v-if="searchResults.length">
      <ul>
          <li v-for="result in searchResults" :key="result.id" @click="fetchProductDetails(result.name)">
              {{ result.name }}
          </li>
      </ul>
  </div>
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



    <!-- Main Content -->
    <v-main>
        <v-navigation-drawer clipped app width="300">
      <v-list nav dense>
        <v-subheader class="green--text text--darken-2 pa-2">Grocery Shopping</v-subheader>
        <v-divider></v-divider>
        <v-list-item-group>
          <v-list-item v-for="item in groceryList" :key="item.id">
            <v-list-item-content>
              <v-list-item-title>
                {{ item.name }} <span v-if="item.counter && item.counter > 1">x{{ item.counter }}</span>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
        <v-divider></v-divider>
        <v-row class="ma-2 green--text">
          With {{ bestStore }}. You can save up to ${{ savings }} compared to other stores.
        </v-row>
       
      </v-list>
    
    </v-navigation-drawer>

    <v-container fluid>
      <v-row align="center" class="mb-5">
        <v-col cols="12" md="12" lg="12">
          <!-- Featured Products Section -->
          <v-row class="text-center">
            <v-col>
            <v-carousel height="300px">
  <v-carousel-item v-for="n in 5" :key="n">
    <v-img :src="'https://source.unsplash.com/random/800x600?art,' + n" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)"></v-img>
  </v-carousel-item>
</v-carousel>

               <h2 class="my-3">Guaranteed Saving through Groceries</h2>
              <p>Save on half-deals and other exclusive offers by comparing prices before visiting the grocery store</p>
              <v-row justify="center">
                <v-chip outlined v-for="category in categories" :key="category" @click="filterByCategory(category)"><v-text>{{ category }}</v-text></v-chip>
              </v-row>
            </v-col>
          </v-row>

          <v-row class="mb-4">
            <v-col cols="12" sm="6" md="4" v-for="product in filteredProducts" :key="product.id">
              <v-card class="elevation-12 mb-5">
                <v-img :src="product.image" height="200px" gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)">
                  <v-btn class="float-right" icon @click="addProductToGrocery(product)" color="green accent-3">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                  <v-card-title class="font-weight-bold white--text">{{ product.name }}</v-card-title>
                </v-img>
                <v-card-text>
                  <v-row>
                    <v-chip outlined v-for="store in product.stores" :key="store.name">
                      <v-text>{{ store.name }}: {{ store.price | currency }}</v-text>
                    </v-chip>
                  </v-row>
                  <v-row>
                    <v-chip color="yellow" class="ma-1">{{ product.discount }}% OFF</v-chip>
                    <v-chip color="success" class="ma-1">Save: {{ product.saveAmount | currency }}</v-chip>
                  </v-row>
                </v-card-text>
                <v-card-actions>
                  <v-btn cols="12" :href="product.link" target="_blank" color="yellow">Compare</v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
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
      drawer: true,
       groceryItem: "",
      searchResults: [],
      productDetails: [],
      groceryList: [],
      selectedCategory: null,
      notifications: [
        { id: 1, message: "This is a sample notification." }
      ],
      categories: ["Fruits n Veggies", "Frozen", "Breakfast", "Asian", "Sweets", "Cooking Essentials", "Meat", "Beverages", "Other"],
      featuredProducts: [
        {
          id: 1,
          name: "Peach Ice Team",
          category: "Fruits n Veggies",
          image: "https://source.unsplash.com/random/500x500?product",
          link: "#",
          stores: [
            { name: "Woolies", price: 3.99 },
            { name: "Coles", price: 3.99 },
            { name: "Aldi", price: 1.99 },
          ],
          discount: 10,
          saveAmount: 3
        },
        {
          id: 2,
          name: "Orea Ice Cream",
          category: "Frozen",
          image: "https://source.unsplash.com/random/500x500?product/3",
          link: "#",
          stores: [
            { name: "Woolies", price: 4.50 },
            { name: "Coles", price: 9.00 },
            { name: "Aldi", price: 4.75 },
          ],
          discount: 10,
          saveAmount: 3
        },
        {
          id: 3,
          name: "Doritos",
          category: "Snacks",
          image: "https://source.unsplash.com/random/500x500?product/2",
          link: "#",
          stores: [
            { name: "Woolies", price: 1.99 },
            { name: "Coles", price: 3.99 },
            { name: "Aldi", price: 2.99 },
          ],
          discount: 10,
          saveAmount: 3
        },
        {
  id: 4,
  name: "Green Tea",
  category: "Beverages",
  image: "https://source.unsplash.com/random/500x500?tea",
  link: "#",
  stores: [
    { name: "Woolies", price: 4.99 },
    { name: "Coles", price: 5.49 },
    { name: "Aldi", price: 4.79 },
  ],
  discount: 5,
  saveAmount: 0.7
},
{
  id: 5,
  name: "Pasta",
  category: "Cooking Essentials",
  image: "https://source.unsplash.com/random/500x500?pasta",
  link: "#",
  stores: [
    { name: "Woolies", price: 2.50 },
    { name: "Coles", price: 2.20 },
    { name: "Aldi", price: 2.00 },
  ],
  discount: 10,
  saveAmount: 0.5
},
{
  id: 6,
  name: "Shrimp Dumplings",
  category: "Asian",
  image: "https://source.unsplash.com/random/500x500?dumplings",
  link: "#",
  stores: [
    { name: "Woolies", price: 7.99 },
    { name: "Coles", price: 8.50 },
    { name: "Aldi", price: 7.50 },
  ],
  discount: 8,
  saveAmount: 1
},
{
  id: 7,
  name: "Eggs",
  category: "Breakfast",
  image: "https://source.unsplash.com/random/500x500?eggs",
  link: "#",
  stores: [
    { name: "Woolies", price: 3.50 },
    { name: "Coles", price: 3.20 },
    { name: "Aldi", price: 3.00 },
  ],
  discount: 5,
  saveAmount: 0.5
},
{
  id: 8,
  name: "Steak",
  category: "Meat",
  image: "https://source.unsplash.com/random/500x500?steak",
  link: "#",
  stores: [
    { name: "Woolies", price: 14.99 },
    { name: "Coles", price: 13.99 },
    { name: "Aldi", price: 13.50 },
  ],
  discount: 7,
  saveAmount: 1.49
},
{
  id: 9,
  name: "Milk Chocolate",
  category: "Sweets",
  image: "https://source.unsplash.com/random/500x500?chocolate",
  link: "#",
  stores: [
    { name: "Woolies", price: 2.50 },
    { name: "Coles", price: 2.70 },
    { name: "Aldi", price: 2.20 },
  ],
  discount: 10,
  saveAmount: 0.5
},
{
  id: 10,
  name: "Red Wine",
  category: "Beverages",
  image: "https://source.unsplash.com/random/500x500?wine",
  link: "#",
  stores: [
    { name: "Woolies", price: 10.99 },
    { name: "Coles", price: 12.99 },
    { name: "Aldi", price: 9.99 },
  ],
  discount: 10,
  saveAmount: 3
},
{
  id: 11,
  name: "Chicken Nuggets",
  category: "Frozen",
  image: "https://source.unsplash.com/random/500x500?nuggets",
  link: "#",
  stores: [
    { name: "Woolies", price: 6.99 },
    { name: "Coles", price: 6.50 },
    { name: "Aldi", price: 6.20 },
  ],
  discount: 5,
  saveAmount: 0.79
},
{
  id: 12,
  name: "Muesli",
  category: "Breakfast",
  image: "https://source.unsplash.com/random/500x500?muesli",
  link: "#",
  stores: [
    { name: "Woolies", price: 5.99 },
    { name: "Coles", price: 5.50 },
    { name: "Aldi", price: 4.99 },
  ],
  discount: 8,
  saveAmount: 1
},
{
  id: 13,
  name: "Olive Oil",
  category: "Cooking Essentials",
  image: "https://source.unsplash.com/random/500x500?olive-oil",
  link: "#",
  stores: [
    { name: "Woolies", price: 8.99 },
    { name: "Coles", price: 7.99 },
    { name: "Aldi", price: 7.50 },
  ],
  discount: 10,
  saveAmount: 1.49
}
      ]
    };
  },
  computed: {
    filteredProducts() {
      if (!this.selectedCategory) return this.featuredProducts;
      return this.featuredProducts.filter(product => product.category === this.selectedCategory);
    },
    storeTotals() {
      let totals = {
        Woolies: 0,
        Coles: 0,
        Aldi: 0,
      };
      this.groceryList.forEach(item => {
        item.stores.forEach(store => {
          totals[store.name] += store.price * (item.counter || 1);
        });
      });
      return totals;
    },
    bestStore() {
      return Object.keys(this.storeTotals).reduce((a, b) => this.storeTotals[a] < this.storeTotals[b] ? a : b);
    },
    savings() {
      let maxPrice = Math.max(...Object.values(this.storeTotals));
      let bestPrice = this.storeTotals[this.bestStore];
      return (maxPrice - bestPrice).toFixed(2);
    }
  },
  methods: {
    login() {
      console.log("Login clicked");
    },
    register() {
      console.log("Register clicked");
    },
    filterByCategory(category) {
      this.selectedCategory = category;
    },
    addProductToGrocery(product) {
      let existingProduct = this.groceryList.find(item => item.id === product.id);
      if (existingProduct) {
        existingProduct.counter += 1;
      } else {
        this.groceryList.push({ ...product, counter: 1 });
      }
    },
    addGrocery() {
      if (this.groceryItem.trim()) {
        this.groceryList.push({id: Date.now(), name: this.groceryItem.trim(), counter: 1});
        this.groceryItem = "";
      }
    },
        async fetchSearchSuggestions() {
        if (!this.groceryItem) return;

        const url = `https://www.woolworths.com.au/apis/ui/product/detail/599999`;
        const response = await fetch(url);
        const data = await response.json();
        this.searchResults = data;  // Adjust based on the structure of the API response
    },

    async fetchProductDetails(searchTerm) {
        const payload = {
            Filters: [],
            IsSpecial: false,
            EnableAdReRanking: false,
            ExcludeSearchTypes: ["UntraceableVendors"],
            GpBoost: 0,
            GroupEdmVariants: true,
            IsRegisteredRewardCardPromotion: null,
            Location: `/shop/search/products?searchTerm=${encodeURIComponent(searchTerm)}`,
            PageNumber: 1,
            PageSize: 24,
            SearchTerm: searchTerm,
            SortType: "TraderRelevance"
        };

        const response = await fetch('https://www.woolworths.com.au/apis/ui/Search/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        const data = await response.json();
        this.productDetails = data;  // Adjust based on the structure of the API response
    },

    async onSearch() {
        if (this.groceryItem.trim().length > 2) {
            await this.fetchSearchSuggestions();
        }
    }
  
  },
  filters: {
    currency(value) {
      return `$${value.toFixed(2)}`;
    }
  }
};
</script>
