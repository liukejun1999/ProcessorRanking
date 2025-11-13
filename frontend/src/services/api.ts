import axios from 'axios'

const api = axios.create({ baseURL: 'http://127.0.0.1:8000/api' })

export async function getMeta(){
  const { data } = await api.get('/meta')
  return data
}

export async function postUpdate(target: string){
  const { data } = await api.post('/update', null, { params: { target } })
  return data
}


export async function getMobileSoC(params: any){
  const { data } = await api.get('/mobile-soc', { params })
  return data
}

export async function getCpu(params: any){
  const { data } = await api.get('/cpu', { params })
  return data
}

export async function getGpu(params: any){
  const { data } = await api.get('/gpu', { params })
  return data
}

