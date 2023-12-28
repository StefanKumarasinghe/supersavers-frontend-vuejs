<!-- eslint-disable vue/multi-word-component-names -->
<template>
  <v-app v-if="authenticated">
    <v-container fluid>
      <div class="mx-3">
        <h1 class="fw-bold">Plan Ahead</h1>
        <p class="fw-bold">
          With Grocery Planner, you can plan your trip to the store so you can
          save on the best deals on the correct items.
        </p>
        <p class="p-3 fw-bold bg-danger text-white">
          Deals will finish in: {{ countdown }}, get your deals before it's gone
        </p>
        <button
          @click="shareShoppingList"
          class="font-weight-bold text-start col-6 col-lg-2 text-success"
        >
          <span class="mdi mdi-share-variant"></span>
          Share List
        </button>
        <button
          @click="shareApp"
          class="col-6 text-start col-lg-2 font-weight-bold text-danger"
        >
          <span class="mdi mdi-share-variant"></span>
          Share the love
        </button>
      </div>
      <v-card flat>
        <v-tabs
          style="height: auto"
          v-model="tab"
          background-color="transparent"
          color="green"
          grow
        >
          <v-tab
            style="height: auto"
            v-for="(item, index) in items"
            :key="index"
            class="font-weight-bold"
          >
            <v-img
              style="max-width: 40px"
              class="mx-auto d-block p-3"
              :src="require(`@/assets/${item.image}`)"
            ></v-img>
          </v-tab>
        </v-tabs>

        <v-tabs-items v-model="tab">
          <!-- First content -->
          <v-tab-item>
            <v-expansion-panels
              v-model="panel1"
              :disabled="disabled1"
              multiple
              flat
            >
              <!-- Woolworths -->
              <v-expansion-panel>
                <v-expansion-panel-header class="mt-5">
                  <h3
                    class="green--text font-weight-bold woolies-logo"
                    style="
                      display: inline-block;
                      word-break: break-word;
                      white-space: nowrap;
                    "
                  >
                    Woolworths
                  </h3>
                  <template v-slot:actions>
                    <v-icon color="black" size="30"> $expand </v-icon>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div class="pb-3">
                    <v-span class="fw-bold" v-show="Unbought_w.length == 0"
                      >No items from Woolworths are added to the item to buy
                      list...</v-span
                    >
                  </div>
                  <div
                    v-for="(list, i) in Unbought_w"
                    :key="i"
                    class="d-flex justify-center"
                  >
                    <div
                      class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-12"
                    >
                      <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                        <div class="p-1">
                          <v-img
                            :src="list.image"
                            alt="Item Image"
                            contain
                            class="mx-auto"
                            min-width="130"
                            max-width="140"
                          ></v-img>
                        </div>
                        <div class="py-3 text-center"></div>
                      </div>
                      <div
                        class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center"
                      >
                        <div class="row">
                          <div class="col-12 col-md-4 col-lg-5 col-sm-12">
                            <div class="font-weight-bold">
                              <h5 class="fw-bold">{{list.name}}</h5>
                              <p
                                class="p-3 bg-danger text-white fw-bold"
                                v-if="shouldShowWarning(list.time)"
                              >
                                This product prices may have changed
                              </p>
                            </div>
                            <div class="py-5">
                              <span class="text-h6">
                                <b
                                  >$
                                  {{(list.new_price * list.quantity).toFixed(2)
                                  }}&nbsp;&nbsp;</b
                                >
                              </span>
                              <span
                                class="black--text font-weight-bold card-avatar-inside"
                                style="
                                  display: inline-block;
                                  word-break: break-word;
                                  white-space: nowrap;
                                "
                              >
                                Save $
                                {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                              </span>
                            </div>
                          </div>
                          <div class="col-12 col-md col-lg col-sm-12">
                            <div class="card-quantity">
                              <div class="fw-bold">Quantity:</div>
                              <v-text-field
                                class="text-input black--text font-weight-bold text-subtitle-2"
                                variant="plain"
                                hide-details="true"
                                v-model="list.quantity"
                                append-outer-icon="mdi-plus"
                                @click:append-outer="increment(list.name)"
                                prepend-icon="mdi-minus"
                                @click:prepend="decrement(list.name)"
                              ></v-text-field>
                            </div>
                          </div>
                          <div class="col-12 col-md-5 col-lg col-sm-12">
                            <div
                              class="col-12 col-md-5 col-lg col-sm-12 d-flex justify-between"
                            >
                              <!-- Remove Button -->
                              <v-btn
                                outlined
                                rounded
                                text
                                @click="removeItemFromCart(list.name)"
                                style="border-radius: 0"
                                class="font-weight-bold"
                                height="42"
                                width="120"
                              >
                                <v-icon color="red">
                                  mdi-close-circle-outline
                                </v-icon>
                                Remove
                              </v-btn>

                              <!-- Buy Button -->
                              <v-btn
                                rounded
                                @click="boughtItem(list.name)"
                                class="font-weight-bold white--text ms-4"
                                style="border-radius: 0"
                                color="green"
                                height="40"
                                width="50"
                              >
                                <v-icon> mdi-check-circle </v-icon>
                              </v-btn>
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
                  <h3
                    class="red--text font-weight-bold coles-logo"
                    style="
                      display: inline-block;
                      word-break: break-word;
                      white-space: nowrap;
                    "
                  >
                    Coles
                  </h3>
                  <template v-slot:actions>
                    <v-icon color="black" size="30"> $expand </v-icon>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div class="pb-3">
                    <v-span class="fw-bold" v-show="Unbought_c.length == 0"
                      >No items from Coles are added to the item to buy
                      list...</v-span
                    >
                  </div>
                  <div
                    v-for="(list, i) in Unbought_c"
                    :key="i"
                    class="d-flex justify-center"
                  >
                    <div
                      class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-12"
                      v-if="list.source == 'Coles' && !list.bought"
                    >
                      <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                        <div class="p-1">
                          <v-img
                            :src="list.image"
                            alt="Item Image"
                            contain
                            class="mx-auto"
                            min-width="130"
                            max-width="140"
                          ></v-img>
                        </div>
                        <div class="py-3 text-center"></div>
                      </div>
                      <div
                        class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center"
                      >
                        <div class="row">
                          <div class="col-12 col-md-4 col-lg-5 col-sm-12">
                            <div class="font-weight-bold">
                              <h5 class="fw-bold">{{list.name}}</h5>
                              <p
                                class="p-3 bg-danger text-white fw-bold"
                                v-if="shouldShowWarning(list.time)"
                              >
                                This product prices may have changed
                              </p>
                            </div>
                            <div class="py-5">
                              <span class="text-h6">
                                <b
                                  >$
                                  {{(list.new_price * list.quantity).toFixed(2)
                                  }}&nbsp;&nbsp;</b
                                >
                              </span>
                              <span
                                class="black--text font-weight-bold card-avatar-inside"
                                style="
                                  display: inline-block;
                                  word-break: break-word;
                                  white-space: nowrap;
                                "
                              >
                                Save $
                                {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                              </span>
                            </div>
                          </div>
                          <div class="col-12 col-md col-lg col-sm-12">
                            <div class="card-quantity">
                              <div class="fw-bold">Quantity:</div>
                              <v-text-field
                                class="text-input black--text font-weight-bold text-subtitle-2"
                                variant="plain"
                                hide-details="true"
                                v-model="list.quantity"
                                append-outer-icon="mdi-plus"
                                @click:append-outer="increment(list.name)"
                                prepend-icon="mdi-minus"
                                @click:prepend="decrement(list.name)"
                              ></v-text-field>
                            </div>
                          </div>
                          <div
                            class="col-12 col-md-5 col-lg col-sm-12 d-flex justify-between"
                          >
                            <!-- Remove Button -->
                            <v-btn
                              outlined
                              rounded
                              text
                              @click="removeItemFromCart(list.name)"
                              style="border-radius: 0"
                              class="font-weight-bold"
                              height="42"
                              width="120"
                            >
                              <v-icon color="red">
                                mdi-close-circle-outline
                              </v-icon>
                              Remove
                            </v-btn>

                            <!-- Buy Button -->
                            <v-btn
                              rounded
                              @click="boughtItem(list.name)"
                              class="font-weight-bold white--text ms-4"
                              style="border-radius: 0"
                              color="green"
                              height="40"
                              width="50"
                            >
                              <v-icon> mdi-check-circle </v-icon>
                            </v-btn>
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
                    <h3
                      class="font-weight-bold iga-logo py-2"
                      style="
                        display: inline-block;
                        word-break: break-word;
                        white-space: nowrap;
                      "
                    >
                      &nbsp;IGA&nbsp;
                    </h3>
                  </div>
                  <template v-slot:actions>
                    <v-icon color="black" size="30"> $expand </v-icon>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div class="pb-3">
                    <v-span class="fw-bold" v-show="Unbought_i.length == 0"
                      >No items from IGA are added to the item to buy
                      list...</v-span
                    >
                  </div>
                  <div
                    v-for="(list, i) in Unbought_i"
                    :key="i"
                    class="d-flex justify-center"
                  >
                    <div
                      class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-12"
                      v-if="list.source == 'IGA' && !list.bought"
                    >
                      <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                        <div class="p-1">
                          <v-img
                            :src="list.image"
                            alt="Item Image"
                            contain
                            class="mx-auto"
                            min-width="130"
                            max-width="140"
                          ></v-img>
                        </div>
                        <div class="py-3 text-center"></div>
                      </div>
                      <div
                        class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center"
                      >
                        <div class="row">
                          <div class="col-12 col-md-4 col-lg-5 col-sm-12">
                            <div class="font-weight-bold">
                              <h5 class="fw-bold">{{list.name}}</h5>
                              <p
                                class="p-3 bg-danger text-white fw-bold"
                                v-if="shouldShowWarning(list.time)"
                              >
                                This product prices may have changed
                              </p>
                            </div>
                            <div class="py-5">
                              <span class="text-h6">
                                <b
                                  >$
                                  {{(list.new_price * list.quantity).toFixed(2)
                                  }}&nbsp;&nbsp;</b
                                >
                              </span>
                              <span
                                class="black--text font-weight-bold card-avatar-inside"
                                style="
                                  display: inline-block;
                                  word-break: break-word;
                                  white-space: nowrap;
                                "
                              >
                                Save $
                                {{ (parseFloat(list.old_price - list.new_price)* list.quantity).toFixed(2) }}
                              </span>
                            </div>
                          </div>
                          <div class="col-12 col-md col-lg col-sm-12">
                            <div class="card-quantity">
                              <div class="fw-bold">Quantity:</div>
                              <v-text-field
                                class="text-input black--text font-weight-bold text-subtitle-2"
                                variant="plain"
                                hide-details="true"
                                v-model="list.quantity"
                                append-outer-icon="mdi-plus"
                                @click:append-outer="increment(list.name)"
                                prepend-icon="mdi-minus"
                                @click:prepend="decrement(list.name)"
                              ></v-text-field>
                            </div>
                          </div>
                          <div class="col-12 col-md-5 col-lg col-sm-12">
                            <div
                              class="col-12 col-md-5 col-lg col-sm-12 d-flex justify-between"
                            >
                              <!-- Remove Button -->
                              <v-btn
                                outlined
                                rounded
                                text
                                @click="removeItemFromCart(list.name)"
                                style="border-radius: 0"
                                class="font-weight-bold"
                                height="42"
                                width="120"
                              >
                                <v-icon color="red">
                                  mdi-close-circle-outline
                                </v-icon>
                                Remove
                              </v-btn>

                              <!-- Buy Button -->
                              <v-btn
                                rounded
                                @click="boughtItem(list.name)"
                                class="font-weight-bold white--text ms-4"
                                style="border-radius: 0"
                                color="green"
                                height="40"
                                width="50"
                              >
                                <v-icon> mdi-check-circle </v-icon>
                              </v-btn>
                            </div>
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
                  <span
                    class="black--text font-weight-bold p-0 card-avatar-inside"
                  >
                    Save {{saveTotal()}}
                  </span>
                </v-avatar>
              </div>
            </div>
          </v-tab-item>

          <!-- Second tab content -->
          <v-tab-item>
            <v-btn
              color="primary"
              class="mx-5 d-block w-100 fw-bold mt-5"
              @click="toggleAdvancedFilter"
              ><v-icon>mdi-filter</v-icon>Advance Filter</v-btn
            >

            <v-collapse v-if="isAdvancedFilterOpen">
              <v-row class="mb-4 w-100 mx-auto px-5">
                <v-col cols="12">
                  <p>
                    Please select a range or a particular day to limit the items
                    you bought
                  </p>
                  <v-date-picker
                    v-model="dateRange"
                    range
                    class="mx-auto d-block"
                    label="Date Range"
                  ></v-date-picker>
                </v-col>
              </v-row>
            </v-collapse>
            <v-expansion-panels
              v-model="panel2"
              :disabled="disabled2"
              multiple
              flat
            >
              <!-- ALL BOUGHT -->

              <v-expansion-panel
                v-for="(group, groupName) in groupedBoughtOrders"
                :key="groupName"
              >
                <v-expansion-panel-header class="mt-1">
                  <div class="">
                    <h4 class="fw-bold p-3">{{ groupName }}</h4>
                  </div>
                  <template v-slot:actions>
                    <v-icon class="" size="30">$expand</v-icon>
                  </template>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <div class="pb-3">
                    <v-span v-show="group.length === 0"
                      >You haven't bought anything...</v-span
                    >
                  </div>

                  <div
                    v-for="(list, i) in group"
                    :key="i"
                    class="d-flex justify-center"
                  >
                    <div
                      class="row box my-4 py-5 col-lg-12 col-md-12 col-sm-12 col-12"
                    >
                      <div class="col-12 col-md-2 col-lg-2 col-sm-12 py-0">
                        <div class="p-1">
                          <v-img
                            :src="list.image"
                            alt="Item Image"
                            contain
                            class="mx-auto"
                            min-width="130"
                            max-width="180"
                          ></v-img>
                        </div>
                        <div class="py-3 text-center">
                          <v-span
                            class="green--text font-weight-bold woolies-logo"
                            v-show="list.source == 'Woolworths'"
                            style="
                              display: inline-block;
                              word-break: break-word;
                              white-space: nowrap;
                            "
                            >Woolworths</v-span
                          >
                          <v-span
                            class="red--text font-weight-bold coles-logo"
                            v-show="list.source == 'Coles'"
                            style="
                              display: inline-block;
                              word-break: break-word;
                              white-space: nowrap;
                            "
                            >Coles</v-span
                          >
                          <v-span
                            class="font-weight-bold iga-logo"
                            v-show="list.source == 'IGA'"
                            style="
                              display: inline-block;
                              word-break: break-word;
                              white-space: nowrap;
                            "
                            >&nbsp;IGA&nbsp;</v-span
                          >
                        </div>
                      </div>
                      <div
                        class="col-12 col-md-10 col-lg-10 col-sm-12 py-0 text-sm-center text-md-start text-lg-start text-center d-flex align-center"
                      >
                        <div class="row">
                          <div class="col-12 col-md col-lg-5 col-sm-12">
                            <div class="fw-bold">
                              <h6 class="fw-bold">{{ list.name }}</h6>
                            </div>
                            <div class="py-5">
                              <span class="text-h6">
                                <b
                                  >$
                                  {{ (list.new_price * list.quantity).toFixed(2)
                                  }}&nbsp;&nbsp;</b
                                >
                              </span>
                              <span
                                class="black--text font-weight-bold card-avatar-inside"
                                style="
                                  display: inline-block;
                                  word-break: break-word;
                                  white-space: nowrap;
                                "
                              >
                                Saved $
                                {{ (parseFloat(list.old_price - list.new_price) * list.quantity).toFixed(2) }}
                              </span>
                            </div>
                          </div>
                          <div class="col-12 col-md col-lg col-sm-12">
                            <div class="card-quantity">
                              <div class="text-subtitle-1">Quantity:</div>
                              <v-text-field
                                class="text-input black--text font-weight-bold text-subtitle-2"
                                variant="plain"
                                hide-details="true"
                                v-model="list.quantity"
                                readonly
                              ></v-text-field>
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
    <Toast ref="Toast" />
  </v-app>
</template>

<script>
import Toast from './components/Toast.vue';

export default {
  metaInfo: {
  // Page Title
  title: 'Supersavers | Plan Ahead and Save Heaps',

  // Meta Tags
  meta: [
    { charset: 'utf-8' }, // Character set
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }, // Responsive design

    // SEO Meta Tags
    { name: 'description', content: 'Explore and manage your shopping cart with Supersavers. Plan ahead, track your spending, view savings, and keep a record of your previous purchases. Maximize your grocery shopping experience!' }, // Page description
    { name: 'keywords', content: 'Supersavers, shopping cart, groceries, plan ahead, track spending, savings, previous purchases, maximize shopping experience' }, // Keywords for SEO

    // Open Graph (OG) Meta Tags
    { property: 'og:title', content: 'Supersavers | My Shopping Cart' }, // Open Graph title
    { property: 'og:description', content: 'Explore and manage your shopping cart with Supersavers. Plan ahead, track your spending, view savings, and keep a record of your previous purchases. Maximize your grocery shopping experience!' }, // Open Graph description
    { property: 'og:image', content: 'https://supersavers.au/banner.png' }, // Open Graph image
    { property: 'og:url', content: 'https://supersavers.au/cart' }, // Open Graph URL
    { property: 'og:type', content: 'website' }, // Open Graph type (e.g., article, website)

    // Twitter Meta Tags
    { name: 'twitter:title', content: 'Supersavers | My Shopping Cart' }, // Twitter title
    { name: 'twitter:description', content: 'Explore and manage your shopping cart with Supersavers. Plan ahead, track your spending, view savings, and keep a record of your previous purchases. Maximize your grocery shopping experience!' }, // Twitter description
    { name: 'twitter:image', content: 'https://supersavers.au/banner.png' }, // Twitter image
    { name: 'twitter:card', content: 'summary_large_image' }, // Twitter card type
  ],
},

    components: {
     Toast
    },
    data () {
      return {
        targetTime: null,
      countdown: null,
        isAdvancedFilterOpen:false,
        dateRange: null,
        authenticated:false,
        panel1: [0, 1, 2],
        panel2: [0, 1, 2],
        disabled1: false,
        disabled2: false,
        tab: null,
        items: [ {
          name:'Items to buy', image:'list.png'}, {name: 'Bought items', image:'calendar.png'}
        ],
        lists: [],
        bought: [],
        unbought:[],
        quantities: []
      }
    },
    async beforeMount() {
      await this.TokenPromise()
      this.lists = this.$store.getters.getList;
      for (let i = 0; i < this.lists.length; i++) {
        this.quantities[i] = this.lists[i].quantity;
      }
    },
    mounted () {
      this.setTargetTime();
      setInterval(this.updateCountdown, 1000);
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
    bought_order() {
        if (this.dateRange) {
          const [start, end] = this.dateRange;
          return this.bought
            .filter(item => item.time >= start && item.time <= end)
            .slice()
            .sort((a, b) => new Date(b.time) - new Date(a.time));
        } else {
          return this.bought.slice().sort((a, b) => new Date(b.time) - new Date(a.time));
        }
      },
    groupedBoughtOrders() {
        const groups = {};
        this.bought_order.forEach((list) => {
        const groupName = this.getGroupName(list.time);
        if (!groups[groupName]) {
            groups[groupName] = [];
          }
          groups[groupName].push(list);
        });
        return groups;
    },
    },
    methods: {
    async SubscriptionCheck() {
        try {
        const response = await fetch(`${this.$GroceryAPI}/valid_subscription`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${this.AuthToken}`,
        },
        });
        if (!response.ok) {
        this.$router.push('/subscription')
        }else{
        this.authenticated=true
        }
    } catch (error) {
        console.error('Something went wrong with verifying your subscription', error);
        this.$refs.Toast.showSnackbar('Something went wrong when accessing our server', 'red', 'mdi-alert-circle');
    }
    },
    shouldShowWarning(time) {
      if (time) {
          const currentTime = new Date();
          // Calculate the difference in days between the current day and Wednesday (considering Sunday as the first day of the week)
          const daysUntilWednesday = (3 - currentTime.getDay() + 7);
          // Create a new Date object for the nearest Wednesday at 1 am
          const nearestWednesday = new Date(currentTime);
          nearestWednesday.setDate(currentTime.getDate() - daysUntilWednesday +1);
          nearestWednesday.setHours(1, 0, 0, 0);
          const wednesdayCutoff = new Date(time);
          // Parse the time string and set the hours, minutes, seconds, and milliseconds to 0
          const timeParts = time.split('T')[1].split(':');
          wednesdayCutoff.setHours(timeParts[0], timeParts[1], timeParts[2], 0);
          // Set the cutoff time to 1 am
          wednesdayCutoff.setHours(1, 0, 0, 0);
          return nearestWednesday > wednesdayCutoff;
        }
        return false;
    },
    getGroupName(date) {
        const currentDate = new Date();
        const itemDate = new Date(date);
        const daysDifference = Math.floor((currentDate - itemDate) / (24 * 60 * 60 * 1000));

        if (daysDifference <= 7) {
          return 'This Week';
        } else if (daysDifference <= 14) {
          return 'Last Week';
        } else {
          return 'A While Ago';
        }
    },
    async beforeMount() {
      await this.TokenPromise();
    },
    async TokenPromise() {
      this.AuthToken = await this.getToken();
      this.verifyAuthProcess();
    },
    setTargetTime() {
  const now = new Date();
  const targetDay = 3; // Wednesday (0 is Sunday, 1 is Monday, ..., 6 is Saturday)
  const targetHour = 0; // 12:00 AM
  const targetMinute = 0;
  const targetSecond = 0;

  // Calculate the time until the next target day
  const timeUntilTargetDay = (targetDay - now.getDay() + 7);

  // Set the target date to the next Wednesday
  this.targetTime = new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate() + timeUntilTargetDay,
    targetHour,
    targetMinute,
    targetSecond
  );
},

updateCountdown() {
  // Set the target date to the next Wednesday using setTargetTime
  this.setTargetTime();

  // Get the current date
  const now = new Date();

  // Calculate the time difference between now and the target date
  const timeDifference = this.targetTime - now;

  // Convert the time difference to days, hours, minutes, and seconds
  const seconds = Math.floor((timeDifference / 1000) % 60);
  const minutes = Math.floor((timeDifference / 1000 / 60) % 60);
  const hours = Math.floor((timeDifference / (1000 * 60 * 60)) % 24);
  const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

  // Update the countdown
  this.countdown = `${days}d ${hours}h ${minutes}m ${seconds}s`;
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
      try {
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
              this.SubscriptionCheck()
            }
          } catch (error) {
          console.error('Something went wrong with verification', error);
          this.$refs.Toast.showSnackbar('Something went wrong', 'red', 'mdi-alert-circle');
        }
    },
    async fetchCart() {
        try {
          const unboughtResponse = await fetch(`${this.$GroceryAPI}/retrieve_unbought`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          const unboughtData = await unboughtResponse.json();
          this.unbought = unboughtData; // Update with your actual data structure
        } catch (error) {
          console.error('Error fetching unbought products:', error);
          this.$refs.Toast.showSnackbar('Something went wrong fetching the cart', 'red', 'mdi-alert-circle');
        }

        try {
          const boughtResponse = await fetch(`${this.$GroceryAPI}/retrieve_bought`, {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${this.AuthToken}`,
            },
          });
          const boughtData = await boughtResponse.json();
          this.bought = boughtData; // Update with your actual data structure
        } catch (error) {
          console.error('Error fetching bought products:', error);
          this.$refs.Toast.showSnackbar('Something went wrong fetching your history', 'red', 'mdi-alert-circle');
        }
    },
    toggleAdvancedFilter() {
      this.isAdvancedFilterOpen = !this.isAdvancedFilterOpen;
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
          this.$refs.Toast.showSnackbar('Something went wrong removing the item', 'red', 'mdi-alert-circle');
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
          this.$refs.Toast.showSnackbar('Session was invalidated', 'red', 'mdi-alert-circle');
          console.error('Error:', error);
          this.$store.commit('clearToken');
          this.$router.push('/login');
          window.location.reload();
        }
      },
      async increment(name) {
        try {
          let index = this.unbought.findIndex(item => item.name == name);
          if (this.unbought[index].quantity<100) {
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
                this.unbought[index].quantity = this.unbought[index].quantity + 1;
              }
            }
        } catch (error) {
            console.error('Error updating cart:', error);
            this.$refs.Toast.showSnackbar('Something went wrong with updating the quantity', 'red', 'mdi-alert-circle');
        }
      },
      async decrement(name) {
        let index = this.unbought.findIndex(item => item.name == name);
        if (this.unbought[index].quantity > 0) {
          try {
            
            const response = await fetch(`${this.$GroceryAPI}/reduce_cart_quantity`, {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${this.AuthToken}`,
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                name: String(this.unbought[index].name),
              }),
            });

            if (response.ok) {
              this.unbought[index].quantity = Math.max(this.unbought[index].quantity - 1, 0);
            } else {
              console.error('Error updating cart:', response.statusText);
            }
          } catch (error) {
            console.error('Error updating cart:', error);
            this.$refs.Toast.showSnackbar('Something went wrong with updating the quantity', 'red', 'mdi-alert-circle');
          }
        } else {
          console.warn('Quantity cannot be less than 0.');
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
      const itemsByStore = {
        Woolworths: [],
        Coles: [],
        IGA: [],
      };
      // Categorize items by store
      for (const item of this.unbought) {
        const quantity = item.quantity || 1;
        const itemMessage = `🛒 ${quantity} x ${item.name}`;
        // Determine the store for the item
        let storeName = 'Unknown';
        if (item.source === 'Woolworths') {
          storeName = 'Woolworths';
        } else if (item.source === 'Coles') {
          storeName = 'Coles';
        } else if (item.source === 'IGA') {
          storeName = 'IGA';
        }
        itemsByStore[storeName].push(itemMessage);
      }
      // Create the message parts
      const messageParts = [];
      for (const storeName in itemsByStore) {
        if (itemsByStore[storeName].length > 0) {
          messageParts.push(`--- ${storeName} ---`);
          messageParts.push(...itemsByStore[storeName]);
        }
      }
      // Add total and save amounts to the message
      const totalMessage = `💵 Your Total Bill: $${this.calTotal()}`;
      const saveMessage = `💰 You Saved: $${this.saveTotal()}!`;
      const detailsMessage = `🌐 For more details, visit (https://supersavers.au) to save heaps on groceries.`;
      messageParts.push(totalMessage);
      messageParts.push(saveMessage);
      messageParts.push(detailsMessage);
      return messageParts.join('\n');
    },
    shareShoppingList() {
      const message = this.generateShareMessage();
      if (navigator.share) {
        navigator
          .share({
            title: 'SuperSavers Grocery List',
            text: message,
          })
          .then(() => this.$refs.Toast.showSnackbar('Shared Successfully', 'green', 'mdi-check-circle'))
          .catch(() => this.$refs.Toast.showSnackbar('Sorry, it was not shared successfully', 'red', 'mdi-alert-circle'));
      } else {
        this.$refs.Toast.showSnackbar('Sadly, you canceled your message', 'red', 'mdi-alert-circle')
      }
    },
    shareApp() {
      if (navigator.share) {
        navigator
          .share({
            title: '💰 Save money with supersavers on groceries! 🛒',
            text: "🌟 You can save heaps at Coles, Woolies, and IGA with supersavers by never missing out on deals. Visit (https://supersavers.au) 🌐",
          })
          .then(() => this.$refs.Toast.showSnackbar('Shared Successfully', 'green', 'mdi-check-circle'))
          .catch(() => this.$refs.Toast.showSnackbar('Sorry, it was not shared successfully', 'red', 'mdi-alert-circle'));
      } else {
        this.$refs.Toast.showSnackbar('Sadly, you canceled your message', 'red', 'mdi-alert-circle')
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
          if (index !== -1) {
            let removedItem = this.unbought.splice(index, 1)[0];
            this.bought.push(removedItem);
            this.$refs.Toast.showSnackbar('Item successfully bought and stored', 'green', 'mdi-check-circle')
          } else {
            console.error(`Could not remove item`);
            this.$refs.Toast.showSnackbar('Could not find the item you are trying to buy. Please do not mess with the code', 'red', 'mdi-alert-circle')
          } 
        } else {
            console.error('Error updating cart:', response.statusText);
            this.$refs.Toast.showSnackbar('Something went wrong with updating your cart', 'red', 'mdi-alert-circle')
        }
      } catch (error) {
          console.error('Error updating cart:', error);
          this.$refs.Toast.showSnackbar('There was an error updating your cart', 'red', 'mdi-alert-circle')
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
          if (index !== -1) {
            this.unbought.splice(index, 1)[0];
            this.$refs.Toast.showSnackbar('Item successfully removed', 'green', 'mdi-check-circle')
          } else {
            this.$refs.Toast.showSnackbar('Could not find that item. Please reload the page', 'red', 'mdi-alert-circle')
          }
        } else {
          this.$refs.Toast.showSnackbar('There was an error updating your cart', 'red', 'mdi-alert-circle')
        }
      } catch (error) {
        console.error('Error updating cart:', error);
        this.$refs.Toast.showSnackbar('There was an error updating your cart', 'red', 'mdi-alert-circle')
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
  display: inline-block;
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
.woolies-logo {
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
  margin-top: 20px;
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
  border: 1px solid rgb(128, 128, 128, 0.3);
  border-radius: 5px;
  margin-left: 20px;
  margin-right: 20px;
}
.img {
  width: 120px;
}
</style>
