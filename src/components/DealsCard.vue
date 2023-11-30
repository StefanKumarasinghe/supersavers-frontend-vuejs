<template>
    <span>
        <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
            <v-img :src="deal.image" width="70%" contain class="text-center mx-auto py-2"></v-img>
            <v-toolbar color="transparent" flat class="py-0">
                <v-avatar color="yellow" rounded width="100" height="35">
                    <span class="black--text font-weight-bold" v-show="deal.new_price != null && deal.old_price != null"> 
                        Save ${{ parseFloat(deal.old_price - deal.new_price).toFixed(2) }}
                    </span>
                </v-avatar>
            </v-toolbar>
            <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
                {{ deal.name }} | {{deal.size}}
            </v-card-title>
            <v-card-text class="text-h5" v-show="deal.new_price && deal.old_price">
                <span class="green--text font-weight-bold mx-2">${{ deal.new_price }}</span>
                <span class="text-decoration-line-through gray--text">${{ deal.old_price }}</span>
            </v-card-text>
            <v-card-text>
                <div class="card-quantity mx-1 my-2">
                    <div class="text-subtitle-1">Quantity:</div>
                    <v-text-field class="text-input black--text font-weight-bold text-subtitle-2" variant="plain" hide-details="true" v-model="quantity" append-outer-icon="mdi-plus" @click:append-outer="increment()" prepend-icon="mdi-minus" @click:prepend="decrement()"></v-text-field>
                </div>
            </v-card-text>
            <v-card-actions class="mx-2"> <!-- Use mt-auto to push the buttons to the bottom -->
                <div class="row">
                    <div class="col-12">
                        <v-btn class="text-none text-h6 mb-3 white--text me-1" width="100%" height="100%" color="green" @click="addItemToCart(deal)" size="small" variant="flat">
                            Add To List
                        </v-btn>
                    </div>
                    <div class="col-12">
                        <v-btn class="text-none text-h6 mb-3" width="100%" height="100%" size="small" variant="flat" @click="Notify(deal)">
                            Listen
                        </v-btn>
                    </div>
                </div>
            </v-card-actions>
        </v-card>
    </span>
</template>

<script>
import { getMessaging, getToken } from 'firebase/messaging';
import firebase from 'firebase/app';

export default {
    props: {
        deal: {
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
        increment () {
            this.quantity += 1;
        },
        decrement () {
            if (this.quantity > 1) {
                this.quantity -= 1;
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
        addItemToCart(product) {
            product.quantity = this.quantity;
            product.bought = false;
            this.$store.dispatch('addItem', product);
            this.error = 'Item was successfully added to the list';
            this.snackbar = true;
        }
    },
};
</script>

<style lang="scss" scoped>

</style>