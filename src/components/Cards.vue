<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <span>
      <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
        <v-img :src="product.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
        <v-toolbar color="transparent" flat v-if="product.coles_price !== product.woolworths_price && product.coles_price !== product.iga_price && product.woolworths_price !== product.iga_price">
          <v-avatar color="yellow" rounded width="100%" height="35" >
            <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && !product.iga_price">
              {{ 
                (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2)) == 0 
                ? ''  
                : 'Save $' + (parseFloat(Math.max(product.coles_price, product.woolworths_price) - Math.min(product.coles_price, product.woolworths_price)).toFixed(2)) + ' at ' + bestStoreForProduct(product)
              }}
            </span>
            <span class="black--text font-weight-bold p-0" v-if="product.coles_price && product.woolworths_price && product.iga_price">
              Save ${{ 
                parseFloat(Math.max(product.coles_price, product.woolworths_price, product.iga_price) - Math.min(product.coles_price, product.woolworths_price, product.iga_price)).toFixed(2) + ' at ' + bestStoreForProduct(product)
              }}
            </span>
          </v-avatar>
        </v-toolbar>
        <v-card-text class="py-1">
          <strong>
            <div class="text-h6" v-if="product.woolworths_price">
              <span class="black--text font-weight-bold">
                ${{ product.woolworths_price }} at
              </span>
              <v-span class="green--text font-weight-bold">
                Woolworths
              </v-span>
            </div>

            <div class="text-h6" v-if="product.coles_price">
              <span class="black--text font-weight-bold">
                ${{ product.coles_price }} at
              </span>
              <v-span class="red--text font-weight-bold">
                Coles
              </v-span>
            </div>

            <div class="text-h6" v-if="product.iga_price">
              <span class="black--text font-weight-bold">
                ${{ product.iga_price }} at
              </span>
              <v-span class="white--text font-weight-bold iga_logo">
                &nbsp;IGA&nbsp;
              </v-span>
            </div>
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
    </span>
</template>

<script>
    export default {
        props: {
            product: {
              type: Object,
              required: true,
            }
        },
        methods: {
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
          }
        }
    }
</script>

<style lang="scss" scoped>

</style>