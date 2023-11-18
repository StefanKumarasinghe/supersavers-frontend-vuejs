<template>
    <span>
        <v-card class="mx-auto rounded-lg d-flex flex-column" max-width="400" height="100%" >
            <v-img :src="deal.image" width="80%" contain class="text-center mx-auto py-5"></v-img>
            <v-toolbar color="transparent" flat>
            <v-avatar color="yellow" rounded width="100" height="35">
                <span class="black--text  font-weight-bold p-0">
                Save ${{ parseFloat(deal.coles_price - deal.woolworths_price).toFixed(2) }}
                </span>
            </v-avatar>
            </v-toolbar>
            <v-card-text class="text-h5">
            <span class="green--text font-weight-bold mx-2">${{ deal.woolworths_price }}</span>
            <span class="text-decoration-line-through gray--text">${{ deal.coles_price }}</span>
            </v-card-text>
            <v-card-title class="black--text font-weight-bold " style="display: inline-block; word-break: break-word;">
            {{ deal.name }} | {{deal.size}}
            </v-card-title>
            <v-spacer></v-spacer> <!-- Add a spacer to push the buttons to the bottom -->
            <v-card-actions class="mx-2 mt-auto"> <!-- Use mt-auto to push the buttons to the bottom -->
            <!-- @click="AddToNotify(product)" -->
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
            deal: {
              type: Object,
              required: true,
            }
        }
    }
</script>

<style lang="scss" scoped>

</style>