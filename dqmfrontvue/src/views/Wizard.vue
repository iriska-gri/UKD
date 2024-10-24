<template>
<v-container
    class="vh-100 back flex-col"
    fluid
>
    <v-row
        class="row_heder_text foot flex-grow-0"
    >
        <v-col
            class="flex-row"
        >
            <h2 class="pl-2 py-0">ИНТЕРАКТИВНЫЙ ПОМОЩНИК</h2>
        </v-col>
        <v-col class="pa-0 justify-end align-center flex-row switch">
            <v-switch
                color="green"
                class="pa-0 pr-5 ma-0 "
                v-model="switch1"
                hide-details
                flat
                :label="switch1?'Карта':'Шаги'"
            ></v-switch>
            <v-icon
                class="pr-5"
                @click="towizard">mdi-close
             </v-icon>
        </v-col>
    </v-row>
    <div v-if="!switch1" class="pa-0 mt-6 d-flex flex-column flex-grow-1">
        <v-row 
            class="flex-grow-0"
        >
            <v-col
                class="flex-column pb-0"
                v-if="'passport' in content"
            >
                <h2 class="pl-2">
                    КОД ПАСПОРТА: {{content.passport.code}}
                </h2>
                <h2 class="pl-2">
                    НАИМЕНОВАНИЕ ПАСПОРТА: {{content.passport.name}}
                </h2>
            </v-col>
        </v-row>
        <v-row class="pa-2 mt-0 center_row">
            <v-col class="pa-0 flex-col col_card_step">
                <v-row class="flex-grow-0">
                    <v-col>
                        <h2 class="pl-3">
                        <br>
                        </h2>
                    </v-col>
                </v-row>
                <v-card
                    height="100%"
                    class="flex-col card_text"
                >
                    <div class="flex-col ma-3 flex-grow-1 d_textcon">
                        <v-row class="flex-grow-0 flex-col mb-1">
                            <v-col class="pa-2 flex-col">
                                <v-card class="r_step flex-grow-1">
                                    <h2 class="px-3 py-1">Шаг {{content.numberstep}}. {{content.name}}</h2>
                                </v-card>
                            </v-col>
                        </v-row>
                        <v-row class="flex-grow-1 r_textcon mb-2 mt-0">
                            <v-col class="flex-col c_textcon pa-0 pl-1">
                                <v-textarea
                                    class="pa-0 px-1"
                                    id="textbox"
                                    ref="textbox"
                                    auto-grow
                                    readonly
                                    solo
                                    flat
                                    hide-details
                                    :value="content.textdescription">
                                    </v-textarea>
                            </v-col>
                        </v-row>
                        <v-row class=" flex-grow-0 " v-if="actionstep.length">
                            <v-col class="pa-2">
                                <v-card >
                                    <div class="r_radioactions">
                                        <v-radio-group
                                            class="px-2"
                                            v-model="actionstep1"
                                            hide-details
                                            dense
                                        >
                                            <v-radio
                                                class="ma-0"
                                                v-for="e in actionstep"
                                                :key="`bt${e.id}`"
                                                :label="`${e.buttontext}`"
                                                :value="e.numberstep"
                                            ></v-radio>
                                        </v-radio-group>
                                    </div>
                                </v-card>
                            </v-col>
                        </v-row>
                    </div>
                </v-card>
            </v-col>
            <v-col 
                class="pa-0 flex-col col_card_step"
            >
                <h2 class="pl-2">
                    ВЕТКА В АИС "НАЛОГ-3":
                </h2>
                <v-card
                    class="flex-col pa-4 card_AIS"
                >
                    <v-row
                        class="row_step pt-1"
                    >
                        <v-col
                            class="pl-1 py-0"
                        >
                            <p class="p-size p-mode">{{content.mode}}</p>
                        </v-col>
                    </v-row>
                </v-card>
                <h2 class="h-carta flex-col justify-end pl-2">
                    <span v-if="(('images' in content) && content.images.length>0)" >РИСУНОК {{content.images[picindx].name}}</span>
                </h2>
                <v-card
                    class="flex-col pa-4 flex-item"
                >
                    <v-row
                        class="flex-item row_step"
                    >
                        <v-col
                            class="flex-col "
                        >
                            <wcarusel                         
                                :images="content.images"
                            />
                        </v-col>
                    </v-row>
                </v-card>
            </v-col>
        </v-row>
        <v-row
            class="flex-grow-0"
        >
            <v-col
                class="flex-row "
                :class="historyarr.length?'justify-space-between':'justify-end'"
            >
                    <v-btn v-if="historyarr.length"
                    @click="minusStep" 
                        color="red"               
                    >
                        <v-icon
                            color="white"
                            style="font-size:1.5rem!important"
                        >mdi-arrow-left
                        </v-icon>
                    </v-btn>
                    <v-btn @click="addStep"
                        color="green"               
                    >
                    <v-icon
                        color="white"
                        style="font-size:1.5rem!important"
                        v-if="actionstep.length"
                    >
                        mdi-arrow-right
                    </v-icon>
                    <span v-else style="color:white">В начало</span>   
                    </v-btn>
            </v-col>
        </v-row>
    </div>   
    <v-row v-else>
        <v-col>
            <DxDiagram
                id="diagram"
                ref="diagram"	
                @item-dbl-click="onItemClick"
                :showGrid='false'
                :simple-view="true"
                :viewUnits ="'cm'"
                units="cm"	    
            >
            <DxEditing        
                :allow-change-shape-text="false"
                :allow-delete-shape="false"
                :allow-delete-connector="false"
                :allow-change-connector-text="false"
                :allow-change-connection="false"
                :allow-add-shape="false"
            /> 
            <DxPageSize
                    :width="21"
                    :height="29.7"
                    :items="[{ text: 'A4 (21cm x 29.7cm)', width: 21, height: 29.7 },
                            { text: 'A3 (29.7cm x 42cm)', width: 29.7, height: 42 }]"
                    />
            <DxPropertiesPanel
                :visibility="panelprop"
                >	   
            </DxPropertiesPanel>
            <DxNodes
                :data-source="flowNodesDataSource"
                :text-expr="'text'"
                :type-expr="'type'"
                :style-expr="itemStyleExpr"
            >
                <DxAutoLayout
                    :type="'layered'"
                    :orientation="'vertical'"
                />
            </DxNodes>
            <DxEdges
                :data-source="flowEdgesDataSource"
                :text-expr="'text'"
                :from-expr="'fromId'"
                :to-expr="'toId'"
            />
            <DxToolbox
                :visibility='"disabled"'>
                <DxGroup
                    :category="'general'"
                    :title="'Фигуры'"
                />
            </DxToolbox>
            <DxViewToolbar
                :visibility='"enabled"'
            />
            </DxDiagram>
        </v-col>
    </v-row>
