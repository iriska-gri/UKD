<template>
    <div class="auth-main Form">
        <v-card
            light
            elevation="10"
            color="#FAFAFA"
            class="px-2 px-md-5 pb-4 ma-5 rounded-lg"
        >
            <v-card-title class="bord">Адрес для смены пароля будет отправлен на почту Lotus</v-card-title>
            <v-container>
                <v-form class="row pt-2">
                    <v-text-field
                        class="col-12"
                        v-model="lotus"
                        light
                        :error-messages="Lotus_Errors"
                        required
                        label="Lotus"
                        hide-details="false"
                        @keypress.enter="submitForm"
                    ></v-text-field>
                    
                    <div class="col-12 col-sm-6">
                        <v-btn block @click.prevent="submitForm">Сбросить пароль</v-btn>
                    </div>
                    <div class="col-12 col-sm-6">
                        <v-btn
                            block
                           @click.prevent="$emit('chView', {value: 'login'})"
                            >Назад</v-btn
                        >
                    </div>
                </v-form>
               
            </v-container>
           
        </v-card>
    </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { clearAxios } from '@/utils/axios-api'
import { required, minLength, email, sameAs } from "vuelidate/lib/validators";
export default {
    name: "restore",
    mixins: [validationMixin],
    data: () => ({
        lotus:'',
        show: false,
        
    }),
    validations: {        
        lotus: {required}
    },
    computed: {
        Lotus_Errors() {
            const errors = [];
            if (!this.$v.lotus.$dirty) return errors;
            !this.$v.lotus.required && errors.push("Обязательное поле");
            return errors;
       },
    },
    methods: {
        submitForm(e) {

            localStorage.removeItem("access");
            if (this.$v.$error || this.$v.$invalid) {
                this.$v.$touch();
            } else {
            const formData = {
                lotus: this.lotus,
                
            };
            
             clearAxios.post("/api/restore/", formData)
            .then((response) => {
                // this.user=response.data.user;                
                this.$emit('chView', {value: 'inputcode',datas:response.data.user})
               
            })
            .catch((error) => {                
               
            });
        }},
    }
};
</script>

<style lang="scss" scoped>
</style>