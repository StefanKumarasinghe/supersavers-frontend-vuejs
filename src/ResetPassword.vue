<template>
    <v-app>
        <v-main>
        <!-- Reset Password Form -->
        <v-container fluid>
            <v-row align="center" justify="center" class="">
                <v-col cols="12" md="6" lg="6">
                    <v-card-title class="font-weight-bold orange--text text--darken-2 text-h4">Reset Password</v-card-title>
                    <v-card-text class="text-lg-h6 font-weight-light">Enter new password and confirm password.</v-card-text>
                    <v-card-text class="my-4">
                    <v-form ref="loginForm" v-on:submit.prevent="submitLogin">
                        <v-text-field 
                            class="text-lg-h6" 
                            v-model="password" 
                            label="Password" 
                            :rules="passwordRules" 
                            required
                            type="password" 
                            prepend-inner-icon="mdi-lock"
                            solo
                            flat
                            rounded
                            outlined
                        ></v-text-field>
                        <v-text-field 
                            class="text-lg-h6" 
                            v-model="confirmPassword" 
                            label="Confirm Password" 
                            :rules="confirmPasswordRules" 
                            required
                            type="password" 
                            prepend-inner-icon="mdi-lock"
                            solo
                            flat
                            rounded
                            outlined
                        ></v-text-field>
                        <v-btn color="orange" class="white--text mt-4 text-h6 font-weight-bold" width="100%" rounded height="45" @click="submitRegistration">submit</v-btn>
                    </v-form>
                    </v-card-text>
                </v-col>

                <!-- The image will be hidden on small screens (md and below) -->
                <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6" md="6" lg="6">
                    <v-img
                        :src="require('@/assets/register.jpg')"
                        alt="Login Image"
                        width="100%"
                        height="100%"
                    ></v-img>
                    <p style="font-size: 10px; margin-top: 5px;" class="text-center">
                        Image by <a href="https://www.freepik.com/free-vector/tiny-family-grocery-bag-with-healthy-food-parents-kids-fresh-vegetables-flat-illustration_12291304.htm#page=2&query=grocery%20cartoon&position=0&from_view=search&track=ais&uuid=3a3d4e0d-173d-46b5-beaf-de16b25ebd7e" target="_blank" rel="noopener noreferrer">pch.vector</a> on Freepik
                    </p>        
                </v-col>
            </v-row>
        </v-container>
        </v-main>
    </v-app>
</template>

<script>
    export default {
        data() {
            return {
                password: '',
                passwordRules: [
                    value => { 
                        if (value?.length >= 8) return true
                        return 'Password needs to be at least 8 characters.'
                    }
                ],
                confirmPassword: '',
                confirmPasswordRules: [
                    value => {
                        if (this.password == value) return true
                        return 'Passwords needs to match.'
                    }
                ]
            }
        },
        methods: {
            async submitRegistration() {
                if (this.$refs.loginForm.validate()) {
                    if (this.password !== this.confirmPassword) {
                        alert("Passwords don't match!");
                    } else {
                        this.$router.push('/login');
                    }
                }
            }
        }
    }
</script>

<style>

</style>