<template>
    <span>
        <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="500" height="100%" >
            <v-img :src="deal.image" width="90%" contain class="text-start mx-auto  py-2">     <button @click="shareApp(deal)" large class="text-start text-danger fw-bold  m-1 font-weight-bold">
      <v-icon class="mdi text-danger mdi-share-variant">mdi-share-variant</v-icon>
    </button></v-img>
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
                        <v-btn class=" fw-bold mb-3 white--text me-1" width="100%" height="45px" color="green" @click="addItemToCart(deal)" size="small" variant="flat">
                            Add To List
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
import Toast from './Toast.vue';

export default {
    components: {
     Toast
    },
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
            quantity: 1,
            snackbar: false,
            snackbarTimeout: 2500
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
        shareApp(product) {
        // Check if the Web Share API is supported by the browser
        if (navigator.share) {
            // Calculate savings
            const savings = product.old_price - product.new_price;

            // Message parts with icons and dynamic content
            const messageParts = [
            `🌟 Hey there! Quick heads up: ${product.name} is on sale right now at ${product.source}! 🎉`,
            `💸 It was originally AUD ${product.old_price}, but now it's only AUD ${product.new_price}.`,
            `💰 Save AUD ${savings} on this deal!`,
            `🛒 Visit supersavers.au to snag this awesome deal 🌈`,
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
            .then(() => this.$refs.Toast.showSnackbar('Shared successfully', 'green', 'mdi-check-circle'))
            .catch(() => this.$refs.Toast.showSnackbar('Something went wrong sharing the message', 'red', 'mdi-alert-circle'));
        } else {
            console.error('Error sharing: Web Share API is not supported');
            this.$refs.Toast.showSnackbar('You have not enabled the sharing feature', 'red', 'mdi-alert-circle');
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
        async addItemToCart(product) {
        try {
            product.quantity = this.quantity;
            if (product.quantity<1) {
                throw ("Product quantity must be positive")
            }
            product.bought = false;
            const response = await fetch(`${this.$GroceryAPI}/add_item_cart`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.AuthToken}`,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name: String(product.name),
                    old_price: parseFloat(product.old_price),
                    new_price: parseFloat(product.new_price),
                    source: String(product.source),
                    quantity: parseInt(product.quantity, 10),
                    image: String(product.image),
                    description: String(product.description),
                }),
            });
            if (response.ok) {
            this.$refs.Toast.showSnackbar('Added to your grocery list successfully', 'green', 'mdi-check-circle');
            }else{
            this.$refs.Toast.showSnackbar('Server refused to accept your key', 'red', 'mdi-alert-circle');  
            }
        } catch (error) {
            console.error('Error adding item to cart:', error);
            this.$refs.Toast.showSnackbar('Something went wrong when adding to your list', 'red', 'mdi-alert-circle')
        }
    }
    },
};
</script>

<style lang="scss" scoped>

</style>