<template>
    <div class="grid auth-main Form">
        
        <v-card
            light
            elevation="10"
            color="#FAFAFA"
            class="px-2 px-md-5 pb-4 ma-5 rounded-lg"
        >
            <v-card-title class="bord">Регистрация</v-card-title>
           
            <v-container>
                <v-form class="row pt-2">
                    <v-text-field
                        class="col-6 col-md-6"
                        v-model="username"
                        :error-messages="usernameErrors"
                        light
                        label="Логин"
                        required
                        @input="$v.username.$touch()"
                        @blur="$v.username.$touch()"
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
                        v-model="lotus"
                        light
                        required
                        :error-messages="Lotus_Errors"                         
                        label="Почта Lotus"
                        @input="$v.lotus.$touch()"
                        @blur="$v.lotus.$touch()"
                    ></v-text-field>
                    <v-text-field
                        class="col-12 col-md-6"
                        v-model="password"
                        :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                        light
                        :error-messages="passwordErrors"
                        label="Пароль"
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
                    <v-text-field
                        class="col-12"
                        v-model="last_name"
                        :error-messages="last_nameErrors"
                        light
                        label="Фамилия"
                        required
                        @input="$v.last_name.$touch()"
                        @blur="$v.last_name.$touch()"
                    ></v-text-field>
                    <v-text-field
                        class="col-12"
                        v-model="first_name"
                        :error-messages="first_nameErrors"
                        light
                        label="Имя"
                        required
                        @input="$v.first_name.$touch()"
                        @blur="$v.first_name.$touch()"
                    ></v-text-field>
                    <v-text-field
                        class="col-12"
                        v-model="middle_name"
                        :error-messages="middle_nameErrors"
                        light
                        label="Отчество"
                        required
                        @input="$v.middle_name.$touch()"
                        @blur="$v.middle_name.$touch()"
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
                            Отправить
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
const cyrillic = (x) => /^[А-Яа-яЁё\s\-]+$/i.test(x);
const passwordRule = (x) =>
    /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$/.test(x);

export default {
    name: "register",
    
    mixins: [validationMixin],
     data() {
        return {
            erroror: [],
            show1: false,
            show2: false,
            username: "",
            // email: "",
            password: "",
            confirmPassword: "",
            last_name: "",
            first_name: "",
            middle_name: "",
            lotus:"",
        }
    },
    validations: {
        username: { required, latin },
        email: { email },
        password: { required, minLength: minLength(8), passwordRule },
        confirmPassword: {
            required,
            minLength: minLength(8),
            sameAs: sameAs("password"),
        },
        last_name: { required, cyrillic },
        first_name: { required, cyrillic },
        middle_name: { required, cyrillic },
        lotus: {required}
    },

    computed: {
        usernameErrors() {
            const errors = [];
            if (!this.$v.username.$dirty) return errors;
            !this.$v.username.required && errors.push("Обязательное поле");
            !this.$v.username.latin &&
                errors.push("Поле должно содержать только латинские буквы");
            return errors;
        },
        emailErrors() {
            const errors = [];
            if (!this.$v.email.$dirty) return errors;
            !this.$v.email.email && errors.push("Неправильно введен email");
            return errors;
        },
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
        last_nameErrors() {
            const errors = [];
            if (!this.$v.last_name.$dirty) return errors;
            !this.$v.last_name.required && errors.push("Обязательное поле");
            !this.$v.last_name.cyrillic &&
                errors.push("Поле должно содержать только русские буквы");
            return errors;
        },
       Lotus_Errors() {
            const errors = [];
            if (!this.$v.first_name.$dirty) return errors;
            !this.$v.first_name.required && errors.push("Обязательное поле");
            return errors;
       },
        first_nameErrors() {
            const errors = [];
            if (!this.$v.first_name.$dirty) return errors;
            !this.$v.first_name.required && errors.push("Обязательное поле");
            !this.$v.first_name.cyrillic &&
                errors.push("Поле должно содержать только русские буквы");
            return errors;
        },
        middle_nameErrors() {
            const errors = [];
            if (!this.$v.middle_name.$dirty) return errors;
            !this.$v.middle_name.required && errors.push("Обязательное поле");
            !this.$v.middle_name.cyrillic &&
                errors.push("Поле должно содержать только русские буквы");
            return errors;
        },
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
                clearAxios.post('/api/v1/users/',{
                    username: this.username,
                    password: this.password,
                    // email: this.email,
                    last_name: this.last_name,
                    first_name: this.first_name,
                    middle_name: this.middle_name,
                    lotus:this.lotus,
                })
                .then(response => {
                    this.$emit('chView', {value: 'login', status: true})
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