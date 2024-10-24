<template>
    <div>
        <v-app>
            <slot/>
        </v-app>
        
    </div>
</template>

<script>
import {baseURL, baseWS} from "@/utils/axios-api"
import { clearAxios } from '@/utils/axios-api'
    export default {
        name: 'auth-layout',
        data(){
            return {
                ws:""
            }
        },
    async mounted(){
        const ip = await clearAxios.get("/api/contacts/ipgetter/")
            
        this.ws= new WebSocket(baseWS+`ws/spy/anonymous/?ip=${ip.data.ip}`)
        
    },
    beforeDestroy() {
        
             this.ws.close()
    },
   

    
    }

</script>

<style lang="scss" scoped>

</style>