<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <span>
      <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="500" height="100%" >
        <button @click="shareApp(product)" large class=" m-1 font-weight-bold">
      <span class="mdi  mdi-share-variant"></span>
    </button>
        <v-img :src="product.image" width="70%" contain class="mx-auto">  </v-img>
        <v-card-title class="black--text font-weight-bold px-4" style="display: inline-block; word-break: break-word;">
          {{ product.name }} | {{product.size}}
          <v-card v-if="product.woolworths_price" :style="isSelected === 'Woolworths' ? 'border: 1px solid green;': ''" :outlined="isSelected!='Woolworths'" @click="selectStore('Woolworths')">
            <v-row>
              <v-col class="green--text font-weight-bold " style="display: inline-block; word-break: break-word; white-space: nowrap;">
                Woolworths
              </v-col>
              <v-col class="d-flex flex-row-reverse" :class="{'grey--text': isSelected !== 'Woolworths', 'text-h5 font-weight-bold': isSelected === 'Woolworths'}">
                ${{ product.woolworths_price }}
              </v-col>
            </v-row>
          </v-card>

          <v-card v-if="product.coles_price" :style="isSelected === 'Coles' ? 'border: 1px solid green;': ''" :outlined="isSelected!='Coles'" @click="selectStore('Coles')">
            <v-row>
              <v-col class="red--text font-weight-bold">
                Coles
              </v-col>
              <v-col class="d-flex flex-row-reverse" :class="{'grey--text': isSelected !== 'Coles', 'text-h5 font-weight-bold': isSelected === 'Coles'}">
                ${{ product.coles_price }}
              </v-col>
            </v-row>
          </v-card>

          <v-card v-if="product.iga_price" :style="isSelected === 'IGA' ? 'border: 1px solid green;': ''" :outlined="isSelected!='IGA'" @click="selectStore('IGA')">
            <v-row>
              <v-col>
                <span class="white--text font-weight-bold iga_logo">&nbsp;IGA&nbsp;</span>
              </v-col>
              <v-col class="d-flex flex-row-reverse" :class="{'grey--text': isSelected !== 'IGA', 'text-h5 font-weight-bold': isSelected === 'IGA'}">
                ${{ product.iga_price }}
              </v-col>
            </v-row>
          </v-card>
        </v-card-title>
        
        <v-spacer></v-spacer> 
        <v-card-actions class="mx-2 mt-auto"> 
          <div class="row">
            <div class="col-12">
              <v-btn class="text-none text-h6 mb-3 white--text me-1" dark width="100%" height="45px" color="green" @click="addItemToCart(product, isSelected)" size="small" variant="flat">
                Add To List
              </v-btn>
            </div>
            <div class="col-12">
              <v-btn class="text-none text-h6 mb-3" width="100%" height="45px" size="small" variant="flat" @click="Notify(product)">
                Listen
              </v-btn>
            </div>
          </div>
        </v-card-actions>

      </v-card>
      <div class="text-center ma-2">
        <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" style="bottom: 0;">
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
      snackbar: false,
      isSelected: "Woolworths",
      quantity: 1,
      snackbarTimeout: 2500
    }
  },
  methods: {
    selectStore(store) {
      // Toggle the isSelected value based on the current state
      this.isSelected = store;

      // You can use the store variable to identify which store is selected
      console.log(`Selected store: ${store}`);
    },
    shareApp(product) {
  // Check if the Web Share API is supported by the browser
  if (navigator.share) {
    // Calculate total and savings
    const totalSavings = product.woolworths_price - product.coles_price;

    // Message parts with icons and dynamic content
    const messageParts = [
      `🌟 Hey friend, check out this awesome deal on ${product.name}! 🌟`,
      `🛍 Woolworths Price: AUD ${product.woolworths_price}`,
      `🛒 Coles Price: AUD ${product.coles_price}`,
      `💰 You're Saving Atleast: AUD ${totalSavings}`,
      `🌈 Visit SuperSavers.au to save on groceries: https://supersavers.au`,
    ];

    // Combine all parts into the final message
    const shareMessage = messageParts.join('\n');

    // Use the Web Share API to share the message
    navigator
      .share({
        title: 'SuperSavers',
        text: shareMessage,
        url: 'https://supersavers.au',
      })
      .then(() => console.log('Shared successfully'))
      .catch((error) => console.error('Error sharing:', error));
  } else {
    console.error('Error sharing: Web Share API is not supported');
  }
},
    async getAndSendNotificationToken() {
      try {
        // Request permission to show notifications
        const permission = await Notification.requestPermission();

        if (permission === 'granted') {
          // Get the messaging instance
          const messaging = getMessaging(firebase);
          
          // Get the current registration token
          const currentToken = await getToken(messaging);

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

        await fetch(`${this.$GroceryAPI}/add_item_notify`, {
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
        this.message = 'Item is added successfully to notify list';
        this.snackbar = true;
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
    async addItemToCart(product, selectedStore) {
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
          x.new_price = storePrices[selectedStore];

          // Set the lowest price store as the source
          x.source = selectedStore;
        } else {
          // No valid prices, set source to null
          x.source = null;
        }

        await fetch(`${this.$GroceryAPI}/add_item_cart`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: String(x.name),
                old_price: parseFloat(x.old_price),
                new_price: parseFloat(x.new_price),
               source: String(x.source),
                quantity: parseInt(x.quantity, 10),
                image: String(x.image),
                description: String(x.description),
            }),
        })
        this.message = 'Item is added successfully to grocery list';
        this.snackbar = true;
        
      } else {
        console.error('Invalid product:', x);
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
  },
};
</script>