</v-container>

</template> 

<script>
import Wcarusel from '../components/wizard/Wcarusel'

import {
  DxDiagram, DxNodes, DxAutoLayout, DxEdges, DxToolbox, DxGroup, DxPropertiesPanel,DxViewToolbar,DxPageSize,DxEditing
} from 'devextreme-vue/diagram';

import ArrayStore from 'devextreme/data/array_store';
import deMessages from "@/utils/ru/ru.json";
import { locale, loadMessages } from "devextreme/localization"

// --------------------------------------------------------------------------------------------- Скрипты
export default {  
    components: {Wcarusel, DxDiagram, DxNodes, DxAutoLayout, DxEdges, DxToolbox, DxGroup, DxPropertiesPanel,DxViewToolbar,DxPageSize,DxEditing},
    data() {
        return {
            panelprop:'',
            historyarr:[],
            flowNodes: [],
            flowEdges: [],
            flowNodesDataSource:[],
		    flowEdgesDataSource:[],
            content :[{
                passport:{
                    code:'',
                    name:''
                },
                step:{
                    name:'',
                    images:[]
                }
                
            }], // Общая АПИ "numberstep", "numberstep_next"
            passportdata : {}, // Данные о паспорте "code", "name", "description"
            stepdata : {}, // Текущий шаг "step", "textdescription", "mode"
            waydata : {}, // Выбор пути "waystep", "public"
            imagedata : {}, // Рисунки
            
            model: 0,
            actionstep:[],
            actionstep1:false,
            passportinf:{},  
            pickname:"" ,
            switch1:false,
            contentmap:[]
                            

        }
    },
    computed: {
    dialog () {
    return this.$store.getters.wizarddialog
  },
   picindx(){
    return this.$store.getters.picindx
   },

},

    methods : {
       

	
		
	preparecontent(){	    
		for(let i=0;i<this.contentmap.length;i++){			
			let pushed = this.flowNodes.findIndex((el)=> el.id==this.contentmap[i].id)
			let type='rectangle'
			if ((this.contentmap[i].numberstep==1)||(this.contentmap[i].actions.length==0)){
					type='terminator'
				}
                else if(this.contentmap[i].actions.length==1){
                    type='process'
                }
				else  {
					type='diamond'
				}
				
				
			if (pushed<0){		
				
			this.flowNodes.push({
				id: this.contentmap[i].id,
				text: `${this.contentmap[i].numberstep}. ${this.contentmap[i].name}`,
                numberstep:this.contentmap[i].numberstep,
				type: type,
			})}
			if (this.contentmap[i].actions.length){
                for (let n=0;n<this.contentmap[i].actions.length;n++){
                  
            this.flowEdges.push({
					fromId:this.contentmap[i].id,
					id: `${this.contentmap[i].actions[n].action.id}-${this.contentmap[i].id}`,
					text: type=="diamond" ? this.contentmap[i].actions[n].action.waystep:null,
					
					toId:this.contentmap[this.contentmap.findIndex((el)=>el.numberstep===this.contentmap[i].actions[n].nextstep)].id
				})
			


                }
		
				
			}
		}
	},
    getFlowNodes() {
		
    return this.flowNodes;
  	},
  	getFlowEdges() {
	
    return this.flowEdges;
  	},
 itemStyleExpr(obj) {
   
      const style = {};
      if (obj.numberstep ==this.content.numberstep) {
        style.fill = '#50C878';
      }
      return style
 },
	onItemClick(e) {     
        this.passportinf.numberstep = e.item.dataItem.numberstep
        this.historyarr.push(this.passportinf.numberstep)
        this.switch1=0

},



        towizard(){
            window.location.pathname="/wizard"
        },
      
        
        getbaseURL(url) {
           
            return url
        },

        addStep() {
      
        // if ('numberstep' in this.passportinf) delete this.passportinf.numberstep
        if (this.actionstep.length){   
           this.historyarr.push(this.passportinf.numberstep)
           this.passportinf.numberstep =this.actionstep1
          
           }
        else{
           
            this.historyarr=[]
            this.passportinf.numberstep=1}   
       
            
           this.getStep()
           
        },

        minusStep(){
            
            if (this.historyarr.length>1){                          
                this.passportinf.numberstep= this.historyarr.pop()
                
            }else{
                
                this.historyarr=[]
                this.passportinf.numberstep=1
                }
            
            this.getStep()
        },
       
        async getStep() {
            
        let data = await this.$http
            .get('/api/wizard/cardread/',  {params:{param:this.passportinf}})
        this.actionstep=[]
        this.content = data.data.results[0]         
        this.$store.commit('picindx', 0)
       
       
        if ('actions' in this.content){
        for (let i = 0; i < this.content.actions.length; i++) {            
            if ('nextstep' in this.content.actions[i]){
                this.actionstep.push({buttontext:this.content.actions[i].action.waystep,
                                    numberstep:this.content.actions[i].nextstep,
                                    id:this.content.actions[i].action.id})
            
            }
        }
        }
       
        this.actionstep1 = ((this.actionstep.length) && ('numberstep' in this.actionstep[0]))? this.actionstep[0].numberstep:false  
              
        if (this.content.images.length){
        this.pickname = this.content.images[0].name}
        
        else{
            this.pickname =''
        }


        },
         async getStepmap() {
        let p={'passport__id':this.passportinf.passport__id} 
      
        let data = await this.$http
            .get('/api/wizard/schemaread/', {params:{param:p}})    

        this.contentmap = data.data.results 
		
        this.preparecontent()
        
        },


        keydevent(event) {
        if(!this.switch1){
         if(!this.dialog){
          if (['Enter'].includes(String(event.code))){
                this.addStep()
          }
            else if(['Backspace'].includes(String(event.code)) && this.historyarr.length){
                this.minusStep()
          }
          else if(String(event.code).slice(0,5)=='Digit' && Number(String(event.code)[String(event.code).length-1])!=0){           
            let selectnumb = (Number(String(event.code)[String(event.code).length-1])>this.actionstep.length-1)? this.actionstep.length :Number(String(event.code)[String(event.code).length-1])
           
            
            this.actionstep1=this.actionstep[selectnumb-1].numberstep
          }
          else if((String(event.code)=='ArrowDown') && this.actionstep.length>1){
            let indx = this.actionstep.findIndex(e=>e.numberstep==this.actionstep1)
            this.actionstep1=this.actionstep[indx+1].numberstep
          }
          else if((String(event.code)=='ArrowUp' )&& this.actionstep.length>1){
            let indx = this.actionstep.findIndex(e=>e.numberstep==this.actionstep1)
            this.actionstep1=this.actionstep[indx-1].numberstep
          }
                
         
          else{
            console.log(event.code)
          }

         }
         if(this.content.images.length>0){
            if (String(event.code)=='ArrowRight'){
                    let newval = this.picindx<this.content.images.length-1?this.picindx+1:0
                    this.$store.commit('picindx', newval)

            }
            else if((String(event.code)=='ArrowLeft')){
                let newval = this.picindx>0?this.picindx-1:this.content.images.length-1
                this.$store.commit('picindx', newval)
            }
            else if((String(event.code)=='Space' )&& this.content.images.length){            
            this.$store.commit('wizarddialog', !this.dialog)           
       
          }
         }
        }

        },
        async standartload(){
             this.$store.commit('picindx', 0)        
        window.addEventListener("keydown", this.keydevent )            
           
        await this.getStep()

        },

        async mapload(){
             await this.getStepmap()
		this.panelprop='auto'
		this.flowNodesDataSource= new ArrayStore({
				key: 'id',
				data: this.getFlowNodes(),
			})
		this.flowEdgesDataSource = new ArrayStore({
				key: 'id',
				data: this.getFlowEdges(),
			})
        }

    },
     created() {
        loadMessages(deMessages);
        locale(navigator.language);
    },

     async mounted(){
        
        this.switch1 = Number(JSON.parse(localStorage.getItem('wizardswitch')))       
        this.passportinf= JSON.parse(localStorage.getItem('wizardinfo'))
        if (!this.switch1){   
            
            this.passportinf['numberstep']=1         
            await this.standartload()
      }
        else{
           await this.mapload()
        }
        
        
    },
    watch:{
        switch1(){         
            if((this.switch1) && (this.contentmap.length==0)){
                
                this.mapload()}
            else {
                     
                this.standartload()}
        }
    },
    beforeDestroy(){
        window.removeEventListener("keydown",this.keydevent)
        this.$store.commit('wizarddialog', false)
        this.$store.commit('picindx', 0)
        //  localStorage.setItem("wizardinfo", JSON.stringify(0))
        localStorage.setItem("wizardswitch", JSON.stringify(0))

    }
}

