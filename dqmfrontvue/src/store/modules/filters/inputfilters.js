export default {
  namespaced: true,
  state: {
    // Фильтры
    ogrn: "",
    inn: "",
    fid: "",
    nocode:"",
    rocode:""
  },
  getters: {
    // Геттеры фильтров
    ogrn(state) {
      
      return state.ogrn;
    },
    inn(state) {
      return state.inn;
    },
    fid(state) {
      return state.fid;
    },
    rocode(state) {
      if((!isNaN(Number(state.rocode))))  return state.rocode
      return 'Пусто';
    },
    nocode(state) {
      if((!isNaN(Number(state.nocode))))  return state.nocode
      return 'Пусто';
    },

  },
  mutations: {
    addFilter(state, { key, value }) {
      state[key] = value;
    },
  },
  actions: {
    addFilter({ state, commit, rootState }, { key, value }) {
      // Добавляет фильтр в хранилище

      commit("addFilter", { key, value });

      if ( ["", null].includes(value)) {
        delete rootState.filterslogic.activefilters[key];
        return;
      }
      rootState.filterslogic.activefilters[key] = { value, postfix: "__startswith", module: 'input' };
    },
  }
};
