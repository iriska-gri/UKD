<template>
    <v-col  class="pb-3 pt-1 px-1">
        
        <layout-label :title="title">
            <div ref="mydiv">
            <v-autocomplete
                :items="items"
                :label="label"
                :value="value"
                @input="updateValue"
                multiple
                small-chips
                :disabled="disabled"
                solo
                dense
                :clearable="value.length > 1 ? true:false "
                hide-details="true"
                ref = "mySelector"
            >
                <template
                    v-slot:prepend-item
                >
                    <v-list-item
                        ripple
                        @click="toggle"
                    >
                        <v-list-item-action>
                            <v-icon
                                :color="value.length > 0 ? 'indigo darken-4' : ''"
                                >{{ icon }}</v-icon
                            >
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>
                                Выбрать все
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </template>
                
                <template  
                    v-slot:selection="{ item, index }"
                >
                    <v-chip
                        v-if="value?index <= aviable:''"
                        color="primary"
                    >
                        <span>
                            {{ item.slice(0, 25) }}{{item.length > 25? '...': '' }}
                        </span>
                    </v-chip>
                    <custom-tooltip
                        v-if="index > aviable"
                        :content="value"
                        :visible="tooltipvisible"
                    >
                        <span ref="greytext"
                            v-if="value?index === aviable+1 && index > 0:''"
                            class="grey--text caption  pointer"
                        >
                        (+{{ value.length - 1 - aviable }})
                        </span>
                    </custom-tooltip>
                </template>
              
            </v-autocomplete>
            </div>
        </layout-label>
        <div><div class="d-flex px-3" id="counter" ref='counter'></div>
        <div class="d-flex" ref='total' id="total"></div>
        </div>
        
    </v-col>
    
</template>

<script>


import CustomTooltip from './CustomTooltip.vue';

export default {
    name: "fc-multi-select",

    data() {
        return {
            item: '',
            tooltipvisible:false,
            
            aviable:0
            // selectedletters:0
        }
    },
    components: {
    CustomTooltip
       
  },
    props: {
        label: {
            type: String,
            default: "Выберите...",
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
        items: {
            type: Array,
        },
        value: {
            type: Array,
        },
    },
    methods: {
        aviablecalc(val){
            // this.selectedletters+=len
           
            let count = 0
            let countold = 0
            this.$refs.total.innerHTML=''
            let blockWidth=this.$refs.mydiv.offsetWidth-70
            this.$refs.counter.innerHTML=''
            
            if(this.$refs.counter){
              
            for (let i=0;i<val.length;i++){
                countold=this.$refs.counter.offsetWidth
                this.$refs.counter.innerHTML += `<span class="mx-2 px-2">${val[i].slice(0, 25) }${val[i].length > 25? '...': '' }</span>`                
                count=this.$refs.counter.offsetWidth
             
                if (blockWidth<= count ){  
                    this.$refs.total.innerHTML= `<span>(+${ val.length - 1 - i })<span> `
                    
                    if    (blockWidth<= countold + this.$refs.total.offsetWidth + 7  ) {return i-2}              
                    return i-1}
            }
            return val.length-1
        }},
        toggle() {
            
            this.$nextTick(() => {
            if (this.likesAllEl) {
                this.$emit('input', []);
            } else {
                this.$emit('input', this.items.slice());
            }
            })
        },
        updateValue(value) {
            this.$emit('input', value);
            this.aviable = this.aviablecalc(value)
        }
    },
   
    computed: {
        

        likesAllEl () {
            return this.value.length === this.items.length
        },
        likesSomeEl () {
            return this.value.length > 0 && !this.items.length
        },
        icon () {
            if (this.likesAllEl) return 'mdi-close-box'
            if (this.likesSomeEl) return 'mdi-minus-box'
            return 'mdi-checkbox-blank-outline'
        },
    },
  
    
};
</script>

<style lang="scss">
#counter, #total {
    position: absolute;
    visibility: hidden;
    
    height: auto;
    width: auto;
    white-space: nowrap; /* Thanks to Herb Caudill comment */
}
.v-autocomplete.v-select.v-input--is-focused input{
    min-width: 5px;
}

</style>