<template>
   <v-col
            class="pa-0 align-self-center pb-3"
            lg="1"
            md="2"
            sm="4"
          >
            <v-menu 
              v-model="datefilter"
              :close-on-content-click="false"
              transition="scale-transition"
              offset-y
              min-width="auto"
            >
              <template
                  v-slot:activator="{on, attrs}"
              >
                <v-text-field
                  title="Даты выгрузки"
                  dense
                  solo
                  :value="formatDate(filt)"              
                  type="date-local"              
                  placeholder="дд.мм.гггг"
                  @input="oninputsingle"
                  v-bind="attrs"
                  hide-details
                  v-on="on"
                >
                </v-text-field>
              </template>
              <v-date-picker
                :first-day-of-week="1"
                :max="events.length? events[0]:false" 
                :min="events.length>1?events[events.length-1]:false"
                :events="events"
                event-color="green lighten-1"
                v-model="filt"
              >
              </v-date-picker>
            </v-menu>
          </v-col>        
</template>

<script>

// import CustomTooltip from "@/components/UI/CustomTooltip.vue"
import CustomTooltip from './CustomTooltip.vue';
import  datepickerf  from "@/utils/datepickerf.js"
import moment from "moment";
export default {
    name: "f-datepicker",
    
  mixins:[datepickerf],
    data() {
        return {
            datefilter:"",
            item: '',
            tooltipvisible:false,
            aviable:0,
            
        }
    },
    props: {
        label: {
            type: String,
            default: "Выберите...",
        },
        events:{
            type:Array,
            default:[]
        },

        field: {
            type: [String, Number],
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        title: {
            type: String,
        },

    },
    methods: {
         oninputsingle(val){
            if (val.length==10){
            try{
            let str=this.formatDateRev(val)
            const newdate=moment(str)
            // =newdate.format("YYYY-MM-DD")
            if (newdate.isValid()){
              this.$store.dispatch("filterslogic/select/addFilter", { key: this.field, str});
            ;
            }
            
            }catch(e){
              console.log(e);
            }
         }
         }
            
    },
    
    computed: {
        filt: {
            get() {
              
                return this.$store.getters[`filterslogic/select/${this.field}`];
            },
            set(value) {
          
                this.$store.dispatch("filterslogic/select/addFilter", { key: this.field, value });
            },
        },
     
    },
  
    beforeDestroy() {
        this.$store.dispatch("filterslogic/mult/addFilter", {
            key: this.field,
            value: [],
        });
    }
};
</script>

<style>

</style>