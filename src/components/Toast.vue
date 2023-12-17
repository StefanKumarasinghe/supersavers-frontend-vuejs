<!-- eslint-disable vue/multi-word-component-names -->
<template>
    <div class="text-center ma-2">
        <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" style="bottom: 0;" >
            <v-avatar size="30px" class="me-3">
                <v-icon :color="snackbarColor">{{ snackbarIcon }}</v-icon>
            </v-avatar>
            <span class="white--text font-weight-bold">{{ snackbarMessage }}</span>
            <template v-slot:action="{ attrs }">
                <v-btn
                    :color="snackbarColor"
                    text
                    v-bind="attrs"
                    @click="snackbar = false"
                >
                    <b>Close</b>
                </v-btn>
            </template>
        </v-snackbar>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                snackbar: false,
                snackbarTimeout:2500,
                snackbarMessage: '',
                snackbarColor: 'green',
                snackbarIcon: 'mdi-check-circle'
            }
        },
        methods: {
            showSnackbar(message, color, icon) {
                this.snackbarMessage = message;
                this.snackbarColor = color;
                this.snackbarIcon = icon;
                this.snackbar = true;
            },
        }
    }
</script>