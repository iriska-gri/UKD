<template>
<div class="flex-container">
  <div class="flex-static_row justify-start pl-5 pt-3 thebiggest_help Help_item_1 mx-auto">ТЕХПОДДЕРЖКА</div>
  <!-- <v-divider></v-divider> -->
    
      <div class="pl-5 mt-5">
        <div class="Help_item_H">Телефон поддержки: {{content.contacts?content.contacts.phone:""}}</div>
        <div class="Help_item_H">Электронная почта: {{content.contacts?content.contacts.email:""}}</div>
      </div>
      
      
  
  <div class="flex-item flex-row Help_item_2" v-if="'contacts' in content">
    <div class="flex-item flex-col Help_item_2_1" >
    
        <v-img   
          contain         
          class="grutIMG"        
          :src="content.contacts.imagepath"
          >
      </v-img>

    </div>
    <div class="flex-item flex-col px-4 pt-3 Help_item_2_2 ">
      <v-card
        class="flex-item Help_item_2_2_1 pa-4" 
        v-html="content.contacts.topblock.replaceAll('px', 'px !important;')"
      >
      </v-card>
 
          <!-- <v-card  class="flex-item Help_item_2_2_2 pa-4" -->
           
    <!-- > -->
    <!-- <template> -->
      <v-data-table
      
      hide-default-footer
      :headers="headers"
      :items="desserts"
      
      class="elevation-1 flex-item Help_item_2_2_2 pa-4"
      ></v-data-table>
    <!-- </template> -->
     <!-- v-html="content.bottomblock.replaceAll('px', 'px !important;')" -->
            
          <!-- </v-card> -->
        
        <div class="flex-static-row bigimg Help_item_2_2_3 pt-5">
        <v-btn class="mb-2"
        color="#1B559E"
         @click="dialog=true">
           <v-icon class="bigimg" color="white">{{ "mdi-wechat" }}</v-icon><span style="color:white">Задать вопрос</span> 
        </v-btn>
        </div>
    </div>
  </div>
    <v-dialog
      @click:outside="dialog=false"
      v-model="dialog"
      persistent
      max-width="800px"
    >      
      <v-card>
        <v-card-title>
          <span class="text-h5 pl-3">Задайте свой вопрос:</span>
        </v-card-title>
        <v-card-text>
          <v-container>
              <v-textarea
                :rows=8
                :error= error
                :success= succes
                :error-messages="errormessage"
                solo
                placeholder="Введите текст..."
                v-model="question" 
                auto-grow
                @input="validatoring"
                   
                ></v-textarea>
          <div>
                            <h2 class="bgpurple ml-2">Приложите файлы:</h2>
                           
                        <multi-input :filesglob="files" :dubfilesglob="dubfiles" :clear="!dialog"  @adfto='adfto'/>
                        </div>
          </v-container>
          <small class="pl-3">{{username}}, наш сотрудник сформирует ответ и отправит его по адресу Lotus:<br>  <b class="pl-3">{{lotus}}</b></small> 
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            
            color="primary"
            @click="dialog = false"
          >
            Отмена
          </v-btn>
          <v-btn
            color="primary"
            
            @click="sends"
          >
            Отправить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</div>
</template>

<script>
import { createNamespacedHelpers } from "vuex";
import MultiInput from '../components/UI/MultiInput'
import jshelper from '@/utils/helper' 

    export default {
        name: "Helper",
      components: {MultiInput},
     data(){
     return {
         files:[],
         dubfiles:new Set(),
         error: false,
         dialog:  false,
         succes: false,
         errormessage: "",
         username:"",
         lotus:"",
         question: '',
         desserts:[],
          headers: [
          {
            text: 'ФИО методолога',
            align: 'start',
            sortable: true,
            value: 'name',
          },
          { text: '№ паспорта ФБ1', value: 'code' },
          { text: 'Контактный телефон', value: 'phone' },
          
        ],
         content:{  
          contacts:{         
            phone: "",
            topblock:"",
            bottomblock:[],
            imagepath:""
          }
         }
     }
     },    

    async mounted() { 
         jshelper.permissiondenied(this.$route.path)
        const data = await this.$http
            .get('/api/contacts/helper/')
        this.content = data.data;      
        
        this.username = `${this.$store.getters.first_name} ${this.$store.getters.middle_name}`
        this.lotus = this.$store.getters.lotus
        this.desserts=jshelper.gettabdata(data.data.metodologs)
    },

    methods:{
       
        sends(){
            
            if (this.question.length==0){
                this.error=true
                this.errormessage="Вы не ввели текст вопроса"
                return
            }
            const sdata = new FormData();
            sdata.append('question', this.question);
            if (this.files.length>0) {                    
                    for (let el of this.files){
                       
                        sdata.append('file',el)                    
                    }
                }
             
            this.$http
                .put('/api/contacts/helper/', sdata)
                .then((data) => {
                    if (data.status==200) {                        
                        this.dialog=false
                        this.question=""
                        this.succes=false
                        this.error=false
                        this.errormessage=""
                        this.files = []
                        this.dubfiles=new Set()
                     

                    } else {
                      alert("Что-то не так");
                    }
        })
        


        },
         adfto(data){
         
            this.files=data[0]
            this.dubfiles=data[1]
            
        },
        validatoring(){
            if(this.error){
                this.error=false
                this.errormessage=""
            }
            if(this.question.length>20) this.succes=true
        },
    


    },
    }


</script>

<style lang="scss">
@import '@/utils/colors.scss';
// tbody {
//      tr:hover {
//         background-color: transparent !important;
//      }
//    }  

 tbody 
 {tr :hover {
  cursor: default;
}}

.thebiggest_help {
  // font-size: 3rem !important;
font-size: 2.5rem!important;
  font-weight: 800;
  color: $bg-purple;
}

.Help_item_1 {
  height: 70px;
}

.Help_item_0 {
  height: 15%;
}

.Help_item_0_1 {
  width: 10%;
}
.Help_item_0_2 {
   width: 20%;
}

.Help_item_2_1 {
  width: 10%;
  min-width: 350px;
  min-height: 150px;
  justify-content: end;
    div .v-responsive__sizer {
      padding-bottom: 0!important;
  }
}

.Help_item_2_2 {
  gap:15px;
  width: 20%;
  min-width: 350px;
}

.Help_item_2_1_1 {
  align-items: center;
}

.Help_item_2_1_2 {
  justify-content: center;
  align-self: center;
  width: 100%;
    div .v-responsive__sizer  {
      padding-bottom: 0!important;
    }
}

.Help_item_2_1_0 {
  padding: 13.5px;
}

.Help_item_2_2_1 {
  background: rgb(145, 255, 0);
  height: 150px;
  overflow-y:auto;
  min-width: 250px;
}

.Help_item_2_2_2 {
  background: rgb(0, 255, 179);
  height: 150px;
  overflow-y:auto;
  min-width: 250px;
}

.Help_item_2_2_3 {
  height: 100px;
  align-self: flex-end;
}

.Help_item_H {
  font-size: 1.2em!important;
  font-weight: 600;
  color:$bg-purple;
  // text-align: start;
}
.grutIMG {
  max-width: 90%;
  max-height: 90%;
  align-self: center;
}



.bigimg{
    font-size: 2em !important;
    color: #B771B9;
    cursor: pointer;
}

@media (max-width: 1750px) {
  .Help_item_0_2 {
    display: none;
  }
}

</style>