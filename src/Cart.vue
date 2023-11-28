<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
        <v-container fluid>
          <div class="mx-3 mt-5">
            <h1>
              SHOPPING LIST
            </h1>
            <p>With Grocery Planner, you can plan your trip so you can save on the best deals when going for groceries.</p>
          </div>
            <v-card flat>
              <v-tabs
                v-model="tab"
                background-color="transparent"
                color="green"
                grow
              >
                <v-tab
                  v-for="item in items"
                  :key="item"
                  class="tab-cart font-weight-bold"
                >
                  {{ item }}
                </v-tab>
              </v-tabs>

              <v-tabs-items v-model="tab">
                <!-- First content -->
                <v-tab-item>

                  <!-- Woolworths -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="green--text font-weight-bold woolies-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>        
                    </div>
                    <div v-for="(list, i) in lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'Woolworths'">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md-4 col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                              </div>
                            </div>
                            <div class="col-12 col-md-5 col-lg col-sm-12">
                              <v-btn outlined rounded text @click="removeItem(i)" class="font-weight-bold text-subtitle-1">Remove</v-btn>
                              <v-btn rounded @click="boughtItem(i, quantities[i])" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green">Bought</v-btn>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Coles -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="red--text font-weight-bold coles-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span>        
                    </div>
                    <div v-for="(list, i) in lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'Coles'">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md-4 col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                              </div>
                            </div>
                            <div class="col-12 col-md-5 col-lg col-sm-12">
                              <v-btn outlined rounded text @click="removeItem(i)" class="font-weight-bold text-subtitle-1">Remove</v-btn>
                              <v-btn rounded @click="boughtItem(i, quantities[i])" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green">Bought</v-btn>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- IGA -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="font-weight-bold iga-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span>     
                    </div>
                    <div v-for="(list, i) in lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'IGA'">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md-4 col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                              </div>
                            </div>
                            <div class="col-12 col-md-5 col-lg col-sm-12">
                              <v-btn outlined rounded text @click="removeItem(i)" class="font-weight-bold text-subtitle-1">Remove</v-btn>
                              <v-btn rounded @click="boughtItem(i, quantities[i])" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green">Bought</v-btn>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <v-divider class="divider"></v-divider>
                  <div class="d-flex flex-row-reverse">
                    <h2 class="black--text">Total: {{calTotal()}}</h2>
                  </div>
                  <div class="d-flex flex-row-reverse py-3 text-h6">
                    <v-avatar rounded width="125" height="35">
                        <span class="black--text font-weight-bold p-0 card-avatar-inside">
                        Save {{saveTotal()}}
                        </span>
                    </v-avatar>
                  </div>

                </v-tab-item>

                <!-- Second tab content -->
                <v-tab-item>

                  <!-- Woolworths -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="green--text font-weight-bold woolies-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>        
                    </div>
                    <div v-show="bought_lists.length == 0">No items from Woolworths are bought...</div>
                    <div v-for="(list, i) in bought_lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'Woolworths'" style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * bought_quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* bought_quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="bought_quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" readonly></v-text-field>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Coles -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="red--text font-weight-bold coles-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span>        
                    </div>
                    <div v-show="bought_lists.length == 0">No items from Coles are bought...</div>
                    <div v-for="(list, i) in bought_lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'Coles'" style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * bought_quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* bought_quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="bought_quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" readonly></v-text-field>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- IGA -->
                  <div class="mt-5 pt-5">
                    <div class="pb-3">
                      <v-span class="font-weight-bold iga-logo text-h4" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span>     
                    </div>
                    <div v-show="bought_lists.length == 0">No items from IGA are bought...</div>
                    <div v-for="(list, i) in bought_lists" :key="i" class="d-flex justify-center">
                      <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'IGA'" style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                        <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                          <div class="p-5 m-5">
                            <v-img :src="list.image" alt="Item Image" contain class="mx-auto" min-width="130" max-width="140"></v-img>
                          </div>
                          <div class="py-3 text-center">
                            <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</v-span>              
                            <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'" style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</v-span> 
                            <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</v-span> 
                          </div>
                        </div>
                        <div class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center">
                          <div class="row">
                            <div class="col-12 col-md col-lg-5 col-sm-12"> 
                              <div class="text-overline font-weight-bold">
                                <h2>{{list.name}}</h2>
                              </div>
                              <div class="py-5">
                                <span class="text-h6">
                                  <b>$ {{(list.woolworths_price * bought_quantities[i]).toFixed(2)}}&nbsp;&nbsp;</b>
                                </span>
                                <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                  Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* bought_quantities[i]).toFixed(2) }}
                                </span>
                              </div>
                            </div>
                            <div class="col-12 col-md col-lg col-sm-12">
                              <div class="card-quantity">
                                <div class="text-subtitle-1">Quantity:</div>
                                <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="bought_quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" readonly></v-text-field>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                </v-tab-item>
              </v-tabs-items>
            </v-card>
        </v-container>
    </v-app>
</template>

