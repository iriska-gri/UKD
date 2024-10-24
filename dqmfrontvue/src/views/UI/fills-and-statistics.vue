<template>
  <v-card class="flex-col flex-grow-1 ">
    <v-tabs
      v-model="tab"
      background-color="primary"
      dark
      class="flex-grow-0"
    >
      <v-tab
        v-for="item in items"
        :key="item.tab"
      >
        {{ item.tab }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item
        v-for="item in items"
        :key="item.tab"
      >
        <v-card class="flex-col flex-grow-1" flat>
          <v-card-text class="d-flex flex-grow-1" >
                        <slot :name='item.content'></slot>
         
            </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>

 export default {
    data () {
      return {
        tab: null,
        items: [
          { tab: 'Заливки', content: 'fills' },
          { tab: 'Статистика(Графики)', content: 'stat' },
          { tab: 'Статистика(Таблица)', content: 'stattable' },
          { tab: 'Статистика online', content: 'statonline' }
        ],
      }
    },
  
    watch: {
      tab(val) {
        if ([1, 2].includes(val)) {         
          this.$store.commit('picindx', val)
          }else{
             console.log(this.$store.getters.picindx);}
        
       
      }
    }
  }
</script>

<style>

</style>