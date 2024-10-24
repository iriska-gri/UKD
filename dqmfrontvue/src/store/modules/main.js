export default {
    state: () => ({
        layout: 'default-layout',
        last_name: '',
        first_name:'',
        photo: '',
        region:"",
        loadFrame: false,
        showform: false,
        wizarddialog:false,
        picindx:0,
       
        

    }),
    getters: {
     
        thisshowForm(state){
            return state.showform
        },
        layout(state) {
            return state.layout
        },
        last_name(state) {
            return state.last_name
        },
        first_name(state) {
            return state.first_name
        },
        photo(state) {
            return state.photo
        },
        loadFrame(state) {
            return state.loadFrame
        },
        lotus(state) {
            return state.lotus
        },
        middle_name(state) {
            return state.middle_name
        },
        region(state){            
            return state.region
        },

        wizarddialog(state){
            return state.wizarddialog
        },
        picindx(state){
            return state.picindx
        },
      

    },
    mutations: {
      
        thisshowForm(state, payload){
            state.showform=payload
        },
        wizarddialog(state, payload) {
            state.wizarddialog = payload
        },
        picindx(state, payload) {
            state.picindx = payload
        },
        setLayout(state, payload) {
            state.layout = payload
        },
        initializeStore(state) {

            if (localStorage.getItem("profile")) {
                const data = Object.entries( JSON.parse(localStorage.getItem("profile")) );
                for (let [key, val] of data) {
                    state[key] = val;
                }
            }
        },

        setProfile(state, param) {
            for (let [key, val] of Object.entries(param)) {
                state[key] = val;
                
            }
        },
        loadFrameTrue(state) {
            state.loadFrame = true;
        },
        loadFrameFalse(state) {
            state.loadFrame = false;
        },
      

     },
    actions: {
      
    },
}