// this.passportinf= JSON.parse(localStorage.getItem('wizardinfo'))

</script>

<style lang="scss">
@import "@/utils/colors.scss";


$bordercard: #ebe7e7;
$footcolor: #f7f7f7;

.switch{
    .theme--light.v-input--switch .v-input--switch__thumb {
        color: $orange;
    }
    .theme--light.v-input--switch .v-input--switch__track {
        color: rgb(255 106 0 / 38%);
    }
    .v-input .v-label {
        font-weight: bold;
        color: $bg-purple;
    }
}

#textbox {
    font-size: 1.5rem!important;
}

#textbox>.v-input__control>.v-input__slot{
    padding: 25px 50px 75px 100px;
}

.back {
    background: $bordercard;
}

.foot {
    background: $bg-white
}


// ---------------------------------------- Внешний контейнер
.row_heder_text {
    min-height: 5vh;
}


.col_name_pass {
    min-width: 85%;
}

.col_card_step {
    min-width: 40vw;
    min-height: 35vh;
}

// ---------------------------------------- Внешний контейнер кон


// ---------------------------------------- Контейнер карточки шагов

.row_step {
    height: 22%;
    
    // min-height: 15px;
}


.row_radio {
    height: 11%;
    // min-height: 15px;
    .v-input--selection-controls {
    margin-top: 0px;
    padding-top: 0px;
    padding-left: 15px;

}

}

