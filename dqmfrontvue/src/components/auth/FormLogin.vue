<template>
    <div class="auth-main Form">
        <v-card
            light
            elevation="10"
            color="#FAFAFA"
            class="px-2 px-md-5 pb-4 ma-5  rounded-lg"
        >
            <v-card-title class="bord mx-3 px-0">Вход</v-card-title>
            <v-container>
                <v-form class="row pt-2">
                    <v-text-field
                        class="col-12"
                        v-model="username"
                        light
                        label="Логин"
                        hide-details="false"
                        @keypress.enter="submitForm"
                    ></v-text-field>
                    <v-text-field
                        class="col-12"
                        v-model="password"
                        :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                        :type="show ? 'text' : 'password'"
                        @click:append="show = !show"
                        @keypress.enter="submitForm"
                        light
                        label="Пароль"
                        hide-details="false"
                    ></v-text-field>
                    <div class="col-12 col-sm-6">
                        <v-btn block @click.prevent="submitForm">Войти</v-btn>
                    </div>
                    <div class="col-12 col-sm-6">
                        <v-btn
                            block
                            @click.prevent="$emit('chView', {value: 'register'})"
                            >Зарегистрироваться</v-btn
                        >
                    </div>
                </v-form>
               <div v-if="crash.length>0" class="col-12"
                        style="position:absolute; bottom: 0; z-index:2; left: 0">
                      <v-alert 
                      dismissible
                      border="bottom"
                      type="error">
                        {{crash}}  
                        <template v-slot:close="{ toggle }">
                            <v-icon @click="closeAlert(toggle)">mdi-close</v-icon>
                        <!-- <v-btn @click="closeAlert(toggle)">Close</v-btn> -->
                            </template>                       
                        </v-alert>
                    </div>
            </v-container>
             <span class="pl-3 pointer"
             @click.prevent="$emit('chView', {value: 'restore'})"             
             >Забыли пароль?</span>
        </v-card>
    </div>
</template>

<script>

export default {
    name: "login",
    data: () => ({
        username: "",
        password: "",
        show: false,
        crash:"",
    }),
    methods: {
        closeAlert(toggle){
            this.crash=""
        },
        submitForm(e) {

            localStorage.removeItem("access");

            const formData = {
                username: this.username,
                password: this.password,
            };
            
            this.$http.post("/api/v1/jwt/my_profile/", formData)
            .then((response) => {
                
                response.data.photo = this.$http.defaults.baseURL.slice(0, -1) + response.data.photo;
                this.$store.commit('setProfile', response.data);
                localStorage.setItem("access", response.data.access);
                localStorage.setItem("refresh", response.data.refresh);
                localStorage.setItem("profile", JSON.stringify(response.data))

                this.$router.push("/");
            })
            .catch((error) => {
                const answer = error.response.data;
                this.crash = answer[Object.keys(answer)[0]]
            });
        },
    }
};
</script>

<style lang="scss">
</style>