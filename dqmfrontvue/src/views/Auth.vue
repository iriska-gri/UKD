<template>
    <div class="grid-main">
        <v-app>
            <form-login
                v-if="nowView == 'login'"
                @chView="changeView"
            ></form-login>
            <form-registration
                v-else-if="nowView == 'register'"
                @chView="changeView"
            ></form-registration>
            <form-restore
             v-else-if="nowView == 'restore'"
            @chView="changeView"
            >
            </form-restore>
           
            <form-inputcode :user='user'
             v-else-if="nowView == 'inputcode'"
            @chView="changeView"
            >
            </form-inputcode>
            <!-- <form-restore
             v-else-if="nowView == 'restore'"
            @chView="changeView"
            >

            </form-restore> -->
            <v-snackbar
                v-model="statusReg"
                >
                Вы успешно зарегестрированы

                <template v-slot:action="{ attrs }">
                    <v-btn
                    color="pink"
                    text
                    v-bind="attrs"
                    @click="statusReg = false"
                    >
                    Закрыть
                    </v-btn>
                </template>
                </v-snackbar>
        </v-app>
    </div>
</template>

<script>
import FormRegistration from "@/components/auth/FormRegistration.vue";
import FormLogin from "@/components/auth/FormLogin.vue";
import FormInputcode from "@/components/auth/FormInputcode.vue";
import FormRestore from "@/components/auth/FormRestore.vue";
export default {
    name: 'AuthView',
    components: { FormRegistration, FormLogin,FormRestore, FormInputcode },
    data: () => ({
        nowView: "login",
        statusReg: false,
        user:{}
    }),
    methods: {
        changeView({value, status=false, datas={}} = {}) {
            this.nowView = value;
            this.statusReg = status;
            this.user=datas
        
        },
    },
};
</script>

<style lang="scss">
.auth-main {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #43425d;
    height: 100vh;
    width: 100%;
}

.bord {
    border-bottom: 1px solid #666666;
    font-size: 1.25rem!important;
}
</style>