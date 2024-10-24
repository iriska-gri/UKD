import axios from "axios";

const baseURL = process.env.NODE_ENV == 'development'? 'http://127.0.0.1:8000/': `http://${window.location.host}/`;
const baseWS = process.env.NODE_ENV == 'development'? 'ws://127.0.0.1:8000/': `ws://${window.location.host}/`;

// для релизного меняем 'http://ukd/'
// const baseURL = 'http://127.0.0.1:8000/';

async function refreshToken() {

    const refresh = localStorage.getItem('refresh');

    try {
        const result = await axios.post('/api/v1/jwt/refresh/', {refresh}, {
            baseURL
        })
      
        if (result.config.data) localStorage.setItem('refresh', JSON.parse(result.config.data).refresh);
        localStorage.setItem('access', result.data.access)
        return result.data.access;
    }
        
    catch(e) {       
        
        localStorage.removeItem('access');
        
        return Promise.reject(e);
    }
}

const axiosApiInstance = axios.create({
    baseURL,
});

const clearAxios = axios.create({
    baseURL,
});

axiosApiInstance.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('access')}`

axiosApiInstance.interceptors.request.use(config => {
    const access = localStorage.getItem('access');
    if (access) {
        config.headers = { 
            'Authorization': `JWT ${access}`,
        }
    }
    return config;
}, error => {
    return Promise.reject(error);
})

axiosApiInstance.interceptors.response.use(
response => {
    return response;
},
async error => {

    const originalRequest = error.config;
    if ((error.response.status === 401 || error.response.status === 403) && !originalRequest._retry) {
    
        originalRequest._retry = true;
        try {

            const token = await refreshToken();
            
            axiosApiInstance.defaults.headers.common['Authorization'] = `JWT ${token}`; 
           
            if (originalRequest.data){
            originalRequest.data = JSON.parse(originalRequest.data);  }          
           
            return axiosApiInstance(originalRequest);

        } catch(e) {            
           
            
            if (window.location.pathname!='/auth') window.location.reload()
            
            return Promise.reject(error);
        }
    }
    return Promise.reject(error);
})

export { axiosApiInstance, clearAxios, baseURL, baseWS }