<script>
    export default {
    data () {
      return {
        tab: null,
        items: [
          'Items to buy', 'Bought items'
        ],
        text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
        quantities: [],
        numberValue:0,
        page: 1,
        pageCount: 0,
        itemsPerPage: 10,
        headers: [
            { text: 'Item', align: 'start', sortable: false },
            { text: 'Name', align: 'start', sortable: false },
            { text: 'Store', value: 'store', sortable: false },
            { text: 'Price', value: 'price', sortable: false },
            { text: 'Quantity', value: 'image', sortable: false },
        ],
        lists: [
            {
                name: "Coca - Cola Classic Soft Drink Bottle",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/032731.jpg",
                source: "Coles",
                woolworths_price: 1.77,
                coles_price: 3.55
            },
            {
                name: "Real Foods Corn Thins Original",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/071422.jpg",
                source: "Woolworths",
                woolworths_price: 1.0,
                coles_price: 2.0
            },
            {
                name: "Coca - Cola Zero Sugar Soft Drink Bottle",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/623034.jpg",
                source: "Coles",
                woolworths_price: 1.77,
                coles_price: 3.55
            },
            {
                name: "Sorbent Toilet Tissue White",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/938184.jpg",
                source: "Woolworths",
                woolworths_price: 9.0,
                coles_price: 9.0
            },
            {
                name: "Smith's Crinkle Cut Potato Chips Original",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/826730.jpg",
                source: "IGA",
                woolworths_price: 2.4,
                coles_price: 4.8
            },
            {
                name: "Golden Crumpets Round",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/049622.jpg",
                source: "Woolworths",
                woolworths_price: 2.2,
                coles_price: 4.4
            },
            {
                name: "Woolworths Chicken Kyiv Garlic",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/769243.jpg",
                source: "Woolworths",
                woolworths_price: 1.5,
                coles_price: 3.0
            },
            {
                name: "Nivea Rich Nourishing Body Lotion Deep Moisturiser For Dry Skin",
                image: "https://cdn0.woolworths.media/content/wowproductimages/large/028694.jpg",
                source: "IGA",
                woolworths_price: 4.75,
                coles_price: 9.5
            }
        ],
        bought_lists: [],
        bought_quantities: []
      }
    },
    created() {
      this.quantities = Array.from({length : this.lists.length}, () => 1)
    },
    methods: {
      increment (index) {
        this.$set(this.quantities, index, this.quantities[index] + 1);
      },
      decrement (index) {
        if (this.quantities[index] > 1) {
          this.$set(this.quantities, index, this.quantities[index] - 1);
        }
      },
      removeItem(index) {
        this.lists.splice(index, 1);
        this.quantities.splice(index, 1);
      },
      calTotal() {
        let sum = 0;
        for (let i = 0; i < this.quantities.length; i++) {
          sum += this.quantities[i] * this.lists[i].woolworths_price;
        }
        return sum.toFixed(2);
      },
      saveTotal() {
        let sum = 0;
        for (let i = 0; i < this.quantities.length; i++) {
          sum += this.quantities[i] * (this.lists[i].coles_price - this.lists[i].woolworths_price);
        }
        return sum.toFixed(2);
      },
      boughtItem(index, quantity) {
        this.bought_quantities.push(quantity);
        this.bought_lists.push(this.lists[index]);
        this.removeItem(index);
      }
    }
  }
</script>

<style>
.theme--light.v-pagination .v-pagination__item--active {
  color: white;
  background-color: orange;
}
.theme--light.v-tabs > .v-tabs-bar .v-tab:not(.v-tab--active) {
  color: black;
}
.tab-cart {
  font-size: 16px;
}
.number-box {
  width: 100px;
  border: 1px solid grey;
}
.card-name {
  padding: 40px 0 !important;
}
.text-input {
  padding-top: 0px;
}
.text-input input {
  text-align: center;
}
.card-quantity {
  width: 130px;
  display:inline-block;
}
.img-avatar {
  border-radius: 0%;
}
.v-card__actions {
  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 0px;
}
.card-avatar-inside {
  background-color: yellow; 
  border-radius: 4px; 
  padding-left: 10px;
  padding-right: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
}
.woolies-logo{
  color: green;
  font-weight: bold;
  font-size: 22px;
}
.coles-logo {
  color: red;
  font-size: 22px;
  font-weight: bold;
}
.iga-logo {
  background-color: red;
  color: white;
  font-size: 22px;
  font-weight: bold;
}
.divider {
  border: 1px solid black;
  margin-top: 30px;
  margin-bottom: 30px;
}
.alert-success {
  margin-bottom: 10px;
  margin-top:20px;
}
.card-col {
  padding: 0px;
}
.v-tab {
  height: 50px;
}
.v-card__title {
  display: block;
}
.row {
  margin: 0px;
}

.box {
  border: 1px solid rgb(128,128,128, 0.3);
  border-radius: 5px;
  margin-left: 20px;
  margin-right:20px;
}
.img {
  width: 120px;
}
</style>