<template>
 <v-col class="pt-1 px-1">
    <layout-label
        :title="title"
        :disabled="disabled"
        class="text-nowrap"
    >
        <v-select
            :items="items"
            :label="label"
            v-model="filt"
            
            :cleaner="cleaner"
            dense
            solo
            hide-details="true"
            :disabled="disabled"
            :menu-props="{closeOnContentClick:true}"
        >
         <template v-if="cleaner" v-slot:append-item>
                            <v-list-item @click="cleans()">
                                <v-list-item-content>
                                    <v-list-item-title>Все</v-list-item-title>
                                </v-list-item-content>
        </v-list-item>
        
         </template>
        </v-select>
    </layout-label>
     </v-col>
</template>

<script>
export default {
    name: "f-select",
    props: {
        label: {
            type: String,
            default: "Выберите...",
        },
        field: {
            type: [String, Number],
        },
        title: {
            type: String,
        },
        cleaner: {
            type: Boolean,
            default: false,
        },
        disabled:{
           type: Boolean,
           default: false,
        }
    },
    methods:{
        cleans(){
             this.filt = '';
             
      
             
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
        items: {
            get() {
                return this.$store.getters[`filterslogic/select/mult_${this.field}`];
            },
            set(value) {
                this.$store.dispatch("filterslogic/select/addFilter", { key: `mult_${this.field}`, value });
            },
        }
    }
};
</script>
