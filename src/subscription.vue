<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <v-app>
        <v-container fluid>
            <v-col cols="12" lg="1" align-self="center">
                    <v-btn elevation="0" color="grey lighten-2" class="text-center font-weight-bold" to="account" flat>
                        <v-icon>mdi-keyboard-backspace</v-icon> back
                    </v-btn> 
                </v-col>
            <v-row class="text-center pt-5">
                
                <v-col cols="11" lg="11">
                    <h3 class="font-weight-bold">Complete your Payment</h3>
                    <p>Select the best type based on your needs</p>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="12" lg="4" md="12" class="d-flex justify-center">
                    <v-col cols="12" lg="12" md="6" sm="6" class="box-border me-lg-5 me-0">
                        <h5 class="green--text font-weight-bold">Monthly payment</h5>
                        <h5 class="font-weight-bold pt-4">$ AUD 3.99</h5>
                        <p class="font-weight-bold">per month</p>
                        <div class="py-1">
                            <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon>
                            Access to our website
                        </div>
                        <div class="py-1">
                            <v-icon color="grey lighten-1">mdi-check-circle-outline</v-icon>
                            Grocery planning
                        </div>
                    </v-col>
                </v-col>
                <v-col cols="12" lg="8" md="12" class="box-border my-5" @click="show">
                    <v-row>
                        <v-radio-group
                            v-model="row"
                            row
                        >
                        <v-col class="box-border me-0 me-lg-5 me-md-5 me-sm-5 " cols="12" lg="5" md="5" sm="5">
                            <v-radio
                                label="Option 1"
                                value="radio-1"
                                color="green"
                            ></v-radio>
                        </v-col>
                        <v-col class="box-border ms-0 ms-lg-5 ms-md-5 ms-sm-5" cols="12" lg="5" md="5" sm="5">
                            <v-radio
                                label="Option 2"
                                value="radio-2"
                                color="green"
                            ></v-radio>
                        </v-col>
                        </v-radio-group>
                    </v-row>
                </v-col>
            </v-row>

        </v-container>
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
                row: null
            }
        },
        methods: {
            show() {
                console.log("sdfdsf");
            }
        }
    }
</script>

<style>
.box-border {
  border: 1px solid lightgray;
  border-radius: 5px;
  padding: 25px;
}
</style>