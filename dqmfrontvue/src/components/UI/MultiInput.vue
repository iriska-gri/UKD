<template>
 <v-file-input
                                v-model="files"
                                dense
                                color="gray"
                                counter
                                multiple
                                @change='addfile'
                                placeholder="Выберите файлы"
                                prepend-inner-icon="mdi-paperclip"
                                prepend-icon=""
                                outlined
                                :show-size="1000"
                            >
                                <template
                                    v-slot:selection="{ index, text }"
                                >
                                    <v-chip
                                        v-if="index < 2"
                                        color="primary accent-4"
                                        dark
                                        label
                                        small
                                        close
                                        @click:close='chipdel(index)'
                                    >
                                        {{ text }}
                                    </v-chip>

                                    <span
                                        v-else-if="index === 2"
                                        class="text-overline grey--text text--darken-3 mx-2"
                                    >
                                        +{{ files.length - 2 }}
                                    </span>
                                </template>
                            </v-file-input> 
</template>

<script>
export default {
    name: "multi-input",
   
    props:{
        filesglob:{type:Array,
               default:[]},
        dubfilesglob:{type:Set,
               default:[]},
        clear:{
            type:Boolean,
            default:false
        }


    },
    data(){
        return{
            files:this.filesglob,
            dubfiles: this.dubfilesglob
        }
    },
    watch: {
        clear(){
            if (this.clear){
           
            this.files=[]
            this.dubfiles=new Set()}
        }
    },
    methods:{
        chipdel(index){
           this.files.splice(index, 1);
            this.dubfiles = new Set(this.files)
           this.$emit('adfto', [this.files,this.dubfiles]) 
        },

        addfile(){
                     
           this.dubfiles = new Set([
          ...this.dubfiles,
          ...this.files
      ])
        this.files=Array.from(this.dubfiles)
        this.$emit('adfto', [this.files,this.dubfiles])
        },

    }
}
</script>

<style>

</style>