.fffd {
        justify-content: space-between;
}

.col_card_image {
    height: 40vh;
}

.col_direction {
    height: 5vh;
}

.card_AIS {
    min-height: 73px;
    max-height: 73px;
    overflow-y: auto;
}


.h-carta {
    height: 4%;
    min-height: 20px;
}

.row_carusel_img {
    height: 100%;
}

@media (max-width: 1264px)  {
// ---------------------------------------- Внешний контейнер    
    .col_code_pass {
        min-width: 100%;
}

    .col_name_pass {
        min-width: 100%;
    }
}
// ---------------------------------------- Внешний контейнер кон
.mycardstep {
    .v-text-field.v-text-field--enclosed .v-text-field__details, .v-text-field.v-text-field--enclosed:not(.v-text-field--rounded)>.v-input__control>.v-input__slot {
    padding: 0px 7px;
}
}

    #diagram {
      height:100%;
    }
.row_heder_text {
    
    min-height: 5vh;

}
.dx-scrollable-scroll-content, .dx-button-mode-contained.dx-button-default {  
  background-color: $bg-purple;
 
}
.dx-diagram{
	border:none
}

.r_radioactions {
    max-height: 325px; // Для маленьких экранов vh не подходит  105
    min-height: 325px; // Для маленьких экранов vh не подходит
    
    overflow: auto;
    .theme--light.v-label
    {
        color: black;
    }
    label {
        font-size: 1.2rem!important;
        font-weight: bold;
    }
}

.d_textcon{
    height: 50vh;
    min-height: 50vh;
}

.r_step {
    max-height: 45px; // Для маленьких экранов vh не подходит
    min-height: 45px; // Для маленьких экранов vh не подходит
    overflow: auto;
}

.r_textcon {
    min-height: 0;
    flex-wrap: nowrap;
}

.c_textcon {
    
    overflow-y:auto;
}

.center_row {
    gap: 8px;
}

.card_text {
    min-height: 350px;// Для маленьких экранов vh не подходит
}

</style>
