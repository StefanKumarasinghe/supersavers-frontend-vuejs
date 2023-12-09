<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
    <v-container fluid>
      <div class="mx-3 mt-5">
        <h1>
          SHOPPING LIST
        </h1>
        <p>With Grocery Planner, you can plan your trip so you can save on the best deals when going for groceries.</p>
        <button @click="shareShoppingList"  class="font-weight-bold col-6 col-lg-3 text-success">
          <span class="mdi  mdi-share-variant"></span>
          Share  List
        </button>
        <button @click="shareApp"  class="col-6 col-lg-3 font-weight-bold text-danger">
          <span class="mdi  mdi-share-variant"></span>
          Share the love
        </button>
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
                  <v-expansion-panels v-model="panel1" :disabled="disabled1" multiple flat>

                    <!-- Woolworths -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <h3 class="green--text font-weight-bold woolies-logo" style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</h3>
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="Unbought_w.length == 0">No items from Woolworths are added to the item to buy list...</v-span>    
                        </div>
                        <div v-for="(list, i) in Unbought_w" :key="i" class="d-flex justify-center">
                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-10" >

                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}} </h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                                  </div>
                                </div>
                                <div class="col-12 col-md-5 col-lg col-sm-12">
                                  <v-btn outlined rounded text @click="removeItemFromCart(list.name)" class="font-weight-bold text-subtitle-1" height="42" width="120">Remove</v-btn>
                                  <v-btn rounded @click="boughtItem(list.name)" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green" height="40" width="120">Buy</v-btn>

                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>

                    <!-- Coles -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <h3 class="red--text font-weight-bold coles-logo " style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</h3>
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="Unbought_c.length == 0">No items from Coles are added to the item to buy list...</v-span>    
                        </div>
                        <div v-for="(list, i) in Unbought_c" :key="i" class="d-flex justify-center">
                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'Coles' && !list.bought">
                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}} </h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                                  </div>
                                </div>
                                <div class="col-12 col-md-5 col-lg col-sm-12">
                                  <v-btn outlined rounded text @click="removeItemFromCart(list.name)" class="font-weight-bold text-subtitle-1" height="42" width="120">Remove</v-btn>
                                  <v-btn rounded @click="boughtItem(list.name)" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green" height="40" width="120">Buy</v-btn>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>

                    <!-- IGA -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <div>
                          <h3 class="font-weight-bold iga-logo py-2" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</h3>
                        </div>
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="Unbought_i.length == 0">No items from IGA are added to the item to buy list...</v-span>    
                        </div>
                        <div v-for="(list, i) in Unbought_i" :key="i" class="d-flex justify-center">
                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" v-if="list.source == 'IGA' && !list.bought">
                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}} </h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)"></v-text-field>
                                  </div>
                                </div>
                                <div class="col-12 col-md-5 col-lg col-sm-12">
                                  <v-btn outlined rounded text @click="removeItemFromCart(list.name)" class="font-weight-bold text-subtitle-1" height="42" width="120">Remove</v-btn>
                                  <v-btn rounded @click="boughtItem(list.name)" class="font-weight-bold white--text ms-4 text-subtitle-1" color="green" height="40" width="120">Buy</v-btn>

                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>

                  <div>
                    <v-divider class="divider"></v-divider>
                    <div class="d-flex flex-row-reverse">
                      <h2 class="black--text">Total: {{calTotal()}}</h2>
                    </div>
                    <div class="d-flex flex-row-reverse py-3 text-h6">
                      <v-avatar rounded width="auto" height="35">
                          <span class="black--text font-weight-bold p-0 card-avatar-inside">
                          Save {{saveTotal()}}
                          </span>
                      </v-avatar>
                    </div>
                  </div>

                </v-tab-item>

                <!-- Second tab content -->
                <v-tab-item>

                  <v-expansion-panels v-model="panel2" :disabled="disabled2" multiple flat>
                    
                    <!-- Woolworths -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <h3 class="green--text font-weight-bold woolies-logo " style="display: inline-block; word-break: break-word; white-space: nowrap;">Woolworths</h3>
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="bought_w.length == 0">No items from Woolworths are added to the bought list...</v-span>    
                        </div>
                        <div v-for="(list, i) in bought_w" :key="i" class="d-flex justify-center">
                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10" style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}}</h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity"  readonly></v-text-field>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>

                    <!-- Coles -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <h3 class="red--text font-weight-bold coles-logo " style="display: inline-block; word-break: break-word; white-space: nowrap;">Coles</h3>        
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="bought_c.length == 0">No items from Coles are added to the bought list...</v-span>    
                        </div>
                        <div v-for="(list, i) in bought_c" :key="i" class="d-flex justify-center">

                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10"  style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}}</h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity"  readonly></v-text-field>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>

                    <!-- IGA -->
                    <v-expansion-panel>
                      <v-expansion-panel-header class="mt-5">
                        <div>
                          <h3 class="font-weight-bold iga-logo" style="display: inline-block; word-break: break-word; white-space: nowrap;">&nbsp;IGA&nbsp;</h3>     
                        </div>
                        <template v-slot:actions>
                          <v-icon color="black" size="30">
                            $expand
                          </v-icon>
                        </template>
                      </v-expansion-panel-header>
                      <v-expansion-panel-content>
                        <div class="pb-3">
                          <v-span v-show="bought_i.length == 0">No items from IGA are added to the bought list...</v-span>    
                        </div>
                        <div v-for="(list, i) in bought_i" :key="i" class="d-flex justify-center">
                          <div class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-8 col-10"  style="color: grey; border: 1px solid grey; background-color: rgb(236, 236, 236, 0.5);">
                            <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                              <div class="p-1">
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
                                    <h4>{{list.name}}</h4>
                                  </div>
                                  <div class="py-5">
                                    <span class="text-h6">
                                      <b>$ {{(list.new_price * list.quantity).toFixed(2)}}&nbsp;&nbsp;</b>
                                    </span>
                                    <span class="black--text font-weight-bold card-avatar-inside" style="display: inline-block; word-break: break-word; white-space: nowrap;"> 
                                      Save $ {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                                    </span>
                                  </div>
                                </div>
                                <div class="col-12 col-md col-lg col-sm-12">
                                  <div class="card-quantity">
                                    <div class="text-subtitle-1">Quantity:</div>
                                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="list.quantity"  readonly></v-text-field>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </v-expansion-panel-content>
                    </v-expansion-panel>
                  </v-expansion-panels>
                </v-tab-item>
              </v-tabs-items>
            </v-card>
        </v-container>
       <v-card-text></v-card-text>
       <v-card-text></v-card-text>
       <v-card-text></v-card-text>
       <v-card-text></v-card-text>
       <v-card-text></v-card-text>
    </v-app>
</template>

<script>
    export default {
    data () {
      return {
        authenticated:false,
        panel1: [0, 1, 2],
        panel2: [0, 1, 2],
        disabled1: false,
        disabled2: false,
        tab: null,
        items: [
          'Items to buy', 'Bought items'
        ],
        lists: [],
        bought: [],
        unbought:[],
        quantities: []
      }
    },
    beforeMount() {
      this.TokenPromise()
      this.lists = this.$store.getters.getList;
      for (let i = 0; i < this.lists.length; i++) {
        this.quantities[i] = this.lists[i].quantity;
      }
      
    },
    computed : {
      Unbought_c() {
      return this.unbought.filter(item => item.source === "Coles");
      },
      Unbought_w() {
        return this.unbought.filter(item => item.source === "Woolworths");
      },
      Unbought_i() {
        return this.unbought.filter(item => item.source === "IGA");
      },
      bought_c() {
        return this.bought.filter(item => item.source === "Coles");
      },
      bought_w() {
       
        return this.bought.filter(item => item.source === "Woolworths");
        
      },
      bought_i() {
        return this.bought.filter(item => item.source === "IGA");
      },
    },
    methods: {
      async beforeMount() {
      await this.TokenPromise();
    },
        async TokenPromise() {
      this.AuthToken = await this.getToken();
      this.verifyAuthProcess();
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
            

          }
    },

    async fetchCart() {
      
        try {
          const response = await fetch(`${this.$GroceryAPI}/retrieve_unbought`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          const data = await response.json();
          this.unbought = data; // Update with your actual data structure
        } catch (error) {
          console.error('Error fetching products:', error);
        }
        try {
          const response = await fetch(`${this.$GroceryAPI}/retrieve_bought`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          const data = await response.json();
          this.bought= data; // Update with your actual data structure
        } catch (error) {
          console.error('Error fetching products:', error);
        }
      },
      async removeProduct(product) {
        try {
         await fetch(`${this.$GroceryAPI}/remove_item_notify`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              woolworths_code: String(product.woolworths_code),
              coles_code: String(product.coles_code),
              iga_code: String(product.iga_code),
            }),
          });
  

          this.products = this.products.filter((prod) => prod.woolworths_code !== product.woolworths_code);
  
        } catch (error) {
          console.error('Error removing product:', error);
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
              await this.fetchCart()
          } else {
            console.error('Error:', response.statusText);
            this.$store.commit('clearToken');
            this.$router.push('/login');
            window.location.reload();
          }
        } catch (error) {
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
        }
    },
  
  
      async increment (index) {
        try {
        
        const response = await fetch(`${this.$GroceryAPI}/increase_cart_quantity`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: String(this.unbought[index].name)
            }),
        });

        if (response.ok) {
            if (this.unbought[index].quantity<100) {
            this.unbought[index].quantity = this.unbought[index].quantity + 1;
            }
             // Update with your actual data structure
        } else {
            console.error('Error updating cart:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
      },
      async decrement (index) {
        if (this.unbought[index].quantity>0) {
        
        
        try {
        
        const response = await fetch(`${this.$GroceryAPI}/reduce_cart_quantity`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: String(this.unbought[index].name)
            }),
        });

        if (response.ok) {
            this.unbought[index].quantity = this.unbought[index].quantity - 1;
             // Update with your actual data structure
        } else {
            console.error('Error updating cart:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
  }
      },
      calTotal() {
        let sum = 0;
        for (let i = 0; i < this.unbought.length; i++) {
          if (this.unbought[i]) {
            sum += this.unbought[i].quantity * (this.unbought[i].new_price);
          }
        }
        return sum.toFixed(2);
      },
      generateShareMessage() {
  const messageParts = [];

  // Separate items by store
  const itemsByStore = {
    Woolworths: [],
    Coles: [],
    IGA: [],
  };

  for (let i = 0; i < this.lists.length; i++) {
    const item = this.lists[i];
    const quantity = this.quantities[i];

    // Determine the store for the item
    let storeName = 'Unknown';
    if (item.source === 'Woolworths') {
      storeName = 'Woolworths';
    } else if (item.source === 'Coles') {
      storeName = 'Coles';
    } else if (item.source === 'IGA') {
      storeName = 'IGA';
    }

    // Construct a part of the message for each item with store information
    const itemMessage = `${quantity} x ${item.name}`;
    
    // Add the item to the corresponding store category
    itemsByStore[storeName].push(itemMessage);
  }

  // Add items from each store to the message
  for (const storeName in itemsByStore) {
    if (itemsByStore[storeName].length > 0) {
      messageParts.push(`--- ${storeName} ---`);
      messageParts.push(...itemsByStore[storeName]);
    }
  }

  // Add total and save amounts to the message
  const totalMessage = `Your Total Bill is ${this.calTotal()}`;
  const saveMessage = `You Saved ${this.saveTotal()} with SuperSavers.au, for more details visit https://supersavers.au to save heaps on groceries...`;
  messageParts.push(totalMessage);
  messageParts.push(saveMessage);

  // Combine all parts into the final message
  const finalMessage = messageParts.join('\n');
  return finalMessage;
},
    shareShoppingList() {
      const message = this.generateShareMessage();

      // Check if the Web Share API is supported by the browser
      if (navigator.share) {
        navigator
          .share({
            title: 'SuperSavers Grocery List',
            text: message,
          })
          .then(() => console.log('Shared successfully'))
          .catch((error) => console.error('Error sharing:', error));
      } else {
        console.error('Error sharing')
      }
    },
    shareApp() {

      // Check if the Web Share API is supported by the browser
      if (navigator.share) {
        navigator
          .share({
            title: 'Save Money with SuperSavers on Groceries',
            text: "You can save heaps at Coles, Woolies and IGA with SuperSavers by never missing out on deals. Visit https://supersavers.au",
          })
          .then(() => console.log('Shared successfully'))
          .catch((error) => console.error('Error sharing:', error));
      } else {
        console.error('Error sharing')
      }
    },
      saveTotal() {
        let sum = 0;
        for (let i = 0; i < this.unbought.length; i++) {
          if (this.unbought[i]) {
            sum += this.unbought[i].quantity * (this.unbought[i].old_price - this.unbought[i].new_price);
          }
        }
        return sum.toFixed(2);
      },
      async boughtItem(name) {
    try {
      
        const response = await fetch(`${this.$GroceryAPI}/update_cart`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: String(name)
            }),
        });

        if (response.ok) {
          let index = this.unbought.findIndex(item => item.name == name);

// If the item is found in unbought, remove it and push it to bought
if (index !== -1) {
  let removedItem = this.unbought.splice(index, 1)[0];
  this.bought.push(removedItem);
} else {
  console.error(`Could not remove item`);
} // Update with your actual data structure
        } else {
            console.error('Error updating cart:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
},
      async removeItemFromCart(name) {
        try {
        const response = await fetch(`${this.$GroceryAPI}/remove_cart`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: String(name)
            }),
        });

        if (response.ok) {
          let index = this.unbought.findIndex(item => item.name == name);

// If the item is found in unbought, remove it and push it to bought
if (index !== -1) {
 this.unbought.splice(index, 1)[0];
 
} else {
  console.error(`Could not remove item`);
}
             // Update with your actual data structure
        } else {
            console.error('Error updating cart:', response.statusText);
        }
    } catch (error) {
        console.error('Error updating cart:', error);
    }
      },

    }
  }
</script>

<style>
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