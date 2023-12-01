<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <span>
      <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
        <h3 align="right"  class="px-2 py-1  "><span v-if="bestStoreForProduct(product)=='Coles'" class="red--text font-weight-bold">{{bestStoreForProduct(product)}}</span><span v-if="bestStoreForProduct(product)=='Woolworths'" class="green--text font-weight-bold">{{bestStoreForProduct(product)}}</span><span v-if="bestStoreForProduct(product)=='IGA'" class="white--text font-weight-bold iga_logo font-weight-bold p-2">  <v-span class="white--text font-weight-bold iga_logo">&nbsp;IGA&nbsp;</v-span></span></h3>
        <v-img :src="product.image" width="70%" contain class="text-center mx-auto"></v-img>
      <v-card-title>
        <h3 class="green--text font-weight-bold" >
            <span class=" p-0" v-if="product.coles_price && product.woolworths_price && !product.iga_price">
              ${{ 
                parseFloat(Math.min(product.coles_price, product.woolworths_price)) 
              }}
            </span>
            <span class=" p-0" v-if="product.coles_price && product.woolworths_price && product.iga_price">
              ${{ 
                parseFloat(Math.min(product.coles_price, product.woolworths_price, product.iga_price))
              }}
            </span>
            <span class=" p-0" v-if="!product.coles_price && product.woolworths_price && product.iga_price">
              ${{ 
                parseFloat(Math.min(product.woolworths_price, product.iga_price))
              }} 
            
            </span>
            <span class=" p-0" v-if="product.coles_price && !product.woolworths_price && product.iga_price">
              ${{ 
                parseFloat(Math.min(product.coles_price, product.iga_price))
              }}
            </span>
          </h3>
          </v-card-title>
          <v-card-title class="py-0">
        <h5 class="py-0">
  
            <v-span class="" v-if="product.woolworths_price">
              <span class="">
                ${{ product.woolworths_price }} at
              </span>
              <v-span class="green--text font-weight-bold">
                Woolworths
              </v-span>
            </v-span>

            <v-span  v-if="product.coles_price">
              <span class="">
                , ${{ product.coles_price }} at
              </span>
              <v-span class="red--text font-weight-bold">
                Coles
              </v-span>
            </v-span>

            <v-span v-if="product.iga_price">
              <span class="">
               & ${{ product.iga_price }} at
              </span>
              <v-span class="white--text font-weight-bold iga_logo">
                &nbsp;IGA&nbsp;
              </v-span>
            </v-span>
        </h5>
        </v-card-title>
        <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
          {{ product.name }} | {{product.size}}
        </v-card-title>
        <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
        <v-card-text>
                <div class="card-quantity mx-1 my-2">
                    <div class="text-subtitle-1">Quantity:</div>
                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="quantity" append-outer-icon="mdi-plus" @click:append-outer="increment()" prepend-icon="mdi-minus" @click:prepend="decrement()"></v-text-field>
                </div>
        </v-card-text>
        <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
          <div class="row">
            <div class="col-12">
              <v-btn class="text-none text-h6 mb-3 white--text me-1" width="100%" height="100%" color="green" @click="addItemToCart(product)" size="small" variant="flat">
                Add To List
              </v-btn>
            </div>
            <div class="col-12">
              <v-btn class="text-none text-h6 mb-3" width="100%" height="100%" size="small" variant="flat" @click="Notify(product)">
                Listen
              </v-btn>
            </div>
          </div>
        </v-card-actions>

      </v-card>
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
    </span>
</template>

<script>
import { getMessaging, getToken } from 'firebase/messaging';
import firebase from 'firebase/app';

export default {
  props: {
    product: {
      type: Object,
      required: true,
    },

    data: {
      AuthToken: null,
      registrationToken: null,
     
    },
  },

  async beforeMount() {
    await this.TokenPromise();
    await this.getAndSendNotificationToken();
  },
  data() {
        return {
            quantity: 1
        }
    },

  methods: {
    async getAndSendNotificationToken() {
      try {
        // Request permission to show notifications
        const permission = await Notification.requestPermission();

        if (permission === 'granted') {
          // Get the messaging instance
          const messaging = getMessaging(firebase);
          
          // Get the current registration token
          const currentToken = await getToken(messaging);
          console.log(currentToken);

          // Assign the registration token to the component data
          this.registrationToken = currentToken;

          // Send the registration token to your server
          // You may want to call your server-side function here to handle the token
          // e.g., this.sendTokenToServer(currentToken);
        }
      } catch (error) {
        console.error('Error getting notification token:', error);
      }
    },

    async TokenPromise() {
      this.AuthToken = await this.getToken();
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

    async Notify(product) {
      try {
        // Use the messaging instance from Firebase
        const messaging = getMessaging(firebase);

        // Get the current registration token
        const currentToken = await getToken(messaging);

        await fetch('http://127.0.0.1:8000/add_item_notify', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: String(product.name),
            registration_token: String(currentToken),
            woolworths_code: String(product.stockcode_w),
            coles_code: String(product.stockcode_c),
            iga_code: String(product.stockcode_i),
            image: String(product.image),
            description: String(product.description),
          }),
        });
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    increment () {
            this.quantity += 1;
        },
        decrement () {
            if (this.quantity > 1) {
                this.quantity -= 1;
            }
     },
     addItemToCart(product) {
  if (product) {
    var x = { ...product }; // Create a copy to avoid modifying the original object
    x.quantity = this.quantity;
    x.bought = false;

    const storePrices = {
      'Woolworths': product.woolworths_price,
      'Coles': product.coles_price,
      'IGA': product.iga_price,
    };

    // Filter out null or undefined prices
    const validPrices = Object.values(storePrices).filter(price => price !== null && price !== undefined);

    // Check if there are valid prices
    if (validPrices.length > 0) {
      // Calculate the old and new prices based on valid prices
      x.old_price = Math.max(...validPrices);
      x.new_price = Math.min(...validPrices);

      // Determine the store with the lowest price
      let lowestStore = Object.keys(storePrices).find(store => storePrices[store] === x.new_price);

      // Set the lowest price store as the source
      x.source = lowestStore;
    } else {
      // No valid prices, set source to null
      x.source = null;
    }

    // Dispatch to the store
    this.$store.dispatch('addItem', x);
    this.error = 'Item was successfully added to the list';
    this.snackbar = true;
  } else {
    console.error('Invalid product:', x);
  }
}
,

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
  },
};
</script>




<style lang="scss" scoped>

</style>