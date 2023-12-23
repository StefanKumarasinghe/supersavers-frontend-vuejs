<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <span>
      <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="500" height="100%" >
        <v-img :src="product.image" width="90%" contain class="mx-auto"><button @click="shareApp(product)" large class="text-start text-danger fw-bold  font-weight-bold">
      <v-icon class="mdi text-danger mdi-share-variant">mdi-share-variant</v-icon>
    </button>  </v-img>
        <v-card-title class="black--text font-weight-bold px-4" style="display: inline-block; word-break: break-word;">
          {{ product.name }} | {{product.size}}
          <v-card class="mt-5" v-if="product.woolworths_price" :style="isSelected === 'Woolworths' ? 'border: 1px solid green;': ''" :outlined="isSelected!='Woolworths'" @click="selectStore('Woolworths')">
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
            <div class="col-6">
              <v-btn class="fw-bold mb-3 white--text me-1" dark width="100%" height="45px" color="green" @click="addItemToCart(product, isSelected)" size="small" variant="flat">
                ADD TO LIST
              </v-btn>
            </div>
            <div class="col-6">
              <v-btn class="mb-3 mx-auto fw-bold mb-3 white--text btn btn-danger" color="red" height="45px" size="small" variant="flat" @click="Notify(product)">
                NOTIFY
              </v-btn>
            </div>
          </div>
        </v-card-actions>

      </v-card>
      <div class="text-center ma-2">
        <Toast ref="Toast" />
      </div>
    </span>
</template>

<script>
import { getMessaging, getToken } from 'firebase/messaging';
import firebase from 'firebase/app';
import Toast from './Toast.vue';

export default {
    components: {
     Toast
    },
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
    this.isSelected = this.pickLowest();
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
    pickLowest() {
    // Initialize with the price of the first product
    let lowestPrice = this.product.woolworths_price;
    let lowestStore = 'Woolworths';
    // Check Coles and update if its price is lower
    if (this.product.coles_price !== null && this.product.coles_price < lowestPrice) {
      lowestPrice = this.product.coles_price;
      lowestStore = 'Coles';
    }
    // Check IGA and update if its price is lower
    if (this.product.iga_price !== null && this.product.iga_price < lowestPrice) {
      lowestStore = 'IGA';
    }
    return lowestStore;
    },
    selectStore(store) {
      this.isSelected = store;
    },
    shareApp(product) {
      if (navigator.share) {
        const totalSavings = Math.abs(parseFloat((product.woolworths_price - product.coles_price).toFixed(2)));
        const messageParts = [
          `🌟 Hey friend, check out this awesome deal on ${product.name}! 🌟`,
          `🛍 Woolworths Price: AUD ${product.woolworths_price}`,
          `🛒 Coles Price: AUD ${product.coles_price}`,
          `💰 You're Saving Atleast: AUD ${totalSavings}`,
          `🌈 Visit supersavers.au to save on groceries`,
        ];
        const shareMessage = messageParts.join('\n');
        navigator
          .share({
            title: 'SuperSavers',
            text: shareMessage,
            url: 'https://supersavers.au',
          })
          .then(() => this.$refs.Toast.showSnackbar('Shared successfully', 'green', 'mdi-check-circle') )
          .catch(() => this.$refs.Toast.showSnackbar('Something went wrong sharing the message', 'red', 'mdi-alert-circle'));
      } else {
        this.$refs.Toast.showSnackbar('You have not enabled the sharing feature', 'red', 'mdi-alert-circle');
      }
    },
    async getAndSendNotificationToken() {
      try {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
          const messaging = getMessaging(firebase);
          const currentToken = await getToken(messaging);
          this.registrationToken = currentToken;
        }else {
          this.$refs.Toast.showSnackbar('You have not enabled notifications. You can always manage settings in Accounts', 'red', 'mdi-alert-circle')
        }
      } catch (error) {
        console.error('Error getting notification token:', error);
        this.$refs.Toast.showSnackbar('You have not enabled notifications. You can always manage settings in Accounts', 'red', 'mdi-alert-circle')
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
        const messaging = getMessaging(firebase);
        
        // Get the current FCM token
        const currentToken = await getToken(messaging);

        if (!currentToken) {
          throw new Error('Unable to retrieve FCM token.');
        }
        const response = await fetch(`${this.$GroceryAPI}/add_item_notify`, {
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

        if (response.ok) {
          this.$refs.Toast.showSnackbar('Successfully added to your wishlist', 'green', 'mdi-check-circle');
        } else {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Unknown error');
        }
      } catch (error) {
        console.error('Error adding to wishlist:', error);
        this.$refs.Toast.showSnackbar('Something went wrong when adding to your wishlist', 'red', 'mdi-alert-circle');
      }
    },
    async addItemToCart(product, selectedStore) {
      try {
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
        const response = await fetch(`${this.$GroceryAPI}/add_item_cart`, {
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
        if (response.ok) {
          this.$refs.Toast.showSnackbar('Successfully added to your grocery list', 'green', 'mdi-check-circle');
        } else {
          this.$refs.Toast.showSnackbar('Unexpected error occurred', 'red', 'mdi-alert-circle');
        }
        
      } else {
        console.error('Invalid product:', x);
        this.$refs.Toast.showSnackbar('There is no such product that you can add to the list', 'red', 'mdi-alert-circle');
      }
    } catch (error) {
        console.error('Error adding to wishlist:', error);
        this.$refs.Toast.showSnackbar('Something went wrong when adding to your list', 'red', 'mdi-alert-circle');
    }
   }
  },
};
</script>
