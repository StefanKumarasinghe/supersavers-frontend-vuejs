<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
        <v-container fluid>
            <v-card flat>
                <v-card-title class="py-5">
                <h1 class="orange--text">
                    Shopping List
                </h1>
                <v-alert
                    outlined
                    type="success"
                    text
                    class="alert-success"
                    color="orange"
                >
                    &nbsp;With Grocery Planner, you can plan your trip so you can save on the best deals when going for groceries
                </v-alert>
                </v-card-title>
                <v-tabs
                v-model="tab"
                background-color="transparent"
                color="orange"
                grow
                >
                <v-tab
                    v-for="item in items"
                    :key="item"
                    class="tab-cart"
                >
                    {{ item }}
                </v-tab>
                </v-tabs>
                <v-tabs-items v-model="tab">
                <!-- First content -->
                <v-tab-item>
                    <v-card flat>
                    <v-card-text>
                        <div style="margin-top: 30px;">
                        <h2 style="color: black;">Stop at <span class="woolies-logo" style="font-size: 25px;">Woolworths</span></h2>
                        <v-col v-for="(list, i) in lists" :key="i" cols="12" lg="12" md="12" class="card-col">
                            <template v-if="list.source == 'Woolworths'">
                            <v-card outlined>
                            <v-list-item>
                                <v-list-item-avatar size="125" class="img-avatar">
                                <v-img :src="list.image" alt="Item Image" contain class="mx-auto" style="height: auto;"></v-img>
                                </v-list-item-avatar>
                                <v-col class="ms-5 card-name" cols="5">
                                <div class="text-overline">
                                    <h3>{{list.name}}</h3>
                                </div>
                                <div class="py-3 text-subtitle1 font-weight-bold">
                                    <span><b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}</b></span>
                                    <v-avatar rounded width="150" height="35" class="card-avatar">
                                    <span class="black--text font-weight-bold p-0 card-avatar-inside"> 
                                        Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                    </span>
                                    </v-avatar>
                                </div>
                                <div style="padding-top:10px;">
                                    <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'">Woolworths</v-span>              
                                    <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'">Coles</v-span> 
                                    <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'">&nbsp;IGA&nbsp;</v-span> 
                                </div>
                                </v-col>
                                <v-col class="card-quantity" cols="3">
                                <v-label style="font-size: 14px;">Quantity</v-label>
                                <v-text-field variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" style="text-align: center;"></v-text-field>
                                <v-btn outlined rounded text @click="removeItem(i)" class="my-5 font-weight-bold">Remove</v-btn>
                                <v-btn rounded @click="boughtItem(i)" class="font-weight-bold mx-3 white--text" color="orange">Bought</v-btn>
                                </v-col>
                            </v-list-item>
                            </v-card>
                            </template>
                        </v-col>
                        </div>
                        <div style="margin-top: 30px;">
                        <h2 style="color: black;">Stop at <span class="coles-logo" style="font-size: 25px;">Coles</span></h2>
                        <v-row>
                            <v-col v-for="(list, i) in lists" :key="i" cols="12" lg="12" md="12" class="card-col">
                            <template v-if="list.source == 'Coles'">
                            <v-card outlined>
                                <v-list-item>
                                <v-list-item-avatar size="130" color="grey" class="img-avatar">
                                    <v-img :src="list.image" alt="Item Image" width="100" contain class="mx-auto"></v-img>
                                </v-list-item-avatar>
                                <v-col class="ms-5 card-name" cols="5">
                                    <div class="text-overline" style="line-height: 25px;">
                                    <h3>{{list.name}}</h3>
                                    </div>
                                    <div class="py-3 text-subtitle1 font-weight-bold">
                                    <span><b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}</b></span>
                                    <v-avatar rounded width="150" height="35" class="card-avatar">
                                        <span class="black--text font-weight-bold p-0 card-avatar-inside"> 
                                        Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                        </span>
                                    </v-avatar>
                                    </div>
                                    <div style="padding-top:10px;">
                                    <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'">Woolworths</v-span>              
                                    <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'">Coles</v-span> 
                                    <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'">&nbsp;IGA&nbsp;</v-span> 
                                    </div>
                                </v-col>
                                <v-col class="card-quantity" cols="3">
                                    <v-label style="font-size: 14px;">Quantity</v-label>
                                    <v-text-field variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" style="text-align: center;"></v-text-field>
                                    <v-btn outlined rounded text @click="removeItem(i)" class="my-5 font-weight-bold">Remove</v-btn>
                                    <v-btn rounded @click="boughtItem(i)" class="font-weight-bold mx-3 white--text" color="orange">Bought</v-btn>
                                </v-col>
                                </v-list-item>
                            </v-card>
                            </template>
                            </v-col>
                        </v-row>
                        </div>
                        <div style="margin-top: 30px;">
                        <h2 style="color: black;">Stop at <span class="iga-logo" style="font-size: 25px;">&nbsp;IGA&nbsp;</span></h2>
                        <v-row>
                            <v-col v-for="(list, i) in lists" :key="i" cols="12" lg="12" md="12" class="card-col">
                            <template v-if="list.source == 'IGA'">
                            <v-card outlined>
                                <v-list-item>
                                <v-list-item-avatar size="130" color="grey" class="img-avatar">
                                    <v-img :src="list.image" alt="Item Image" width="100" contain class="mx-auto"></v-img>
                                </v-list-item-avatar>
                                <v-col class="ms-5 card-name" cols="5">
                                    <div class="text-overline" style="line-height: 25px;">
                                    <h3>{{list.name}}</h3>
                                    </div>
                                    <div class="py-3 text-subtitle1 font-weight-bold">
                                    <span><b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}</b></span>
                                    <v-avatar rounded width="150" height="35" class="card-avatar">
                                        <span class="black--text font-weight-bold p-0 card-avatar-inside"> 
                                        Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                        </span>
                                    </v-avatar>
                                    </div>
                                    <div style="padding-top:10px;">
                                    <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'">Woolworths</v-span>              
                                    <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'">Coles</v-span> 
                                    <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'">&nbsp;IGA&nbsp;</v-span> 
                                    </div>
                                </v-col>
                                <v-col class="card-quantity" cols="3">
                                    <v-label style="font-size: 14px;">Quantity</v-label>
                                    <v-text-field variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" @click:append-outer="increment(i)" prepend-icon="mdi-minus" @click:prepend="decrement(i)" style="text-align: center;"></v-text-field>
                                    <v-btn outlined rounded text @click="removeItem(i)" class="my-5 font-weight-bold">Remove</v-btn>
                                    <v-btn rounded @click="boughtItem(i)" class="font-weight-bold mx-3 white--text" color="orange">Bought</v-btn>
                                </v-col>
                                </v-list-item>
                            </v-card>
                            </template>
                            </v-col>
                            <v-divider class="divider"></v-divider>
                        </v-row>
                        </div>
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
                    </v-card-text>
                    </v-card>
                </v-tab-item>
                <!-- Second tab content -->
                <v-tab-item>
                    <v-card flat>
                    <v-card-title>
                        <div style="margin-top: 30px;">
                        <h3>Bought list</h3>
                        <v-col v-for="(list, i) in bought_lists" :key="i" cols="12" lg="12" md="12" class="card-col">
                            <v-card outlined style="color: grey;
        border: 1px solid grey;
        background-color: rgb(236, 236, 236, 0.5);">
                            <v-list-item>
                                <v-list-item-avatar size="125" class="img-avatar">
                                <v-img :src="list.image" alt="Item Image" contain class="mx-auto" style="height: auto;"></v-img>
                                </v-list-item-avatar>
                                <v-col class="ms-5 card-name" cols="5">
                                <div class="text-overline">
                                    <h3>{{list.name}}</h3>
                                </div>
                                <div class="py-3 text-subtitle1 font-weight-bold">
                                    <span><b>$ {{(list.woolworths_price * quantities[i]).toFixed(2)}}</b></span>
                                    <v-avatar rounded width="150" height="35" class="card-avatar">
                                    <span class="black--text font-weight-bold p-0 card-avatar-inside"> 
                                        Save $ {{ (parseFloat(list.coles_price - list.woolworths_price)* quantities[i]).toFixed(2) }}
                                    </span>
                                    </v-avatar>
                                </div>
                                <div style="padding-top:10px;">
                                    <v-span class="green--text font-weight-bold woolies-logo" v-show="list.source == 'Woolworths'">Woolworths</v-span>              
                                    <v-span class="red--text font-weight-bold coles-logo" v-show="list.source == 'Coles'">Coles</v-span> 
                                    <v-span class="font-weight-bold iga-logo" v-show="list.source == 'IGA'">&nbsp;IGA&nbsp;</v-span> 
                                </div>
                                </v-col>
                                <v-col class="card-quantity" cols="3">
                                <v-label style="font-size: 14px;">Quantity</v-label>
                                <v-text-field variant="plain" hide-details="true" v-model="quantities[i]" append-outer-icon="mdi-plus" prepend-icon="mdi-minus" style="text-align: center;" readonly></v-text-field>
                                </v-col>
                            </v-list-item>
                            </v-card>
                        </v-col>
                        </div>
                    </v-card-title>
                    </v-card>
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
        bought_lists: []
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
      boughtItem(index) {
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
.number-box {
  width: 100px;
  border: 1px solid grey;
}
.card-name {
  padding: 40px 0 !important;
}
.card-quantity {
  padding: 38px 0 !important;
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
.card-avatar {
  border-radius: 0;
  justify-content: start;
  margin-left: 20px;
}
.card-avatar-inside {
  background-color: yellow; 
  padding: 6px; 
}
.woolies-logo{
  color: green;
  margin-right: 20px;
  font-size: 20px;
  font-weight: bold;
}
.coles-logo {
  color: red;
  margin-right: 20px;
  font-size: 20px;
  font-weight: bold;
}
.iga-logo {
  background-color: red;
  color: white;
  font-size: 20px;
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
</style>