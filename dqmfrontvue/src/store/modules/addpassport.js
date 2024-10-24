// 'code','name', 'description', 'code_name_process', 'responsible', 'sub_system', 'criticality', 'priority', 'reason_occurrence', 'detection_method', 
// 'probability_of_occurrence', 'algorithm_creation_period', 'selection_aproval_period', 'date_of_formation_of_the_initial_list', 'count_into_the_initial_list', 
// 'description_algorithm','external_sources', 'reason_occurrence_new', 'measures_to_eliminate_causes', 'application_numbers'

export default {
    namespaced: true,
    state: () => ({
        fields: {
            code: null,
            name: null,
            description: null,
            code_name_process: null,
            responsible: null,
            sub_system: null,
            criticality: null,
            priority: null,
            reason_occurrence: null,
            detection_method: null,
            probability_of_occurrence: null,
            algorithm_creation_period: null,
            selection_aproval_period: null,
            date_of_formation_of_the_initial_list: null,
            count_into_the_initial_list: null,
            description_algorithm: null,
            external_sources: null,
            reason_occurrence_new: null,
            measures_to_eliminate_causes: null,
            application_numbers: null,
        }
        
    }),
    getters: {
        code(state) {
            return state.fields.code
        },
        getfields(state, x) {
           
            return state.fields.code
        },
    },
    mutations: {
        addField(state, {field, value}) {
            state.fields[field] = value;
        }
    },
    actions: {
      
    },
}