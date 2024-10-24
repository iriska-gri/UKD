<template>
    <div>
        <v-app>

            <v-overlay v-if="chLoadFrame" :value="true" z-index="100" >
                <v-progress-circular
                    :size="100"
                    :width="7"
                    color="primary"
                    indeterminate
                ></v-progress-circular>
            </v-overlay>
            <navbar-main></navbar-main>
            <v-main><slot /></v-main>
            
        </v-app>
    </div>
</template>

<script>
import {baseURL, baseWS} from "@/utils/axios-api"
import NavbarMain from "../components/NavbarMain.vue";
import { clearAxios } from '@/utils/axios-api'
export default {
    components: {
        NavbarMain,
    },

    computed: {
        chLoadFrame() {
            return this.$store.getters.loadFrame
        }
    },
       
    async mounted() {
       
        let us = JSON.parse(localStorage.getItem('profile'))
        
        this.$store.commit("initializeStore");
        this.$store.commit("loadFrameFalse");   
        const ip = await clearAxios.get("/api/contacts/ipgetter/")  
        // &region=${us.region}

        this.ws= new WebSocket(baseWS+`ws/spy/logged/?ip=${ip.data.ip}&sn=${us.last_name}&region=${us.region}`)
       
   
    },



    beforeDestroy(){
        console.log("navminus");
        this.ws.close()
    }

};
</script>

<style lang="scss" scoped>
</style>