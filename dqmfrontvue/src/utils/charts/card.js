export default {
    methods: {
        stiled(data){
            let gradient = data.map((e)=>{return e}).join(", ")
            return `background: ${data[0]}; background: -webkit-linear-gradient(to right,${gradient}; background: linear-gradient(to right, ${gradient});` 
        }
    }
}