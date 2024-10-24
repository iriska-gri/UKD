<template>
    <div class="grid auth-main Form">
        
        <v-card
            light
            elevation="10"
            color="#FAFAFA"
            class="px-2 px-md-5 pb-4 ma-5 rounded-lg"
        >
            <v-card-title class="bord">Восстановление пароля</v-card-title>
          
            <v-container>
                 <b>{{user.first_name}} {{user.middle_name}}</b>, введите код подтверждения и новый пароль
                <v-form class="row pt-2">
                    <v-text-field
                        class="col-6 col-md-6"
                        :v-model="username"
                        disabled
                        light
                        :label='user.login'
                        
                    ></v-text-field>
                    <v-text-field
                        class="col-6 col-md-6"
                        v-model="randomurl"
                        :error-messages="Code_Errors"
                        required
                        light
                        label="Проверочный код"
                        
                    ></v-text-field>
                    <!-- <v-text-field
                        class="col-6 col-md-3"
                        v-model="email"
                        light
                        :error-messages="emailErrors"
                        label="Почта"
                        @input="$v.email.$touch()"
                        @blur="$v.email.$touch()"
                    ></v-text-field> -->
                    
                    <v-text-field
                        class="col-12 col-md-6"
                        v-model="password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        light
                        :error-messages="passwordErrors"
                        label="Новый Пароль"
                        required
                        :type="show1 ? 'text' : 'password'"
                        counter
                        @input="$v.password.$touch()"
                        @blur="$v.password.$touch()"
                        @click:append="show1 = !show1"
                    ></v-text-field>
                    <v-text-field
                        class="col-12 col-md-6"
                        v-model="confirmPassword"
                        :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                        light
                        :type="show2 ? 'text' : 'password'"
                        counter
                        :error-messages="confirmPasswordErrors"
                        label="Повторите пароль"
                        required
                        @input="$v.confirmPassword.$touch()"
                        @blur="$v.confirmPassword.$touch()"
                        @click:append="show2 = !show2"
                    ></v-text-field>
                    
                   
                    
                    <div v-if="erroror.length>0" class="col-12"
                        style="position:absolute; bottom: 0; z-index:2; left: 0">
                      <v-alert 
                      dismissible
                      border="bottom"
                      type="error">
                        {{errtext()}}                         
                        </v-alert>
                    </div>
                    <div class="col-6">
                        <v-btn block elevation="3" @click="submit">
                            Изменить пароль
                        </v-btn>
                    </div>
                    <div class="col-6">
                        <v-btn
                            block
                            elevation="3"
                            @click.prevent="$emit('chView', {value: 'login'})"
                        >
                            Назад
                        </v-btn>
                    </div>
                </v-form>
                
            </v-container>
           
        </v-card>
         
    </div>
    
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, minLength, email, sameAs } from "vuelidate/lib/validators";
import { clearAxios } from '@/utils/axios-api'

// const mustBeCool = (value) => !helpers.req(value) || value.indexOf('cool') >= 0
const latin = (x) => /^[A-za-z]+$/i.test(x);
const cyrillic = (x) => /^[А-Яа-яЁё]+$/i.test(x);
const passwordRule = (x) =>
    /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$/.test(x);

export default {
    name: "inputcode",
    
    mixins: [validationMixin],
    props:{
        user:{type:Object,
        default:{}}
    },
     data() {
        return {
            erroror: [],
            show1: false,
            show2: false,
            username: "",
            // email: "",
            password: "",
            confirmPassword: "",
            randomurl:'',

           
        }
    },

    validations: {
        
        randomurl: { required },
        password: { required, minLength: minLength(8), passwordRule },
        confirmPassword: {
            required,
            minLength: minLength(8),
            sameAs: sameAs("password"),
        },
        
    },

    computed: {        
        passwordErrors() {
            const errors = [];
            if (!this.$v.password.$dirty) return errors;
            !this.$v.password.required && errors.push("Обязательное поле");
            !this.$v.password.minLength &&
                errors.push("Пароль должен быть более 8 символов");
            !this.$v.password.passwordRule &&
                errors.push("Cтрочные и прописные латинские буквы, цифры");
            return errors;
        },
        confirmPasswordErrors() {
            const errors = [];
            if (!this.$v.confirmPassword.$dirty) return errors;
            !this.$v.confirmPassword.sameAs &&
                errors.push("Пароли не совпадают");
            return errors;
        },

        Code_Errors(){
            
             const errors = [];
            if (!this.$v.randomurl.$dirty) return errors;
            !this.$v.randomurl.required && errors.push("Обязательное поле");
            return errors;
        }
       
    },
    methods: {
        errtext(){
            return this.erroror.map((e)=>{return e}).join(", ")

        },
        submit() {
            
            if (this.$v.$error || this.$v.$invalid) {
                this.$v.$touch();
            } else {
                this.erroror=[]
                clearAxios.post('/api/restore/',{
                    
                    password: this.password,                                       
                    randomurl:this.randomurl,
                })
                .then(response => {
                    this.$emit('chView', {value: 'login', status: false})
                })
                .catch(error => {
                    
                    for (let [key, val] of Object.entries(error.response.data)){
                        this.erroror.push(val[0])
                    }                    
                
                })
            }
            
        },
        clear() {
            this.$v.$reset();
            this.username = "";
            this.email = "";
        },
    },
};
</script>

<style lang="scss">

.grid {
    padding: 20%;
}

.v-messages__message {
    position: absolute;
}

@media (max-width: 1200px) {
    .grid {
        padding: 0;
    }

}


</style>