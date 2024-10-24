import { bus } from "@/main";
// import formatter from "@/utils/helper"
import  glob from "@/utils/helper"

export  default  {
  methods:{
    formatter(integer){
      
      return ((integer>=10000)||(integer<=-10000))?new Intl.NumberFormat('ru-RU').format(integer):integer
    },    
    colorbarchart(data, key, filters, colors=['#B572B8','#BC4BC2']){
      let alpha='4D'
      // ***
      // colors[0] - пассив, [1] - актив
      // ***
      let newcolor = []
      let nocol = []
      
      
          for (let i=0;i<data.length;i++){      
                
            newcolor.push(`${key}__in` in filters && filters[`${key}__in`].includes(data[i][key])?colors[1]:colors[0]+alpha)
            nocol.push(colors[0])      
           
          }
  
      return newcolor.includes(colors[1])?newcolor:nocol
    },



    builddata4chart(data, labelKey, labelprefix=false, labelsuff=false, bw=0, bg='#B572B8', filler=false){
      let ob={'labels':[],
            "datasets":[
              {data:[],              
              borderColor:bg,
              borderWidth: bw,
              tension:0,
              borderJoinStyle:"round",
              tension: .25,
              label: 'НД',
              backgroundColor: bg,
              fill: filler,
              
            },]
          }
      
  
      for (let el in data){      
        ob.labels.push(`${labelprefix? `${data[el][labelprefix]} - `:''}${data[el][labelKey]}${labelsuff?` ${data[el][labelsuff]}`:''}`)
        ob.datasets[0].data.push(data[el].countData)
        }
      
      return ob
    },

   
    calcheightchart(vh){
      return window.innerHeight*vh/100
  },
    chartBarOpt(label,type=false){
      let ob= { 
        responsive: true,
        layout: { },  
        
        maintainAspectRatio: false,
        onHover:(event, elements, chart) => {
          const target = event.native ? event.native.target : event.target;
          target.style.cursor = elements[0] ? 'pointer' : 'default';
        },
        onClick:(event, elements, chart) => {
          if (type){
           
            if (elements[0]) {  
              let senf=""          
              const i = elements[0].index;
              if(type=="region__name"){
                senf = chart.data.labels[i].replace(" - ", ". ").trim()
             }
              else if(type=="passport__code"){
                

                senf = chart.data.labels[i].split("-")[0].trim()
             
              }
              bus.$emit('addFilBar', {val:senf, type:type})
            }}
        },
        
        indexAxis: 'y',                     
        plugins:{ 
          
          legend: {                                
              display: false},
              tooltip: {
                enabled: true,
                backgroundColor: '#43425D',
                callbacks: {
                  title:function(context){
                    // console.log(`context`, context);
                    // console.log(passportnamed);
                   return glob.passportnamed(context[0].label).map((e)=>{return e}).join("\n")

                },
                  label: function(context) {
                      let label = context.dataset.label || '';

                      if (label) {
                          label += ': ';
                      }
                      if (context.parsed.x !== null) {
                    
                          label += ((context.parsed.x>=10000)||(context.parsed.x<=-10000))?new Intl.NumberFormat('ru-RU').format(context.parsed.x):context.parsed.x
                      }
                      return label;
                  }
                }
            },         
                title: {
                display: true,
                text: label
              },  
              datalabels: {
                display:true,
                anchor: 'end',
                align: 'end',
                formatter: (val) => this.formatter(val)
                }                           
                },                                     
        scales:
        
        
            {  
                                                                 
              y:{  
                                                          
                grid: {                                    
                     lineWidth:0,
                     drawBorder: false
                    },
                                                       
                ticks:{
                  
                    crossAlign: "far",
                    callback: function(value){return `${this.getLabelForValue(value).slice(0,20)}...`}
                        }
            },
            xAxis: {   
              grace:"10%",                                                 
                grid:{
                    lineWidth:0, 
                    
                    drawBorder: false},                                
                ticks:{  
                                                  
                color:"transparent" },                                                            
            },
                                      
        }
         }
    return ob
  }
  


,
// для линейных графиков с несколькими dataset
  data4liinearchart(data, pre_data, datalabelkey){
    let linearchart={labels: [],datasets: [] };
    
    for (let[key,val] of Object.entries(pre_data)){
      val.data=[]
  }
    for (let i=0; i<data.length; i++){
      let datal = data[i][datalabelkey]
      if (datalabelkey=="date_unloading") {
        const [y,m,d]= datal.split("-")
        datal = `${d}.${m}.${y}`
      }    
      linearchart.labels.push(datal)

      for (let[key,val] of Object.entries(pre_data)){
         data[i][key]=data[i][key]==0?null:data[i][key]
          val['data'].push(data[i][key])
        
      }
  }
  for (let[key,val] of Object.entries(pre_data)){
      linearchart.datasets.push(val)
      
  }
  
  return linearchart
  },
}

}

