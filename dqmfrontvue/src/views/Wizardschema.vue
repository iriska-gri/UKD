<template>
<div class="d-flex flex-column " style="height:100vh">
<v-row
        class="row_heder_text  flex-grow-0"
    >
        <v-col
            class=" ml-3 my-2"
        >
        <h2 class="pl-2 py-0">ИНТЕРАКТИВНЫЙ ПОМОЩНИК</h2>
        </v-col>
        <v-col class="d-flex justify-end mt-2 mr-1" >
            <v-icon
            
             @click="towizard">mdi-close</v-icon>
        </v-col>
    </v-row>
<div class="d-flex flex-grow-1 flex-column">
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
		:allow-change-connection="true"
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
</div></div>
</template>
<script>

import {
  DxDiagram, DxNodes, DxAutoLayout, DxEdges, DxToolbox, DxGroup, DxPropertiesPanel,DxViewToolbar,DxPageSize,DxEditing
} from 'devextreme-vue/diagram';

import ArrayStore from 'devextreme/data/array_store';
import deMessages from "@/utils/ru/ru.json";
import { locale, loadMessages } from "devextreme/localization"

export default {
  components: {
    DxDiagram, DxNodes, DxAutoLayout, DxEdges, DxToolbox, DxGroup, DxPropertiesPanel,DxViewToolbar,DxPageSize,DxEditing
  },
  data() {
    return {
		panelprop:'',
		// Фигуры
		flowNodes: [],
		// {
		// 	id: 107,
		// 	text: 'Начало мочало начала мочал качало начала качальных умчал',
		// 	type: 'terminator',
		// },
		// {
		// 	id: 108,
		// 	text: 'Действие без решения/кваадрат',
		// 	type: 'process',
		// 	// rectangle
		// },
		// {
		// 	id: 118,
		// 	text: 'Вопрос, который вызывает варианты ответов (радиокнопок больше 1)',
		// 	type: 'diamond',
		// },
		
		// ],
		// стрелки и текст
		flowEdges: [],
		// {
		// 	fromId: 107,
		// 	id: 116,
		// 	text: null,
		// 	toId: 108,
		// },		
		// {
		// 	fromId: 118,
		// 	id: 122,
		// 	text: 'текст радиокнопки',
		// 	toId: 121,
		// },	
		// ],
		flowNodesDataSource:[],
		flowEdgesDataSource:[],
    }
  },
  created() {
        loadMessages(deMessages);
        locale(navigator.language);
    },

  methods: {
	 async getStepmap() {
            
        let data = await this.$http
            .get('/api/wizard/schemaread/', )
     

        this.content = data.data.results 
		
        this.preparecontent()
        
        },

	
		
	preparecontent(){	
			
		let allsteps = []
		let dblstep=[]
		for(let i=0;i<this.content.length;i++){
			
			if (allsteps.includes(this.content[i].step.id)) dblstep.push(this.content[i].step.id)
			allsteps.push(this.content[i].step.id)
		}
	
		for(let i=0;i<this.content.length;i++){			
			let pushed = this.flowNodes.findIndex((el)=> el.id==this.content[i].step.id)
			let type='rectangle'
			if ((this.content[i].numberstep==1)||(this.content[i].nextstep==null)){
					type='terminator'
				}
				else if (dblstep.includes(this.content[i].step.id)) {
					type='diamond'
				}
				
				
			if (pushed<0){		
				
			this.flowNodes.push({
				id: this.content[i].step.id,
				text: this.content[i].step.name,
				type: type,
			})}
			if (this.content[i].nextstep!=null){
				this.flowEdges.push({
					fromId:this.content[i].step.id,
					id: `${this.content[i].button.id}-${this.content[i].step.id}`,
					text: type=="diamond"?this.content[i].button.waystep:null,
					// text:this.content[i].button.waystep,
					toId:this.content[i].nextstep.id
				})
			}
			// if (i==3) {break
				
			// }
		}
	},




	 towizard(){
            window.location.pathname="/wizard"
        },
	getFlowNodes() {
		
    return this.flowNodes;
  	},
  	getFlowEdges() {
	
    return this.flowEdges;
  	},

	onItemClick(e) {
  var itemKey = e.item.key;
//   	var connectors = e.component.getItems().filter(function (item) {
//     	return item.itemType === "connector" && (item.fromKey === itemKey || item.toKey === itemKey);
//   		});
//   var relativeShapes = [];
//   connectors.forEach(element => {
//     if (element.fromKey === itemKey) relativeShapes.push(e.component.getItemByKey(element.toKey)); // all subsequent shapes 
//     if (element.toKey === itemKey) relativeShapes.push(e.component.getItemByKey(element.fromKey)); // all previous shapes
//   });

},




	},

	async mounted() {
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


	
  }

</script>
<style lang="scss">
@import "@/utils/colors.scss";

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
</style>