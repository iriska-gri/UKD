import { axiosApiInstance } from "@/utils/axios-api";
import multifilters from "@/store/modules/filters/multifilters";
import inputfilters from "@/store/modules/filters/inputfilters";
import chainfilters from "@/store/modules/filters/chainfilters";
import selectfilters from "@/store/modules/filters/selectfilters";


export default {
  namespaced: true,
  state: {
    // Служебные
    activefilters: {},
    fieldsfilter: {},
    includeFilters: [],
    interpritateChain: {
      __gte: "with_",
      __lte: "by_",
    },
  },
  mutations: {
    clear_select(state, key){
      state.select[key] = '';
      delete state.activefilters[key]
      
    },
    
    setFields(state, fieldsfilter) {      
      state.fieldsfilter = fieldsfilter;
    },
    setIncludeFilters(state, value) {      
      state.includeFilters = value;
    },
    filtersClear(state) {           
      state.activefilters = {};
      
    },
    clear_mult(state, key) {
      state.mult[key] = [];
      delete state.activefilters[key]
    },
    clear_input(state, key) {
      state.input[key] = "";
      delete state.activefilters[key]
    },
    clear_chain(state, key) {
      const type = key.slice(-5);
      if (state.interpritateChain[type]) {
        let field = key.slice(0, -5);
        if (!state.includeFilters.includes(field)) {
          state.chain[`${state.interpritateChain[type]}${field}`] = "";
          delete state.activefilters[key];
        }
        
      } else {
        if (!state.includeFilters.includes(key)) {
          state.chain[`with_${key}`] = "";
          state.chain[`by_${key}`] = "";
          delete state.activefilters[key];
        }
      }
    },
  },
  actions: {
    cleartypeerror({ state, commit }){
      commit(`clear_select`, 'type_error');
    },
 
    clear({ state, commit }) {
     
      for (let [key, { module } = val] of Object.entries(state.activefilters)) {
       
        commit(`clear_${module}`, key);
      }
    },

    async addFilter({ dispatch, state }, { key, value }) {
     
      await dispatch(`${state.fieldsfilter[key].module}/addFilter`, { key, value });
    },

    async addDate({dispatch}, {value, period, field}) {
      const arr = ['with', 'by'];
      value.forEach((date, index) => {
        dispatch('chain/addDate', {key: `${arr[index]}_${field}`, value: date, period, field, type: arr[index]})
      })
      
    },
    



    async getFilters({ state }, settingsFilt) {
    
      try {
        const res = await axiosApiInstance.post(
          "/api/statistic/getfilters/",
          settingsFilt
        );
        
        if ("passport__code" in res.data){
            res.data.passport__code.sort((a,b)=>{
              if (Number(String(a).replace("_",".").replace(" ",".").split(".")[0]) > Number(String(b).replace("_",".").replace(" ",".").split(".")[0])) return 1;
              if (Number(String(a).replace("_",".").replace(" ",".").split(".")[0]) <  Number(String(b).replace("_",".").replace(" ",".").split(".")[0])) return -1;
              return 0
            })
        }
       
        for (let [key, val] of Object.entries(res.data)) {          
     
          state[state.fieldsfilter[key].module][`mult_${key}`] = val;
        
        }
        // ! ПЕРЕДЕЛАТЬ
       
        if ( ['/statistic/justification','/statistic/list','/dashboard',].includes(String(window.location.pathname))){  
                 
            for (let [key,val] of Object.entries(res.data)){
                
                if (key == 'date_unloading') {
                  res.data[key]=val.filter(element => element != "1900-01-01")
                }
                  
            }

         
        }       
        
        return res.data;
      } catch (e) {
        console.log(e);
        return e;
      }
    },
    async getFiltersWithoutRecord({ state }, settingsFilt) {
      
      try {
        const res = await axiosApiInstance.post(
          "/api/statistic/getfilters/",
          settingsFilt
        );
        
        return res.data;
      } catch (e) {
       
        return e;
      }
    },
    activefilters({ state }, includesField = []) {
      
      const obj = {};
      for (let [key, item] of Object.entries(state.activefilters)) {
       
        if (includesField.includes(key)) continue;
            if (['rocode','nocode'].includes(key) && isNaN(Number(item.value))){
              item.postfix=""
              item.value= ''             
            }
           
          obj[`${key}${item.postfix}`] =
            state.fieldsfilter[key] && state.fieldsfilter[key].correct
              ? state.fieldsfilter[key].correct(item.value)
              : (['user__region__name','region__name'].includes(key)) ? item.value.map((el) => el=="00. Центральный Аппарат"?         
                obj[`user__region__isnull`] = true   :  el.replace(/\d\d\.\s/, '')):item.value
               
            
      
          
            }

      return obj;
    },
  },

  modules: {
    mult: multifilters,
    input: inputfilters,
    chain: chainfilters,
    select: selectfilters,

  },
};
