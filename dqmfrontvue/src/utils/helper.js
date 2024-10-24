import moment from 'moment';

function passportnamed(str, delimiter=50){ 
    let arr=[] 
    let step=1
    let o=0     
    if (str.length>delimiter){
        while ((delimiter*step)<str.length+delimiter){
        let i= str.indexOf(" ", delimiter*step)
        if (i>0){
            arr.push(str.substring(o,i))
            o=i
            step+=1
        }else{
            arr.push(str.substring(o,str.length))
            break
        }    
        }
     return arr
    }
    else{
        return [str]
    }
}




function formatter(integer){
    return ((integer>=10000)||(integer<=-10000))?new Intl.NumberFormat('ru-RU').format(integer):integer
  }    

function checkDate(date) {
    return /^(0?[1-9]|[12][0-9]|3[01])[\.](0?[1-9]|1[012])[\.]\d{4}$/.test(date);
}
function logout(rout){         
    ["access","refresh","profile"].forEach((el)=>{localStorage.removeItem(el)})
    rout.push("/auth")    
}

function insertRegion(region){
    return region.map((e)=>{return e}).join(". ")
}

function changeFormatDate(date) {
    // Изменения формата дат
    date = moment(date, "YYYY-MM-DD");   
    
    if  (date.isValid()&& !date.isSame(moment("1900-01-01","YYYY-MM-DD"))) {return date.format("DD.MM.YYYY")}
    else if(date.isSame(moment("1900-01-01","YYYY-MM-DD")) && !(['/statistic/passports'].includes(String(window.location.pathname)))) return "Первоначальная"
    else return ''
}   

function changeFormatDateReverse(date) {
    // Изменения формата дат
    
    date = moment(date, "DD.MM.YYYY");
    
    if (date.isValid() && date!=moment("1900-01-01")) {return date.format("YYYY-MM-DD")}
    else{
        return "1900-01-01"}
    
}
function splitter(int){
    if (int.split('.').length>2) {
  
    return int.split('.').reverse().join(".").replace(".","").split("").reverse().join("")
}
    else return int
}

function customSortDataTable(items, key, isDesc){
   
    items.sort((a, b) => {        
        if (key[0]=="name"){
            if (String(a.name).toLowerCase().replace(/[^a-zа-яё.]/gi, '') > String(b.name).toLowerCase().replace(/[^a-zа-яё.]/gi, '')) return  isDesc[0]?1:-1;
            if (String(a.name).toLowerCase().replace(/[^a-zа-яё.]/gi, '') <  String(b.name).toLowerCase().replace(/[^a-zа-яё.]/gi, '')) return isDesc[0]?-1:1;
        }
        if (['code', 'passport__code'].includes(key[0])){
            
            let one = String(a[key[0]]).replace("_",".").replace(/[a-zа-яё]/gi, '')
            let two = String(b[key[0]]).replace("_",".").replace(/[a-zа-яё]/gi, '')



            if (parseFloat(splitter(one)) > parseFloat(splitter(two))) return isDesc[0]?1:-1;
            if (parseFloat(splitter(one)) <  parseFloat(splitter(two))) return isDesc[0]?-1:1;
        }
        if (['countCompare', 'growth', 'countData', 'percentage'].includes(key[0])){
            
            if (parseFloat(String(a[key[0]]).replace(/\s/g, '')) > parseFloat(String(b[key[0]]).replace(/\s/g, ''))) return isDesc[0]?1:-1;
            if (parseFloat(String(a[key[0]]).replace(/\s/g, '')) <  parseFloat(String(b[key[0]]).replace(/\s/g, ''))) return isDesc[0]?-1:1;
        }
        
        else{
            if (String(a[key[0]]).trim().toLowerCase() > String(b[key[0]]).trim().toLowerCase()) return isDesc[0]?1:-1;
            if (String(a[key[0]]).trim().toLowerCase() <  String(b[key[0]]).trim().toLowerCase()) return isDesc[0]?-1:1;
        }

    return 0

    })
return items
}

function gettabdata(data){
    let ob = []
    for (let i=0; i<data.length;i++){
      
      ob.push({name: data[i].methodolog.name,
                phone:data[i].methodolog.phone? data[i].methodolog.phone:"Не указан",
                code : sortedjoin(data[i].connectedPassport) 
                // this.sortandjoin(data[i].connectedPassport)
      })
      
    }
   return ob
}

function sortedjoin(data){          
  return data.map((e)=>{return e.code}).join(", ")
}

function permissiondenied(path){
    console.log(path);
    let up = []
    let userpermission = JSON.parse(localStorage.getItem('profile')).permission.access
    userpermission.forEach(e=>up.push(e.link))
    if (!up.includes(path)){
        window.location.href="/"
    }
}

export default {logout, changeFormatDate, changeFormatDateReverse, customSortDataTable, insertRegion, splitter, gettabdata, formatter, passportnamed, permissiondenied}
    
