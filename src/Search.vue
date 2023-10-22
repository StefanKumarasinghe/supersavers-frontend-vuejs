<!-- eslint-disable vue/multi-word-component-names -->
<template>
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
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="searchTerm" @change="fetchProducts" label="Search for a product" outlined clearable></v-text-field>
      </v-col>
    </v-row>

    <v-row v-if="products.length">
      <v-col v-for="product in products" :key="product.name" cols="12" md="4">
        <v-card>
          <v-img :src="product.image" height="200"></v-img>
          <v-card-title>{{ product.name }} | {{ product.size }} | {{ product.brand }}</v-card-title>
          <v-chip outlined color="green">Woolies: {{ product.woolworths_price ? `$${product.woolworths_price}` : 'N/A' }}</v-chip>
          <v-chip outlined color="red" >Coles: {{ product.coles_price ? `$${product.coles_price}` : 'N/A' }}</v-chip>
          <v-card-text>{{ product.description }}</v-card-text>
          <v-card-actions>
            <v-btn color="green" @click="addProductToGrocery(product)">Add to Grocery List</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      searchTerm: '',
      products: [],
      groceryList: []
    };
  },
  computed: {
    storeTotals() {
      let totals = {
        Woolies: 0,
        Coles: 0
        // Add more stores as needed
      };
      this.groceryList.forEach(item => {
        if(item.woolworths_price) {
          totals.Woolies += item.woolworths_price;
        }
        if(item.coles_price) {
          totals.Coles += item.coles_price;
        }
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
    async fetchProducts() {
      const response = await fetch(`http://127.0.0.1:8000/search/${encodeURIComponent(this.searchTerm)}`);
      this.products = await response.json();
    },
    addProductToGrocery(product) {
      let existingProduct = this.groceryList.find(item => item.name === product.name);
      if (existingProduct) {
        existingProduct.counter += 1;
      } else {
        this.groceryList.push({ ...product, counter: 1 });
      }
    }
  }
};
</script>
