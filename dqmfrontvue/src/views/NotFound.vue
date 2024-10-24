
<template>
<v-container class="flex-col vh-100 " fluid>
            <v-col
                class="flex-col"
                >
                <v-row class="align-self-center flex-col">
                  <v-col class="text-bottom grey--text lighten-5">
                    Сожалеем, но страница не найдена или скачиваемый файл не существует
                  </v-col>
                    <v-col
                        class="align-self-center"
                    >
                        <v-img   
                          contain  
                          height="600"     
                          :src= buratinos()
                          >
                      </v-img>
                    </v-col>
                  <v-col class="ma-auto text-center paragraph-text grey--text lighten-5">
                    Попробуйте <a @click="$router.back()"> вернуться</a> обратно и повторить попытку, либо обратитесь в службу поддержки
                  </v-col>
                </v-row>
            </v-col>
</v-container>
  <!-- <div class="NotFound">
    <v-container>
      <v-layout row wrap>
        <v-flex xs12>
          <v-card height="400" color="transparent" flat>
            <div class="display-3 mt-5">404</div>
            <div class="grey--text lighten-5">
              Сожалеем, но страница не найдена или скачиваемый файл не существует
            </div>
            <div class="paragraph-text mt-2">
              <br />
              <br />Попробуйте вернуться обратно и повторить попытку, либо обратитесь в службу поддержки
            </div>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </div> -->
</template>

<script>

import {baseURL} from "@/utils/axios-api"
    export default {
        name: "notfound",
    
   
 
    methods:{
        buratinos(){            
            return baseURL+'media/uploads/404.png'
        }
    }
    }
    
               
                

</script>
<style lang="scss">
@import '@/utils/colors.scss';
  .paragraph-text {
    font-size: 18px;
  }

  .grutIMG {
  max-width: 90%;
  max-height: 90%;
  align-self: center;
}

.entrance {
    max-width: 550px;
    min-width: 550px;
}

.heightvol {
    min-height: 29.5%;
}

.gruit {
  height: 20%;
}

</style>