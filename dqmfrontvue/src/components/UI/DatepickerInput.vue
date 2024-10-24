<template>
  <v-menu 
          
          v-model="model"
          :close-on-content-click="false"
          
          transition="scale-transition"
          offset-y
          :max-width="maxwidth"
          min-width="auto"
        >
          <template v-slot:activator="{on, attrs }">
            <!-- v-model="item.$value" -->
            <layout-label :title="layoutlabel" />
            <v-text-field
              :value="formatDate(valYYYY_DD_MM)"              
              type="date-local"              
              placeholder="дд.мм.гггг"
              @focus="datekey=i"
              @input="oninput"
              v-bind="attrs"
              v-on="on"
              
              class="pt-0"
            >
          
            
            </v-text-field>
          </template>
         
          <v-date-picker
          :first-day-of-week="1"
            :min="min" 
            :max="max"
            :events="eventarr"
            
            event-color="green lighten-1"
            v-model="valYYYY_DD_MM"
            @input="i==1? datefrom = false:dateto=false"
            
          ></v-date-picker>
        </v-menu>
</template>

<script>
import  datepickerf  from "@/utils/datepickerf.js"
export default {
    name:"datepicker-input",
    mixins:[datepickerf],
    props:{
        maxwidth:{
            type: String,

        },
        layoutlabel:{
            type:String
        },
        valYYYY_DD_MM:{
            type:String
        },
        eventarr:{
            type:Array,
            default: []
        },
        model:{
          default:[]
        },
        min:{
          default:"0001-01-01"
        },
        max:{default:"9999-01-01"}

    }

}
</script>

<style>

</style>