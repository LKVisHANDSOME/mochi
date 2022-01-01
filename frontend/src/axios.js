import axios from 'axios'

axios.defaults.baseURL = process.env.VUE_APP_AXIOS_BASEURL
axios.defaults.headers.common['Authorization'] = 'Bearder' + localStorage.getItem('token')
axios.defaults.withCredentials = true
