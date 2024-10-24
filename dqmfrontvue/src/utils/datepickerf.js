import moment from "moment";
export  default  {
    methods:{
        formatDate (date) {
            try {
         
                    if (!date) return null
                    if (date.split('-').length==3){
                    const [year, month, day] = date.split('-')
                    return `${day}.${month}.${year}`
                    }
                }
            catch{return date}
                
              },
          formatDateRev (date) {
                    
                   
                    if (!date) return null
                    const [day, month, year] = date.split('.')
                    if (date.split('.').length==3){
                    return `${year}-${month}-${day}`
                    }
                },
          oninput(val){
            
            try{
            let str=this.formatDateRev(val)
            const newdate=moment(str)
            // =newdate.format("YYYY-MM-DD")
            if (newdate.isValid()){
              this.date_unloading[this.datekey].$value=str
            }
            
            }catch(e){
              console.log(e);
            }
            
          },
          oninputsingle(val){
            
            try{
            let str=this.formatDateRev(val)
            const newdate=moment(str)
            // =newdate.format("YYYY-MM-DD")
            if (newdate.isValid()){
              this.date_unloading.$value=str
            }
            
            }catch(e){
              console.log(e);
            }
            
          },
          oninputnotFilter(val){
            try{
              let str=this.formatDateRev(val)
              const newdate=moment(str)
              // =newdate.format("YYYY-MM-DD")
              if (newdate.isValid()){
                this.date_unloading=str
              }
              
              }catch(e){
                console.log(e);
              }

          }

    }
}