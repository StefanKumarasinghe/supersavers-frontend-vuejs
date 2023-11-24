<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <span>
      <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
        <h3 align="right"  class="px-2 py-1  "><span v-if="bestStoreForProduct(product)=='Coles'" class="red--text font-weight-bold">{{bestStoreForProduct(product)}}</span><span v-if="bestStoreForProduct(product)=='Woolworths'" class="green--text font-weight-bold">{{bestStoreForProduct(product)}}</span><span v-if="bestStoreForProduct(product)=='IGA'" class="white--text font-weight-bold iga_logo font-weight-bold p-2">  <v-span class="white--text font-weight-bold iga_logo">&nbsp;IGA&nbsp;</v-span></span></h3>
        <v-img :src="product.image" width="90%" contain class="text-center mx-auto"></v-img>
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
        <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
          <v-btn class="text-none text-subtitle-1 mb-3 white--text" color="green" @click="addItemToCart(product)" size="small" variant="flat">
              Add To List
          </v-btn>
          <v-btn class="text-none text-subtitle-1 mb-3" size="small" variant="flat" @click="Notify(product)">
              Listen
          </v-btn>
        </v-card-actions>
      </v-card>
    </span>
</template>

<script>
    export default {
      props: {
  product: {
    type: Object,
    required: true,
  },
  data:{
    AuthToken:null,

  }
},

async beforeMount() {
    await this.TokenPromise();
  },

        methods: {
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
    console.log(this.AuthToken);

    const response = await fetch('http://127.0.0.1:8000/add_item_notify', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.AuthToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
      name: String(product.name),
    woolworths_code: String(product.stockcode_w),
    coles_code: String(product.stockcode_c),
    iga_code: String(product.stockcode_i),
    image: String(product.image),
    description: String(product.description),
  
}),

    });

    const data = await response.json();
    console.log(data.status);
  } catch (error) {
    console.error('Error fetching products:', error);
  }
},
addItemToCart(product) {
     this.$store.dispatch('addItem', product);
     alert('Item added')
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
          }
        }
    }
</script>

<style lang="scss" scoped>

</style>