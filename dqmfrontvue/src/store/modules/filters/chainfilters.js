import moment from "moment";

let convertDate = (date) => {

  if (date =="Первоначальная") {    
    date="01.01.1900"}
  return moment(date, 'DD.MM.YYYY').format('YYYY-MM-DD');
}

export default {
  namespaced: true,
  state: {
    // Фильтры
    with_date_unloading: '',
    by_date_unloading: '',
    mult_date_unloading: [],
    mult_date_unloading__ens:[],
    with_justify__agreement_date: '',
    by_justify__agreement_date: '',
    mult_justify__agreement_date: [],
    with_date:"",
    by_date:"",
    date:"",
    mult_date:[]
  },
  getters: {
    // Геттеры фильтров
    with_date(state) {
      
      return state.with_date;
    },
    with_date_unloading(state) {
      
      return state.with_date_unloading;
    },
    by_date_unloading(state) {
      
        return state.by_date_unloading;
      },
      
     date(state) {      
        return state.date;
    },
    by_date(state) {      
        return state.by_date;
    },

    mult_date(state){
      return state.mult_date.map(el=> {return moment(el).format("DD.MM.YYYY")})
    },

    mult_date_unloading(state) {
      
      if (['/statistic/monitoring','/statistic/monitoringifns','/loadfile','/statistic/list', '/ens/monitoring','/ens/monitoringifns','/ens/list'].includes(String(window.location.pathname))){
        return state.mult_date_unloading.map((el) =>{
          
          if (el=="1900-01-01") return 'Первоначальная'        
          return moment(el).format("DD.MM.YYYY")}
        );
      }
      else{ 
         
        let a= state.mult_date_unloading.filter(element => element != '1900-01-01')   
        return a.map((el) =>{     
          return moment(el).format("DD.MM.YYYY")}
        );
     }
    },
    
    with_justify__agreement_date(state) {
      return state.with_justify__agreement_date;
    },
    by_justify__agreement_date(state) {
        return state.by_justify__agreement_date;
      },
    mult_justify__agreement_date(state) {
      
      return state.mult_justify__agreement_date.map((el) =>
        moment(el).format("DD.MM.YYYY")
      );
    },
    
    dateuploading(state) {
      
      return [state.with_date_unloading, state.by_date_unloading];
    }
  },
  mutations: {
    addFilter(state, { key, value }) {
      state[key] = value;
    },
  },
  actions: {
    addFilter({ commit }, { key, value }) {
      // Добавляет фильтр в хранилище
     
      commit("addFilter", { key, value});
    },
    async addDate({dispatch, state, rootState}, { key, value, period, field, type }) {

        await dispatch("addFilter", { key, value });
        
        if (period) {
          let postfix = type == 'with'? '__gte': '__lte';
          if (value) {
            rootState.filterslogic.activefilters[`${field}${postfix}`] = {value: convertDate(value), postfix: '', module: 'chain'};
          } else {
            delete rootState.filterslogic.activefilters[`${field}${postfix}`];
          }
        } else {
            if (state[`with_${field}`] && state[`by_${field}`]) {
              rootState.filterslogic.activefilters[field] = {value: [convertDate(state[`with_${field}`]), convertDate(state[`by_${field}`])], postfix: '__in', module: 'chain'};
            } else {
              delete rootState.filterslogic.activefilters[field];
            }
        }

    },
    clearDate({state}, field) {

      state[`with_${field}`] = '';
      state[`by_${field}`] = '';
    }
  },
};
