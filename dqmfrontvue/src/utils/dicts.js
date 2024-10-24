import moment from 'moment';
class DictPassportFields {

    constructor() {
       
        this.names = ['code','name', 'description', 'code_name_process',
        'responsible', 'sub_system', 'criticality', 'priority', 'reason_occurrence',
        'detection_method', 'probability_of_occurrence', 'algorithm_creation_period',
        'selection_aproval_period', 'date_of_formation_of_the_initial_list',
        'count_into_the_initial_list', 'description_algorithm','external_sources',
        'reason_occurrence_new', 'measures_to_eliminate_causes', 'application_numbers'];

        this.numbers = ['1.1.', '1.2.', '1.3.', '1.6.', '1.4.', '1.5.', '1.7.', '1.8.', '2.1.', 
        '2.2.', '2.3.', '3.1.', '3.2.', '3.3.', '3.4.', '4.1.', '4.2.', '5.1.', '5.2.', '5.3.'];
        
        this.dictTranslater = this.changeDict();

        this.handler = {
            'code': this.deleteN,
            'priority': this.deleteList,
            'date_of_formation_of_the_initial_list': this.formatDate,
            'algorithm_creation_period':  this.formatDate,
            'selection_aproval_period':  this.formatDate,
            'probability_of_occurrence': this.convertBoolean,
        }
    }

    changeDict(key_for_get='names') {
        return this[key_for_get=='names'? 'numbers': 'names'].reduce((acc, val, index) => {
            acc[val] = this[key_for_get][index]
            return acc;
        }, {})
    }

    getValue(key, value, translater=false) {
        key = translater? this.dictTranslater[key]: key;
        if (!key) return undefined;
        return {key, value : this.handler[key]? this.handler[key](value) :value};
    }

    deleteN(val) {
        return val.trim().replace(/^(№\s*)?/, '');
    }
    deleteList(val) {
        return val.trim().replace(/^(\d*\.)?(\s*)?/, '').replace(/(\;?\.?\,?)$/, '');
    }

    static deleteYear(val) {
        return val.trim().replace(/\s*год$/, '')
    }

    formatDate(val) {

        if (typeof val != 'string') {
            return moment(val).format('YYYY-MM-DD')
        };

        return moment(new Date(`01.01.${DictPassportFields.deleteYear(val)}`)).format('YYYY-MM-DD');
    }

    convertBoolean(val) {
        val = val.toLowerCase();
        return val == 'да'? true: false;
    }
}

const DictPassport = new DictPassportFields()

export { DictPassport }